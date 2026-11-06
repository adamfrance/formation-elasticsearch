"""L'assistant de Patrimoine : il cherche les monuments qui répondent à la question (recherche hybride : les mots et
le sens), puis demande à un modèle de langage de rédiger la réponse à partir de ces seules sources, en les citant.

    python rag/rag.py "Quelles abbayes cisterciennes de Bourgogne sont protégées ?"
    python rag/rag.py --modele llama3.2:3b "…"                 un autre modèle local (Ollama)
    python rag/rag.py --fournisseur mistral "…"                l'API de Mistral (clé dans MISTRAL_API_KEY)
    python rag/rag.py --region Bourgogne-Franche-Comté "…"     seulement les monuments d'une région (un filtre)

Connexion à Elasticsearch : ES_URL, ES_CA (le certificat http_ca.crt) et ES_PASSWORD (le mot de passe de elastic).
"""
import argparse
import os

import requests
from elasticsearch import Elasticsearch

CONSIGNE = (
    "Tu es l'assistant de Patrimoine, le moteur de recherche des monuments historiques de France. "
    "Réponds en français, en trois à six phrases, uniquement à partir des sources données. "
    "Cite la référence de chaque source utilisée entre crochets, par exemple [PA00112529]. "
    "Si les sources ne permettent pas de répondre, dis-le simplement, sans rien inventer.")


def chercher(es, question, nombre=5, region=None):
    """Les monuments les plus proches de la question : mots (multi_match) et sens (semantic), fusionnés par RRF ;
    avec une région, les deux recherches ne regardent que ses monuments."""
    filtre = [{"term": {"region": region}}] if region else []
    mots = {"bool": {"must": {"multi_match": {"query": question, "fields": ["titre^3", "historique"]}}, "filter": filtre}}
    sens = {"bool": {"must": {"semantic": {"field": "historique_sens", "query": question}}, "filter": filtre}}
    reponse = es.search(index="monuments", size=nombre, source=["titre", "commune", "region", "historique"],
                        retriever={"rrf": {"retrievers": [{"standard": {"query": mots}}, {"standard": {"query": sens}}]}})
    return [{"reference": h["_id"], **h["_source"]} for h in reponse["hits"]["hits"]]


def contexte(sources):
    """Les sources, une par paragraphe, avec leur référence : c'est tout ce que le modèle aura sous les yeux."""
    return "\n\n".join(f"[{s['reference']}] {s['titre']} ({s['commune']}, {s.get('region', '')}) : "
                       f"{s.get('historique', '(pas d’historique)')[:800]}" for s in sources)  # 800 caractères par source


def rediger_ollama(question, sources, modele):
    """La question au modèle local, par l'API d'Ollama : la consigne, puis les sources et la question."""
    reponse = requests.post(os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat", timeout=900, json={
        "model": modele, "stream": False, "options": {"temperature": 0},     # la réponse d'un bloc, le moins de hasard
        "messages": [{"role": "system", "content": CONSIGNE},
                     {"role": "user", "content": f"Sources :\n\n{contexte(sources)}\n\nQuestion : {question}"}]})
    reponse.raise_for_status()
    return reponse.json()["message"]["content"]


def rediger_mistral(question, sources, modele):
    """La même demande à l'API de Mistral : payante à l'usage, la clé dans MISTRAL_API_KEY."""
    reponse = requests.post("https://api.mistral.ai/v1/chat/completions", timeout=120,
                            headers={"Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}"}, json={
        "model": modele, "temperature": 0,
        "messages": [{"role": "system", "content": CONSIGNE},
                     {"role": "user", "content": f"Sources :\n\n{contexte(sources)}\n\nQuestion : {question}"}]})
    reponse.raise_for_status()
    return reponse.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    arguments.add_argument("question")
    arguments.add_argument("--fournisseur", choices=["ollama", "mistral"], default="ollama")
    arguments.add_argument("--modele", default=None, help="qwen2.5:3b (Ollama) ou mistral-small-latest (Mistral)")
    arguments.add_argument("--region", default=None, help="Bourgogne-Franche-Comté, Bretagne…")
    a = arguments.parse_args()
    es = Elasticsearch(os.environ.get("ES_URL", "https://localhost:9200"), ca_certs=os.environ["ES_CA"],
                       basic_auth=("elastic", os.environ["ES_PASSWORD"]))      # l'adresse, le certificat, le mot de passe
    sources = chercher(es, a.question, region=a.region)
    print("Sources :")
    for s in sources:
        print(f"  [{s['reference']}] {s['titre']} ({s['commune']})")
    if a.fournisseur == "mistral":
        texte = rediger_mistral(a.question, sources, a.modele or "mistral-small-latest")
    else:
        texte = rediger_ollama(a.question, sources, a.modele or "qwen2.5:3b")
    print(f"\nRéponse ({a.modele or 'modèle par défaut'}) :\n{texte}")
