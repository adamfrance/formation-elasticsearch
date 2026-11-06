# Elasticsearch : indexation de contenu — jour 2 : les commandes des diapositives

Chaque bloc est celui du bouton « Copier » de la diapositive, dans l'ordre de la journée : les commandes du terminal, les requêtes de la console de Kibana et le contenu des fichiers à créer. Le numéro est celui de la diapositive.

## Diapositive 3

**Ce matin : redémarrer Elasticsearch, puis Kibana**

Dans le terminal :

- dans un nouveau terminal, celui d'Elasticsearch : aller dans son dossier
- démarrer Elasticsearch ; il reste allumé, et ce terminal avec lui
- dans un nouveau terminal, celui de Kibana, une fois Elasticsearch prêt : aller dans son dossier
- démarrer Kibana ; on attend « Kibana is now available »

```bash
cd ~/elastic/elasticsearch-9.5.6
bin/elasticsearch

cd ~/elastic/kibana-9.5.6
bin/kibana
```

## Diapositive 4

**Repartir au même point : le script de reprise**

Dans le terminal :

- si un atelier d'hier n'a pas abouti : le script de la correction remet les pipelines, les templates, les index et l'alias

```bash
bash ~/projets/formation-elasticsearch/corrige-jour1/patrimoine/reprise/reprise-jour2.sh
```

## Diapositive 7

**Les outils de l'après-midi, à installer dès ce matin**

Dans le terminal :

- un Python à part pour le cours, dans ~/elastic/venv
- y installer le client d'Elasticsearch, requests, FastAPI et uvicorn
- installer Ollama, qui fait tourner les modèles de langue (sudo demande votre mot de passe)
- télécharger le modèle Qwen 2.5 (1,9 Go)
- télécharger le modèle Llama 3.2 (2,0 Go)
- la liste des modèles installés

```bash
python3 -m venv ~/elastic/venv
~/elastic/venv/bin/pip install "elasticsearch>=9,<10" requests fastapi uvicorn

curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
ollama list
```

## Diapositive 8

**Sans droits d'administrateur : Python avec uv**

Dans le terminal :

- installer uv dans votre dossier (~/.local/bin), sans sudo
- recréer avec uv le Python du cours, pip compris (--seed, --clear)
- y installer le client d'Elasticsearch, requests, FastAPI et uvicorn

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
~/.local/bin/uv venv --clear --seed ~/elastic/venv
~/elastic/venv/bin/pip install "elasticsearch>=9,<10" requests fastapi uvicorn
```

## Diapositive 9

**Sans droits d'administrateur : Ollama dans votre dossier**

Dans le terminal :

- le dossier qui recevra Ollama
- télécharger Ollama (1,5 Go), le décompresser et l'extraire dans ~/.local
- démarrer Ollama en arrière-plan ; son journal va dans ~/elastic/ollama.log
- télécharger le modèle Qwen 2.5
- télécharger le modèle Llama 3.2
- la version d'Ollama, puis les modèles installés

```bash
mkdir -p ~/.local
curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst | zstd -d | tar -xf - -C ~/.local
~/.local/bin/ollama serve > ~/elastic/ollama.log 2>&1 &
~/.local/bin/ollama pull qwen2.5:3b
~/.local/bin/ollama pull llama3.2:3b
~/.local/bin/ollama --version; ~/.local/bin/ollama list
```

## Diapositive 10

**Les données d'exemple de Kibana, pour les démonstrations du module 4**

Dans la console de Kibana :

- charger les données d'exemple d'une boutique en ligne (kbn: : une requête à Kibana)
- puis celles de vols d'avion

```text
POST kbn:/api/sample_data/ecommerce

POST kbn:/api/sample_data/flights
```

## Diapositive 11

**Les mêmes données d'exemple, depuis le terminal avec curl**

Dans le terminal :

- charger la boutique d'exemple par l'API de Kibana (on attend 4675 commandes)
- puis les vols d'avion (on attend 13014 vols)

```bash
curl -s -u "elastic:$ELASTIC_PASSWORD" -X POST 'http://localhost:5601/api/sample_data/ecommerce' \
  -H 'kbn-xsrf: true' -H 'x-elastic-internal-origin: Kibana'; echo

curl -s -u "elastic:$ELASTIC_PASSWORD" -X POST 'http://localhost:5601/api/sample_data/flights' \
  -H 'kbn-xsrf: true' -H 'x-elastic-internal-origin: Kibana'; echo
```

## Diapositive 17

**Démonstration : une boutique en ligne**

Dans la console de Kibana :

- deux commandes de chemises, payées en euros, de plus de 100 € : une requête bool

```text
GET /kibana_sample_data_ecommerce/_search
{
  "size": 2,
  "_source": [
    "customer_full_name",
    "taxful_total_price",
    "products.product_name"
  ],
  "query": {
    "bool": {
      "must": [{"match": {"products.product_name": "shirt"}}],
      "filter": [
        {"term": {"currency": "EUR"}},
        {"range": {"taxful_total_price": {"gte": 100}}}
      ]
    }
  }
}
```

## Diapositive 18

**Démonstration : des vols vers la France**

Dans la console de Kibana :

- deux vols vers la France : should, « l'un ou l'autre », fait monter le score sans être obligatoire

```text
GET /kibana_sample_data_flights/_search
{
  "size": 2,
  "_source": [
    "OriginCityName",
    "DestCityName",
    "Carrier",
    "FlightDelayMin"
  ],
  "query": {
    "bool": {
      "filter": [{"term": {"DestCountry": "FR"}}],
      "should": [
        {"term": {"Carrier": "Kibana Airlines"}},
        {"range": {"FlightDelayMin": {"gte": 60}}}
      ],
      "minimum_should_match": 1,
      "must_not": [{"term": {"Cancelled": true}}]
    }
  }
}
```

## Diapositive 20

**Correction : chapelles classées de Bretagne**

Dans la console de Kibana :

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune", "protection"],
  "query": {
    "bool": {
      "must": [{"match": {"historique": "chapelle"}}],
      "filter": [
        {"term": {"region": "Bretagne"}},
        {"term": {"protection": "classé MH"}}
      ],
      "must_not": [{"term": {"denomination": "église"}}]
    }
  }
}
GET /monuments/_count
{
  "query": {
    "bool": {
      "filter": [
        {"terms": {"region": ["Bretagne", "Normandie"]}},
        {"term": {"siecle": "12e siècle"}},
        {"exists": {"field": "localisation"}}
      ]
    }
  }
}
```

## Diapositive 21

**Les filtres d'intervalle : range**

Dans la console de Kibana :

- les fiches mises à jour depuis une date, les plus récentes d'abord

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "mise_a_jour"],
  "sort": [{"mise_a_jour": "desc"}],
  "query": {"range": {"mise_a_jour": {"gte": "2026-10-01"}}}
}
```

## Diapositive 24

**Démonstration : _explain détaille le calcul**

Dans la console de Kibana :

- pourquoi Carcassonne a ce score pour « carcassonne » : le calcul détaillé

```text
GET /monuments/_explain/PA00102588
{"query": {"match": {"titre": "carcassonne"}}}
```

## Diapositive 26

**Correction : match, en OU puis en ET**

Dans la console de Kibana :

- « abbaye cistercienne » : l'un des deux mots suffit (OU)
- les deux mots exigés (operator: and)

```text
GET /monuments/_count
{"query": {"match": {"historique": "abbaye cistercienne"}}}

GET /monuments/_count
{
  "query": {
    "match": {
      "historique": {"query": "abbaye cistercienne", "operator": "and"}
    }
  }
}
```

## Diapositive 27

**Correction : plusieurs champs, avec des poids**

Dans la console de Kibana :

- chercher dans plusieurs champs ; ^3 : le titre compte trois fois plus

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "multi_match": {
      "query": "abbaye cistercienne",
      "fields": ["titre^3", "denomination.texte^2", "historique"]
    }
  }
}
```

## Diapositive 28

**Correction : l'expression exacte, et la syntaxe des utilisateurs**

Dans la console de Kibana :

- l'expression exacte « Viollet-le-Duc », les mots dans l'ordre
- la syntaxe d'un champ de recherche : guillemets pour une expression, - pour exclure

```text
GET /monuments/_count
{
  "query": {"match_phrase": {"historique": "Viollet-le-Duc"}}
}

GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune"],
  "query": {
    "simple_query_string": {
      "query": "\"pont suspendu\" -péage",
      "fields": ["titre^2", "historique"]
    }
  }
}
```

## Diapositive 29

**Correction : corriger la pertinence avec function_score**

Dans la console de Kibana :

- la même recherche, le score des monuments classés MH doublé

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune", "protection"],
  "query": {
    "function_score": {
      "query": {
        "multi_match": {
          "query": "château fort",
          "fields": ["titre^3", "historique"]
        }
      },
      "functions": [
        {
          "filter": {"term": {"protection": "classé MH"}},
          "weight": 2
        }
      ],
      "score_mode": "multiply"
    }
  }
}
```

## Diapositive 30

**Les suggestions à la frappe : search_as_you_type**

Dans la console de Kibana :

- proposer des titres pendant la frappe : « abbaye du mont sai »

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "multi_match": {
      "query": "abbaye du mont sai",
      "type": "bool_prefix",
      "fields": [
        "suggestion",
        "suggestion._2gram",
        "suggestion._3gram"
      ]
    }
  }
}
```

## Diapositive 31

**Démonstration : le suggesteur completion**

Dans la console de Kibana :

- un index dont le champ titre sert aux suggestions (completion)
- les titres qui commencent par « le p »

```text
PUT /livres-suggestion
{
  "mappings": {"properties": {"titre": {"type": "completion"}}}
}

GET /livres-suggestion/_search
{
  "_source": false,
  "suggest": {
    "livres": {"prefix": "le p", "completion": {"field": "titre"}}
  }
}
```

## Diapositive 32

**Une faute de frappe : la recherche floue**

Dans la console de Kibana :

- « Carcasonne », une lettre oubliée : aucun résultat
- la même faute, avec fuzziness : les monuments de Carcassonne

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune"],
  "query": {"match": {"commune.texte": "Carcasonne"}}
}

GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune"],
  "query": {
    "match": {
      "commune.texte": {"query": "Carcasonne", "fuzziness": "AUTO"}
    }
  }
}
```

## Diapositive 33

**La surbrillance : montrer pourquoi le résultat est là**

Dans la console de Kibana :

- les passages où « Viollet-le-Duc » apparaît, mis en évidence

```text
GET /monuments/_search
{
  "size": 2,
  "_source": ["titre"],
  "query": {"match": {"historique": "Viollet-le-Duc"}},
  "highlight": {
    "fields": {
      "historique": {"fragment_size": 120, "number_of_fragments": 1}
    },
    "pre_tags": ["<mark>"],
    "post_tags": ["</mark>"]
  }
}
```

## Diapositive 36

**Démonstration : les agrégations d'une boutique**

Dans la console de Kibana :

- les 3 premières catégories de la boutique, et le panier moyen de chacune

```text
GET /kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {"field": "category.keyword", "size": 3},
      "aggs": {
        "panier_moyen": {"avg": {"field": "taxful_total_price"}}
      }
    },
    "par_jour": {
      "date_histogram": {"field": "order_date", "calendar_interval": "week"}
    }
  }
}
```

## Diapositive 37

**Les facettes de Patrimoine**

Dans la console de Kibana :

- les abbayes, comptées par région et par siècle : les facettes d'un site

```text
GET /monuments/_search
{
  "size": 0,
  "query": {"match": {"historique": "abbaye"}},
  "aggs": {
    "regions": {"terms": {"field": "region", "size": 5}},
    "siecles": {"terms": {"field": "siecle", "size": 5}},
    "protections": {"terms": {"field": "protection", "size": 3}}
  }
}
```

## Diapositive 38

**Une facette cochée : post_filter**

Dans la console de Kibana :

- une facette cochée : les résultats filtrés, les comptes des facettes inchangés

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "region"],
  "query": {"match": {"historique": "abbaye"}},
  "aggs": {"regions": {"terms": {"field": "region", "size": 5}}},
  "post_filter": {"term": {"region": "Bourgogne-Franche-Comté"}}
}
```

## Diapositive 39

**Une agrégation sur les protections (nested)**

Dans la console de Kibana :

- les protections comptées par type, à l'intérieur de chaque fiche (nested)

```text
GET /monuments/_search
{
  "size": 0,
  "aggs": {
    "protections": {
      "nested": {"path": "protections"},
      "aggs": {
        "types": {"terms": {"field": "protections.type", "size": 4}},
        "premiere": {
          "min": {"field": "protections.date", "format": "yyyy"}
        },
        "derniere": {
          "max": {
            "field": "protections.date",
            "format": "yyyy-MM-dd"
          }
        }
      }
    }
  }
}
```

## Diapositive 40

**Autour de moi : geo_distance, et le tri par distance**

Dans la console de Kibana :

- les monuments à moins de 5 km d'un point, les plus proches d'abord

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "geo_distance": {
      "distance": "5km",
      "localisation": {"lat": 43.2064, "lon": 2.3655}
    }
  },
  "sort": [
    {
      "_geo_distance": {
        "localisation": {"lat": 43.2064, "lon": 2.3655},
        "order": "asc",
        "unit": "km"
      }
    }
  ]
}
```

## Diapositive 41

**Un rectangle, une grille : pour la carte**

Dans la console de Kibana :

- compter les monuments d'un rectangle, sur Paris
- les carreaux de la carte qui ont le plus de monuments

```text
GET /monuments/_count
{
  "query": {
    "geo_bounding_box": {
      "localisation": {
        "top_left": {"lat": 48.95, "lon": 2.2},
        "bottom_right": {"lat": 48.8, "lon": 2.5}
      }
    }
  }
}

GET /monuments/_search
{
  "size": 0,
  "aggs": {
    "carreaux": {
      "geotile_grid": {"field": "localisation", "precision": 5, "size": 3}
    }
  }
}
```

## Diapositive 43

**Correction : la requête du moteur**

Dans la console de Kibana :

- la requête du moteur de Patrimoine : le texte, les filtres et les facettes, en une fois

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune", "region", "siecle"],
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {"query": "abaye cistercienne", "fields": ["titre^3", "denomination.texte^2", "historique"], "fuzziness": "AUTO"}
        }
      ],
      "filter": [{"term": {"protection": "classé MH"}}]
    }
  },
  "highlight": {
    "fields": {"historique": {"fragment_size": 100, "number_of_fragments": 1}},
    "pre_tags": ["<mark>"],
    "post_tags": ["</mark>"]
  },
  "aggs": {"regions": {"terms": {"field": "region", "size": 5}}, "siecles": {"terms": {"field": "siecle", "size": 5}}},
  "post_filter": {"term": {"region": "Occitanie"}}
}
```

## Diapositive 44

**Correction : la réponse du moteur**

Dans la console de Kibana :

- la même requête : on lit maintenant sa réponse

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune", "region", "siecle"],
  "query": {
    "bool": {
      "must": [
        {
          "multi_match": {
            "query": "abaye cistercienne",
            "fields": [
              "titre^3",
              "denomination.texte^2",
              "historique"
            ],
            "fuzziness": "AUTO"
          }
        }
      ],
      "filter": [{"term": {"protection": "classé MH"}}]
    }
  },
  "highlight": {
    "fields": {
      "historique": {"fragment_size": 100, "number_of_fragments": 1}
    },
    "pre_tags": ["<mark>"],
    "post_tags": ["</mark>"]
  },
  "aggs": {
    "regions": {"terms": {"field": "region", "size": 5}},
    "siecles": {"terms": {"field": "siecle", "size": 5}}
  },
  "post_filter": {"term": {"region": "Occitanie"}}
}
```

## Diapositive 45

**Correction : les châteaux autour de Chambord**

Dans la console de Kibana :

- les châteaux autour de Chambord

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune"],
  "query": {
    "bool": {
      "must": [{"match": {"denomination.texte": "château"}}],
      "filter": [
        {
          "geo_distance": {
            "distance": "20km",
            "localisation": {"lat": 47.616, "lon": 1.517}
          }
        }
      ]
    }
  },
  "sort": [
    {
      "_geo_distance": {
        "localisation": {"lat": 47.616, "lon": 1.517},
        "order": "asc",
        "unit": "km"
      }
    }
  ]
}
```

## Diapositive 51

**Démonstration : quatre vecteurs, rangés à la main**

Dans la console de Kibana :

- créer l'index : un champ dense_vector à 2 dimensions, comparé par le cosinus
- ranger les quatre mots et leurs vecteurs, en une requête _bulk

```text
PUT /vecteurs-demo
{"mappings": {"properties": {"nom": {"type": "keyword"}, "v": {"type": "dense_vector", "dims": 2, "similarity": "cosine"}}}}

POST /vecteurs-demo/_bulk?refresh=true
{"index": {"_id": "1"}}
{"nom": "château fort", "v": [1.0, 0.1]}
{"index": {"_id": "2"}}
{"nom": "forteresse", "v": [0.9, 0.2]}
{"index": {"_id": "3"}}
{"nom": "abbaye", "v": [0.2, 1.0]}
{"index": {"_id": "4"}}
{"nom": "monastère", "v": [0.3, 0.9]}
```

## Diapositive 52

**Démonstration : quatre vecteurs, et la question**

Dans la console de Kibana :

- les deux vecteurs les plus proches de la question [0.9, 0.3]

```text
GET /vecteurs-demo/_search
{
  "knn": {
    "field": "v",
    "query_vector": [0.9, 0.3],
    "k": 2,
    "num_candidates": 10
  },
  "_source": ["nom"]
}
```

## Diapositive 54

**Les modèles fournis, et la licence**

Dans la console de Kibana :

- les modèles qu'Elasticsearch déclare d'office
- appeler le modèle E5 : refusé en licence gratuite

```text
GET /_inference?filter_path=endpoints.inference_id,endpoints.task_type,endpoints.service

POST /_inference/text_embedding/.multilingual-e5-small-elasticsearch
{"input": ["une abbaye isolée au milieu des bois"]}
```

## Diapositive 58

**Activer la licence d'essai de 30 jours**

Dans la console de Kibana :

- la licence actuelle
- activer l'essai de 30 jours
- la licence après : son type et sa date de fin

```text
GET /_license

POST /_license/start_trial?acknowledge=true

GET /_license?filter_path=license.type,license.status,license.expiry_date
```

## Diapositive 59

**Le modèle E5 : un texte devient 384 nombres**

Dans la console de Kibana :

- une phrase devient 384 nombres (le premier appel charge le modèle, d'où les 10 minutes permises)
- deux phrases au même sens : des vecteurs proches

```text
POST /_inference/text_embedding/.multilingual-e5-small-elasticsearch?timeout=10m
{"input": ["une abbaye isolée au milieu des bois"]}

POST /_inference/text_embedding/.multilingual-e5-small-elasticsearch
{
  "input": [
    "un château fort au bord de la mer",
    "une forteresse sur la côte"
  ]
}
```

## Diapositive 60

**Le champ sémantique dans le template**

Dans la console de Kibana :

- le template, avec le champ historique_sens (semantic_text)
- créer monuments-v3, avec ce template

```text
PUT /_index_template/monuments
{
  "index_patterns": ["monuments-v*"],
  "composed_of": ["patrimoine-analyse"],
  "priority": 200,
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "refresh_interval": "1s",
      "index.final_pipeline": "monuments-protections"
    },
    "mappings": {
      "dynamic": false,
      "properties": {
        "reference": {"type": "keyword"},
        "titre": {
          "type": "text",
          "analyzer": "francais_patrimoine",
          "fields": {"exact": {"type": "keyword"}},
          "copy_to": "suggestion"
        },
        "suggestion": {
          "type": "search_as_you_type",
          "analyzer": "francais_simple"
        },
        "denomination": {
          "type": "keyword",
          "fields": {
            "texte": {
              "type": "text",
              "analyzer": "francais_patrimoine"
            }
          }
        },
        "commune": {
          "type": "keyword",
          "fields": {
            "texte": {"type": "text", "analyzer": "francais_simple"}
          }
        },
        "departement": {"type": "keyword"},
        "departement_code": {"type": "keyword"},
        "region": {"type": "keyword"},
        "siecle": {"type": "keyword"},
        "protection": {"type": "keyword"},
        "historique_protection": {"type": "text", "index": false},
        "protections": {
          "type": "nested",
          "properties": {
            "date": {
              "type": "date",
              "format": "yyyy/MM/dd||yyyy",
              "ignore_malformed": true
            },
            "type": {"type": "keyword"}
          }
        },
        "historique": {
          "type": "text",
          "analyzer": "francais_patrimoine",
          "copy_to": ["historique_sens"]
        },
        "statut": {"type": "keyword"},
        "localisation": {"type": "geo_point"},
        "objets": {"type": "keyword"},
        "mise_a_jour": {"type": "date"},
        "erreur_ingestion": {"type": "keyword"},
        "historique_sens": {
          "type": "semantic_text",
          "inference_id": ".multilingual-e5-small-elasticsearch"
        }
      }
    }
  },
  "_meta": {
    "description": "Patrimoine : réglages et mapping des index de monuments"
  }
}

PUT /monuments-v3
```

## Diapositive 61

**Vectoriser les monuments : une tâche de fond**

Dans la console de Kibana :

- recopier la Bretagne d'abord, en tâche de fond
- puis tous les autres monuments
- où en sont les recopies ?

```text
POST /_reindex?wait_for_completion=false
{"source": {"index": "monuments", "query": {"term": {"region": "Bretagne"}}}, "dest": {"index": "monuments-v3"}}

POST /_reindex?wait_for_completion=false
{
  "source": {"index": "monuments", "query": {"bool": {"must_not": {"term": {"region": "Bretagne"}}}}},
  "dest": {"index": "monuments-v3"}
}

GET /_tasks?actions=*reindex&detailed=true&filter_path=nodes.*.tasks.*.action,nodes.*.tasks.*.status.total,nodes.*.tasks.*.status.created,nodes.*.tasks.*.running_time_in_nanos
```

## Diapositive 63

**Les photos : des vecteurs calculés à côté**

~/projets/formation-elasticsearch/patrimoine/photos/vectoriser.py : à coller dans nano, deux diapositives plus loin

```python
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
```

## Diapositive 64

**Le fichier fourni : la liste des 300 photos**

~/projets/formation-elasticsearch/patrimoine/photos/photos-liste.ndjson : à coller dans nano, diapositive suivante

```json
{"reference":"PA00081941","nom":"palais des papes","fichier":"00 0711 Avignon (Frankreich) - Kathetrale und Papstpalast.jpg"}
{"reference":"PA00103291","nom":"pont du Combe Roussiere","fichier":"Pont de la Combe Roussière.jpg"}
{"reference":"PA00102588","nom":"cité de Carcassonne","fichier":"Cité de Carcassonne.jpg"}
{"reference":"PA00110460","nom":"abbaye du Mont-Saint-Michel","fichier":"Le Mont-Saint-Michel Abbaye de Mont-Saint-Michel Südseite 03.jpg"}
{"reference":"PA00084875","nom":"château du Haut-Koenigsbourg","fichier":"France Haut-Koenigsbourg aerial view (cropped).jpg"}
{"reference":"PA00078776","nom":"cathédrale Notre-Dame de Reims","fichier":"Reims Cathedral 016 8341.jpg"}
{"reference":"PA00113932","nom":"basilique Sainte-Marie-Madeleine","fichier":"Vezelay-7776-Bearbeitet.jpg"}
{"reference":"PA00092209","nom":"abbaye de Mozac","fichier":"Façade abbatiale Saint-Pierre de Mozac.jpg"}
{"reference":"PA00103057","nom":"pont Ambroix","fichier":"Ambrussum pont Ambroix.JPG"}
{"reference":"PA00086570","nom":"Paris-Lyon","fichier":"P1210896 Paris XII gare de Lyon rwk.jpg"}
{"reference":"IA00129694","nom":"cimetière des Chiens","fichier":"AsnieresSurSeine CimetiereDesChiens Portail.jpg"}
{"reference":"PA00118437","nom":"abbaye d'Aulps","fichier":"Aulps abbey 04.jpg"}
{"reference":"PA00086780","nom":"cimetière du Père-Lachaise","fichier":"Main gate of the Père-Lachaise Cemetery, Paris 13 June 2014.jpg"}
{"reference":"PA00103208","nom":"abbaye de Saint-Gilles","fichier":"Abbatiale Saint-Gilles 07.jpg"}
{"reference":"PA00097268","nom":"château d'Azay-le-Ferron","fichier":"Château d'Azay-Le-Ferron.jpg"}
{"reference":"PA13000065","nom":"L'Estaque","fichier":"Gare-Estaque06.jpg"}
{"reference":"MI041","nom":"château de Saché","fichier":"Saché Castle.jpg"}
{"reference":"EA30000033","nom":"port-Camargue","fichier":"Aerial view of Port Camargue.jpg"}
{"reference":"PA00118434","nom":"église Saint-Gervais-et-Saint-Protais de Saint-Gervais-les-Bains","fichier":"St-Gervais-les-Bains 100610 (4).JPG"}
{"reference":"PA30000018","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA30000019","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA00094677","nom":"Castel-Gesta","fichier":"Castel Gesta - Toulouse 02.jpg"}
{"reference":"PA00118365","nom":"colonne de Charles Félix","fichier":"Colonne de Charles Félix, Bonneville.jpg"}
{"reference":"PA00108749","nom":"maison Trochon","fichier":"Quai Fosse n17.JPG"}
{"reference":"PA00114905","nom":"remparts de Senlis","fichier":"Senlis (Oise), rempart des Ôtages.jpg"}
{"reference":"PA00086006","nom":"statue équestre d'Henri IV","fichier":"Equestrian monument to Henri IV of France 2009-06-02.jpg"}
{"reference":"PA00090572","nom":"théâtre Victor Hugo","fichier":"Fougères - théâtre façade.jpg"}
{"reference":"PA00093587","nom":"viaduc de Barajol","fichier":"Saint-Amandin - viaduc de Barajols 20200810-02.jpg"}
{"reference":"PA06000050","nom":"église Saint-Jean-Baptiste de Coaraze","fichier":"Coaraze -20.JPG"}
{"reference":"PA00118426","nom":"église Saint-Jean-Baptiste de La Roche-sur-Foron","fichier":"Église Saint-Jean-Baptiste de La Roche-sur-Foron-04 (2019).jpg"}
{"reference":"ACR0000709","nom":"église Saint-Léon de Paris","fichier":"Église Saint Léon - Paris XV (FR75) - 2026-06-28 - 14.jpg"}
{"reference":"PA00118451","nom":"église Saint-Maurice de Thônes","fichier":"Façade Église Saint-Maurice de Thônes (août 2026).JPG"}
{"reference":"PA00118379","nom":"église Saint-Nicolas de Combloux","fichier":"Combloux, Rhône-Alpes.jpg"}
{"reference":"PA00107580","nom":"église Saint-Étienne de Lille","fichier":"Lille Eglise Saint Etienne.jpg"}
{"reference":"PA00105790","nom":"manufacture d'armes de Châtellerault","fichier":"Châtellerault - La Manufacture - Musée.JPG"}
{"reference":"IA73001294","nom":"temple de Diane d'Aix-les-Bains","fichier":"Savoy juli 09 251a.jpg"}
{"reference":"PA00085683","nom":"Saint Maurice","fichier":"2014-09-07 14-29-30 statue-PA00085683.jpg"}
{"reference":"IA97200198","nom":"église Notre-Dame-de-la-Délivrande du Morne-Rouge","fichier":"ND Délivrande Morne-Rouge 1.jpg"}
{"reference":"PA00107596","nom":"hôtel des Cariatides","fichier":"Lille maison cariatides.JPG"}
{"reference":"PA00111521","nom":"église Notre-Dame de Malloué","fichier":"Malloué - Eglise Notre-Dame (1).JPG"}
{"reference":"PA25000013","nom":"forge de Montagney","fichier":"Montagney, vue générale de la forge.jpg"}
{"reference":"PA00084197","nom":"moulin d'Henri IV","fichier":"Barbaste site moulin des tours.jpg"}
{"reference":"PA97200003","nom":"villa Primerose","fichier":"Fort-de-France - Villa Primerose, février 2014, 01.jpg"}
{"reference":"IA00111985","nom":"monument national du Hartmannswillerkopf","fichier":"Vosges 013.jpg"}
{"reference":"PA00091137","nom":"tumulus de Crucuny","fichier":"Tumulus de Crucuny 7591.JPG"}
{"reference":"PA00079933","nom":"hôtel de ville d'Épinay-sur-Seine","fichier":"Hôtel ville Épinay Seine 1.jpg"}
{"reference":"PA00089294","nom":"manoir de Gollodic","fichier":"Manoir de Gollodic à Lanrivain.jpg"}
{"reference":"PA00090568","nom":"maison, 20 rue du Nançon","fichier":"Fougères - 20 rue du Nançon.jpg"}
{"reference":"IA41000016","nom":"cloître Saint-Saturnin","fichier":"« Cloître » de Saint-Saturnin.JPG"}
{"reference":"IA11000063","nom":"chapelle des Pénitents-Bleus de Narbonne","fichier":"2023-07-08 12-44-18 - Narbonne - Chapelle des Pénitents-Bleus.jpg"}
{"reference":"PA00107456","nom":"hôtel du Dauphin","fichier":"Hôtel du Dauphin - Douai.jpg"}
{"reference":"PA00117244","nom":"ferme des Loives","fichier":"Vue d'ensemble de la ferme des Loives.jpg"}
{"reference":"PA09000024","nom":"ensemble monumental de Tourtouse","fichier":"L'église et le donjon-clocher de Tourtouse (Ariège).jpg"}
{"reference":"PA00090202","nom":"chapelle Saint-Herbot de Saint-Herbot","fichier":"Saint-Herbot (29) Église 02.jpg"}
{"reference":"PA29000029","nom":"monument aux morts de Saint-Pol-de-Léon","fichier":"Saint-Pol-de-Léon (29) Monument aux morts 01.JPG"}
{"reference":"PA50000090","nom":"théâtre Roger-Ferdinand","fichier":"Saint-Lô - Théâtre Roger Ferdinand.JPG"}
{"reference":"PA53000037","nom":"église Saint-Martin de Louvigné","fichier":"Louvigné - Église Saint-Martin 01.jpg"}
{"reference":"IA35005135","nom":"moulin à marée de Montmarin","fichier":"Montmarin.jpg"}
{"reference":"IA00125099","nom":"église Saint-Maurice de La Chapelle-d'Abondance","fichier":"St Maurice church in La Chapelle-d'Abondance (1).jpg"}
{"reference":"PA02000093","nom":"monument américain de Château-Thierry","fichier":"Monument américain de Château-Thierry.jpg"}
{"reference":"PA00088482","nom":"jardin des plantes de Paris","fichier":"Paris 75005 Grande Galerie de l'Evolution 20070804.jpg"}
{"reference":"PA00110608","nom":"Tatihou","fichier":"Île de Tatihou.jpg"}
{"reference":"PA75130007","nom":"église Sainte-Anne de la Butte-aux-Cailles","fichier":"Église Sainte Anne Butte Cailles - Paris XIII (FR75) - 2021-07-21 - 2.jpg"}
{"reference":"IA00067391","nom":"abbaye Saint-Winoc de Bergues","fichier":"0 Tours de l'ancienne abbaye St-Winoc à Bergues (Nord) 1.jpg"}
{"reference":"IA63000560","nom":"Le Mont-Dore","fichier":"Gare du Mont Dore 10.JPG"}
{"reference":"MI049","nom":"atelier Renoir","fichier":"Essoyes atelier Renoir.jpg"}
{"reference":"PA00089961","nom":"château de Joyeuse Garde","fichier":"Château de la Joyeuse Garde, ruine de la porte.jpg"}
{"reference":"PA00117779","nom":"château de la Barollière","fichier":"Château de la Barollière.jpg"}
{"reference":"PA00114885","nom":"château royal de Senlis et prieuré Saint-Maurice","fichier":"Senlis - Château royal.jpg"}
{"reference":"PA66000026","nom":"ermitage Saint-Guillem de Combret","fichier":"Ermitage St Guilhem de Combret.JPG"}
{"reference":"PA70000034","nom":"maison forte de Chariez","fichier":"Chariez. Maison forte. 2015-01-13..JPG"}
{"reference":"PA00103609","nom":"promenade du Peyrou","fichier":"Promenade du Peyrou Montpellier.jpg"}
{"reference":"PA00109435","nom":"église Saint-Clément de Saint-Clément-des-Levées","fichier":"Saint-Clément-des-Levées - Église Saint-Clément 20210729-01.jpg"}
{"reference":"IA00051858","nom":"église Saint-Jean-Baptiste de Saint-Léger-en-Yvelines","fichier":"St Léger 78 Église2.jpg"}
{"reference":"PA00118428","nom":"église Sainte-Agathe de Rumilly","fichier":"Église Sainte-Agathe de Rumilly.jpg"}
{"reference":"PA92000004","nom":"soufflerie Hispano-Suiza","fichier":"Soufflerie Hispano-Suiza.jpg"}
{"reference":"PA00081180","nom":"obélisque d'Arles","fichier":"Arles Obélisque.jpg"}
{"reference":"PA00086721","nom":"école normale de musique de Paris","fichier":"EcoleNormaledeMusiquedeParis.JPG"}
{"reference":"MI179","nom":"musée Curie","fichier":"Pavillon Pasteur.jpg"}
{"reference":"PA55000002","nom":"ossuaire de Douaumont","fichier":"Ossuaire de Douaumont, Verdun 1914-1918 P-FG-CP-01050-13.jpg"}
{"reference":"PA00135390","nom":"voie Domitienne","fichier":"Ambrussum voies marquées 10-04-2006.jpg"}
{"reference":"MI206","nom":"musée national Eugène-Delacroix","fichier":"Musée Delacroix, Paris 29 May 2017 001.jpg"}
{"reference":"PA00081103","nom":"pavillon Vendôme","fichier":"Pavillon de Vendome Aix-en-Provence 01.jpg"}
{"reference":"IA00126359","nom":"cimetière de Levallois-Perret","fichier":"Levallois-Perret Cemetery6845.JPG"}
{"reference":"PA04000037","nom":"clos de Villeneuve","fichier":"Clos de Villeneuve à 04210 Valensole.jpg"}
{"reference":"PA74000039","nom":"statue du Christ-Roi","fichier":"Statue du Christ-Roi des Houches.jpg"}
{"reference":"PA00092687","nom":"abbaye Saint-André de Lavaudieu","fichier":"F08.Lavaudieu.0151.JPG"}
{"reference":"ACR0000004","nom":"barrage de Génissiat","fichier":"Talsperre Genissiat 01 09.jpg"}
{"reference":"PA00103023","nom":"voie Domitienne","fichier":"Ambrussum voies marquées 10-04-2006.jpg"}
{"reference":"PA00091516","nom":"dolmen du Kernourz","fichier":"K 1 Tumulus von Kernours C.jpg"}
{"reference":"EA92000017","nom":"tours Aillaud","fichier":"Tours Aillaud, de la prefecture des Hauts de Seine.JPG"}
{"reference":"PA00091076","nom":"alignements de Kermario","fichier":"Kermario-Mitte und -West.jpg"}
{"reference":"PA00117820","nom":"hôtel de ville de Lyon","fichier":"Avant de l’hôtel de ville (Lyon, 2026).jpg"}
{"reference":"PA00117986","nom":"stade de Gerland","fichier":"Matmut stadium de gerland.jpg"}
{"reference":"PA00098337","nom":"château de Blois","fichier":"Loire Cher Blois1 tango7174.jpg"}
{"reference":"PA00093524","nom":"château de Val","fichier":"Chateau de Val.jpg"}
{"reference":"IA00007313","nom":"La Roche-aux-Fées","fichier":"LaRocheAuxFees Dolmen 2 20070408.jpg"}
{"reference":"PA00080780","nom":"cathédrale Saint-Nicolas","fichier":"Cathédrale ortodoxe russe.jpg"}
{"reference":"PA00089847","nom":"château de Brest","fichier":"17-10-2005-318donjonbrest.jpg"}
{"reference":"PA00093448","nom":"abbaye Saint-Géraud d'Aurillac","fichier":"Aurillac - Eglise Saint-Géraud -1.jpg"}
{"reference":"PA00086068","nom":"annexe du siège central du Crédit lyonnais","fichier":"P1030070 Paris II rue Ménars Immeuble n°6 rwk.JPG"}
{"reference":"PA00103592","nom":"hôtel des Trésoriers de France","fichier":"Hôtel des Trésoriers de France (Montpeller) - 1.jpg"}
{"reference":"PA00090803","nom":"malouinière de la Chipaudière","fichier":"Malouinière de la Chipaudière - vue du jardin 3.JPG"}
{"reference":"PA97600002","nom":"mosquée de Tsingoni","fichier":"Tsingoni minaret.jpg"}
{"reference":"PA00094510","nom":"couvent des Augustins de Toulouse","fichier":"Augustins - Grand cloître et clocher des Augustins de Toulouse.jpg"}
{"reference":"PA00090870","nom":"Grand Bé","fichier":".00 2361 Fort du Petit Bé - Ford Grand Bé (Bucht von Saint-Malo).jpg"}
{"reference":"IA35022170","nom":"hôtel de Cuillé","fichier":"Rennes - HôteldeCuillé façade.jpg"}
{"reference":"MI142","nom":"maison « Le Paraïs »","fichier":"Maison Paraïs Manosque 3.jpg"}
{"reference":"PA00116616","nom":"manoir de Marmont","fichier":"Manoir marmont 2014-09-07 16.54.45.jpg"}
{"reference":"PA02000005","nom":"monument de la Pierre d'Haudroy","fichier":"Monument de la Pierre d'Haudroy 012pcp.jpg"}
{"reference":"PA97600007","nom":"mosquée de Tsingoni","fichier":"Tsingoni minaret.jpg"}
{"reference":"PA00114907","nom":"remparts de Senlis","fichier":"Senlis (Oise), rempart des Ôtages.jpg"}
{"reference":"PA00114909","nom":"remparts de Senlis","fichier":"Senlis (Oise), rempart des Ôtages.jpg"}
{"reference":"PA00114890","nom":"remparts de Senlis","fichier":"Senlis (Oise), rempart des Ôtages.jpg"}
{"reference":"PA01000049","nom":"Vierge du Mas Rillier","fichier":"Vierge du Mas Rillier.jpg"}
{"reference":"PA00118383","nom":"église Notre-Dame-de-l'Assomption de Cordon","fichier":"Clocher de Cordon.jpg"}
{"reference":"PA00103976","nom":"église Saint-Fructueux de Camélas","fichier":"Camelas Eglise.JPG"}
{"reference":"PA00090559","nom":"église Saint-Léonard de Fougères","fichier":"Fougères (35) Église Saint-Léonard Flanc nord.jpg"}
{"reference":"PA00087009","nom":"église Saint-Martin de La Genevraye","fichier":"Eglise Saint-Martin de La Genevraye.jpg"}
{"reference":"PA00118454","nom":"château de Ripaille","fichier":"Thonon-les-Bains Ripaille.jpg"}
{"reference":"PA00103064","nom":"voie Domitienne","fichier":"Ambrussum voies marquées 10-04-2006.jpg"}
{"reference":"PA00103175","nom":"voie Domitienne","fichier":"Ambrussum voies marquées 10-04-2006.jpg"}
{"reference":"PA00103408","nom":"voie Domitienne","fichier":"Ambrussum voies marquées 10-04-2006.jpg"}
{"reference":"IA00130866","nom":"église Saint-Sulpice de Gennes-sur-Seiche","fichier":"Gennes-sur-Seiche (35) Église 2.jpg"}
{"reference":"IA00006702","nom":"hôtel Gefflot de Marigny","fichier":"Fougères (35) Hôtel de Marigny 01.JPG"}
{"reference":"PA62000055","nom":"hôtel de ville de Calais","fichier":"Calais hotel de ville face.jpg"}
{"reference":"PA00103594","nom":"hôtel de Varennes","fichier":"Hôtel de Varennes à Montpellier (France).jpg"}
{"reference":"PA00083179","nom":"entrepôt Lainé","fichier":"Entrepôt Lainé.JPG"}
{"reference":"PA00109565","nom":"menhir de la Broussardière","fichier":"FrancePaysDeLaLoireMontaudinMenhirBoussardiere.jpg"}
{"reference":"PA59000062","nom":"salle des fêtes de Lille-Fives","fichier":"Lille salle fetes Five.JPG"}
{"reference":"PA00083806","nom":"croix de cimetière de Saint-Sulpice-et-Cameyrac","fichier":"Croix cimetière Saint Sulpice vue générale.JPG"}
{"reference":"PA25000036","nom":"château de Lods","fichier":"Lods, le château-2.jpg"}
{"reference":"PA00113852","nom":"palais archiépiscopal de Sens","fichier":"2012--DSC 0160--Ancien-Palais-des-archevêques-de-Sens.jpg"}
{"reference":"PA00086629","nom":"maison Ozenfant","fichier":"P1110724 Paris XIV square de Montsouris et avenue de Reille rwk.JPG"}
{"reference":"PA00089421","nom":"manoir de Toul-an-Golet","fichier":"Toul-an-golet.png"}
{"reference":"PA00090349","nom":"maison des Cariatides","fichier":"Quimper - Maison des Cariatides - 4 rue du Guéodet - 001.jpg"}
{"reference":"PA00096834","nom":"abbaye Saint-Martin de Massay","fichier":"Massay - Abbaye Saint-Martin - Salle capitulaire et tour Chamborand de l'église Saint-Paxent (ancienne abbatiale).JPG"}
{"reference":"PA00097249","nom":"château de Villemesle","fichier":"Boisgassonchatovillemesle.JPG"}
{"reference":"PA00102791","nom":"chapelle des Pénitents blancs de Narbonne","fichier":"Chapelle des Pénitents blancs de Narbonne001.JPG"}
{"reference":"PA00102813","nom":"immeuble, 3 rue de Lamourguier","fichier":"Immeuble, 3 rue de Lamourguier.jpg"}
{"reference":"PA46000057","nom":"dolmen des Barrières n° 3","fichier":"Dolmen des Barrières n°3 Miers 4.jpg"}
{"reference":"PA00082886","nom":"église Saint-Pierre-et-Saint-Paul de Saint-Paul-Lizonne","fichier":"Stpaulliz eg1.JPG"}
{"reference":"PA00092474","nom":"croix de Vollore-Ville","fichier":"Vollore-Ville - Croix place de la Poste 20210811-02.jpg"}
{"reference":"PA29000051","nom":"manoir du Laz","fichier":"Manoir du Laz.jpg"}
{"reference":"PA37000008","nom":"hôtel de la Caisse d'épargne de Loches","fichier":"Hotel de Caisse d'Epargne in Loches.jpg"}
{"reference":"PA26000034","nom":"hôtel de ville de Valence","fichier":"Valence 2006-03-03 006.jpg"}
{"reference":"PA00117318","nom":"cirque romain de Vienne","fichier":"Pyramide de Vienne (Isère).jpg"}
{"reference":"PA00100694","nom":"abbaye de Graville","fichier":"Graville1.jpg"}
{"reference":"PA00095426","nom":"cathédrale Notre-Dame-de-la-Sède de Tarbes","fichier":"Cathédrale Notre-Dame-de-la-Sède de Tarbes.JPG"}
{"reference":"PA00104538","nom":"château de Vilhonneur","fichier":"Vilhonneur3.JPG"}
{"reference":"PA00080809","nom":"villa Arson","fichier":"Villa Arson - ancien batiment.jpg"}
{"reference":"PA75050002","nom":"collège Sainte-Barbe","fichier":"Collège Sainte-Barbe, 4 rue Valette, Paris 5e 1.jpg"}
{"reference":"PA00088402","nom":"collège de Beauvais","fichier":"RueJ-de-beauvais.jpg"}
{"reference":"PA00100297","nom":"collégiale Saint-Pierre du Dorat","fichier":"St Peter collegiate in Le Dorat (1).jpg"}
{"reference":"PA00086509","nom":"Colonel Fabien","fichier":"Édicule Guimard - station Colonel Fabien.jpg"}
{"reference":"EA12000001","nom":"viaduc de Millau","fichier":"00 0237 Millau - Département Aveyron.jpg"}
{"reference":"IA92000336","nom":"Gare du Val d'Or","fichier":"Gare Val d'Or.JPG"}
{"reference":"PA30000028","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA30000010","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA30000004","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA30000009","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA60000021","nom":"carrière du Chauffour","fichier":"Thiescourt Carriere Chauffour Jeanne d'Arc.jpg"}
{"reference":"PA00118375","nom":"château de Clermont","fichier":"Château de Clermont - Galeries intérieures - 12 (2022).jpg"}
{"reference":"MI151","nom":"château de Voltaire","fichier":"Vue sur la façade Est du château de Voltaire depuis le jardin français.jpg"}
{"reference":"PA00116395","nom":"château de Voltaire","fichier":"Vue sur la façade Est du château de Voltaire depuis le jardin français.jpg"}
{"reference":"PA00090558","nom":"couvent des Clarisses Urbanistes de Fougères","fichier":"Couvent des Clarisses Urbanistes de Fougères 02.jpg"}
{"reference":"IA94000411","nom":"fort de Montrouge","fichier":"Fort de montrouge portique.jpg"}
{"reference":"IA67007715","nom":"abbatiale Saint-Étienne de Marmoutier","fichier":"Marmoutier eglise.jpg"}
{"reference":"PA00095597","nom":"église Saint-André de Magrin","fichier":"St Andrew church in St-Andre (5).jpg"}
{"reference":"PA2B000041","nom":"église Saint-Blaise de Poggio-Marinaccio","fichier":"Eglise-Saint-Blaise2.jpg"}
{"reference":"IA40001327","nom":"église Saint-Saturnin de Léon","fichier":"Léon - Landes (40).jpg"}
{"reference":"IA35027186","nom":"stade du Commandant Bougouin","fichier":"Vélodrome Rennes.JPG"}
{"reference":"PA44000064","nom":"château de Rochefort","fichier":"La Haie-Fouassière château Rochefort.jpg"}
{"reference":"IA00015510","nom":"chapelle Notre-Dame-de-la-Salette de Lavigny","fichier":"Chapelle de Lavigny.jpg"}
{"reference":"IA00014718","nom":"chapelle Notre-Dame-du-Chêne de Scey-Maisières","fichier":"Scey-Maisières. Chapelle de l'ermitage de Notre-Dame du chêne. 2015-12-19.JPG"}
{"reference":"PA11000053","nom":"église Notre-Dame-du-Cros de Caunes-Minervois","fichier":"Caunes-Minervois - chapelle Notre-Dame-du-Cros de Caunes-Minervois - 20130531165417.jpg"}
{"reference":"IA00015345","nom":"chapelle Saint-Claude-et-Saint-Thiébaud de Saint-Lothain","fichier":"Saint Lothain 31.jpg"}
{"reference":"IA00014284","nom":"chapelle Sainte-Trinité-Saint-Roch-Saint-Sébastien dite chapelle Niai Nion de Dommartin","fichier":"Dommartin - chapelle Niai-Nion.jpg"}
{"reference":"PA72000056","nom":"chapelle Saint-Maximin de Montreuil","fichier":"Montreuil - Ancienne église Saint-Maximin.jpg"}
{"reference":"IA78000249","nom":"temple protestant de Jouy-en-Josas","fichier":"Temple Jouy-en-Josas facade2.jpg"}
{"reference":"IA00049439","nom":"bibliothèque du Chapitre, Cathédrale de Noyon","fichier":"Noyon (60), cathédrale Notre-Dame, bibliothèque du chapitre, façade principale sud-est 2.jpg"}
{"reference":"PA13000086","nom":"hôtel Léautaud de Mas Blanc","fichier":"Hôtel de Léautaud de Mas-Blanc 01.jpg"}
{"reference":"PA62000158","nom":"monument aux morts de Béthune","fichier":"Béthune - Monument aux morts.jpg"}
{"reference":"IA63000695","nom":"hôtel de ville de La Bourboule","fichier":"La Bourboule - hôtel de ville 20200811.jpg"}
{"reference":"IA00060678","nom":"immeuble, 15 rue Gabrielle","fichier":"Immeuble 15 rue Gabrielle Charenton Pont 3.jpg"}
{"reference":"IA00076112","nom":"usine de Matériel Électrique Industriel","fichier":"Usine Matériel Électrique Industriel - Montrouge (FR92) - 2026-11-01 - 3.jpg"}
{"reference":"IA29000436","nom":"chapelle Saint-Diboan de Loc Ivy","fichier":"Tréméven Chapelle Saint-Diboan 1920.jpg"}
{"reference":"IA29003401","nom":"chapelle Notre-Dame-de-Lorette de Plogonnec","fichier":"305 Plogonnec Chapelle Notre-Dame de Lorette.jpg"}
{"reference":"IA00027815","nom":"chapelle funéraire de la famille Chièze","fichier":"Le Vesinet.Chieze.Mvc-004x.jpg"}
{"reference":"IA56003335","nom":"grand séminaire de Vannes","fichier":"Vannes grand séminaire.JPG"}
{"reference":"IA00115028","nom":"maison au 19 rue du Docteur Stoltz","fichier":"Andlau rDocteurStoltz 19.JPG"}
{"reference":"IA35132819","nom":"marégraphe de Saint-Servan","fichier":"FMIB 36840 Observatoire Maregraphique etable a l'Embouchure de la Rance, a Saint-Servan (Ille-et-Vilaine).jpeg"}
{"reference":"IA00014323","nom":"chapelle de la Vierge d'Houtaud","fichier":"Houtaud, la chapelle de la Vierge.jpg"}
{"reference":"EA67141193","nom":"faculté de droit","fichier":"Unistra tour de chimie et faculté de droit Strasbourg août 2019.jpg"}
{"reference":"PA75070008","nom":"église Saint-François-Xavier de Paris","fichier":"Saint-François Xavier 2010.jpg"}
{"reference":"PA00100697","nom":"église Saint-Joseph du Havre","fichier":"Église Saint-Joseph (52304780830).jpg"}
{"reference":"PA00114578","nom":"château de Chantilly","fichier":"Chateau de Chantilly FRA 003.JPG"}
{"reference":"PA00106840","nom":"fort de Metz-Queuleu","fichier":"Fort de Queuleu.jpg"}
{"reference":"IA00124576","nom":"château de l'Ortenbourg","fichier":"Château de l'Ortenbourg face est vue aérienne.jpg"}
{"reference":"IA00020394","nom":"chêne d'Allouville","fichier":"Chêne d'Allouville-Bellefosse 02.jpg"}
{"reference":"PA00091380","nom":"dolmen de Kercadoret","fichier":"Dolmen de Kercadoret à Locmariaquer Jean-Charles GUILLO.JPG"}
{"reference":"PA00085839","nom":"colonne Médicis","fichier":"Fontaine de la Halle aux Blés Paris 4e 001.jpg"}
{"reference":"PA00085790","nom":"colonne Vendôme","fichier":"Vendome Column A.jpg"}
{"reference":"IA00075644","nom":"synagogue de Rosheim","fichier":"Rosheim Synagogue d.jpg"}
{"reference":"PA00082810","nom":"Combe-Capelle","fichier":"Plandelacollinedecombecapelle.jpg"}
{"reference":"PA00092254","nom":"abbaye de Montpeyroux","fichier":"Puy-Guillaume Abbaye de Montpeyroux.jpg"}
{"reference":"PA00108653","nom":"La Cigale","fichier":"Restaurant La Cigale (devanture) - Nantes.jpg"}
{"reference":"PA00104086","nom":"Ruscino","fichier":"Château-Roussillon - Oppidum de Ruscino-01.jpg"}
{"reference":"PA00078437","nom":"ouvrage de La Ferté","fichier":"La Ferté 01.JPG"}
{"reference":"PA00090553","nom":"La Roche-aux-Fées","fichier":"LaRocheAuxFees Dolmen 2 20070408.jpg"}
{"reference":"PA00118343","nom":"château d'Annecy","fichier":"Château d'Annecy.jpg"}
{"reference":"PA00082100","nom":"cathédrale Notre-Dame-de-Nazareth d'Orange","fichier":"Orange (Vaucluse), Cathédrale Notre-Dame-de-Nazareth..JPG"}
{"reference":"PA00118438","nom":"collégiale Saint-Jacques de Sallanches","fichier":"Sallanches - Collégiale Saint-Jacques-le-Majeur - 1.jpg"}
{"reference":"IA00065244","nom":"église Saint-Martin de Montmédy","fichier":"Montmédy haut E1aJPG.jpg"}
{"reference":"PA00097335","nom":"abbaye de Déols","fichier":"Déols - Abbey - 2.jpg"}
{"reference":"PA30000022","nom":"aqueduc de Nîmes","fichier":"Pont du Gard ..jpg"}
{"reference":"PA00118338","nom":"pierre à Passet","fichier":"Bloc erratique sculpté d'Allinges - PA00118338.jpg"}
{"reference":"PA00118296","nom":"cathédrale Saint-Jean-Baptiste de Saint-Jean-de-Maurienne","fichier":"Saint-Jean-de-Maurienne - Cathédrale -1.JPG"}
{"reference":"PA00098260","nom":"château de Tours","fichier":"Tours - château.JPG"}
{"reference":"PA00108760","nom":"théâtre Graslin","fichier":"Théâtre Graslin - Place Graslin, Nantes.jpg"}
{"reference":"PA00098336","nom":"cathédrale Saint-Louis de Blois","fichier":"Cathedrale St Louis.jpg"}
{"reference":"PA00099112","nom":"Stantari","fichier":"Stantari.jpg"}
{"reference":"PA00132602","nom":"tour de Capo-Nero","fichier":"Tour génoise de Capu Neru (golfe de Valinco, Corse-du-Sud).jpg"}
{"reference":"PA00099279","nom":"tour de la Mortella","fichier":"Tour de la Mortella.jpg"}
{"reference":"PA22000021","nom":"château de Léhon","fichier":"Chateau Léhon.JPG"}
{"reference":"MI036","nom":"fort Sarah Bernhardt","fichier":"Belle-Ile fort de Sarah Bernard juillet.jpg"}
{"reference":"PA00086586","nom":"pavillon de la barrière d'eau","fichier":"Pavillon de la barrière d'eau, Paris - 03.jpg"}
{"reference":"PA37000024","nom":"maison","fichier":"Maison, 40 rue Picois, Loches.jpg"}
{"reference":"IA68004393","nom":"ferme au 61 rue de la Vallée","fichier":"Soultzmatt rVallée 61.JPG"}
{"reference":"IA00005908","nom":"chapelle Saint-Thégonnec de Plogonnec","fichier":"234 Plogonnec Chapelle Saint-Egonnec.jpg"}
{"reference":"IA00005905","nom":"chapelle Saint-Albin de Plogonnec","fichier":"248 Plogonnec Chapelle Saint-Albin.jpg"}
{"reference":"IA21000313","nom":"monument aux morts de la guerre de 1870 de Beaune","fichier":"Beaune - Monument aux morts de la guerre de 1870-1871.jpg"}
{"reference":"IA21000113","nom":"hôtel de la Caisse d'épargne de Beaune","fichier":"Beaune Eté2016 la caisse d'épargne.jpg"}
{"reference":"PA75170009","nom":"ancienne usine des cafés Patin","fichier":"Façade du 8 rue de Levis à Paris.jpg"}
{"reference":"IA85000461","nom":"hôtel de la Caisse d'épargne de Fontenay-le-Comte","fichier":"Fontenay-le-Comte - Place Belliard (3) - cropped.jpg"}
{"reference":"PA41000073","nom":"église Saint-Denis de Villexanton","fichier":"Villexanton-église.jpg"}
{"reference":"IA63000338","nom":"église Saint-Georges de Nébouzat","fichier":"Nebouzat l'église dédiée à saint Georges.jpg"}
{"reference":"IA00014097","nom":"église Saint-Gervais-Saint-Protais de Sombacour","fichier":"Sombacour, église - img 44344.jpg"}
{"reference":"IA00015908","nom":"église Saint-Léger de Virey","fichier":"Virey, l'église.jpg"}
{"reference":"IA00015571","nom":"église Saint-Rémy de Plainoiseau","fichier":"Église St Rémy Plainoiseau 5.jpg"}
{"reference":"IA00016223","nom":"église Saints-Pierre-et-Paul de Gézier-et-Fontenelay","fichier":"Gézier, l'église.jpg"}
{"reference":"PA83000040","nom":"église Saint-Pierre de Salernes","fichier":"Salernes - église 3.JPG"}
{"reference":"IA00015464","nom":"chapelle Notre-Dame-du-Mont","fichier":"Chapelle mortuaire de Frontenay (Jura).jpg"}
{"reference":"IA00020475","nom":"chapelle Saint-Gilles d'Alvimbuc","fichier":"Veauville-lès-Baons (Seine-Mar.) chapelle Saint-Gilles d'Alvimbuc (02).jpg"}
{"reference":"PA79000047","nom":"chapelle Saint-Joseph de la Chapelle-Largeau","fichier":"Chapelle Saint-Joseph (La Chapelle-Largeau)2.jpg"}
{"reference":"IA00131079","nom":"église Saint-Malo de Paramé","fichier":"Saint-Malo (35) Église Saint-Malo de Paramé.jpg"}
{"reference":"PA23000027","nom":"château du domaine de La Forêt","fichier":"Château de Blessac.jpg"}
{"reference":"PA62000159","nom":"palais de justice de Béthune","fichier":"Bethune tribunal.jpg"}
{"reference":"PA97100071","nom":"monument aux morts de Petit-Canal","fichier":"WW1 monument Petit-Canal 2010-03-28.jpg"}
{"reference":"IA00006711","nom":"hôtel Hay de Bonteville","fichier":"Fougères, 10bis rue Lesueur.jpg"}
{"reference":"IA00008347","nom":"château de Menoray","fichier":"Locmalo Château de Menoray Lemaire 1.png"}
{"reference":"IA00060679","nom":"immeuble, 33 rue Gabrielle, 1 rue Labouret","fichier":"Immeuble 33 rue Gabrielle 1 rue Labouret Charenton Pont 4.jpg"}
{"reference":"IA63000557","nom":"bureau de poste de Mont-Dore","fichier":"Le Mont-Dore la poste.JPG"}
{"reference":"IA00013852","nom":"chapelle Sainte-Anne de Montlebon","fichier":"Montlebon, la chapelle Sainte-Anne.jpg"}
{"reference":"IA00014850","nom":"chapelle du Sacré-Cœur d'Audincourt","fichier":"Audincourt, Chapelle du Sacré-Cœur.jpg"}
{"reference":"IA35026321","nom":"château de Maurepas","fichier":"Château de Maurepas (956.0002.179).jpg"}
{"reference":"PA00095110","nom":"dolmen de la Beaune","fichier":"Issendolus Baune.JPG"}
{"reference":"IA35026313","nom":"lycée Assomption","fichier":"L'Assomption-Rennes.jpg"}
{"reference":"IA22005206","nom":"château de Kermaria","fichier":"Château de Kermaria (Yvignac-la-Tour, Côtes-d'Armor).jpg"}
{"reference":"IA56000304","nom":"château de Meslien","fichier":"018 Cléguer Château de Meslien.jpg"}
{"reference":"IA47000844","nom":"chapelle Notre-Dame-du-Lot d'Aiguillon","fichier":"Aiguillon - Musée Raoul-Dastrac -1.JPG"}
{"reference":"IA00060685","nom":"immeuble, 3 place Henri IV","fichier":"Immeuble 3 place Henri IV Charenton Pont 3.jpg"}
{"reference":"IA59002358","nom":"ancienne église Saint-Vincent-de-Paul du Crétinier","fichier":"Saint-Vincent-de-Paul Crétinier.jpg"}
{"reference":"IA54001087","nom":"chapelle Notre-Dame-de-Sion de Villars","fichier":"Chaouilley, Chapelle Notre-Dame de Villars 1.jpg"}
{"reference":"PA00084719","nom":"Temple-musée et site archéologique du Donon","fichier":"Donon Musée 01 05 2012 2.jpg"}
{"reference":"PA21000111","nom":"monument à Lazare Carnot","fichier":"Nolay Statue de Carnot 4.jpg"}
{"reference":"IA00014240","nom":"chapelle Notre-Dame-des-Sept-Douleurs de Courvières","fichier":"Courvières, chapelle - img 52056.jpg"}
{"reference":"PA00107907","nom":"bâtiment de l'École nationale supérieure des arts et industries textiles","fichier":"Roubaix Ensait.JPG"}
{"reference":"PA22000057","nom":"viaduc de Douvenant","fichier":"Langueux + Saint-Brieuc - Viaduc de Douvenant (rénové) 03.jpg"}
{"reference":"PA00086639","nom":"villa Seurat","fichier":"P1110202 Paris XIV villa Seurat rwk.JPG"}
{"reference":"PA00118417","nom":"église Notre-Dame-de-l'Assomption de Peillonnex","fichier":"Prieuré de Peillonex.JPG"}
{"reference":"PA00118407","nom":"église Saint-Jean-Baptiste de Megève","fichier":"Église de Megève 1.jpg"}
{"reference":"IA00125097","nom":"église Saint-Laurent de Châtel","fichier":"Église St-Laurent de Châtel (octobre 2021).JPG"}
{"reference":"PA00118368","nom":"église Saint-Michel de Chamonix-Mont-Blanc","fichier":"Eglise de chamonix.jpg"}
{"reference":"PA74000053","nom":"église de la Conversion-de-Saint-Paul de Saint-Paul-en-Chablais","fichier":"St Paul en Chablais église (1).JPG"}
{"reference":"PA00116235","nom":"château du Broutel","fichier":"Rue (Somme), France, Château du Broutel.JPG"}
{"reference":"PA00091186","nom":"dolmens de Mané Braz","fichier":"Dscn5212-mane-braz 800x600.jpg"}
{"reference":"PA00090555","nom":"beffroi de Fougères","fichier":"Fougères (35) Beffroi 13.JPG"}
{"reference":"IA35000308","nom":"Aquarium et Musée de la Mer de Dinard","fichier":"Dinard - Villa Bric à Brac 20200604-01.jpg"}
{"reference":"PA00097744","nom":"église Saint-Aignan d'Épeigné-les-Bois","fichier":"Epeigné-les-Bois église.jpg"}
{"reference":"PA00108397","nom":"église Saint-Léonard de Saint-Léonard","fichier":"Saint-Léonard - Église Saint-Léonard - 1.jpg"}
{"reference":"PA00108427","nom":"église Saint-Martin de Samer","fichier":"Samer - Église Saint-Martin.jpg"}
{"reference":"PA47000008","nom":"chapelle Notre-Dame-de-Tout-Pouvoir de Fongrave","fichier":"Fongrave - Chapelle Notre-Dame-de-Tout-Pouvoir -1.JPG"}
{"reference":"IA00033783","nom":"église Notre-Dame-de-la-Légion-d'honneur","fichier":"Longué - Église Notre-Dame-de-la-Légion-d'honneur.JPG"}
{"reference":"PA00084046","nom":"hôtel Hutot de Latour","fichier":"Agen - Hôtel Hutot de Latour -4.JPG"}
{"reference":"IA68007596","nom":"nécropole nationale du Wettstein","fichier":"Orbey 044.JPG"}
{"reference":"PA00091094","nom":"dolmen de Roch-Feutet","fichier":"Dolmen Roch-Feutet.JPG"}
{"reference":"PA00078844","nom":"immeubles sur la place du Général-Leclerc","fichier":"Ancienne Caisse d'Epargne 3726.JPG"}
{"reference":"PA00089866","nom":"église Saint-Jérôme de Cast","fichier":"Eglise Saint Jérôme - Cast.jpg"}
{"reference":"PA00093588","nom":"château de Roffiac","fichier":"Roffiac - tour du château 20200813-01.jpg"}
{"reference":"PA00106512","nom":"ancien hôtel de ville de Commercy","fichier":"Commercy.JPG"}
{"reference":"PA00135257","nom":"maison Saint-Yves","fichier":"Saint-Brieuc - Nouveau grand séminaire en 1926 - AD22 - 16FI4811.jpg"}
{"reference":"PA26000024","nom":"ancien temple protestant","fichier":"Poet Laval - temple Ancien village.jpg"}
{"reference":"PA00109052","nom":"petit menhir du Champ de la Garde","fichier":"Cholet petit-mnh-champ-garde 01.jpg"}
{"reference":"IA62002528","nom":"église de l'Immaculée-Conception de Saint-Omer","fichier":"Faubourg du Haut Pont - panoramio.jpg"}
{"reference":"IA00013855","nom":"église Notre-Dame-du-Rosaire des Fontenottes","fichier":"Montlebon, église des Fontenottes.jpg"}
{"reference":"IA63000257","nom":"église Saint-Sébastien de Saint-Genès-Champespe","fichier":"Saint-Genès-Champespe - Église Saint-Sébastien 20200810-01.jpg"}
{"reference":"PA00116633","nom":"hôtel Goudard-Ruelle","fichier":"Hotel goudard-ruelle2.jpg"}
{"reference":"PA00085821","nom":"hôtel de Villemaré","fichier":"Paris Hôtel de l'État-Major de la Place et du Gouvernement militaire 2012 6.jpg"}
{"reference":"PA00118461","nom":"hôtel de ville de Thonon-les-Bains","fichier":"200505-Thonon Hotel de Ville.JPG"}
```

## Diapositive 65

**Créer les deux fichiers des photos**

Dans le terminal : coller les trois lignes, puis Entrée :

- créer le dossier des photos
- ouvrir vectoriser.py : y coller son code, Ctrl+O, Entrée, Ctrl+X
- puis la liste des 300 photos, de la même façon

```bash
mkdir -p ~/projets/formation-elasticsearch/patrimoine/photos && \
nano ~/projets/formation-elasticsearch/patrimoine/photos/vectoriser.py && \
nano ~/projets/formation-elasticsearch/patrimoine/photos/photos-liste.ndjson
```

## Diapositive 66

**Les commandes : l'environnement de CLIP, puis les vecteurs**

Dans le terminal :

- un second Python à part, pour le modèle CLIP
- PyTorch, la bibliothèque de calcul, en version pour processeur
- CLIP (sentence-transformers), la lecture des images (pillow), les téléchargements (requests)
- aller dans le dossier des photos
- vectoriser les 300 photos : chaque photo devient un vecteur, dans photos.ndjson

```bash
python3 -m venv ~/elastic/venv-photos
~/elastic/venv-photos/bin/pip install -q torch --index-url https://download.pytorch.org/whl/cpu
~/elastic/venv-photos/bin/pip install -q sentence-transformers pillow requests
cd ~/projets/formation-elasticsearch/patrimoine/photos
~/elastic/venv-photos/bin/python vectoriser.py 300 photos.ndjson
```

## Diapositive 67

**Le champ dense_vector, et les 300 photos**

Dans la console de Kibana :

- l'index des photos, avec un champ dense_vector pour leurs vecteurs
- Puis le chargement des 300 photos, dans le terminal : diapositive suivante

```text
PUT /photos
{
  "mappings": {
    "properties": {
      "reference": {"type": "keyword"},
      "nom": {"type": "text"},
      "fichier": {"type": "keyword", "index": false},
      "image": {"type": "keyword", "index": false},
      "vecteur": {
        "type": "dense_vector",
        "dims": 512,
        "similarity": "cosine"
      }
    }
  }
}

# Puis le chargement des 300 photos, dans le terminal : diapositive suivante
```

## Diapositive 68

**Le chargement des 300 photos, dans le terminal**

Dans le terminal :

- une ligne d'action avant chaque photo, dans le fichier à charger
- charger les 300 photos en une requête _bulk

```bash
cd ~/projets/formation-elasticsearch/patrimoine/photos
jq -c '{"index":{"_id":.reference}}, .' photos.ndjson > ~/elastic/photos-bulk.ndjson
curl -s --cacert ~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt -u "elastic:$ELASTIC_PASSWORD" -X POST 'https://localhost:9200/photos/_bulk?refresh=true' -H 'Content-Type: application/x-ndjson' --data-binary @$HOME/elastic/photos-bulk.ndjson | jq -c '{errors, took, items: (.items|length)}'
curl -s --cacert ~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt -u "elastic:$ELASTIC_PASSWORD" 'https://localhost:9200/_cat/count/photos?v'
```

## Diapositive 69

**La recherche : les photos qui ressemblent à la Cité de Carcassonne**

Dans la console de Kibana :

- les 5 photos dont le vecteur est le plus proche de celui de la Cité ; « Copier » copie ses 512 nombres

```text
GET /photos/_search
{
  "knn": {
    "field": "vecteur",
    "query_vector": [
      -0.24887,
      -0.23371,
      -0.16023,
      -0.08413,
      0.35068,
      0.0744,
      0.25779,
      0.41635,
      -0.54527,
      0.20157,
      0.05907,
      -0.07996,
      0.11365,
      0.46802,
      -0.45504,
      0.15832,
      0.33828,
      0.27681,
      0.07864,
      -0.04606,
      0.48989,
      0.53413,
      0.30918,
      -0.6854,
      -0.52575,
      0.46897,
      0.41717,
      -0.25718,
      -0.20779,
      0.18743,
      0.29124,
      0.30009,
      0.45136,
      0.14774,
      0.38453,
      -0.10797,
      -0.37719,
      -0.23152,
      -0.13496,
      1.02091,
      0.19809,
      0.16584,
      -0.26081,
      0.11515,
      0.23652,
      -1.22356,
      0.2166,
      -0.25208,
      0.27898,
      -0.02553,
      0.62263,
      -0.28972,
      0.16615,
      0.76379,
      0.59213,
      -0.36104,
      -0.0382,
      -0.1914,
      -0.35169,
      0.52219,
      -0.17725,
      -0.34275,
      0.04537,
      -0.51452,
      0.25915,
      -0.007,
      -0.28808,
      -0.37583,
      -0.20265,
      -0.50843,
      -0.50321,
      0.22684,
      -0.29695,
      -0.39376,
      -0.57,
      0.17902,
      -0.54561,
      -0.50338,
      0.45498,
      -0.1559,
      0.08293,
      -0.14413,
      0.11631,
      0.41232,
      0.0472,
      0.4389,
      -0.64268,
      -0.26923,
      -0.62624,
      0.06933,
      0.07822,
      -0.00986,
      -5.42595,
      1.05089,
      0.2685,
      -0.2587,
      -0.02185,
      -0.06218,
      0.31652,
      -1.01376,
      -0.3234,
      -1.0282,
      -0.28407,
      0.23548,
      0.55267,
      0.06934,
      -1.18422,
      0.17675,
      -0.08897,
      -0.18323,
      -0.19041,
      -0.29735,
      -0.12829,
      -0.13843,
      -0.39912,
      0.40793,
      0.33052,
      0.07348,
      0.21244,
      0.23657,
      -0.01979,
      0.2376,
      0.44395,
      0.18595,
      -0.3516,
      -0.19028,
      -0.05272,
      0.24966,
      0.42299,
      -0.23673,
      0.26655,
      0.2866,
      0.30229,
      0.77035,
      -0.12137,
      0.39246,
      0.4657,
      -0.17043,
      -0.03436,
      0.24333,
      0.28867,
      0.44351,
      0.58337,
      -0.11012,
      0.61764,
      0.55207,
      -0.06215,
      -0.06175,
      -0.03161,
      0.58407,
      -0.07855,
      -0.1085,
      0.27063,
      -0.12455,
      -0.09796,
      0.44202,
      -0.50526,
      -0.15219,
      -0.16948,
      -0.21452,
      -0.16254,
      -0.17977,
      -0.15555,
      -0.12203,
      0.35604,
      -0.29845,
      1.14383,
      -0.34428,
      0.23783,
      0.45241,
      0.00244,
      -0.79941,
      -0.4924,
      -0.03554,
      -0.18884,
      -0.57533,
      -0.15988,
      -0.22413,
      0.37811,
      0.03903,
      -0.94119,
      -0.51166,
      0.1673,
      0.04495,
      -0.69969,
      -0.17844,
      0.01674,
      -0.24737,
      0.22253,
      -0.028,
      0.40415,
      -0.09724,
      0.40483,
      -0.55519,
      0.24132,
      -0.16811,
      0.42008,
      -0.08395,
      0.62399,
      -0.50393,
      -0.13234,
      0.43418,
      0.38335,
      0.15235,
      -0.15357,
      0.09354,
      0.1972,
      -0.12599,
      0.29549,
      -0.52459,
      0.28034,
      -0.03217,
      0.21513,
      0.12392,
      0.13079,
      0.37862,
      -0.06819,
      -0.28666,
      0.66564,
      -0.57539,
      0.01946,
      0.74621,
      -0.15819,
      0.1502,
      -0.17831,
      0.25312,
      0.13207,
      -0.11479,
      -0.20071,
      0.01606,
      0.03287,
      -0.13533,
      -0.51153,
      -0.14499,
      0.17246,
      0.08824,
      -9e-05,
      -0.2377,
      -0.13433,
      -0.0338,
      0.16576,
      -0.29152,
      -0.02533,
      0.03577,
      0.16361,
      -0.00132,
      0.04224,
      0.17098,
      -0.10663,
      -0.06634,
      -0.27981,
      0.48062,
      0.28648,
      -0.18884,
      0.40006,
      0.19298,
      -0.22875,
      -0.3246,
      1.13102,
      -0.2969,
      -0.34443,
      -0.32249,
      0.91016,
      1.02491,
      -0.04217,
      0.13958,
      0.03826,
      -0.46384,
      -0.17663,
      0.32027,
      -0.28896,
      0.00491,
      0.28739,
      -0.58856,
      -0.28064,
      0.01784,
      0.09382,
      -0.5902,
      0.03089,
      0.18887,
      0.16391,
      0.13997,
      0.24351,
      0.16587,
      -0.03986,
      -0.06407,
      -0.04405,
      0.03814,
      0.23311,
      -0.48936,
      0.31933,
      -0.29339,
      -0.04771,
      -0.34531,
      0.10634,
      -0.66877,
      -0.07188,
      -0.2912,
      -0.14988,
      0.41972,
      -0.09325,
      0.69077,
      -0.26119,
      -0.29727,
      -0.3416,
      -0.40701,
      -0.31189,
      0.2874,
      0.14291,
      0.6884,
      -0.00611,
      -0.2149,
      0.76797,
      -0.14958,
      0.33197,
      -0.05672,
      0.25274,
      -0.41643,
      -0.00732,
      -0.32507,
      0.06884,
      1.31973,
      0.18534,
      -0.41007,
      -0.03622,
      -0.1865,
      -0.38603,
      0.20911,
      0.02184,
      -0.08935,
      -0.54988,
      -0.55079,
      -0.04633,
      0.04713,
      0.0007,
      0.19506,
      0.21342,
      0.15731,
      -0.06358,
      -0.22152,
      0.32759,
      0.44994,
      0.1703,
      -0.00125,
      -0.30813,
      -0.28724,
      -0.24346,
      -0.39091,
      -0.4965,
      0.02234,
      0.28888,
      -0.19012,
      0.26058,
      -0.05262,
      0.2549,
      0.2689,
      -0.39345,
      -1.42054,
      -0.40773,
      0.09025,
      0.18243,
      0.05381,
      0.46254,
      -0.65235,
      -1.2562,
      -0.38323,
      0.43868,
      -0.69085,
      0.21108,
      0.04112,
      0.06217,
      0.21206,
      -0.71135,
      0.39718,
      -0.19686,
      0.663,
      0.30282,
      -0.38628,
      0.56922,
      -0.16173,
      0.15878,
      -0.35152,
      -0.72917,
      0.03795,
      -0.21351,
      0.03138,
      -0.07298,
      0.09097,
      0.10856,
      1.34739,
      -0.061,
      -0.07156,
      0.07003,
      -0.01618,
      -0.15051,
      0.1693,
      0.30665,
      -0.28319,
      0.36739,
      -0.132,
      -0.33733,
      -0.11957,
      -0.12231,
      -0.24677,
      0.38193,
      0.23332,
      0.11408,
      0.15696,
      -0.114,
      -0.60293,
      -0.4587,
      -0.17955,
      0.10595,
      0.46564,
      -0.08496,
      0.13895,
      -0.3096,
      -0.12006,
      -0.09067,
      -0.0468,
      -0.35589,
      -0.09425,
      0.18794,
      -0.53562,
      0.10694,
      0.3137,
      -0.03264,
      -0.64402,
      0.26891,
      0.53138,
      -0.35419,
      -0.20412,
      0.45362,
      -0.0809,
      0.16369,
      0.01748,
      0.11108,
      -0.19931,
      -0.23582,
      0.49781,
      0.1724,
      0.56267,
      0.35633,
      -0.66907,
      0.13283,
      0.31078,
      -0.2734,
      0.04022,
      -0.21298,
      0.24739,
      -0.54041,
      -0.0329,
      0.058,
      0.79158,
      -0.30455,
      0.4919,
      0.04117,
      -0.31792,
      0.16385,
      -0.20868,
      -0.57674,
      0.27979,
      -0.25241,
      -0.18897,
      0.01172,
      -0.12643,
      0.31835,
      -0.05425,
      -0.50015,
      0.00796,
      0.4206,
      -0.01762,
      0.37007,
      0.04559,
      0.02839,
      -0.06234,
      -0.1127,
      -0.33135,
      0.14006,
      -0.18609,
      -0.06363,
      -0.5406,
      -0.30903,
      0.22423,
      -0.1831,
      -0.19622,
      0.26305,
      0.28506,
      -0.13575,
      0.07076,
      -0.70821,
      -0.03743,
      -0.63547,
      -0.46477,
      0.16166,
      -0.17946,
      0.38002,
      -0.31013,
      0.02347,
      0.07691,
      0.31497,
      -0.02141,
      -0.09756,
      -0.13992,
      -0.17816,
      -0.07485,
      -0.30426,
      0.19709,
      -0.39587,
      0.12301,
      -0.2421,
      0.11836
    ],
    "k": 5,
    "num_candidates": 100
  },
  "_source": ["nom", "image"]
}
```

## Diapositive 71

**Le fichier fourni : une phrase changée en vecteur**

~/projets/formation-elasticsearch/patrimoine/photos/texte_en_vecteur.py : à coller dans nano, diapositive suivante

```python
"""Le vecteur d'une phrase, dans le même espace que les photos : CLIP multilingue (le texte en français).

    python texte_en_vecteur.py "un château fort au bord de la mer"
"""
import json
import sys

from sentence_transformers import SentenceTransformer

modele = SentenceTransformer("sentence-transformers/clip-ViT-B-32-multilingual-v1")
print(json.dumps([round(x, 5) for x in modele.encode(sys.argv[1]).tolist()]))
```

## Diapositive 72

**Créer le script, puis changer la phrase en vecteur**

Dans le terminal :

- créer texte_en_vecteur.py : y coller son code, Ctrl+O, Entrée, Ctrl+X
- aller dans le dossier des photos
- la phrase devient 512 nombres ; l'écran n'en montre que le début (cut)

```bash
nano ~/projets/formation-elasticsearch/patrimoine/photos/texte_en_vecteur.py && \
cd ~/projets/formation-elasticsearch/patrimoine/photos && \
~/elastic/venv-photos/bin/python texte_en_vecteur.py "un château fort au bord de la mer" | cut -c1-80
```

## Diapositive 73

**La recherche : « un château fort au bord de la mer »**

Dans la console de Kibana :

- les 5 photos les plus proches de la phrase ; « Copier » copie ses 512 nombres

```text
GET /photos/_search
{
  "knn": {
    "field": "vecteur",
    "query_vector": [
      -0.13559,
      -0.16279,
      0.00641,
      0.01289,
      0.09399,
      -0.15378,
      -0.08288,
      -0.78928,
      -0.17836,
      0.31843,
      0.13661,
      -0.2384,
      0.21898,
      -0.18511,
      0.27304,
      -0.09374,
      0.0731,
      0.055,
      0.08939,
      0.19339,
      0.16485,
      0.17385,
      0.35687,
      -0.09481,
      0.00626,
      0.43032,
      0.1713,
      0.08578,
      -0.17312,
      0.35044,
      -0.00194,
      0.09906,
      0.31821,
      0.30741,
      -0.20294,
      0.01765,
      -0.1119,
      -0.0732,
      -0.15836,
      0.25024,
      0.20168,
      0.17574,
      0.09465,
      0.10912,
      0.10125,
      -0.0725,
      0.51989,
      -0.29539,
      -0.01477,
      -0.19233,
      0.04905,
      0.09213,
      -0.08,
      0.05408,
      -0.10053,
      -0.0173,
      -0.29846,
      -0.0394,
      0.02376,
      0.05651,
      -0.12401,
      -0.28987,
      -0.09199,
      -0.12507,
      0.06362,
      0.00654,
      -0.11533,
      0.25608,
      0.05352,
      -0.18905,
      -0.28927,
      -0.20055,
      -0.1326,
      -0.22976,
      -0.22295,
      -0.21781,
      0.22559,
      -0.23253,
      -0.04477,
      -0.23534,
      -0.08549,
      -0.0007,
      0.03871,
      0.13687,
      -0.10783,
      -0.09831,
      -0.43329,
      -0.00625,
      -0.55011,
      0.21939,
      0.053,
      -0.09996,
      -1.16275,
      0.22237,
      -0.11828,
      0.10388,
      0.05907,
      0.18141,
      0.27365,
      -0.39745,
      -0.02743,
      -0.19739,
      0.10766,
      0.12624,
      0.05492,
      0.13953,
      -0.0476,
      -0.05836,
      0.00327,
      -0.12836,
      0.08853,
      -0.16851,
      0.0464,
      0.05153,
      0.03278,
      -0.14299,
      -0.14527,
      0.21817,
      -0.19615,
      0.12031,
      0.16014,
      -0.69826,
      0.35265,
      -0.58638,
      0.14384,
      -0.02456,
      -0.23815,
      -0.18512,
      0.11429,
      0.04556,
      -0.00502,
      0.08693,
      -0.10205,
      5.22771,
      -0.12449,
      -0.12637,
      0.04276,
      0.10518,
      -0.32611,
      -0.2081,
      0.03477,
      -0.39251,
      0.12025,
      0.08358,
      -0.00398,
      0.04617,
      0.09083,
      0.07594,
      0.15623,
      -0.22261,
      -0.06003,
      0.06062,
      -0.42814,
      0.07906,
      -0.15234,
      -0.31884,
      -0.04014,
      -0.11991,
      0.00856,
      0.0674,
      0.00196,
      0.10017,
      0.03232,
      -0.03631,
      -0.03826,
      -0.18075,
      0.38146,
      -0.0176,
      -0.47334,
      0.15685,
      0.30738,
      -0.03004,
      0.20482,
      0.14806,
      0.03631,
      0.19572,
      -0.44933,
      -0.04247,
      -0.42695,
      -0.06817,
      -0.0132,
      0.09234,
      0.06432,
      -0.02549,
      -0.24959,
      0.1811,
      0.3422,
      -0.01337,
      0.17234,
      0.11421,
      -0.10552,
      0.04548,
      0.02697,
      0.00174,
      0.10979,
      0.00268,
      -0.16841,
      -0.13312,
      0.16933,
      0.18422,
      -0.27071,
      0.00568,
      -0.14945,
      -0.21047,
      -0.02444,
      -0.10219,
      0.19728,
      -0.11701,
      -0.11533,
      -0.02343,
      0.46533,
      0.10584,
      -0.04745,
      0.25706,
      0.38198,
      0.0201,
      -0.25015,
      0.19461,
      0.02173,
      0.18701,
      -0.04563,
      0.01927,
      0.03516,
      -0.11315,
      -0.03187,
      0.14242,
      0.09417,
      -0.21031,
      -0.04325,
      0.02315,
      0.04046,
      0.09994,
      -0.29365,
      -0.02347,
      0.0265,
      -0.03095,
      -0.09313,
      -0.11727,
      -0.36084,
      0.04307,
      0.14265,
      -0.0234,
      0.07798,
      0.12009,
      0.10366,
      0.16675,
      -0.18824,
      -0.08521,
      -0.2437,
      -0.44556,
      -0.1348,
      -0.42178,
      0.38961,
      0.05763,
      0.08434,
      -0.00421,
      0.01163,
      -0.32762,
      0.15409,
      0.27977,
      0.43879,
      -0.22213,
      0.12686,
      0.20407,
      -0.05021,
      -0.06666,
      0.29923,
      -0.12301,
      -0.21111,
      -0.07793,
      0.23621,
      0.01962,
      0.21934,
      -0.12963,
      -0.28485,
      0.01821,
      -0.12183,
      0.05958,
      0.01405,
      -0.07996,
      0.12518,
      -0.23702,
      0.24285,
      0.1821,
      -0.1386,
      0.32751,
      0.05568,
      0.09158,
      0.05936,
      -0.2636,
      -0.03553,
      -0.21073,
      -0.14231,
      0.16595,
      -0.48671,
      -0.16735,
      0.01035,
      -0.07776,
      -0.07523,
      0.01695,
      0.01457,
      -0.4084,
      0.24732,
      0.14753,
      -0.13249,
      -0.17198,
      -0.00221,
      0.23289,
      0.09641,
      -0.10835,
      -0.10599,
      -0.29498,
      5.21907,
      0.08278,
      0.03273,
      -0.16004,
      -0.1256,
      -0.27646,
      -0.08401,
      -0.18773,
      0.44735,
      0.38247,
      0.37593,
      -0.19059,
      -0.06714,
      0.30186,
      0.16798,
      0.07374,
      -0.07767,
      -1.66445,
      -0.10444,
      -0.2817,
      0.09757,
      -0.19305,
      -0.10336,
      -0.04461,
      0.0399,
      0.09791,
      0.1639,
      0.20813,
      0.02983,
      -0.17333,
      0.17124,
      -0.06334,
      0.38559,
      -0.25667,
      -0.05581,
      -0.08096,
      -0.03279,
      -0.0622,
      0.07947,
      0.05282,
      0.12331,
      0.00686,
      -0.40236,
      -0.12166,
      -0.48008,
      -0.09373,
      0.15174,
      0.21609,
      -0.11663,
      -0.1757,
      0.14175,
      0.30608,
      -0.23378,
      -0.02359,
      0.12634,
      -0.30349,
      -0.07671,
      -0.30163,
      -0.12252,
      -0.04495,
      -0.06778,
      0.15056,
      -0.07578,
      0.50428,
      -0.2522,
      -0.22686,
      0.13818,
      0.20096,
      -0.07252,
      -0.1898,
      -0.15053,
      0.4218,
      0.40576,
      -0.10659,
      0.03697,
      0.09421,
      0.02226,
      0.11896,
      -0.31213,
      0.32698,
      0.06483,
      0.11731,
      -0.17701,
      -0.11481,
      -0.04547,
      0.24864,
      -0.27262,
      0.70271,
      -0.05088,
      0.08231,
      -0.15409,
      -0.11268,
      -0.24679,
      -0.04657,
      -0.01366,
      -0.02811,
      -0.03043,
      -0.07442,
      0.35973,
      -0.20747,
      -0.14976,
      0.29883,
      0.38346,
      0.13463,
      -0.23403,
      0.47571,
      0.12962,
      0.25344,
      0.15539,
      -0.06109,
      -0.08942,
      -0.62992,
      0.19144,
      -0.07141,
      -0.34424,
      -0.03828,
      0.11737,
      -0.02222,
      -0.03985,
      -0.37341,
      0.03963,
      0.32108,
      -0.26254,
      0.21076,
      0.22812,
      -0.01459,
      -0.02839,
      -0.15497,
      -0.05434,
      -0.1496,
      -0.24877,
      0.00242,
      0.1644,
      0.16348,
      -0.05101,
      0.00228,
      -0.19278,
      0.08475,
      -0.28442,
      0.04089,
      0.09242,
      0.01823,
      0.25681,
      -0.20405,
      -0.23166,
      0.18606,
      -0.09703,
      0.09073,
      -0.20421,
      -0.08344,
      0.20531,
      0.12925,
      0.24002,
      -0.02369,
      0.08803,
      -0.1419,
      -0.24169,
      0.22945,
      -0.07343,
      -0.124,
      -0.16355,
      -0.07094,
      -0.13223,
      -0.06145,
      -0.39888,
      -0.01924,
      -0.26092,
      -0.15192,
      -0.18895,
      -0.34279,
      0.26079,
      0.32119,
      -0.00366,
      -0.06169,
      0.15629,
      -0.21961,
      0.12375,
      -0.02642,
      0.07814,
      -0.09285,
      -0.18644,
      0.57517,
      0.05691,
      -0.22456,
      0.14827,
      -0.15732,
      -0.23832,
      0.10109,
      -0.02343,
      -0.02957,
      -0.16267,
      0.33113,
      -0.04934,
      0.08573,
      0.11366,
      0.30973,
      -0.03788,
      0.02976,
      -0.32514,
      -0.02887
    ],
    "k": 5,
    "num_candidates": 100
  },
  "_source": ["nom", "image"]
}
```

## Diapositive 75

**La recherche : « un phare »**

Dans la console de Kibana :

- les 5 photos les plus proches de « un phare » ; « Copier » copie ses 512 nombres

```text
GET /photos/_search
{
  "knn": {
    "field": "vecteur",
    "query_vector": [
      -0.21793,
      0.05874,
      0.07235,
      0.04716,
      0.02158,
      -0.2856,
      -0.31207,
      -1.04633,
      -0.23588,
      0.59453,
      -0.03107,
      -0.19729,
      0.27089,
      -0.19051,
      0.3339,
      0.02135,
      0.0482,
      -0.14028,
      -0.07168,
      -0.1171,
      0.39468,
      0.10946,
      0.12291,
      0.18312,
      -0.1081,
      0.37817,
      0.04361,
      -0.11071,
      -0.02125,
      0.10262,
      0.04603,
      0.20692,
      0.04623,
      0.07987,
      -0.1642,
      0.06789,
      0.03859,
      0.2359,
      -0.11321,
      0.08107,
      0.03031,
      -0.4051,
      0.02023,
      0.28838,
      -0.05034,
      0.03618,
      0.05636,
      0.1042,
      -0.19015,
      0.02842,
      -0.05196,
      -0.05023,
      -0.02797,
      -0.17269,
      -0.20719,
      0.06453,
      -0.20842,
      -0.14974,
      -0.07655,
      -0.16412,
      -0.00099,
      -0.12236,
      -0.01415,
      -0.13924,
      0.09582,
      -0.18293,
      -0.22353,
      -0.00766,
      0.12711,
      -0.12946,
      0.15832,
      -0.12384,
      -0.11715,
      0.12567,
      0.12369,
      -0.06104,
      0.15195,
      -0.16784,
      0.08785,
      0.02827,
      -0.02188,
      -0.03867,
      -0.0154,
      0.27553,
      -0.11979,
      0.17885,
      -0.02376,
      0.02876,
      0.02453,
      -0.0406,
      0.06381,
      -0.08222,
      -1.49852,
      0.07392,
      -0.27631,
      0.14282,
      -0.05385,
      0.1351,
      -0.01115,
      -0.34496,
      0.26607,
      -0.04156,
      0.08525,
      -0.13427,
      -0.11567,
      -0.24193,
      0.03433,
      0.02392,
      0.0416,
      0.10103,
      -0.11751,
      0.04955,
      -0.03841,
      -0.14693,
      -0.26766,
      -0.08398,
      -0.41686,
      0.09409,
      0.02885,
      0.19589,
      0.00294,
      -0.38525,
      0.19689,
      -0.10689,
      0.22303,
      0.17047,
      0.06775,
      0.0703,
      -0.19658,
      0.15854,
      -0.12567,
      0.2305,
      -0.09069,
      5.69734,
      0.00677,
      -0.14389,
      -0.23539,
      -0.36565,
      0.11228,
      -0.02406,
      -0.04933,
      -0.24651,
      -0.16021,
      -0.0109,
      -0.24201,
      0.01751,
      0.08777,
      -0.01492,
      0.16587,
      -0.10642,
      -0.17446,
      -0.20924,
      -0.08074,
      -0.10839,
      0.08019,
      -0.10473,
      -0.03148,
      0.0525,
      -0.01847,
      -0.10892,
      0.02096,
      0.05349,
      0.05886,
      0.10723,
      0.05175,
      -0.0784,
      0.09559,
      0.01963,
      0.10778,
      0.08133,
      0.20486,
      -0.15044,
      0.06378,
      -0.03971,
      -0.11369,
      -0.00453,
      -0.37342,
      -0.06479,
      -0.03046,
      0.06228,
      0.18509,
      0.09104,
      0.03478,
      0.00044,
      -0.01846,
      -0.08579,
      0.08033,
      0.09008,
      -0.02944,
      -0.06171,
      0.16723,
      0.0803,
      -0.18985,
      -0.17094,
      0.07714,
      0.06373,
      -0.15114,
      0.09418,
      -0.00595,
      -0.09904,
      -0.21005,
      -0.10982,
      0.18547,
      0.05655,
      0.04743,
      0.07895,
      0.02523,
      -0.08576,
      -0.07228,
      -0.08571,
      0.12263,
      0.09523,
      -0.00493,
      0.0547,
      0.04145,
      0.08241,
      -0.01822,
      -0.20419,
      -0.18668,
      -0.043,
      0.06879,
      -0.09903,
      -0.07235,
      0.00312,
      0.25066,
      0.12522,
      -0.01107,
      0.14601,
      0.0224,
      -0.18085,
      -0.00153,
      0.08288,
      0.11842,
      -0.13917,
      -0.01363,
      0.45278,
      0.08404,
      -0.02447,
      -0.06247,
      -0.24198,
      0.02014,
      0.09033,
      -0.16049,
      0.03909,
      -0.18883,
      0.14387,
      -0.11225,
      -0.02936,
      0.16545,
      -0.16204,
      -0.09444,
      -0.13575,
      0.07617,
      0.08405,
      0.04901,
      0.08042,
      0.00525,
      -0.23684,
      0.09399,
      0.27043,
      0.02907,
      -0.11405,
      0.01659,
      0.01895,
      -0.0067,
      0.01113,
      0.25613,
      0.19224,
      -0.28443,
      -0.05036,
      0.06114,
      0.13656,
      0.30199,
      -0.13646,
      0.012,
      -0.00387,
      -0.26784,
      -0.055,
      -0.01741,
      -0.01476,
      0.14873,
      -0.06821,
      -0.13608,
      0.0962,
      -0.04953,
      -0.02828,
      0.08552,
      0.0947,
      0.11755,
      -0.24855,
      0.08368,
      -0.08761,
      -0.03708,
      0.232,
      -0.28289,
      0.01526,
      -0.28775,
      -0.0806,
      -0.10697,
      -0.06458,
      0.17733,
      -0.07199,
      0.09731,
      0.22143,
      -0.07391,
      -0.04755,
      -0.08723,
      -0.04648,
      0.10649,
      -0.2495,
      -0.0414,
      -0.01211,
      5.68911,
      -0.04546,
      0.03307,
      0.18909,
      0.05658,
      -0.01495,
      0.25387,
      0.08962,
      0.24505,
      0.28276,
      0.41505,
      0.07098,
      -0.13587,
      0.27459,
      -0.01837,
      0.20033,
      0.07696,
      -2.25405,
      -0.11874,
      0.02786,
      -0.00344,
      0.01863,
      0.13864,
      -0.39109,
      0.04572,
      0.00895,
      -0.22347,
      0.00976,
      -0.1195,
      -0.14636,
      0.08522,
      0.08743,
      0.23041,
      -0.08759,
      0.21041,
      -0.00728,
      -0.19501,
      0.02835,
      -0.02127,
      -0.03869,
      0.17826,
      0.02195,
      -0.10651,
      -0.03299,
      -0.15278,
      -0.0489,
      0.08075,
      0.13473,
      -0.05566,
      -0.22178,
      0.04634,
      0.2165,
      -0.03442,
      -0.21878,
      -0.08022,
      0.04241,
      -0.06585,
      -0.09305,
      -0.13383,
      -0.03909,
      -0.02951,
      0.07813,
      -0.05433,
      -0.11583,
      -0.23941,
      0.14986,
      -0.08292,
      0.05878,
      -0.24075,
      -0.04817,
      0.20242,
      0.1231,
      0.16055,
      -0.11547,
      0.00576,
      -0.02923,
      0.08304,
      0.02145,
      -0.28722,
      0.27279,
      0.00651,
      0.20884,
      -0.16703,
      0.03178,
      0.12537,
      -0.18627,
      -0.13088,
      0.573,
      -0.04207,
      0.0229,
      0.02047,
      0.12443,
      -0.11129,
      -0.17813,
      0.00958,
      -0.11438,
      0.13059,
      -0.16207,
      0.08014,
      -0.12633,
      -0.08977,
      0.29152,
      -0.17047,
      0.20312,
      -0.08135,
      0.19007,
      -0.05317,
      0.01378,
      0.03296,
      -0.06341,
      -0.10625,
      -0.40129,
      0.07224,
      0.01686,
      -0.26005,
      -0.14737,
      0.16167,
      0.19261,
      0.05051,
      -0.14872,
      -0.18071,
      0.21798,
      0.07168,
      -0.03522,
      -0.01547,
      0.07159,
      -0.18868,
      -0.31902,
      -0.01091,
      -0.26201,
      -0.16078,
      0.01355,
      0.07612,
      0.3095,
      0.03805,
      -0.48391,
      0.03152,
      0.17604,
      0.24482,
      0.18856,
      0.03139,
      0.03112,
      0.04432,
      0.11137,
      -0.04175,
      0.11234,
      0.10663,
      -0.14735,
      0.04341,
      -0.04931,
      0.20049,
      0.09104,
      0.13689,
      0.03282,
      0.29251,
      -0.17667,
      -0.24126,
      0.11667,
      0.02272,
      -0.14754,
      0.04933,
      -0.09414,
      -0.12306,
      -0.03853,
      -0.04319,
      0.34116,
      -0.22838,
      0.14069,
      -0.07137,
      -0.55597,
      0.10678,
      -0.04551,
      -0.06763,
      -0.14099,
      0.20665,
      0.1053,
      0.1744,
      -0.24805,
      -0.06224,
      0.29657,
      -0.04574,
      0.63489,
      0.19465,
      -0.03786,
      0.12495,
      0.06851,
      -0.1955,
      0.16214,
      -0.07239,
      -0.05672,
      -0.12604,
      0.15011,
      0.23457,
      -0.19119,
      0.0208,
      0.2135,
      -0.10508,
      -0.27191,
      -0.13957,
      -0.11005
    ],
    "k": 5,
    "num_candidates": 100
  },
  "_source": ["nom", "image"]
}
```

## Diapositive 83

**La bascule vers monuments-v3**

Dans la console de Kibana :

- combien de monuments dans monuments-v3 ?
- basculer l'alias de monuments-v2 à monuments-v3
- la taille de chaque version

```text
GET /_cat/count/monuments-v3?v

POST /_aliases
{
  "actions": [
    {
      "remove": {"index": "monuments-v2", "alias": "monuments"}
    },
    {"add": {"index": "monuments-v3", "alias": "monuments"}}
  ]
}

GET /_cat/indices/monuments-v*?v&h=index,docs.count,store.size&s=index
```

## Diapositive 84

**« Une abbaye isolée au milieu des bois », par les mots**

Dans la console de Kibana :

- la question, cherchée par les mots

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "match": {"historique": "une abbaye isolée au milieu des bois"}
  }
}
```

## Diapositive 85

**La même question, par le sens**

Dans la console de Kibana :

- la même question, cherchée par le sens (le champ sémantique)

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "semantic": {
      "field": "historique_sens",
      "query": "une abbaye isolée au milieu des bois"
    }
  }
}
```

## Diapositive 86

**Hybride : rrf**

Dans la console de Kibana :

- les deux recherches, mots et sens, fusionnées par leurs rangs (rrf)

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {"query": {"multi_match": {"query": "abbaye isolée dans la forêt", "fields": ["titre^3", "historique"]}}}
        },
        {"standard": {"query": {"semantic": {"field": "historique_sens", "query": "abbaye isolée dans la forêt"}}}}
      ],
      "rank_window_size": 50
    }
  }
}
```

## Diapositive 87

**Hybride : linear, le sens pèse deux fois plus**

Dans la console de Kibana :

- mots et sens, fusionnés par leurs scores

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "retriever": {
    "linear": {
      "retrievers": [
        {
          "retriever": {
            "standard": {"query": {"multi_match": {"query": "abbaye isolée dans la forêt", "fields": ["titre^3", "historique"]}}}
          },
          "weight": 1,
          "normalizer": "minmax"
        },
        {
          "retriever": {"standard": {"query": {"semantic": {"field": "historique_sens", "query": "abbaye isolée dans la forêt"}}}},
          "weight": 2,
          "normalizer": "minmax"
        }
      ]
    }
  }
}
```

## Diapositive 88

**Le sens et un filtre : un phare battu par les vagues, en Bretagne**

Dans la console de Kibana :

- le sens, plus un filtre exact : la région Bretagne

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune", "region"],
  "query": {
    "bool": {
      "must": {
        "semantic": {
          "field": "historique_sens",
          "query": "un phare battu par les vagues"
        }
      },
      "filter": {"term": {"region": "Bretagne"}}
    }
  }
}
```

## Diapositive 89

**La recherche par le sens est approchée ; les mots, eux, sont sûrs**

Dans la console de Kibana :

- les phares, par le mot du titre
- combien de phares sans historique, puis combien en tout

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre", "commune"],
  "query": {
    "bool": {
      "must": {"match": {"titre": "phare"}},
      "filter": {"term": {"region": "Bretagne"}}
    }
  }
}

GET /monuments/_count
{
  "query": {
    "bool": {
      "must": {"match": {"titre": "phare"}},
      "must_not": {"exists": {"field": "historique"}}
    }
  }
}

GET /monuments/_count
{"query": {"match": {"titre": "phare"}}}
```

## Diapositive 90

**Plus de voisins examinés : la même question en knn**

Dans la console de Kibana :

- la même question en knn, 50 voisins examinés (num_candidates)

```text
GET /monuments/_search
{
  "size": 5,
  "_source": ["titre"],
  "query": {
    "knn": {
      "field": "historique_sens",
      "k": 5,
      "num_candidates": 50,
      "query_vector_builder": {
        "text_embedding": {"model_text": "un phare battu par les vagues"}
      },
      "filter": {"term": {"region": "Bretagne"}}
    }
  }
}
```

## Diapositive 91

**L'assistant de Patrimoine : le code**

~/projets/formation-elasticsearch/patrimoine/rag/rag.py : à coller dans nano, diapositive suivante

```python
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
```

## Diapositive 92

**Créer le fichier de l'assistant**

Dans le terminal : coller les deux lignes, puis Entrée :

- créer le dossier de l'assistant
- ouvrir rag.py : y coller son code, Ctrl+O, Entrée, Ctrl+X

```bash
mkdir -p ~/projets/formation-elasticsearch/patrimoine/rag && \
nano ~/projets/formation-elasticsearch/patrimoine/rag/rag.py
```

## Diapositive 93

**La réponse de Qwen 2.5 (3 milliards de paramètres)**

Dans le terminal :

- l'adresse, le certificat et le mot de passe d'Elasticsearch, pour l'assistant ; puis la question, au modèle Qwen 2.5

```bash
cd ~/projets/formation-elasticsearch/patrimoine
export ES_URL=https://localhost:9200 ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt ES_PASSWORD="$ELASTIC_PASSWORD"
~/elastic/venv/bin/python rag/rag.py --modele qwen2.5:3b 'Quelles abbayes cisterciennes de Bourgogne sont protégées, et pourquoi sont-elles remarquables ?'
```

## Diapositive 94

**La réponse de Llama 3.2 (3 milliards de paramètres)**

Dans le terminal :

- aller dans le dossier du fil rouge
- la même question, avec le modèle Llama 3.2

```bash
cd ~/projets/formation-elasticsearch/patrimoine
~/elastic/venv/bin/python rag/rag.py --modele llama3.2:3b 'Quelles abbayes cisterciennes de Bourgogne sont protégées, et pourquoi sont-elles remarquables ?'
```

## Diapositive 95

**La correction : un filtre de région dans la recherche**

Dans le terminal :

- aller dans le dossier du fil rouge
- la même question, la recherche limitée à la Bourgogne-Franche-Comté

```bash
cd ~/projets/formation-elasticsearch/patrimoine
~/elastic/venv/bin/python rag/rag.py --modele qwen2.5:3b --region Bourgogne-Franche-Comté 'Quelles abbayes cisterciennes de Bourgogne sont protégées, et pourquoi sont-elles remarquables ?'
```

## Diapositive 96

**Une question hors sujet : l'assistant le dit**

Dans le terminal :

- aller dans le dossier du fil rouge
- une question à laquelle les monuments ne répondent pas

```bash
cd ~/projets/formation-elasticsearch/patrimoine
~/elastic/venv/bin/python rag/rag.py --modele qwen2.5:3b 'Quel est le prix du billet d’entrée au Mont-Saint-Michel ?'
```

## Diapositive 105

**Créer la clé d'API de Patrimoine**

Dans la console de Kibana :

- créer une clé d'API qui ne peut que lire l'index monuments, valable 30 jours

```text
POST /_security/api_key
{
  "name": "patrimoine-api",
  "expiration": "30d",
  "role_descriptors": {
    "patrimoine-api": {
      "indices": [
        {"names": ["monuments"], "privileges": ["read"]},
        {"names": ["recherches"], "privileges": ["create_doc", "create_index"]}
      ]
    }
  }
}
```

## Diapositive 106

**La clé à l'essai : ce qu'elle peut, ce qu'elle ne peut pas**

Dans le terminal :

- lire avec la clé : compter les monuments
- écrire avec la clé : refusé

```bash
export ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt

curl -s --cacert $ES_CA -H "Authorization: ApiKey $CLE" 'https://localhost:9200/monuments/_count' | jq -c .

curl -s --cacert $ES_CA -H "Authorization: ApiKey $CLE" -H 'Content-Type: application/json' -X PUT 'https://localhost:9200/monuments/_doc/essai' -d '{"titre":"essai"}' | jq -c .error.type,.status

curl -s --cacert $ES_CA -H "Authorization: ApiKey $CLE" 'https://localhost:9200/livres/_search' | jq -c .error.type,.status
```

## Diapositive 108

**Le client Python, en trois appels**

~/projets/formation-elasticsearch/patrimoine/recherche/essai_client.py : à coller dans nano (« Créer les trois fichiers »)

```python
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
```

## Diapositive 109

**La petite API de Patrimoine**

~/projets/formation-elasticsearch/patrimoine/recherche/api.py : à coller dans nano (« Créer les trois fichiers »)

```python
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
```

## Diapositive 110

**La page de recherche : une page HTML, sans bibliothèque**

~/projets/formation-elasticsearch/patrimoine/recherche/index.html : à coller dans nano (« Créer les trois fichiers »)

```html
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Patrimoine</title>
<style>
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f6f4ef;color:#1f1d1a}
header{background:#7a2e0e;color:#fff;padding:22px 28px}
header h1{margin:0;font-size:26px}
header p{margin:4px 0 0;opacity:.85}
form{display:flex;gap:10px;padding:18px 28px;background:#fff;border-bottom:1px solid #e3ddd2}
input{flex:1;font-size:17px;padding:10px 14px;border:1px solid #cfc6b6;border-radius:8px}
button{font-size:16px;padding:10px 18px;border:0;border-radius:8px;background:#7a2e0e;color:#fff;cursor:pointer}
main{display:grid;grid-template-columns:240px 1fr;gap:24px;padding:20px 28px}
aside h2{font-size:14px;text-transform:uppercase;letter-spacing:.05em;color:#7a2e0e}
aside a{display:flex;justify-content:space-between;padding:4px 0;color:inherit;text-decoration:none}
aside a.choisie{font-weight:700;color:#7a2e0e}
article{background:#fff;border:1px solid #e3ddd2;border-radius:10px;padding:14px 18px;margin-bottom:12px}
article h3{margin:0 0 4px;font-size:18px}
article small{color:#6b6458}
article p{margin:8px 0 0;line-height:1.45}
mark{background:#ffe08a}
#etat{color:#6b6458}
</style>
</head>
<body>
<header><h1>Patrimoine</h1><p>Les monuments historiques de France (base Mérimée, ministère de la Culture)</p></header>
<form id="recherche"><input id="q" placeholder="abbaye cistercienne, château fort, pont romain…" autofocus>
<button>Chercher</button></form>
<main><aside id="facettes"></aside><section><p id="etat"></p><div id="resultats"></div></section></main>
<script>
const API = "http://localhost:8000/recherche";
let region = null;

function texte(t) {                                    // un texte sûr à placer dans la page
  const d = document.createElement("div"); d.textContent = t ?? ""; return d.innerHTML;
}

async function chercher() {
  const q = document.getElementById("q").value.trim();
  if (!q) return;
  const adresse = API + "?q=" + encodeURIComponent(q) + (region ? "&region=" + encodeURIComponent(region) : "");
  try {
    const donnees = await (await fetch(adresse)).json();
    document.getElementById("etat").textContent = donnees.total + " monuments" + (region ? " · " + region : "");
    document.getElementById("resultats").innerHTML = donnees.resultats.map(m =>
      `<article><h3>${texte(m.titre)}</h3><small>${texte(m.commune)} · ${texte(m.region)} · ${texte((m.siecle || []).join(", "))}</small>` +
      (m.extrait ? `<p>${m.extrait}</p>` : "") + `</article>`).join("");      // extrait déjà échappé par l'API
    document.getElementById("facettes").innerHTML = "<h2>Régions</h2>" + donnees.facettes.regions.map(f =>
      `<a href="#" data-region="${texte(f.valeur)}" class="${f.valeur === region ? "choisie" : ""}">` +
      `<span>${texte(f.valeur)}</span><span>${f.nombre}</span></a>`).join("");
  } catch (erreur) {
    document.getElementById("etat").textContent = "La recherche n'a pas pu joindre l'API : " + erreur.message;
  }
}

document.getElementById("recherche").addEventListener("submit", e => { e.preventDefault(); region = null; chercher(); });
document.getElementById("facettes").addEventListener("click", e => {
  const lien = e.target.closest("a"); if (!lien) return;
  e.preventDefault(); region = lien.dataset.region === region ? null : lien.dataset.region; chercher();
});
</script>
</body>
</html>
```

## Diapositive 111

**Créer les trois fichiers de la page de recherche**

Dans le terminal : coller les quatre lignes, puis Entrée :

- créer le dossier de la page de recherche
- ouvrir essai_client.py : y coller son code, Ctrl+O, Entrée, Ctrl+X
- puis api.py, de la même façon
- puis index.html, de la même façon

```bash
mkdir -p ~/projets/formation-elasticsearch/patrimoine/recherche && \
nano ~/projets/formation-elasticsearch/patrimoine/recherche/essai_client.py && \
nano ~/projets/formation-elasticsearch/patrimoine/recherche/api.py && \
nano ~/projets/formation-elasticsearch/patrimoine/recherche/index.html
```

## Diapositive 112

**Lancer le client, puis l'API : le premier terminal**

Dans le terminal :

- dans le terminal de l'API, où CLE est défini : aller dans le dossier de la page
- le certificat et la clé d'API, dans l'environnement
- essayer le client Python : trois appels à Elasticsearch
- démarrer l'API sur le port 8000 ; elle reste allumée, et ce terminal avec elle

```bash
cd ~/projets/formation-elasticsearch/patrimoine/recherche
export ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt ES_API_KEY="$CLE"
~/elastic/venv/bin/python essai_client.py
~/elastic/venv/bin/uvicorn api:app --port 8000
```

## Diapositive 113

**Servir la page : le second terminal**

Dans le terminal :

- dans un autre nouveau terminal, celui de la page : aller dans son dossier
- servir la page sur le port 8080 ; on l'ouvre ensuite à http://localhost:8080

```bash
cd ~/projets/formation-elasticsearch/patrimoine/recherche
python3 -m http.server 8080
```

## Diapositive 115

**CORS vérifié : l'adresse autorisée, et une autre**

Dans le terminal :

- l'API appelée depuis l'adresse de la page : autorisée
- l'API appelée depuis une autre adresse : pas d'autorisation

```bash
curl -s -o /dev/null -D - -H 'Origin: http://localhost:8080' 'http://localhost:8000/recherche?q=pont' | grep -i -E '^(HTTP|access-control)'

curl -s -o /dev/null -D - -H 'Origin: http://exemple.com' 'http://localhost:8000/recherche?q=pont' | grep -i -E '^(HTTP|access-control)'
```

## Diapositive 118

**Une Search Application sans licence : refusée**

Dans la console de Kibana :

- créer une Search Application : refusé sans licence

```text
PUT /_application/search_application/patrimoine
{"indices": ["monuments-v2"]}
```

## Diapositive 119

**Démonstration : une Search Application**

Dans la console de Kibana :

- créer la Search Application : l'index et le modèle de requête
- chercher par elle, avec le seul paramètre q

```text
PUT /_application/search_application/patrimoine
{
  "indices": ["monuments-v2"],
  "template": {
    "script": {
      "source": {
        "query": {
          "multi_match": {
            "query": "{{q}}",
            "fields": ["titre^3", "historique"]
          }
        },
        "size": 3,
        "_source": ["titre", "commune"]
      },
      "params": {"q": "*"}
    }
  }
}

POST /_application/search_application/patrimoine/_search
{"params": {"q": "abbaye cistercienne"}}
```

## Diapositive 121

**Le journal des recherches lentes : le régler**

Dans la console de Kibana :

- noter dans le journal toute recherche de plus de 5 ms

```text
PUT /monuments/_settings
{
  "index.search.slowlog.threshold.query.info": "5ms",
  "index.search.slowlog.threshold.fetch.info": "5ms"
}
```

## Diapositive 122

**Le journal des recherches lentes : le lire**

Dans le terminal :

- les deux dernières lignes du journal des recherches lentes, résumées

```bash
tail -n 2 ~/elastic/elasticsearch-9.5.6/logs/patrimoine_index_search_slowlog.json | jq -c '{niveau: ."log.level", duree_ms: ((."elasticsearch.slowlog.took_millis" // 0)|tonumber), requete: (."elasticsearch.slowlog.source"|.[0:150])}'
```

## Diapositive 123

**La Profile API : où passe le temps**

Dans la console de Kibana :

- où passe le temps d'une recherche lente (un joker, *abbaye*)

```text
GET /monuments/_search
{
  "profile": true,
  "size": 0,
  "query": {
    "wildcard": {
      "titre.exact": {"value": "*abbaye*", "case_insensitive": true}
    }
  }
}
```

## Diapositive 124

**Les recherches sans résultat, et les plus fréquentes**

Dans la console de Kibana :

- les questions qui n'ont rien trouvé, les plus fréquentes
- les questions les plus fréquentes

```text
GET /recherches/_search
{
  "size": 0,
  "query": {"term": {"resultats": 0}},
  "aggs": {
    "questions": {"terms": {"field": "q.keyword", "size": 5}}
  }
}

GET /recherches/_search
{
  "size": 0,
  "aggs": {
    "questions": {"terms": {"field": "q.keyword", "size": 5}}
  }
}
```

## Diapositive 126

**Les documents fournis de la question 3 : l'église et ses objets**

Dans la console de Kibana : l'index, l'église et trois objets (le bouton copie tout) :

- l'index qui relie l'église et ses objets (join)
- l'église, le parent
- ses trois objets (cloche, autel, statue), chacun rangé avec l'église (routing)

```text
PUT /patrimoine-liens
{
  "mappings": {
    "properties": {
      "titre": {"type": "text"},
      "materiaux": {"type": "keyword"},
      "lien": {"type": "join", "relations": {"monument": "objet"}}
    }
  }
}

PUT /patrimoine-liens/_doc/PA00113932
{"titre": "Église de la Madeleine, Vézelay", "lien": "monument"}

PUT /patrimoine-liens/_doc/PM89001432?routing=PA00113932
{"titre": "cloche", "materiaux": "bronze", "lien": {"name": "objet", "parent": "PA00113932"}}

PUT /patrimoine-liens/_doc/PM89001430?routing=PA00113932
{"titre": "autel", "materiaux": "pierre", "lien": {"name": "objet", "parent": "PA00113932"}}

PUT /patrimoine-liens/_doc/PM89001431?routing=PA00113932
{"titre": "statue : Christ en croix", "materiaux": "bois : taillé", "lien": {"name": "objet", "parent": "PA00113932"}}
```
