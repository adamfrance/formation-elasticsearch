"""Charge un fichier CSV du ministère (séparateur « | ») dans un index, par paquets de 2 000 lignes, en passant chaque
ligne par un pipeline d'ingestion : ce que font Filebeat et Logstash, sans eux (secours de la reprise du jour 2).
Rien à installer : seulement la bibliothèque standard de Python.

    python3 charger.py merimee.csv monuments-v1 monuments-nettoyage
"""
import base64
import csv
import json
import os
import ssl
import sys
import urllib.request

fichier, index, pipeline = sys.argv[1:4]
contexte = ssl.create_default_context(cafile=os.environ["ES_CA"])
jeton = base64.b64encode(f"elastic:{os.environ['ELASTIC_PASSWORD']}".encode()).decode()


def envoyer(lignes):
    corps = "".join(lignes).encode()
    requete = urllib.request.Request(f"{os.environ['ES_URL']}/{index}/_bulk?pipeline={pipeline}", data=corps,
                                     method="POST", headers={"Content-Type": "application/x-ndjson",
                                                             "Authorization": f"Basic {jeton}"})
    with urllib.request.urlopen(requete, context=contexte) as reponse:
        return json.load(reponse)["errors"]


csv.field_size_limit(10**9)
paquet, total, erreurs = [], 0, 0
with open(fichier, newline="", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter="|"):
        document = {cle: valeur for cle, valeur in ligne.items() if valeur}
        paquet += [json.dumps({"index": {"_id": ligne["Reference"]}}) + "\n",
                   json.dumps(document, ensure_ascii=False) + "\n"]
        total += 1
        if len(paquet) == 4000:
            erreurs += envoyer(paquet)
            paquet = []
if paquet:
    erreurs += envoyer(paquet)
print(f"{total} lignes envoyées, paquets en erreur : {erreurs}")
