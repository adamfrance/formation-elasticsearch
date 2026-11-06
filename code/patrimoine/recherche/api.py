"""La petite API de Patrimoine. La page de recherche l'appelle ; elle interroge Elasticsearch avec une clé d'API que le
navigateur ne voit jamais (lecture de l'alias monuments, écriture dans l'index recherches), et note chaque recherche
pour repérer celles qui ne trouvent rien.

    export ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt ES_API_KEY="$CLE"
    ~/elastic/venv/bin/uvicorn api:app --port 8000          (Ctrl+C l'arrête)
"""
import os
from datetime import datetime, timezone

from elasticsearch import Elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

es = Elasticsearch(os.environ.get("ES_URL", "https://localhost:9200"), ca_certs=os.environ["ES_CA"],
                   api_key=os.environ["ES_API_KEY"])          # la clé d'API, lue dans l'environnement
app = FastAPI(title="Patrimoine")
# Le navigateur n'accepte la réponse que si l'API autorise l'adresse de la page (CORS)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8080"], allow_methods=["GET"])


@app.get("/recherche")
def recherche(q: str, region: str | None = None):
    """La requête du moteur (module 4) : plein texte pondéré, fautes tolérées, surlignage, facettes."""
    reponse = es.search(
        index="monuments", size=10, source=["titre", "commune", "region", "siecle"],
        query={"bool": {"must": [{"multi_match": {"query": q, "fields": ["titre^3", "denomination.texte^2", "historique"],
                                                  "fuzziness": "AUTO"}}]}},
        post_filter={"term": {"region": region}} if region else None,
        aggs={"regions": {"terms": {"field": "region", "size": 13}}, "siecles": {"terms": {"field": "siecle", "size": 8}}},
        highlight={"fields": {"historique": {"fragment_size": 160, "number_of_fragments": 1}},
                   "pre_tags": ["<mark>"], "post_tags": ["</mark>"], "encoder": "html"})   # le texte échappé, sauf <mark>
    total = reponse["hits"]["total"]["value"]
    # chaque recherche notée : la question, la région, le nombre de résultats (0 = une recherche sans résultat)
    es.index(index="recherches", document={"q": q, "region": region, "resultats": total,
                                           "date": datetime.now(timezone.utc).isoformat()})
    return {                                                  # ce que la page affiche
        "total": total,
        "resultats": [{"reference": h["_id"], **h["_source"],
                       "extrait": (h.get("highlight", {}).get("historique") or [""])[0]}
                      for h in reponse["hits"]["hits"]],
        "facettes": {nom: [{"valeur": b["key"], "nombre": b["doc_count"]} for b in agg["buckets"]]
                     for nom, agg in reponse["aggregations"].items()}}
