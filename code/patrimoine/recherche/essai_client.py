"""Le client Python officiel avec la clé d'API de Patrimoine : compter, chercher, puis demander qui est le cluster
(refusé : la clé n'a que les droits qu'on lui a donnés).

    export ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt ES_API_KEY="$CLE"
    ~/elastic/venv/bin/python essai_client.py
"""
import os

from elasticsearch import AuthorizationException, Elasticsearch

es = Elasticsearch(os.environ.get("ES_URL", "https://localhost:9200"), ca_certs=os.environ["ES_CA"],
                   api_key=os.environ["ES_API_KEY"])          # l'adresse, le certificat et la clé viennent de l'environnement
print("Monuments :", es.count(index="monuments")["count"])
for monument in es.search(index="monuments", q="abbaye cistercienne", size=3)["hits"]["hits"]:   # q= : comme dans l'adresse
    print(" ", monument["_id"], monument["_source"]["titre"], "·", monument["_source"]["commune"])
try:
    print("Cluster :", es.info()["cluster_name"])              # refusé : la clé n'a aucun droit sur le cluster
except AuthorizationException as erreur:
    print("es.info() refusé :", erreur.message, "(la clé n'a aucun droit sur le cluster)")
