# Elasticsearch : indexation de contenu — les supports

- `formation-elasticsearch-jour1-diapos.html` et `formation-elasticsearch-jour2-diapos.html` : les diapositives des deux
  jours. GitHub n'affiche pas une page HTML : cloner la branche, puis ouvrir le fichier dans le navigateur.
- `code/patrimoine/` : les fichiers de Patrimoine montrés sur les diapositives, rangés comme dans
  `~/projets/formation-elasticsearch/patrimoine/` (Logstash, Filebeat, pipelines, templates, photos, assistant, page de
  recherche, script de reprise) ; `code/patrimoine/console/` : les requêtes de la console, jour par jour.
- `code/commandes/jour-1.md` et `jour-2.md` : toutes les commandes des diapositives, dans l'ordre, avec le numéro de
  chaque diapositive (le lien « Toutes les commandes » au pied d'une diapositive mène à sa section).
- `code/demos/` : les requêtes des démonstrations.

```bash
cd ~/projets/formation-elasticsearch
git clone -b supports https://github.com/adamfrance/formation-elasticsearch.git supports
```

Pour récupérer une nouvelle version : `cd ~/projets/formation-elasticsearch/supports && git pull`.
