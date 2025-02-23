
# Imports
import requests
import stouputils as stp
import os
from typing import Literal, Any
from flask import Flask, request, jsonify


# Constants
ROOT: str = stp.clean_path(os.path.dirname(os.path.abspath(__file__)))
API_URL: str = "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcours-et-reussite-des-bacheliers-en-licence"


# Flask app
app: Flask = Flask(__name__)


# Fonction pour récupérer les données de l'API
def fetch_data(query: str) -> list[dict]:
    """ Lance la requête à l'API et retourne les résultats.
    La limite des requêtes est de 100 résultats par requête, il faut donc parfois faire plusieurs requêtes pour récupérer tous les résultats.

    Args:
        query (str): la requête à envoyer à l'API
    Returns:
        list: la liste des résultats
    """
    offset = 0
    results = []
    while True:
        response = requests.get(f"{API_URL}/records?{query}&limit=100&offset={offset}").json()
        results += response["results"]
        if len(response["results"]) < 100:
            break
        offset += 100
    return results

