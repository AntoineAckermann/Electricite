# Electricite
Plusieurs scripts sur l'électricité (France) : prix, génération, modélisation, prédiction de la consommation, ... En fonction de mes intérêts du moment.
J'ajoute les scripts au fur et à mesure de mon travail.

* get_data.py : obtenir un fichier CSV (ou pkl) des données de production horaire par source (source RTE) et de prix horaires (source ENTSOE) pour la maille France depuis 2012.

* get_data_weather.py : obtenir les données horaires de température par département (utile pour la prédiction).
  
* marginal_price.py : obtenir le prix de l'électricité étant donnés les _bids_ des producteurs et la demande (intersection des deux courbes).

* prediction.py : script de base permettant de tester différentes approches pour la prédiction de la consommation.
