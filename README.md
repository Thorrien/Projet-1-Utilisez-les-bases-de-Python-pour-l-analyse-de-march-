# Utilisez les bases de Python pour l'analyse de marché

Version bêta d'un script pour suivre les prix des livres chez [Books to Scrape](https://books.toscrape.com/), un revendeur de livres en ligne.

## Table des Matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Auteur](#auteur)

## Installation

Pour installer les dépendances de ce projet, assurez-vous d'avoir [Python](https://www.python.org/) installé. Ensuite, exécutez la commande suivante dans le répertoire racine de votre projet :
```
pip install -r requirements.txt
```


## Utilisation

Une fois les dépendances installées, exécutez le script main.py à l'aide de la commande suivante :
```
python main.py
```

** Attention, le temps de traitement peut être long en fonction du contenu du site internet, les derniers tests montrent un temps de traitement de : 05 minutes et 05 secondes environ. **

## Résultat

Les données récupérées seront enregistrées dans le dossier Données et les sous dossier portant le nom de chaque catégorie. Dans ces dossiers vous trouverez : 
- Les csv des données
- les images de chaque livre ayant comme nom l'UPC


## Auteur

BARILLER Eric