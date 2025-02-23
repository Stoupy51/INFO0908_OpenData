
# 🎓 INFO0908_OpenData

Basé sur une API, Parcours et réussite des bachelières et bacheliers inscrits pour la première fois en licence.<br>
L'API sur laquelle le projet est basé est disponible à l'adresse suivante : https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcours-et-reussite-des-bacheliers-en-licence/table/?sort=redoublement_en_l1<br>
Je vous conseille de regarder à quoi ressemble les données grâce à ce lien ou avec notre documentation.

## 🛠️ Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Stoupy51/INFO0908_OpenData
   cd INFO0908_OpenData
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

# 📚 Utilisation

Pour démarrer le serveur, exécutez le fichier `server.py` :<br>
`python server.py`<br>
Le serveur sera accessible à l'adresse `http://localhost:5000/`.

# 📂 Structure du projet
```bash
INFO0908_OpenData/
├── docs/              # Documentation générée
├── models/            # Modèles de ML entraînés
├── src/               # Code source
│   ├── ml/            # Scripts de machine learning
│   └── ...            # Autres modules
├── server.py          # Point d'entrée du serveur
└── requirements.txt   # Dépendances Python
```

# 🔌 API / Documentation

Veuillez lire la [documentation](docs/build/html/index.html) pour plus de détails sur les endpoints disponibles.

