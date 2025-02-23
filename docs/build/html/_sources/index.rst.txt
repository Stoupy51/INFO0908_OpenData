
🎓 INFO0908_OpenData
====================
Basé sur une API, Parcours et réussite des bachelières et bacheliers inscrits pour la première fois en licence.

L'API sur laquelle le projet est basé est disponible à l'adresse suivante : https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcours-et-reussite-des-bacheliers-en-licence/table/?sort=redoublement_en_l1

Je vous conseille de regarder à quoi ressemble les données grâce à ce lien ou avec notre [documentation](https://stoupy51.github.io/INFO0908_OpenData/index.html).

📚 Overview
-----------
Pour démarrer le serveur, exécutez le fichier `server.py` :

`python server.py`

Le serveur sera accessible à l'adresse `http://localhost:5000/`.

🚀 Project Structure
-------------------
.. code-block:: bash

   INFO0908_OpenData/
   ├── docs/              # Documentation générée
   ├── models/            # Modèles de ML entraînés
   ├── src/               # Code source
   │   ├── ml/            # Scripts de machine learning
   │   └── ...            # Autres modules
   ├── server.py          # Point d'entrée du serveur
   └── requirements.txt   # Dépendances Python

📖 Module Documentation
----------------------
.. toctree::
   :maxdepth: 10
   :caption: Contents:

   modules/src


⚡ Indices and Tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
