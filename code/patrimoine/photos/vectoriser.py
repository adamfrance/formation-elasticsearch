"""Les photos des monuments, vectorisées à côté d'Elasticsearch : Elasticsearch ne fait pas tourner de modèle d'images,
on calcule donc le vecteur de chaque photo avec CLIP (un modèle qui place images et textes dans le même espace), puis
on range les vecteurs dans un champ dense_vector.

    python vectoriser.py 300 photos.ndjson        les 300 photos de photos-liste.ndjson (fichier fourni)

La liste a été tirée de Wikidata le 2 novembre 2026 (des monuments qui ont une référence Mérimée et une photo) : la
même pour tous, pour retrouver les résultats du cours.
Chaque ligne du fichier produit : référence Mérimée, nom, adresse de la photo (Wikimedia Commons), vecteur (512 nombres).
"""
import io
import json
import sys
import time
import urllib.parse

import requests
from PIL import Image
from sentence_transformers import SentenceTransformer

AGENT = {"User-Agent": "formation-elasticsearch/1.0 (https://github.com/adamfrance)"}

nombre, sortie = int(sys.argv[1]), sys.argv[2]
with open("photos-liste.ndjson", encoding="utf-8") as f:   # une photo par ligne : référence, nom, fichier de Commons
    lignes = [json.loads(ligne) for ligne in f]
modele = SentenceTransformer("clip-ViT-B-32")             # CLIP : une image devient 512 nombres (téléchargé une fois)
with open(sortie, "w", encoding="utf-8") as f:
    gardees = 0
    for ligne in lignes:
        adresse = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
                   + urllib.parse.quote(ligne["fichier"]) + "?width=320")   # la photo en petit : assez pour CLIP
        try:
            image = Image.open(io.BytesIO(requests.get(adresse, headers=AGENT, timeout=60).content)).convert("RGB")
        except Exception:                                 # une photo introuvable est sautée
            continue
        ligne |= {"image": adresse, "vecteur": [round(x, 5) for x in modele.encode(image).tolist()]}   # 5 décimales
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        gardees += 1
        time.sleep(0.2)                                   # poliment : Wikimedia limite le rythme des robots
        if gardees == nombre:
            break
print(f"{gardees} photos vectorisées dans {sortie}")
