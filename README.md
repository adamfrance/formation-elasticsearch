# Elasticsearch : indexation de contenu

Formation de deux jours, jeudi 5 et vendredi 6 novembre 2026, sur Elasticsearch 9.5.6. Fil rouge : **Patrimoine**, le
moteur de recherche des monuments historiques de France, construit sur les données ouvertes du ministère de la Culture
(Plateforme ouverte du patrimoine, POP).

Ce dépôt reçoit, chaque soir, le support du jour et la correction du fil rouge.

| Branche | Ce qu'elle contient | Quand |
|---|---|---|
| `main` | ce fichier et les démonstrations (`demos/`, à coller dans la console de Kibana) | dès le début |
| `supports` | les diapositives de chaque journée (HTML, avec toutes les commandes et leurs résultats) | le soir |
| `jour-1`, `jour-2` | le dossier `patrimoine/` tel qu'il est à la fin de la journée, et les corrections | le soir |

## Récupérer le support et la correction, le soir

```bash
cd ~/projets/formation-elasticsearch
git clone -b supports https://github.com/adamfrance/formation-elasticsearch.git supports
git clone -b jour-1 https://github.com/adamfrance/formation-elasticsearch.git corrige-jour1
```

Ouvrir `supports/formation-elasticsearch-jour1-diapos.html` dans le navigateur : les flèches du clavier changent de
diapositive, le bouton « Copier » copie chaque commande ; en ajoutant `?document` à la fin de l'adresse, toutes les
diapositives s'affichent l'une sous l'autre, pour lire ou imprimer.

## Repartir au même point, le matin du jour 2

Si un atelier du jour 1 n'a pas abouti, le script de reprise remet tout en place (pipelines, templates, les 46 761
monuments, l'alias `monuments`) ; Elasticsearch doit tourner :

```bash
export ELASTIC_PASSWORD='votre mot de passe'
bash ~/projets/formation-elasticsearch/corrige-jour1/patrimoine/reprise/reprise-jour2.sh
```

## Les données

- Monuments (Mérimée), objets (Palissy) : ministère de la Culture, POP, Licence Ouverte ;
  [pop.culture.gouv.fr](https://www.pop.culture.gouv.fr/).
- Photos des monuments : Wikimedia Commons, licences CC BY-SA ; l'auteur et la licence de chaque photo sont dans
  `patrimoine/photos/credits.txt`.
