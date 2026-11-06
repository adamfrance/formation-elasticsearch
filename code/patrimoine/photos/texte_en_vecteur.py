"""Le vecteur d'une phrase, dans le même espace que les photos : CLIP multilingue (le texte en français).

    python texte_en_vecteur.py "un château fort au bord de la mer"
"""
import json
import sys

from sentence_transformers import SentenceTransformer

modele = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")
print(json.dumps([round(x, 5) for x in modele.encode(sys.argv[1]).tolist()]))
