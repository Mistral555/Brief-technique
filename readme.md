# Test Technique – Gestion de Données avec Python, Pandas et SQLite

Ce projet a été réalisé dans le cadre d’un entretien technique. Il consiste à importer, traiter et stocker des données issues de fichiers CSV hébergés sur Google Sheets, puis à les insérer dans une base de données SQLite à l’aide de Python et Pandas.

## Fonctionnalités principales

- **Importation de données** :
  - Téléchargement de trois fichiers CSV (produits, magasins, ventes) depuis des URLs publiques Google Sheets.
  - Nettoyage et renommage des colonnes pour correspondre au schéma de la base de données.

- **Traitement des données** :
  - Génération d’une clé primaire unique pour la table `ventes` en concaténant plusieurs champs, afin d’éviter les doublons.

- **Création de la base de données** :
  - Création des tables `produits`, `magasins`, `ventes` et `resultats` dans une base SQLite.
  - Définition des clés primaires et des relations entre les tables.

- **Insertion des données** :
  - Insertion des données dans les tables `produits` et `magasins` via Pandas.
  - Insertion contrôlée dans la table `ventes` pour éviter les doublons.

## Structure du projet

```
docker-compose.yml
script/
    Dockerfile
    requirements.txt
    script.py
```

- `script.py` : Script principal contenant l’ensemble du traitement.
- `requirements.txt` : Dépendances Python nécessaires (pandas, requests, etc.).
- `Dockerfile` : Pour l’exécution du script dans un conteneur Docker.
- `docker-compose.yml` : (optionnel) Pour l’orchestration via Docker Compose.

## Lancement du projet

1. **Installer les dépendances** :
   ```bash
   pip install -r script/requirements.txt
   ```

2. **Exécuter le script** :
   ```bash
   python script/script.py
   ```

3. **(Optionnel) Utiliser Docker** :
   ```bash
   docker build -t test-technique ./script
   docker run --rm -v ${PWD}/data:/data test-technique
   ```

## Points à discuter

- Le choix de la clé primaire pour la table `ventes` (concaténation des champs) a été fait pour éviter les doublons sans gestion d’auto-incrément.
- Le script est facilement réutilisable pour d’autres structures de données similaires.

## Auteur

Zoubir MABED

