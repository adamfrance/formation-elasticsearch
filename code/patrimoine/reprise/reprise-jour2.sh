#!/usr/bin/env bash
# Reprise du jour 2 : remet Patrimoine dans l'état de la fin du jour 1 (pipelines, templates, monuments-v1 et
# monuments-v2 avec leurs 46 761 monuments, alias monuments vers monuments-v2), sur un Elasticsearch qui tourne.
# Sans danger si tout est déjà en place.
#
#   export ELASTIC_PASSWORD='…'
#   bash ~/projets/formation-elasticsearch/corrige-jour1/patrimoine/reprise/reprise-jour2.sh
set -euo pipefail
P="$(cd "$(dirname "$0")/.." && pwd)"                    # le dossier patrimoine qui contient ce script
export ES_URL=https://localhost:9200 ES_CA=~/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt
es() { curl -s --cacert "$ES_CA" -u "elastic:$ELASTIC_PASSWORD" -H 'Content-Type: application/json' "$@"; echo; }

echo "1. Les pipelines et les templates"
es -X PUT "$ES_URL/_ingest/pipeline/monuments-nettoyage" -d @"$P/pipelines/monuments-nettoyage.json"
es -X PUT "$ES_URL/_ingest/pipeline/monuments-protections" -d @"$P/pipelines/monuments-protections.json"
es -X PUT "$ES_URL/_component_template/patrimoine-analyse" -d @"$P/templates/patrimoine-analyse.json"
es -X PUT "$ES_URL/_index_template/monuments" -d @"$P/templates/monuments.json"

echo "2. Les monuments du ministère dans monuments-v1"
csv=~/projets/formation-elasticsearch/patrimoine/donnees/merimee.csv     # le fichier téléchargé à l'atelier 2
[ -f "$csv" ] || csv="$P/donnees/merimee.csv"
[ -f "$csv" ] || { mkdir -p "$P/donnees" && curl -sS -o "$csv" https://ministere-culture.s3.sbg.io.cloud.ovh.net/POP/merimee.csv; }
python3 "$P/reprise/charger.py" "$csv" monuments-v1 monuments-nettoyage
es -X POST "$ES_URL/monuments-v1/_refresh" > /dev/null

echo "3. monuments-v2, recopiée de monuments-v1"
es -X POST "$ES_URL/_reindex?wait_for_completion=true&refresh=true&filter_path=total,created,updated,failures" \
  -d '{"source":{"index":"monuments-v1"},"dest":{"index":"monuments-v2"}}'

echo "4. L'alias monuments vers monuments-v2"
if es "$ES_URL/_alias/monuments" | grep -q '"aliases"'; then
  es -X POST "$ES_URL/_aliases" -d '{"actions":[{"remove":{"index":"*","alias":"monuments"}},{"add":{"index":"monuments-v2","alias":"monuments"}}]}'
elif es -o /dev/null -w '%{http_code}' "$ES_URL/monuments" | grep -q 200; then
  es -X POST "$ES_URL/_aliases" -d '{"actions":[{"remove_index":{"index":"monuments"}},{"add":{"index":"monuments-v2","alias":"monuments"}}]}'
else
  es -X POST "$ES_URL/_aliases" -d '{"actions":[{"add":{"index":"monuments-v2","alias":"monuments"}}]}'
fi
es "$ES_URL/_cat/count/monuments?v"
