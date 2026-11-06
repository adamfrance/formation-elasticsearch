# Elasticsearch : indexation de contenu — jour 1 : les commandes des diapositives

Chaque bloc est celui du bouton « Copier » de la diapositive, dans l'ordre de la journée : les commandes du terminal, les requêtes de la console de Kibana et le contenu des fichiers à créer. Le numéro est celui de la diapositive.

## Diapositive 4

**Votre poste est-il prêt ?**

Dans le terminal :

```bash
nproc; free -h | head -2; df -h ~ | tail -1
curl --version | head -1; jq --version; git --version; python3 --version
python3 -m venv /tmp/essai-venv; /tmp/essai-venv/bin/pip --version
```

## Diapositive 6

**Créer notre arborescence**

Dans le terminal :

```bash
mkdir -p ~/elastic
mkdir -p ~/projets/formation-elasticsearch/patrimoine/donnees
mkdir -p ~/projets/formation-elasticsearch/patrimoine/logstash
mkdir -p ~/projets/formation-elasticsearch/patrimoine/filebeat
mkdir -p ~/projets/formation-elasticsearch/patrimoine/photos
mkdir -p ~/projets/formation-elasticsearch/patrimoine/rag
mkdir -p ~/projets/formation-elasticsearch/patrimoine/recherche
ls -1 ~/projets/formation-elasticsearch/patrimoine
```

## Diapositive 7

**Lancer les téléchargements dès maintenant**

Dans le terminal :

```bash
mkdir -p ~/elastic ~/projets/formation-elasticsearch/patrimoine/donnees
cd ~/elastic
for logiciel in elasticsearch/elasticsearch kibana/kibana logstash/logstash beats/filebeat/filebeat; do
  curl -sSO https://artifacts.elastic.co/downloads/$logiciel-9.5.6-linux-x86_64.tar.gz
  curl -sSO https://artifacts.elastic.co/downloads/$logiciel-9.5.6-linux-x86_64.tar.gz.sha512
done
ls -lh
```

## Diapositive 28

**Vérifier l'archive et l'extraire**

Dans le terminal :

```bash
cd ~/elastic
sha512sum -c elasticsearch-9.5.6-linux-x86_64.tar.gz.sha512

cd ~/elastic
tar -xzf elasticsearch-9.5.6-linux-x86_64.tar.gz
cd elasticsearch-9.5.6
ls
du -sh .
```

## Diapositive 29

**La mémoire et le nom du cluster**

Dans le terminal :

```bash
cd ~/elastic/elasticsearch-9.5.6
cat > config/jvm.options.d/memoire.options <<'FIN'
-Xms1g
-Xmx1g
FIN
cat config/jvm.options.d/memoire.options

cd ~/elastic/elasticsearch-9.5.6
cat >> config/elasticsearch.yml <<'FIN'
cluster.name: patrimoine
node.name: noeud-1
FIN
grep -v '^#' config/elasticsearch.yml | grep -v '^$'
```

## Diapositive 30

**Le premier démarrage**

Dans le terminal :

```bash
bin/elasticsearch
```

## Diapositive 31

**Le mot de passe de l'utilisateur elastic**

Dans le terminal :

```bash
cd ~/elastic/elasticsearch-9.5.6
bin/elasticsearch-reset-password -u elastic -b
```

## Diapositive 32

**Ce que le premier démarrage a écrit**

Dans le terminal :

```bash
cd ~/elastic/elasticsearch-9.5.6
grep -v '^#' config/elasticsearch.yml | grep -v '^$'; ls config/certs
```

## Diapositive 33

**Le premier appel**

Dans le terminal :

```bash
curl --cacert config/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

## Diapositive 34

**Sans certificat ou sans le bon mot de passe : refusé**

Dans le terminal :

```bash
curl -sS -u elastic:x https://localhost:9200; echo; curl -sS http://localhost:9200; echo

cd ~/elastic/elasticsearch-9.5.6
curl -s --cacert config/certs/http_ca.crt -u elastic:mauvais https://localhost:9200 | jq .
```

## Diapositive 44

**Inscrire Kibana auprès d'Elasticsearch**

Dans le terminal :

```bash
cd ~/elastic
sha512sum -c kibana-9.5.6-linux-x86_64.tar.gz.sha512
tar -xzf kibana-9.5.6-linux-x86_64.tar.gz
du -sh kibana-9.5.6

cd ~/elastic/elasticsearch-9.5.6
JETON=$(bin/elasticsearch-create-enrollment-token -s kibana | tail -1)
cd ~/elastic/kibana-9.5.6
bin/kibana-setup --enrollment-token "$JETON"
```

## Diapositive 45

**Démarrer Kibana, et le voir prêt**

Dans le terminal :

- dans un nouveau terminal, celui de Kibana : aller dans son dossier
- démarrer Kibana ; il reste allumé, et ce terminal avec lui

```bash
cd ~/elastic/kibana-9.5.6

bin/kibana
```

## Diapositive 49

**Explorer le cluster dans la console**

Dans la console de Kibana :

```text
GET /_cat/health?v&h=cluster,status,node.total,shards,pri,unassign,active_shards_percent

GET /_cat/nodes?v&h=name,node.role,heap.percent,ram.percent,cpu,master
```

## Diapositive 51

**Les documents fournis : trois monuments**

Dans la console de Kibana : au-dessus de chaque fiche, écrire sa requête (le bouton copie les trois) :

- PA00110460 · Abbaye et dépendances (Le Mont-Saint-Michel)
- PA00103291 · Pont du Gard et aqueduc romain de Nîmes (Vers-Pont-du-Gard)

```text
# PA00110460 · Abbaye et dépendances (Le Mont-Saint-Michel)
{
  "titre": "Abbaye et dépendances",
  "denomination": "abbaye",
  "commune": "Le Mont-Saint-Michel",
  "departement": "Manche",
  "region": "Normandie",
  "siecle": "11e siècle;16e siècle",
  "protection": "classé MH",
  "historique": "Abbaye bénédictine de style gothique dédiée à l'archange Saint-Michel construite du 11e au 16e siècle."
}

# PA00103291 · Pont du Gard et aqueduc romain de Nîmes (Vers-Pont-du-Gard)
{
  "titre": "Pont du Gard et aqueduc romain de Nîmes",
  "denomination": "site archéologique;pont aqueduc",
  "commune": "Vers-Pont-du-Gard",
  "departement": "Gard",
  "region": "Occitanie",
  "siecle": "Gallo-romain",
  "protection": "classé MH;inscrit MH partiellement;protection partielle",
  "historique": "Importance de cet aqueduc dans la connaissance architecturale et technique des aqueducs romains et dans son lien avec la cité de Nîmes. Long de cinquante kilomètres, depuis les sources de l'Eure à Uzès jusqu'à son arrivée au castellum divisorium, l'ouvrage canalisait l'eau destinée à alimenter Nîmes. Construit au 1er siècle après JC."
}

# PA00102588 · Cité de Carcassonne (Carcassonne)
{
  "titre": "Cité de Carcassonne",
  "denomination": "fortification d'agglomération;agglomération",
  "commune": "Carcassonne",
  "departement": "Aude",
  "region": "Occitanie",
  "siecle": "5e siècle;11e siècle;12e siècle",
  "protection": "classé MH",
  "historique": "Cité médiévale fortifiée dotée d'un système défensif important, très restaurée au 19e siècle par Viollet-le-Duc. Une portion des murailles remonte au 5e siècle, sans doute suite au passage des Wisigoths. Le château date des 11e et 12e siècles. La porte Narbonnaise et toute la partie méridionale de l'enceinte intérieure, ainsi que le couronnement des tours, ont été construits au 13e siècle, après que le dernier vicomte de Carcassonne eut abandonné en 1247 ses droits seigneuriaux à Saint-Louis. L'enceinte extérieure paraît être peu postérieure à ces dernières constructions."
}
```

## Diapositive 52

**Correction : l'index des monuments, jaune**

Dans la console de Kibana :

```text
PUT /monuments
{
  "settings": {"number_of_shards": 1, "number_of_replicas": 1}
}
GET /_cat/shards/monuments?v&h=index,shard,prirep,state,docs,node

GET /_cluster/health/monuments
```

## Diapositive 53

**Correction : ranger les trois monuments**

Dans la console de Kibana : les trois requêtes (le bouton les copie en entier) :

```text
PUT /monuments/_doc/PA00110460
{
  "titre": "Abbaye et dépendances",
  "denomination": "abbaye",
  "commune": "Le Mont-Saint-Michel",
  "departement": "Manche",
  "region": "Normandie",
  "siecle": "11e siècle;16e siècle",
  "protection": "classé MH",
  "historique": "Abbaye bénédictine de style gothique dédiée à l'archange Saint-Michel construite du 11e au 16e siècle."
}

PUT /monuments/_doc/PA00103291
{
  "titre": "Pont du Gard et aqueduc romain de Nîmes",
  "denomination": "site archéologique;pont aqueduc",
  "commune": "Vers-Pont-du-Gard",
  "departement": "Gard",
  "region": "Occitanie",
  "siecle": "Gallo-romain",
  "protection": "classé MH;inscrit MH partiellement;protection partielle",
  "historique": "Importance de cet aqueduc dans la connaissance architecturale et technique des aqueducs romains et dans son lien avec la cité de Nîmes. Long de cinquante kilomètres, depuis les sources de l'Eure à Uzès jusqu'à son arrivée au castellum divisorium, l'ouvrage canalisait l'eau destinée à alimenter Nîmes. Construit au 1er siècle après JC."
}

PUT /monuments/_doc/PA00102588
{
  "titre": "Cité de Carcassonne",
  "denomination": "fortification d'agglomération;agglomération",
  "commune": "Carcassonne",
  "departement": "Aude",
  "region": "Occitanie",
  "siecle": "5e siècle;11e siècle;12e siècle",
  "protection": "classé MH",
  "historique": "Cité médiévale fortifiée dotée d'un système défensif important, très restaurée au 19e siècle par Viollet-le-Duc. Une portion des murailles remonte au 5e siècle, sans doute suite au passage des Wisigoths. Le château date des 11e et 12e siècles. La porte Narbonnaise et toute la partie méridionale de l'enceinte intérieure, ainsi que le couronnement des tours, ont été construits au 13e siècle, après que le dernier vicomte de Carcassonne eut abandonné en 1247 ses droits seigneuriaux à Saint-Louis. L'enceinte extérieure paraît être peu postérieure à ces dernières constructions."
}
```

## Diapositive 54

**Correction : lire, puis chercher**

Dans la console de Kibana :

```text
GET /monuments/_doc/PA00103291

GET /monuments/_search
{"query": {"match": {"historique": "aqueduc romain"}}}
```

## Diapositive 55

**Démarrer un second nœud**

Dans le terminal :

```bash
cd ~/elastic/elasticsearch-9.5.6
JETON_NOEUD=$(bin/elasticsearch-create-enrollment-token -s node | tail -1)
cd ~/elastic
mkdir -p noeud-2
tar -xzf elasticsearch-9.5.6-*.tar.gz -C noeud-2 --strip-components=1
printf -- '-Xms512m\n-Xmx512m\n' > noeud-2/config/jvm.options.d/memoire.options
printf 'cluster.name: patrimoine\nnode.name: noeud-2\n' >> noeud-2/config/elasticsearch.yml
cd noeud-2
nohup bin/elasticsearch -p ~/elastic/noeud-2.pid --enrollment-token "$JETON_NOEUD" > ~/elastic/noeud-2.log 2>&1 &
```

## Diapositive 56

**Un second nœud, et le cluster passe au vert**

Dans la console de Kibana :

```text
GET /_cat/nodes?v&h=name,node.role,heap.percent,master

GET /_cat/shards/monuments?v&h=index,shard,prirep,state,docs,node

GET /_cluster/health/monuments
```

## Diapositive 66

**Démonstration : créer, puis lire**

Dans la console de Kibana :

```text
PUT /livres/_doc/1
{
  "titre": "Le Petit Prince",
  "auteur": "Antoine de Saint-Exupéry",
  "annee": 1943,
  "genres": "conte;jeunesse"
}
GET /livres/_doc/1
```

## Diapositive 67

**Démonstration : un identifiant automatique, une modification**

Dans la console de Kibana :

```text
POST /livres/_doc
{
  "titre": "L’Étranger",
  "auteur": "Albert Camus",
  "annee": 1942,
  "genres": "roman"
}
POST /livres/_update/1
{"doc": {"pages": 96}}
GET /livres/_doc/1
```

## Diapositive 70

**Démonstration : deux écritures en conflit**

Dans la console de Kibana :

```text
PUT /livres/_create/1
{"titre": "Le Petit Prince"}
PUT /livres/_doc/1?if_seq_no=0&if_primary_term=1
{"titre": "Le Petit Prince", "annee": 1943}
```

## Diapositive 73

**Démonstration : _bulk, plusieurs opérations en une requête**

Dans la console de Kibana :

```text
POST /livres/_bulk
{"index": {"_id": "1"}}
{"titre": "Le Petit Prince", "auteur": "Antoine de Saint-Exupéry", "annee": 1943, "genres": "conte;jeunesse"}
{"index": {"_id": "2"}}
{"titre": "Les Misérables", "auteur": "Victor Hugo", "annee": 1862, "genres": "roman"}
{"index": {"_id": "3"}}
{"titre": "Germinal", "auteur": "Émile Zola", "annee": 1885, "genres": "roman"}
{"create": {"_id": "2"}}
{"titre": "Les Misérables, en double"}
{"update": {"_id": "3"}}
{"doc": {"pages": 592}}
{"delete": {"_id": "999"}}
```

## Diapositive 75

**Les dix monuments à copier**

Dans la console de Kibana : les vingt lignes, sous la requête que vous allez écrire :

```text
{"index": {"_id": "PA00078776"}}
{"titre": "Cathédrale Notre-Dame", "denomination": "cathédrale", "commune": "Reims", "departement": "Marne", "region": "Grand Est", "siecle": "13e siècle", "protection": "classé MH", "historique": "Ancienne salle du Trésor et restes du cloître : datation non précisée ; Cathédrale : 13e siècle."}
{"index": {"_id": "PA00081941"}}
{"titre": "Palais des Papes", "denomination": "palais", "commune": "Avignon", "departement": "Vaucluse", "region": "Provence-Alpes-Côte d'Azur", "siecle": "14e siècle", "protection": "classé MH", "historique": "Palais élevé au 14e siècle quand la ville était siège de la papauté."}
{"index": {"_id": "PA00084875"}}
{"titre": "Château du Haut-Koenigsbourg (ou Hohenkoenigsbourg)", "denomination": "château fort", "commune": "Orschwiller", "departement": "Bas-Rhin", "region": "Grand Est", "siecle": "12e siècle;15e siècle;1er quart 20e siècle", "protection": "classé MH", "historique": "Ancien château médiéval attesté depuis le 12e siècle et démoli lors de la Guerre de Trente Ans. Les ruines du château sont données par la Ville de Sélestat à l'empereur d'Allemagne Guillaume II en 1899. De 1901 à 1908, ce dernier fait consolider l'édifice par l'architecte Bodo Ebhardt. S'appuyant sur une importante documentation, celui-ci réalise une restitution du château dans son état supposé du 15e siècle. Le même programme de restitution s'applique aussi aux aménagements intérieurs, la peinture des murs et des voûtes étant confiée à Léo Schnug, peintre strasbourgeois. Devenu un véritable château-musée, il attire de très nombreux visiteurs. La propriété du château (anciennement propriété de l'Etat, ministère de la culture) a été transférée au département le 1er janvier 2007."}
{"index": {"_id": "PA00112529"}}
{"titre": "Abbaye de Fontenay", "denomination": "abbaye", "commune": "Marmagne", "departement": "Côte-d'Or", "region": "Bourgogne-Franche-Comté", "siecle": "1ère moitié 12e siècle", "protection": "classé MH", "historique": "Abbaye fondée en 1118 par Saint-Bernard."}
{"index": {"_id": "PA00103091"}}
{"titre": "Amphithéâtre ou Arènes", "denomination": "amphithéâtre;arène", "commune": "Nîmes", "departement": "Gard", "region": "Occitanie", "siecle": "Haut-Empire", "protection": "classé MH", "historique": "Les arènes, situées au centre de la ville, étaient destinées à la présentation de chasses et de combats de gladiateurs. Au Moyen-Age, le monument servit de refuge à une partie de la population urbaine. Des maisons, deux églises et le château des chevaliers des Arènes y furent construits avant d'être démolis au début du 19e siècle. La structure des arènes est constituée par un ensemble complexe de galeries concentriques et rayonnantes, couvertes par des voûtes de divers types, permettant d'assurer aisément la circulation du public. La piste centrale est accessible par deux entrées principales sur le grand axe et par deux petites portes aux extrémités du petit axe. Deux galeries souterraines servaient sans doute de coulisses et de logement pour la machinerie. Une cavea de 34 gradins pouvait recevoir environ 25.000 spectateurs. Elle était abritée par un velum tendu sur des câbles que portaient 120 mâts plantés dans des consoles. Certains des spectateurs disposaient de places réservées, signalées par des inscriptions. Des sillons gravés sur les gradins, indiquaient sans doute les limites des places individuelles."}
{"index": {"_id": "PA00099066"}}
{"titre": "Maison de Napoléon Bonaparte", "denomination": "maison", "commune": "Ajaccio", "departement": "Corse-du-Sud", "region": "Corse", "siecle": "17e siècle;18e siècle", "protection": "classé MH", "historique": "La construction de la maison remonte au début du 17e siècle. Elle possédait à cette époque deux étages. A la naissance de Napoléon, l'édifice comprenait trois étages. Charles Bonaparte, père de Napoléon, construisit une terrasse en 1774. Au rez-de-chaussée, le vestibule à escalier donne accès aux étages. S'y trouvent également une cuisine, des caves, buchers et pièces de débarras. Le premier étage comprend un salon, une salle à manger, le cabinet de travail de Charles Bonaparte et la chambre où est né Napoléon. Une galerie éclairée par six fenêtres sur rue et six fenêtres et portes à balcon, donnent sur la terrasse qui est de niveau avec l'étage. La galerie donne accès au fumoir, à une chambre et une pièce servant de cabinet de travail ou de toilette. Les deux derniers étages présentent la même distribution et comprenaient des chambres à coucher. Pendant l'enfance de Napoléon, la famille occupait les deux premiers étages. Le mobilier de la maison semble avoir été renouvelé en partie par Joseph Bonaparte lorsqu'il revint d'Italie comme commissaire des guerres."}
{"index": {"_id": "PA46000020"}}
{"titre": "Cité religieuse", "denomination": "ensemble religieux", "commune": "Rocamadour", "departement": "Lot", "region": "Occitanie", "siecle": "Moyen Age;19e siècle", "protection": "inscrit MH partiellement;classé MH partiellement;protection totale", "historique": "Le renom du pélerinage marial de Rocamadour place cette petite cité du Haut Quercy parmi les sites majeurs du monde chrétien depuis le Moyen Age. En 1105, première mention certaine de l'église Sainte-Marie ou Notre-Dame sur une bulle du pape Pascal II. L'ensemble des bâtiments qui constituent la cité religieuse est construit au 12e siècle (découverte d'un corps \"integrum\" identifié comme celui de Saint-Amadour) : au milieu du 12e siècle, Notre-Dame, Saint-Michel Saint-Sauveur et Saint-Amadour existent ; en 1223, mention de la salle neuve du palais abbatial. Des reconstructions partielles ponctuent les prises et pillages dont la cité est victime jusqu'au 16e siècle. Réduit à une dimension locale aux 17e et 18e siècles, le pélerinage périclite et les procès-verbaux d'époque révolutionnaire notent l'état ruiniforme des bâtiments. La restauration matérielle du site sera orchestrée par les évêques de Cahors à partir de 1842 et conduite par l'abbé Cheval, à partir du noyau médiéval. Première campagne de restauration de 1858 à 1864 : Saint-Sauveur-Saint-Amadour (1858-1860) , Sainte-Anne (1861-1862) et Notre-Dame (1860-1864) ; Saint-Michel restaurée en 1865, Saint-Blaise vers 1867 ; dernière phase du chantier concernant le palais abbatial, la porterie et Saint-Jean-Baptiste entre 1869 et 1872."}
{"index": {"_id": "PA00096993"}}
{"titre": "Cathédrale Notre-Dame", "denomination": "cathédrale", "commune": "Chartres", "departement": "Eure-et-Loir", "region": "Centre-Val de Loire", "siecle": "11e siècle;13e siècle;16e siècle", "protection": "classé MH"}
{"index": {"_id": "PA00081815"}}
{"titre": "Chapelle et pont Saint-Bénézet", "denomination": "chapelle;pont", "commune": "Avignon", "departement": "Vaucluse", "region": "Provence-Alpes-Côte d'Azur", "siecle": "12e siècle", "protection": "classé MH"}
{"index": {"_id": "PA00099077"}}
{"titre": "Enceinte fortifiée dite citadelle", "denomination": "citadelle", "commune": "Bonifacio", "departement": "Corse-du-Sud", "region": "Corse", "protection": "inscrit MH partiellement;classé MH partiellement"}
```

## Diapositive 76

**Correction : dix monuments d'un coup**

Dans la console de Kibana :

```text
POST /monuments/_bulk
{"index": {"_id": "PA00078776"}}
{"titre": "Cathédrale Notre-Dame", "denomination": "cathédrale", "commune": "Reims", "departement": "Marne", "region": "Grand Est", "siecle": "13e siècle", "protection": "classé MH", "historique": "Ancienne salle du Trésor et restes du cloître : datation non précisée ; Cathédrale : 13e siècle."}
{"index": {"_id": "PA00081941"}}
{"titre": "Palais des Papes", "denomination": "palais", "commune": "Avignon", "departement": "Vaucluse", "region": "Provence-Alpes-Côte d'Azur", "siecle": "14e siècle", "protection": "classé MH", "historique": "Palais élevé au 14e siècle quand la ville était siège de la papauté."}
{"index": {"_id": "PA00084875"}}
{"titre": "Château du Haut-Koenigsbourg (ou Hohenkoenigsbourg)", "denomination": "château fort", "commune": "Orschwiller", "departement": "Bas-Rhin", "region": "Grand Est", "siecle": "12e siècle;15e siècle;1er quart 20e siècle", "protection": "classé MH", "historique": "Ancien château médiéval attesté depuis le 12e siècle et démoli lors de la Guerre de Trente Ans. Les ruines du château sont données par la Ville de Sélestat à l'empereur d'Allemagne Guillaume II en 1899. De 1901 à 1908, ce dernier fait consolider l'édifice par l'architecte Bodo Ebhardt. S'appuyant sur une importante documentation, celui-ci réalise une restitution du château dans son état supposé du 15e siècle. Le même programme de restitution s'applique aussi aux aménagements intérieurs, la peinture des murs et des voûtes étant confiée à Léo Schnug, peintre strasbourgeois. Devenu un véritable château-musée, il attire de très nombreux visiteurs. La propriété du château (anciennement propriété de l'Etat, ministère de la culture) a été transférée au département le 1er janvier 2007."}
{"index": {"_id": "PA00112529"}}
{"titre": "Abbaye de Fontenay", "denomination": "abbaye", "commune": "Marmagne", "departement": "Côte-d'Or", "region": "Bourgogne-Franche-Comté", "siecle": "1ère moitié 12e siècle", "protection": "classé MH", "historique": "Abbaye fondée en 1118 par Saint-Bernard."}
{"index": {"_id": "PA00103091"}}
{"titre": "Amphithéâtre ou Arènes", "denomination": "amphithéâtre;arène", "commune": "Nîmes", "departement": "Gard", "region": "Occitanie", "siecle": "Haut-Empire", "protection": "classé MH", "historique": "Les arènes, situées au centre de la ville, étaient destinées à la présentation de chasses et de combats de gladiateurs. Au Moyen-Age, le monument servit de refuge à une partie de la population urbaine. Des maisons, deux églises et le château des chevaliers des Arènes y furent construits avant d'être démolis au début du 19e siècle. La structure des arènes est constituée par un ensemble complexe de galeries concentriques et rayonnantes, couvertes par des voûtes de divers types, permettant d'assurer aisément la circulation du public. La piste centrale est accessible par deux entrées principales sur le grand axe et par deux petites portes aux extrémités du petit axe. Deux galeries souterraines servaient sans doute de coulisses et de logement pour la machinerie. Une cavea de 34 gradins pouvait recevoir environ 25.000 spectateurs. Elle était abritée par un velum tendu sur des câbles que portaient 120 mâts plantés dans des consoles. Certains des spectateurs disposaient de places réservées, signalées par des inscriptions. Des sillons gravés sur les gradins, indiquaient sans doute les limites des places individuelles."}
{"index": {"_id": "PA00099066"}}
{"titre": "Maison de Napoléon Bonaparte", "denomination": "maison", "commune": "Ajaccio", "departement": "Corse-du-Sud", "region": "Corse", "siecle": "17e siècle;18e siècle", "protection": "classé MH", "historique": "La construction de la maison remonte au début du 17e siècle. Elle possédait à cette époque deux étages. A la naissance de Napoléon, l'édifice comprenait trois étages. Charles Bonaparte, père de Napoléon, construisit une terrasse en 1774. Au rez-de-chaussée, le vestibule à escalier donne accès aux étages. S'y trouvent également une cuisine, des caves, buchers et pièces de débarras. Le premier étage comprend un salon, une salle à manger, le cabinet de travail de Charles Bonaparte et la chambre où est né Napoléon. Une galerie éclairée par six fenêtres sur rue et six fenêtres et portes à balcon, donnent sur la terrasse qui est de niveau avec l'étage. La galerie donne accès au fumoir, à une chambre et une pièce servant de cabinet de travail ou de toilette. Les deux derniers étages présentent la même distribution et comprenaient des chambres à coucher. Pendant l'enfance de Napoléon, la famille occupait les deux premiers étages. Le mobilier de la maison semble avoir été renouvelé en partie par Joseph Bonaparte lorsqu'il revint d'Italie comme commissaire des guerres."}
{"index": {"_id": "PA46000020"}}
{"titre": "Cité religieuse", "denomination": "ensemble religieux", "commune": "Rocamadour", "departement": "Lot", "region": "Occitanie", "siecle": "Moyen Age;19e siècle", "protection": "inscrit MH partiellement;classé MH partiellement;protection totale", "historique": "Le renom du pélerinage marial de Rocamadour place cette petite cité du Haut Quercy parmi les sites majeurs du monde chrétien depuis le Moyen Age. En 1105, première mention certaine de l'église Sainte-Marie ou Notre-Dame sur une bulle du pape Pascal II. L'ensemble des bâtiments qui constituent la cité religieuse est construit au 12e siècle (découverte d'un corps \"integrum\" identifié comme celui de Saint-Amadour) : au milieu du 12e siècle, Notre-Dame, Saint-Michel Saint-Sauveur et Saint-Amadour existent ; en 1223, mention de la salle neuve du palais abbatial. Des reconstructions partielles ponctuent les prises et pillages dont la cité est victime jusqu'au 16e siècle. Réduit à une dimension locale aux 17e et 18e siècles, le pélerinage périclite et les procès-verbaux d'époque révolutionnaire notent l'état ruiniforme des bâtiments. La restauration matérielle du site sera orchestrée par les évêques de Cahors à partir de 1842 et conduite par l'abbé Cheval, à partir du noyau médiéval. Première campagne de restauration de 1858 à 1864 : Saint-Sauveur-Saint-Amadour (1858-1860) , Sainte-Anne (1861-1862) et Notre-Dame (1860-1864) ; Saint-Michel restaurée en 1865, Saint-Blaise vers 1867 ; dernière phase du chantier concernant le palais abbatial, la porterie et Saint-Jean-Baptiste entre 1869 et 1872."}
{"index": {"_id": "PA00096993"}}
{"titre": "Cathédrale Notre-Dame", "denomination": "cathédrale", "commune": "Chartres", "departement": "Eure-et-Loir", "region": "Centre-Val de Loire", "siecle": "11e siècle;13e siècle;16e siècle", "protection": "classé MH"}
{"index": {"_id": "PA00081815"}}
{"titre": "Chapelle et pont Saint-Bénézet", "denomination": "chapelle;pont", "commune": "Avignon", "departement": "Vaucluse", "region": "Provence-Alpes-Côte d'Azur", "siecle": "12e siècle", "protection": "classé MH"}
{"index": {"_id": "PA00099077"}}
{"titre": "Enceinte fortifiée dite citadelle", "denomination": "citadelle", "commune": "Bonifacio", "departement": "Corse-du-Sud", "region": "Corse", "protection": "inscrit MH partiellement;classé MH partiellement"}
```

## Diapositive 77

**Correction : compter, puis regarder les shards**

Dans la console de Kibana :

```text
GET /monuments/_count

GET /_cat/shards/monuments?v
```

## Diapositive 79

**Démonstration : six livres, trois shards**

Dans la console de Kibana :

```text
PUT /livres-3
{
  "settings": {"number_of_shards": 3, "number_of_replicas": 0}
}
GET /_cat/shards/livres-3?v&h=index,shard,prirep,docs

GET /livres-3/_search_shards?routing=4&filter_path=shards.shard,shards.primary
```

## Diapositive 80

**Démonstration : une clé de routage choisie**

Dans la console de Kibana :

```text
PUT /livres-3/_doc/7?routing=camus
{
  "titre": "La Peste",
  "auteur": "Albert Camus",
  "annee": 1947
}
GET /livres-3/_doc/7

GET /livres-3/_doc/7?routing=camus
```

## Diapositive 85

**Les processeurs disponibles**

Dans la console de Kibana :

```text
GET /_nodes/ingest?filter_path=nodes.*.ingest.processors.type
```

## Diapositive 86

**Démonstration : un pipeline, essayé avant de servir**

Dans la console de Kibana :

```text
PUT /_ingest/pipeline/livres-nettoyage
{
  "description": "Livres : les genres en liste, la date d’ajout",
  "processors": [{"split": {"field": "genres", "separator": ";"}}, {"set": {"field": "ajoute_le", "value": "{{_ingest.timestamp}}"}}]
}
POST /_ingest/pipeline/livres-nettoyage/_simulate
{"docs": [{"_source": {"titre": "Le Petit Prince", "genres": "conte;jeunesse"}}]}
```

## Diapositive 87

**Démonstration : le pipeline à l'écriture**

Dans la console de Kibana :

```text
PUT /livres/_doc/4?pipeline=livres-nettoyage
{
  "titre": "Vingt mille lieues sous les mers",
  "auteur": "Jules Verne",
  "annee": 1870,
  "genres": "roman;aventure"
}
GET /livres/_doc/4
```

## Diapositive 89

**Les fichiers fournis : les deux pipelines**

Dans la console de Kibana : les deux pipelines, avec leur requête (le bouton copie les deux en entier) :

```text
PUT /_ingest/pipeline/monuments-nettoyage
{
  "description": "Patrimoine : une ligne de la base Mérimée ramenée à des champs courts et propres",
  "processors": [
    {
      "rename": {
        "field": "Reference",
        "target_field": "reference",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Titre_editorial_de_la_notice",
        "target_field": "titre",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Denomination_de_l_edifice",
        "target_field": "denomination",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Commune_forme_editoriale",
        "target_field": "commune",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Departement_en_lettres",
        "target_field": "departement",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Departement_format_numerique",
        "target_field": "departement_code",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Region",
        "target_field": "region",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Siecle_de_la_campagne_principale_de_construction",
        "target_field": "siecle",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Typologie_de_la_protection",
        "target_field": "protection",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Date_et_typologie_de_la_protection",
        "target_field": "historique_protection",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Historique",
        "target_field": "historique",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Statut_juridique_de_l_edifice",
        "target_field": "statut",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "coordonnees_au_format_WGS84",
        "target_field": "localisation",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Lien_vers_la_base_Palissy",
        "target_field": "objets",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Date_de_la_derniere_mise_a_jour",
        "target_field": "mise_a_jour",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "denomination",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "departement_code",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "siecle",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "protection",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "statut",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "objets",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "gsub": {
        "field": "objets",
        "pattern": "^https://www.pop.culture.gouv.fr/notice/palissy/",
        "replacement": "",
        "ignore_missing": true
      }
    },
    {
      "remove": {
        "keep": [
          "reference",
          "titre",
          "denomination",
          "commune",
          "departement",
          "departement_code",
          "region",
          "siecle",
          "protection",
          "historique_protection",
          "historique",
          "statut",
          "localisation",
          "objets",
          "mise_a_jour"
        ]
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "field": "erreur_ingestion",
        "value": "{{ _ingest.on_failure_message }}"
      }
    }
  ]
}

PUT /_ingest/pipeline/objets-nettoyage
{
  "description": "Patrimoine : une ligne de la base Palissy (objets mobiliers) ramenée à des champs courts et propres",
  "processors": [
    {
      "rename": {
        "field": "Reference",
        "target_field": "reference",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Titre_editorial",
        "target_field": "titre",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Denomination",
        "target_field": "denomination",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Commune_forme_editoriale",
        "target_field": "commune",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Departement_en_lettres",
        "target_field": "departement",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Region",
        "target_field": "region",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Siecle_de_creation",
        "target_field": "siecle",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Typologie_de_la_protection",
        "target_field": "protection",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Historique",
        "target_field": "historique",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Description",
        "target_field": "description",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Materiaux",
        "target_field": "materiaux",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Nom_de_l_edifice",
        "target_field": "edifice",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Reference_a_une_notice_Merimee_MH",
        "target_field": "monument",
        "ignore_missing": true
      }
    },
    {
      "rename": {
        "field": "Date_de_la_derniere_mise_a_jour",
        "target_field": "mise_a_jour",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "denomination",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "siecle",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "protection",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "materiaux",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "split": {
        "field": "monument",
        "separator": "\\s*;\\s*",
        "ignore_missing": true
      }
    },
    {
      "remove": {
        "keep": [
          "reference",
          "titre",
          "denomination",
          "commune",
          "departement",
          "region",
          "siecle",
          "protection",
          "historique",
          "description",
          "materiaux",
          "edifice",
          "monument",
          "mise_a_jour"
        ]
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "field": "erreur_ingestion",
        "value": "{{ _ingest.on_failure_message }}"
      }
    }
  ]
}
```

## Diapositive 90

**Le fichier fourni : la ligne brute de Carcassonne**

Dans la console de Kibana : la ligne, déjà dans sa requête de simulation (le bouton copie tout) :

```text
POST /_ingest/pipeline/monuments-nettoyage/_simulate
{
  "docs": [
    {
      "_source": {
        "Reference": "PA00102588",
        "Etablissement_affectataire_de_l_edifice": "direction générale des patrimoines",
        "Nature_de_la_protection": "liste;arrêté",
        "Auteur_de_l_edifice": "Viollet-le-Duc Eugène (architecte)",
        "Cadastre": "E 99, 109 à 112, 138, 1868;E5 1755;1633, 1129 P",
        "Commune_forme_index": "Carcassonne",
        "Copyright": "© Monuments historiques, 1992. Cette notice reprend intégralement les termes de l’arrêté de protection au titre des Monuments historiques. Elle répond à l’obligation réglementaire du ministère de la Culture d’établir la liste générale des immeubles protégés (art. R. 621-80 du Code du patrimoine). Elle est donc opposable et fait foi juridiquement. Aucune copie numérique ou papier ne sera fournie par courrier ni courriel. Le dossier de protection complet et l’arrêté sont consultables uniquement sur place, dans la salle de lecture de la Médiathèque du patrimoine et de la photographie (MPP), à Charenton-le-Pont (Val-de-Marne).",
        "Denomination_de_l_edifice": "fortification d'agglomération;agglomération",
        "Date_de_la_derniere_mise_a_jour": "2026-03-04",
        "Date_de_creation_de_la_notice": "1993-10-21",
        "Typologie_du_dossier": "dossier de protection",
        "Date_et_typologie_de_la_protection": "1862 : classé MH ; 1926/12/22 : classé MH ; 1942/01/15 : classé MH ; 1932/05/28 : classé MH ; 1942/07/11 : classé MH",
        "Departement_format_numerique": "11",
        "Departement_en_lettres": "Aude",
        "Cadre_de_l_etude": "recensement immeubles MH",
        "Historique": "Cité médiévale fortifiée dotée d'un système défensif important, très restaurée au 19e siècle par Viollet-le-Duc. Une portion des murailles remonte au 5e siècle, sans doute suite au passage des Wisigoths. Le château date des 11e et 12e siècles. La porte Narbonnaise et toute la partie méridionale de l'enceinte intérieure, ainsi que le couronnement des tours, ont été construits au 13e siècle, après que le dernier vicomte de Carcassonne eut abandonné en 1247 ses droits seigneuriaux à Saint-Louis. L'enceinte extérieure paraît être peu postérieure à ces dernières constructions.",
        "Identifiant_Agregee": "IYUJ8N",
        "COG_Insee_lors_de_la_protection": "11069",
        "Liens_externes": "https://mediatheque-patrimoine.culture.gouv.fr/sites/mediatheque/files/documents/liste_mh_1862_0.pdf",
        "Lien_vers_la_base_Archiv_MH": "https://archives-map.culture.gouv.fr/archive/recherche/simple/n:19?RECH_S=PA00102588&RECH_DocumentsNumerises=0&Archives.RECH_Valid=&type=simple",
        "Observations": "site inscrit 20 07 1943 (arrêté) : cité et son cadre ; site inscrit 10 03 1977 (arrêté) : centre historique de la ville basse",
        "Precision_affectataire": "édifice géré par le CMN (Centre des Monuments Natonaux)",
        "Precision_de_la_localisation": "Anciennement région de : Languedoc-Roussillon",
        "Precision_de_la_protection": "Les fortifications : classement par liste de 1862 - Les deux parcelles de terrain, lieux-dits Talus de la Barbacane et Porte d'Aude (cad. E 99, 1868) : classement par arrêté du 22 décembre 1926 - Les parcelles dénommées Champ Rigal Cadène et Grand Champ Sabatier Jalabert, à l'exclusion d'une zone délimitée sur le plan annexé à l'arrêté (cad. 1633, 1129 P) : classement par arrêté du 15 janvier 1942 - Le terrain compris entre la Cité et le grand séminaire (cad. E5 1755) : classement par arrêté du 28 mai 1932 - Le terrain dit Champ du Tournoi, situé en bordure du chemin de la Cité de Carcassonne à Sainte-Croix (cad. E 109 à 112, 138) : classement par arrêté du 11 juillet 1942",
        "Typologie_de_la_protection": "classé MH",
        "Lien_vers_la_base_Palissy": "https://www.pop.culture.gouv.fr/notice/palissy/PM11003104",
        "Region": "Occitanie",
        "Siecle_de_campagne_secondaire_de_construction": "19e siècle",
        "Siecle_de_la_campagne_principale_de_construction": "5e siècle;11e siècle;12e siècle",
        "Format_abrege_du_siecle_de_construction": "5e s.;11e s.;12e s.",
        "Typologie_de_la_zone_de_protection": "liste du patrimoine mondial ; site inscrit",
        "Statut_juridique_de_l_edifice": "propriété de l'État",
        "Titre_editorial_de_la_notice": "Cité de Carcassonne",
        "Commune_forme_editoriale": "Carcassonne",
        "coordonnees_au_format_WGS84": "43.2064207097729,2.36556718854597"
      }
    }
  ]
}
```

## Diapositive 91

**Correction : la ligne brute de Carcassonne, nettoyée**

Dans la console de Kibana :

```text
POST /_ingest/pipeline/monuments-nettoyage/_simulate
{
  "docs": [
    {
      "_source": {
        "Reference": "PA00102588",
        "Etablissement_affectataire_de_l_edifice": "direction générale des patrimoines",
        "Nature_de_la_protection": "liste;arrêté",
        "Auteur_de_l_edifice": "Viollet-le-Duc Eugène (architecte)",
        "Cadastre": "E 99, 109 à 112, 138, 1868;E5 1755;1633, 1129 P",
        "Commune_forme_index": "Carcassonne",
        "Copyright": "© Monuments historiques, 1992. Cette notice reprend intégralement les termes de l’arrêté de protection au titre des Monuments historiques. Elle répond à l’obligation réglementaire du ministère de la Culture d’établir la liste générale des immeubles protégés (art. R. 621-80 du Code du patrimoine). Elle est donc opposable et fait foi juridiquement. Aucune copie numérique ou papier ne sera fournie par courrier ni courriel. Le dossier de protection complet et l’arrêté sont consultables uniquement sur place, dans la salle de lecture de la Médiathèque du patrimoine et de la photographie (MPP), à Charenton-le-Pont (Val-de-Marne).",
        "Denomination_de_l_edifice": "fortification d'agglomération;agglomération",
        "Date_de_la_derniere_mise_a_jour": "2026-03-04",
        "Date_de_creation_de_la_notice": "1993-10-21",
        "Typologie_du_dossier": "dossier de protection",
        "Date_et_typologie_de_la_protection": "1862 : classé MH ; 1926/12/22 : classé MH ; 1942/01/15 : classé MH ; 1932/05/28 : classé MH ; 1942/07/11 : classé MH",
        "Departement_format_numerique": "11",
        "Departement_en_lettres": "Aude",
        "Cadre_de_l_etude": "recensement immeubles MH",
        "Historique": "Cité médiévale fortifiée dotée d'un système défensif important, très restaurée au 19e siècle par Viollet-le-Duc. Une portion des murailles remonte au 5e siècle, sans doute suite au passage des Wisigoths. Le château date des 11e et 12e siècles. La porte Narbonnaise et toute la partie méridionale de l'enceinte intérieure, ainsi que le couronnement des tours, ont été construits au 13e siècle, après que le dernier vicomte de Carcassonne eut abandonné en 1247 ses droits seigneuriaux à Saint-Louis. L'enceinte extérieure paraît être peu postérieure à ces dernières constructions.",
        "Identifiant_Agregee": "IYUJ8N",
        "COG_Insee_lors_de_la_protection": "11069",
        "Liens_externes": "https://mediatheque-patrimoine.culture.gouv.fr/sites/mediatheque/files/documents/liste_mh_1862_0.pdf",
        "Lien_vers_la_base_Archiv_MH": "https://archives-map.culture.gouv.fr/archive/recherche/simple/n:19?RECH_S=PA00102588&RECH_DocumentsNumerises=0&Archives.RECH_Valid=&type=simple",
        "Observations": "site inscrit 20 07 1943 (arrêté) : cité et son cadre ; site inscrit 10 03 1977 (arrêté) : centre historique de la ville basse",
        "Precision_affectataire": "édifice géré par le CMN (Centre des Monuments Natonaux)",
        "Precision_de_la_localisation": "Anciennement région de : Languedoc-Roussillon",
        "Precision_de_la_protection": "Les fortifications : classement par liste de 1862 - Les deux parcelles de terrain, lieux-dits Talus de la Barbacane et Porte d'Aude (cad. E 99, 1868) : classement par arrêté du 22 décembre 1926 - Les parcelles dénommées Champ Rigal Cadène et Grand Champ Sabatier Jalabert, à l'exclusion d'une zone délimitée sur le plan annexé à l'arrêté (cad. 1633, 1129 P) : classement par arrêté du 15 janvier 1942 - Le terrain compris entre la Cité et le grand séminaire (cad. E5 1755) : classement par arrêté du 28 mai 1932 - Le terrain dit Champ du Tournoi, situé en bordure du chemin de la Cité de Carcassonne à Sainte-Croix (cad. E 109 à 112, 138) : classement par arrêté du 11 juillet 1942",
        "Typologie_de_la_protection": "classé MH",
        "Lien_vers_la_base_Palissy": "https://www.pop.culture.gouv.fr/notice/palissy/PM11003104",
        "Region": "Occitanie",
        "Siecle_de_campagne_secondaire_de_construction": "19e siècle",
        "Siecle_de_la_campagne_principale_de_construction": "5e siècle;11e siècle;12e siècle",
        "Format_abrege_du_siecle_de_construction": "5e s.;11e s.;12e s.",
        "Typologie_de_la_zone_de_protection": "liste du patrimoine mondial ; site inscrit",
        "Statut_juridique_de_l_edifice": "propriété de l'État",
        "Titre_editorial_de_la_notice": "Cité de Carcassonne",
        "Commune_forme_editoriale": "Carcassonne",
        "coordonnees_au_format_WGS84": "43.2064207097729,2.36556718854597"
      }
    }
  ]
}
```

## Diapositive 92

**Le piège du « 2A » : un code de département n'est pas un nombre**

Dans la console de Kibana :

```text
POST /_ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "convert": {"field": "departement_code", "type": "integer"}
      }
    ]
  },
  "docs": [
    {"_source": {"departement_code": "11"}},
    {"_source": {"departement_code": "2A"}}
  ]
}
```

## Diapositive 103

**Télécharger le fichier du ministère**

Dans le terminal :

- dans le terminal de travail : aller dans le dossier des données
- télécharger le fichier du ministère (96 Mo)
- sa taille, puis son nombre de lignes
- le début des deux premières lignes : les noms des colonnes, puis un premier monument

```bash
cd ~/projets/formation-elasticsearch/patrimoine/donnees

curl -sSO https://ministere-culture.s3.sbg.io.cloud.ovh.net/POP/merimee.csv

ls -lh merimee.csv
wc -l merimee.csv

head -c 160 merimee.csv; echo; sed -n 2p merimee.csv | cut -c1-160
```

## Diapositive 105

**Installer Logstash et Filebeat : vérifier, puis extraire les archives**

Dans le terminal de travail : les deux archives téléchargées ce matin :

- dans le dossier des logiciels : vérifier l'archive de Logstash (on attend « OK »), l'extraire, voir le dossier créé et sa taille
- Filebeat : la même chose

```bash
cd ~/elastic
sha512sum -c logstash-9.5.6-linux-x86_64.tar.gz.sha512
tar -xzf logstash-9.5.6-linux-x86_64.tar.gz
du -sh logstash-9.5.6

sha512sum -c filebeat-9.5.6-linux-x86_64.tar.gz.sha512
tar -xzf filebeat-9.5.6-linux-x86_64.tar.gz
du -sh filebeat-9.5.6-linux-x86_64
```

## Diapositive 106

**La configuration de Logstash**

~/projets/formation-elasticsearch/patrimoine/logstash/patrimoine.conf : à coller dans nano, deux diapositives plus loin

```text
# Patrimoine : Filebeat envoie chaque ligne des fichiers du ministère de la Culture (port 5044),
# Logstash la découpe en colonnes, Elasticsearch la range (le pipeline d'ingestion nettoie les champs).
input {
  beats {                      # Filebeat envoie ici
    port => 5044
  }
}

filter {
  if [fields][base] == "merimee" {
    csv {                      # la ligne découpée en colonnes nommées
      separator => "|"
      skip_header => true        # la première ligne : les noms des colonnes
      skip_empty_columns => true # une colonne vide n'est pas gardée
      columns => ["Reference", "Destination_actuelle_de_l_edifice", "Adresse_forme_index",
                  "Etablissement_affectataire_de_l_edifice", "Autre_appellation_de_l_edifice",
                  "Nature_de_la_protection", "Auteur_de_l_edifice", "Cadastre", "Commune_forme_index",
                  "Copyright", "Type_de_couverture", "Datation_de_l_edifice", "Denomination_de_l_edifice",
                  "Lieu_de_conservation_d_un_element_architectural_deplace", "Description_de_l_edifice",
                  "Dimensions_normalisees_des_edicules_uniquement", "Date_de_Label",
                  "Date_de_la_derniere_mise_a_jour", "Date_de_creation_de_la_notice", "Domaine",
                  "Typologie_du_dossier", "Date_et_typologie_de_la_protection", "Departement_format_numerique",
                  "Departement_en_lettres", "Partie_d_elevation_exterieure",
                  "Source_de_l_energie_utilisee_par_l_edifice",
                  "Emplacement__forme_et_structure_de_l_escalier", "Description_de_l_elevation_interieure",
                  "etat_de_conservation", "Cadre_de_l_etude", "Genre_du_destinataire", "Historique",
                  "Nom_du_cours_d_eau_traversant_ou_bordant_l_edifice", "Identifiant_Agregee",
                  "COG_Insee_lors_de_la_protection", "Justification_attribution",
                  "Justification_de_la_datation", "Liens_externes", "Lieudit", "Lien_vers_la_base_Archiv_MH",
                  "Materiaux_du_gros_oeuvre", "Nom_du_redacteur", "Observations", "Precision_affectataire",
                  "Partie_constituante_non_etudiee", "Partie_constituante", "Precision_sur_la_denomination",
                  "Personnes_liees_a_l_edifice", "Typologie_de_plan", "Precision_de_la_localisation",
                  "Precision_de_la_protection", "Description_de_l_iconographie", "Typologie_de_la_protection",
                  "Precision_sur_le_statut_de_l_edifice", "Reference_a_un_ensemble",
                  "Lien_vers_la_base_Joconde", "Lien_vers_la_base_Palissy",
                  "References_des_parties_constituantes_etudiees", "Region",
                  "Elements_remarquables_dans_l_edifice", "Remploi",
                  "Renvoi_vers_une_notice_de_la_base_Merimee_ou_Palissy",
                  "Indexation_iconographique_normalisee", "Siecle_de_campagne_secondaire_de_construction",
                  "Siecle_de_la_campagne_principale_de_construction",
                  "Format_abrege_du_siecle_de_construction", "Typologie_de_la_zone_de_protection",
                  "Statut_juridique_de_l_edifice", "Technique_du_decor_porte_de_l_edifice",
                  "Titre_editorial_de_la_notice", "Materiaux_de_la_couverture",
                  "Couverts_ou_decouverts_du_jardin_de_l_edifice", "Vocable___pour_les_edifices_cultuels",
                  "Typologie_du_couvrement", "Adresse_forme_editoriale", "Commune_forme_editoriale",
                  "coordonnees_au_format_WGS84", "Producteur"]
    }
    # l'index et le pipeline de cette base, dans @metadata : utilisés par la sortie, jamais rangés
    mutate { add_field => { "[@metadata][index]" => "monuments" "[@metadata][pipeline]" => "monuments-nettoyage" } }
  } else if [fields][base] == "palissy" {
    csv {
      separator => "|"
      skip_header => true
      skip_empty_columns => true
      columns => ["Reference", "Contexte_d_acquisition", "Adresse_forme_index", "Auteur_du_projet",
                  "Appellation_d_usage", "Personne_morale_creatrice_de_l_objet",
                  "Auteur_de_l_oeuvre_ou_createur_de_l_objet", "References_de_publications",
                  "Categorie_technique", "Commune_forme_index", "Copyright", "Annee_de_creation",
                  "Denomination", "Date_du_recolement", "Lieu_de_deplacement_de_l_objet", "Description",
                  "Dimensions", "Date_de_la_derniere_mise_a_jour", "Date_de_creation_de_la_notice", "Domaine",
                  "Date_et_typologie_de_la_protection", "Departement_format_numerique",
                  "Departement_en_lettres", "Nom_de_l_edifice", "Emplacement_de_l_oeuvre_dans_l_edifice",
                  "Etat", "Cadre_de_l_etude", "Lieu_de_creation", "References_d_expositions", "Historique",
                  "Identifiant_Agregee", "Inscription", "COG_Insee", "Justification_de_la_datation",
                  "Lien_vers_la_base_Arcade", "Liens_externes", "Lieudit", "Lien_vers_la_base_INHA",
                  "Lien_vers_la_base_Archiv_MH", "Statut_juridique_de_l_objet", "Materiaux",
                  "Numero_artificiel_de_differenciation_de_l_objet", "Numero_d_inventaire_affecte_a_l_objet",
                  "Nom_du_redacteur", "Numero_de_l_arrete_de_protection", "Observations", "Lieu_de_provenance",
                  "Intitule_de_l_ensemble", "Partie_constituante_non_etudiee", "Partie_constituante",
                  "Precision_sur_la_denomination", "Precision_sur_les_dimensions", "Personnes_liees_a_l_objet",
                  "Precision_sur_l_etat", "Precision_sur_l_inscription", "Precision_sur_la_localisation",
                  "Precision_sur_la_protection", "Precision_sur_la_representation",
                  "Typologie_de_la_protection", "Reference_a_une_notice_Merimee_MH", "Reference_a_un_ensemble",
                  "Lien_vers_la_base_Joconde", "Lien_vers_la_base_Museofile",
                  "Reference_a_une_partie_constituante", "Region",
                  "Renvoi_vers_une_notice_Palissy_MH_ou_Merimee_MH", "Indexation_iconographique_normalisee",
                  "Siecle_de_creation", "Format_abrege_du_siecle_de_creation",
                  "Sources_d_archives_et_bases_de_donnees_de_reference", "Etape_de_creation",
                  "Statut_juridique_du_proprietaire", "Structure_et_typologie", "Theme_de_l_etude",
                  "Titre_editorial", "Titre_iconographique", "Informations_relatives_aux_vols",
                  "Adresse_forme_editoriale", "Commune_forme_editoriale", "Typologie_du_dossier",
                  "Code_INSEE_commune_actuelle", "Edifice_actuel"]
    }
    mutate { add_field => { "[@metadata][index]" => "objets" "[@metadata][pipeline]" => "objets-nettoyage" } }
  }
}

output {
  elasticsearch {
    hosts => ["https://localhost:9200"]
    ssl_certificate_authorities => ["${HOME}/elastic/elasticsearch-9.5.6/config/certs/http_ca.crt"]
    user => "elastic"
    password => "${ELASTIC_PASSWORD}"       # lu dans l'environnement
    index => "%{[@metadata][index]}"
    pipeline => "%{[@metadata][pipeline]}"
    document_id => "%{Reference}"           # la référence Mérimée sert d'identifiant
  }
}
```

## Diapositive 107

**La configuration de Filebeat**

~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml : à coller dans nano, diapositive suivante

```yaml
# Patrimoine : Filebeat lit les fichiers CSV du ministère de la Culture, ligne par ligne,
# et envoie chaque ligne à Logstash. Le champ fields.base dit de quelle base vient la ligne.
filebeat.inputs:
  - type: filestream          # une entrée par fichier, lu ligne par ligne, avec son identifiant
    id: merimee
    paths:
      - ${HOME}/projets/formation-elasticsearch/patrimoine/donnees/merimee.csv
    fields:
      base: merimee
  - type: filestream
    id: palissy
    enabled: false             # la suite pour ceux qui ont fini
    paths:
      - ${HOME}/projets/formation-elasticsearch/patrimoine/donnees/palissy.csv
    fields:
      base: palissy

output.logstash:               # tout part vers Logstash
  hosts: ["localhost:5044"]
```

## Diapositive 108

**Créer les deux fichiers de configuration, avec nano**

Dans le terminal : coller les quatre lignes, puis Entrée :

- créer les deux dossiers, celui de Logstash, puis celui de Filebeat
- ouvrir le fichier de Logstash : y coller son code, Ctrl+O, Entrée, Ctrl+X
- puis celui de Filebeat, de la même façon

```bash
mkdir -p ~/projets/formation-elasticsearch/patrimoine/logstash && \
mkdir -p ~/projets/formation-elasticsearch/patrimoine/filebeat && \
nano ~/projets/formation-elasticsearch/patrimoine/logstash/patrimoine.conf && \
nano ~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml
```

## Diapositive 109

**Tester la configuration de Logstash**

Dans le terminal :

- dans un nouveau terminal, celui de Logstash : d'abord export ELASTIC_PASSWORD='votre mot de passe', puis aller dans le dossier de Logstash
- tester la configuration, puis s'arrêter : on attend « Configuration OK »

```bash
cd ~/elastic/logstash-9.5.6

bin/logstash -f ~/projets/formation-elasticsearch/patrimoine/logstash/patrimoine.conf --config.test_and_exit
```

## Diapositive 110

**Démarrer Logstash, et le voir prêt**

Dans le terminal :

- dans le même terminal, celui de Logstash
- démarrer Logstash avec notre configuration ; il reste allumé, et ce terminal avec lui

```bash
cd ~/elastic/logstash-9.5.6

bin/logstash -f ~/projets/formation-elasticsearch/patrimoine/logstash/patrimoine.conf
```

## Diapositive 111

**Tester Filebeat : sa configuration, puis le lien avec Logstash**

Dans le terminal :

- dans un nouveau terminal, celui de Filebeat : aller dans son dossier
- Filebeat refuse un fichier que d'autres peuvent modifier : on retire ce droit
- le fichier est-il valide ? on attend « Config OK »
- Logstash répond-il sur le port 5044 ? on attend « talk to server... OK »

```bash
cd ~/elastic/filebeat-9.5.6-linux-x86_64

chmod go-w ~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml

./filebeat test config -c ~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml

./filebeat test output -c ~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml
```

## Diapositive 112

**Démarrer Filebeat : les monuments arrivent**

Dans le terminal :

- dans le terminal de Filebeat, celui des tests
- démarrer Filebeat : il lit merimee.csv et envoie chaque ligne à Logstash ; -e : son journal s'affiche ici

```bash
cd ~/elastic/filebeat-9.5.6-linux-x86_64

./filebeat -e -c ~/projets/formation-elasticsearch/patrimoine/filebeat/filebeat.yml
```

## Diapositive 114

**46 761 monuments en 91 secondes**

Dans la console de Kibana :

- combien de monuments dans l'index ? on attend 46 761
- combien de fiches ont une erreur de nettoyage ? on attend 0
- combien de lignes Logstash n'a pas su découper ? on attend 0

```text
GET /monuments/_count

GET /monuments/_count?q=erreur_ingestion:*

GET /monuments/_count?q=tags:_csvparsefailure
```

## Diapositive 115

**Carcassonne, arrivée par Filebeat et Logstash**

Dans la console de Kibana :

- relire une fiche connue, Carcassonne, par sa référence

```text
GET /monuments/_doc/PA00102588
```

## Diapositive 118

**L'API Search lite : chercher dans l'adresse**

Dans la console de Kibana :

- chercher « Viollet-le-Duc » dans l'adresse même : 3 résultats, titre et commune seulement

```text
GET /monuments/_search?q=Viollet-le-Duc&size=3&_source=titre,commune
```

## Diapositive 119

**L'API Search lite : champs, opérateurs, erreurs**

Dans la console de Kibana :

- compter les châteaux de Bretagne : deux conditions reliées par AND (%20 : un espace)
- chercher « cistercienne » dans le seul champ historique : 2 résultats
- une parenthèse jamais fermée : l'erreur que renvoie une recherche mal écrite

```text
GET /monuments/_count?q=region:Bretagne%20AND%20denomination:château

GET /monuments/_search?q=historique:cistercienne&size=2&_source=titre,commune,siecle

GET /monuments/_search?q=region:(Bretagne
```

## Diapositive 127

**Le mapping deviné : ce qu'Elasticsearch a choisi**

Dans la console de Kibana :

- le type qu'Elasticsearch a deviné pour quatre champs, à l'arrivée des fiches

```text
GET /monuments/_mapping/field/localisation,departement_code,siecle,mise_a_jour
```

## Diapositive 128

**Piège : le premier document décide du type**

Dans la console de Kibana :

- un premier document : le code 75, écrit comme un nombre
- un second document : le code « 2A »
- le type que le premier document a fixé pour le champ

```text
PUT /essai-departements/_doc/1
{"departement_code": 75}

PUT /essai-departements/_doc/2
{"departement_code": "2A"}

GET /essai-departements/_mapping
```

## Diapositive 129

**Corriger le type sur l'index en place ? Refusé**

Dans la console de Kibana :

- changer le type du champ, sur l'index qui existe déjà

```text
PUT /essai-departements/_mapping
{"properties": {"departement_code": {"type": "keyword"}}}
```

## Diapositive 130

**La solution au piège du « 2A » : le type écrit avant le premier document**

Dans la console de Kibana : les quatre requêtes, l'une après l'autre :

- créer l'index avec le type keyword, avant tout document
- le même 75 qu'au piège
- puis « 2A » ; ?refresh=true : cherchable tout de suite
- chercher la valeur exacte « 2A »

```text
PUT /essai-departements-v2
{"mappings": {"properties": {"departement_code": {"type": "keyword"}}}}

PUT /essai-departements-v2/_doc/1
{"departement_code": 75}

PUT /essai-departements-v2/_doc/2?refresh=true
{"departement_code": "2A"}

GET /essai-departements-v2/_search
{"query": {"term": {"departement_code": "2A"}}}
```

## Diapositive 131

**Piège : ni carte ni facettes**

Dans la console de Kibana :

- les monuments à moins de 2 km d'un point de Carcassonne
- compter les monuments par région (une facette)

```text
GET /monuments/_search
{
  "query": {
    "geo_distance": {"distance": "2km", "localisation": "43.2064,2.3655"}
  }
}

GET /monuments/_search
{
  "size": 0,
  "aggs": {"regions": {"terms": {"field": "region"}}}
}
```

## Diapositive 132

**Avec le sous-champ keyword, la facette marche**

Dans la console de Kibana :

- la même facette, sur le sous-champ exact region.keyword : les 5 premières régions

```text
GET /monuments/_search
{
  "size": 0,
  "aggs": {
    "regions": {"terms": {"field": "region.keyword", "size": 5}}
  }
}
```

## Diapositive 136

**Démonstration : avec object, la recherche se trompe**

Dans la console de Kibana :

- un livre et ses deux éditions, rangées comme de simples objets
- chercher une édition Gallimard de 1943, qui n'existe pas

```text
PUT /livres-editions/_doc/1?refresh=true
{
  "titre": "Le Petit Prince",
  "editions": [
    {"editeur": "Reynal & Hitchcock", "annee": 1943},
    {"editeur": "Gallimard", "annee": 1946}
  ]
}

GET /livres-editions/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"editions.editeur": "Gallimard"}},
        {"match": {"editions.annee": 1943}}
      ]
    }
  }
}
```

## Diapositive 137

**Démonstration : avec nested, l'index et le livre**

Dans la console de Kibana :

- créer l'index : editions déclaré nested, chaque édition gardée avec son éditeur et son année
- le même livre et ses deux éditions ; ?refresh=true : cherchable tout de suite

```text
PUT /livres-editions-n
{
  "mappings": {
    "properties": {
      "titre": {"type": "text"},
      "editions": {"type": "nested", "properties": {"editeur": {"type": "keyword"}, "annee": {"type": "integer"}}}
    }
  }
}

PUT /livres-editions-n/_doc/1?refresh=true
{
  "titre": "Le Petit Prince",
  "editions": [{"editeur": "Reynal & Hitchcock", "annee": 1943}, {"editeur": "Gallimard", "annee": 1946}]
}
```

## Diapositive 138

**Démonstration : avec nested, la recherche est juste**

Dans la console de Kibana :

- Gallimard en 1943, dans une même édition : la requête nested cherche édition par édition
- Gallimard en 1946 : cette édition existe

```text
GET /livres-editions-n/_search
{
  "query": {
    "nested": {
      "path": "editions",
      "query": {"bool": {"must": [{"term": {"editions.editeur": "Gallimard"}}, {"term": {"editions.annee": 1943}}]}}
    }
  }
}

GET /livres-editions-n/_search
{
  "query": {
    "nested": {
      "path": "editions",
      "query": {"bool": {"must": [{"term": {"editions.editeur": "Gallimard"}}, {"term": {"editions.annee": 1946}}]}}
    }
  }
}
```

## Diapositive 139

**Démonstration : join, une église et ses objets protégés**

Dans la console de Kibana : l'index, l'église et ses trois objets (le bouton copie tout) :

- un index où un monument et ses objets sont reliés (type join)
- l'église, le parent (monument)
- ses trois objets, chacun rangé sur le même shard que l'église (routing)

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

## Diapositive 140

**Démonstration : chercher par le parent, ou par l'enfant**

Dans la console de Kibana :

- les monuments qui ont au moins un objet
- les objets dont le monument parent a « Vézelay » dans son titre

```text
GET /patrimoine-liens/_search
{
  "query": {
    "has_child": {"type": "objet", "query": {"match_all": {}}}
  }
}

GET /patrimoine-liens/_search
{
  "_source": ["titre", "materiaux"],
  "query": {
    "has_parent": {
      "parent_type": "monument",
      "query": {"match": {"titre": "Vézelay"}}
    }
  }
}
```

## Diapositive 146

**Démonstration : deux analyseurs prédéfinis**

Dans la console de Kibana :

- découper la phrase avec l'analyseur standard
- la même phrase avec l'analyseur french

```text
POST /_analyze
{"analyzer": "standard", "text": "L’abbaye du Mont-Saint-Michel et ses Châteaux"}

POST /_analyze
{"analyzer": "french", "text": "L’abbaye du Mont-Saint-Michel et ses Châteaux"}
```

## Diapositive 147

**Démonstration : une chaîne écrite à la main**

Dans la console de Kibana :

- composer son analyseur : découpage standard, minuscules, accents retirés

```text
POST /_analyze
{"tokenizer": "standard", "filter": ["lowercase", "asciifolding"], "text": "L’abbaye du Mont-Saint-Michel et ses Châteaux"}
```

## Diapositive 156

**L'analyseur de Patrimoine**

Atelier 3, étape 1 : dans la console de Kibana, coller, puis exécuter

```text
PUT /_component_template/patrimoine-analyse
{
  "template": {
    "settings": {
      "analysis": {
        "filter": {
          "elision_fr": {
            "type": "elision",
            "articles_case": true,
            "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
          },
          "mots_vides_fr": {"type": "stop", "stopwords": "_french_"},
          "racine_fr": {"type": "stemmer", "language": "light_french"}
        },
        "analyzer": {
          "francais_patrimoine": {"tokenizer": "standard", "filter": ["elision_fr", "lowercase", "mots_vides_fr", "racine_fr", "asciifolding"]},
          "francais_simple": {"tokenizer": "standard", "filter": ["elision_fr", "lowercase", "asciifolding"]}
        }
      }
    }
  },
  "_meta": {"description": "Patrimoine : les deux analyseurs français, communs à tous les index"}
}
```

## Diapositive 157

**Le pipeline des protections**

Atelier 3, étape 2 : dans la console de Kibana, coller, puis exécuter

```text
PUT /_ingest/pipeline/monuments-protections
{
  "description": "Patrimoine : l'historique des protections découpé en objets { date, type }",
  "processors": [
    {
      "gsub": {
        "field": "historique_protection",
        "pattern": "\\u00a0",
        "replacement": " ",
        "ignore_missing": true,
        "description": "espaces insécables remplacées par des espaces"
      }
    },
    {
      "script": {
        "lang": "painless",
        "source": "String h = ctx.historique_protection;\nif (h != null) {\n  List liste = new ArrayList();\n  for (String p : h.splitOnToken(' ; ')) {\n    int i = p.indexOf(' : ');\n    if (i > 0) {\n      liste.add(['date': p.substring(0, i).trim(), 'type': p.substring(i + 3).trim()]);\n    }\n  }\n  ctx.protections = liste;\n}",
        "description": "« 1862 : classé MH ; 1926/12/22 : inscrit MH » en liste d'objets"
      }
    }
  ]
}
```

## Diapositive 158

**Le template d'index des monuments**

Atelier 3, étape 3 : dans la console de Kibana, coller, puis exécuter

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
        "historique": {"type": "text", "analyzer": "francais_patrimoine"},
        "statut": {"type": "keyword"},
        "localisation": {"type": "geo_point"},
        "objets": {"type": "keyword"},
        "mise_a_jour": {"type": "date"},
        "erreur_ingestion": {"type": "keyword"}
      }
    }
  },
  "_meta": {
    "description": "Patrimoine : réglages et mapping des index de monuments"
  }
}
```

## Diapositive 159

**Simuler le template avant de créer l'index**

Atelier 3, étape 4 : dans la console de Kibana, coller, puis exécuter

```text
POST /_index_template/_simulate_index/monuments-v1
```

## Diapositive 160

**Correction : créer l'index, recopier les monuments**

Dans la console de Kibana :

- créer monuments-v1 : le template s'applique tout seul
- y recopier les 46 761 monuments, et attendre la fin
- compter : on attend 46 761

```text
PUT /monuments-v1

POST /_reindex?wait_for_completion=true&refresh=true
{
  "source": {"index": "monuments"},
  "dest": {"index": "monuments-v1"}
}

GET /monuments-v1/_count
```

## Diapositive 161

**Correction : les deux analyseurs à l'essai**

Dans la console de Kibana :

- notre analyseur francais_patrimoine sur une phrase
- notre analyseur francais_simple sur la même phrase

```text
POST /monuments-v1/_analyze
{"analyzer": "francais_patrimoine", "text": "L’abbaye et les Châteaux de la Loire"}

POST /monuments-v1/_analyze
{"analyzer": "francais_simple", "text": "L’abbaye et les Châteaux de la Loire"}
```

## Diapositive 163

**Correction : l'alias, en une seule opération**

Dans la console de Kibana :

- supprimer l'ancien index monuments et donner son nom, comme alias, à monuments-v1, en une seule requête
- vers quel index pointe l'alias monuments ?
- compter par l'alias : les monuments de monuments-v1

```text
POST /_aliases
{
  "actions": [
    {"remove_index": {"index": "monuments"}},
    {"add": {"index": "monuments-v1", "alias": "monuments"}}
  ]
}

GET /_cat/aliases/monuments?v

GET /monuments/_count
```

## Diapositive 164

**Correction : la carte et les facettes marchent**

Dans la console de Kibana :

- la même recherche à 2 km de Carcassonne : localisation est maintenant un point GPS
- la même facette par région : region est maintenant un keyword

```text
GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "commune"],
  "query": {
    "geo_distance": {"distance": "2km", "localisation": "43.2064,2.3655"}
  }
}

GET /monuments/_search
{
  "size": 0,
  "aggs": {"regions": {"terms": {"field": "region", "size": 5}}}
}
```

## Diapositive 165

**Si vous avez fini : nested, et les dates mal écrites**

Dans la console de Kibana :

- les monuments classés MH avant 1900 : date et type dans la même protection (nested)
- combien de fiches ont un champ écarté (_ignored), une date mal écrite par exemple ?
- trois de ces fiches, avec le nom du champ écarté

```text
GET /monuments/_count
{
  "query": {
    "nested": {
      "path": "protections",
      "query": {"bool": {"filter": [{"term": {"protections.type": "classé MH"}}, {"range": {"protections.date": {"lt": "1900"}}}]}}
    }
  }
}

GET /monuments/_count
{"query": {"exists": {"field": "_ignored"}}}

GET /monuments/_search
{
  "size": 3,
  "_source": ["titre", "historique_protection"],
  "fields": ["_ignored"],
  "query": {"exists": {"field": "_ignored"}}
}
```

## Diapositive 166

**La configuration d'un index : ce qui se change à chaud**

Dans la console de Kibana :

- lire quatre réglages de l'index
- changer à chaud les répliques et le rafraîchissement

```text
GET /monuments-v1/_settings?filter_path=*.settings.index.number_of_shards,*.settings.index.number_of_replicas,*.settings.index.refresh_interval,*.settings.index.final_pipeline

PUT /monuments-v1/_settings
{"index": {"number_of_replicas": 0, "refresh_interval": "30s"}}
```

## Diapositive 167

**La configuration d'un index : ce qui est figé**

Dans la console de Kibana :

- changer le nombre de shards d'un index qui existe

```text
PUT /monuments-v1/_settings
{"index": {"number_of_shards": 2}}
```

## Diapositive 168

**Recharger sans coupure : la version 2, puis la bascule**

Dans la console de Kibana :

- créer monuments-v2 : le template s'applique tout seul
- y recopier les monuments de monuments-v1
- basculer l'alias de monuments-v1 à monuments-v2, en une seule requête
- vers quel index pointe l'alias monuments ?

```text
PUT /monuments-v2

POST /_reindex?wait_for_completion=true&refresh=true
{
  "source": {"index": "monuments-v1"},
  "dest": {"index": "monuments-v2"}
}

POST /_aliases
{
  "actions": [
    {
      "remove": {"index": "monuments-v1", "alias": "monuments"}
    },
    {"add": {"index": "monuments-v2", "alias": "monuments"}}
  ]
}

GET /_cat/aliases/monuments?v
```

## Diapositive 169

**Ce que comptent les index**

Dans la console de Kibana :

- la taille et le nombre de fiches de chaque index monuments-v
- le nombre de fiches de monuments-v2

```text
GET /_cat/indices/monuments-v*?v&h=index,health,docs.count,store.size&s=index

GET /_cat/count/monuments-v2?v
```

## Diapositive 177

**Ce soir : récupérer le corrigé avec git**

Dans un terminal, après la session

```text
cd ~/projets/formation-elasticsearch
git clone -b jour-1 https://github.com/adamfrance/formation-elasticsearch.git corrige-jour1
```
