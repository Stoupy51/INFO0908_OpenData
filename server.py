import re
from flask import Flask, request, jsonify
import requests
import pandas as pd
import json


app = Flask(__name__)

# API URL: http://
API_URL = "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcours-et-reussite-des-bacheliers-en-licence/"

NB_ITEMS = requests.get(API_URL + "records").json()['total_count']
print(NB_ITEMS)

@app.route('/api/all-data', methods=['GET'])
def get_all_data():
    data  = requests.get(API_URL + "records?where=sexe%3D1").json()
    NB_ITEMS = data['total_count']
    return jsonify(data)

# récupérer le nb d’hommes
@app.route('/api/nb-hommes-femmes', methods=['GET'])
def get_nb_hommes(groupby = ""): # total # discipline # bac # mention bac
    data_h = []
    data_f = []

    for i in range(0, NB_ITEMS, 100):
        req = json.loads(requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D1&limit=100&offset=" + str(i)).json())
        data_h += req["results"]
        req = json.loads(requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D2&limit=100&offset=" + str(i)).json())
        data_f += req["results"]

    if groupby == "":
        somme_h = [ligne["effectif_neobacheliers_passage"] + ligne["effectif_neobacheliers_reussite"] for ligne in data_h]
        somme_h = sum(somme_h)
        somme_f = [ligne["effectif_neobacheliers_passage"] + ligne["effectif_neobacheliers_reussite"] for ligne in data_f]
        somme_f = sum(somme_f)
        resultat = {"total_h":somme_h, "total_f":somme_f}
    print(f"Affichage du nombre d'hommes et de femmes")
    print(len(data_h),len(data_f), (len(data_h)+len(data_f)))
    return jsonify(resultat)


# récupérer la liste des différentes disciplines / grandes disciplines 
@app.route('/api/disciplines', methods=['GET'])
def get_disciplines():
    data = requests.get(API_URL + "records?select=discipline").json()
    # compter le nombre de disciplines distinctes
    # nbDisciplines = 
    return jsonify(data)


# récupérer le nombre d’étudiants par disciplines / grandes disciplines
@app.route('/api/nb-etudiants-disciplines', methods=['GET'])
def get_nb_etudiants_disciplines():
    data = requests.get(API_URL + "records?select=discipline").json()
    return jsonify(data)


# récupérer la liste des différentes mentions au Bac
@app.route('/api/mentions-bac', methods=['GET'])
def get_mentions_bac():
    data = requests.get(API_URL + "records?select=mention_bac").json()
    return jsonify(data)


# récupérer le nombre d’étudiants par mention au bac
@app.route('/api/nb-etudiants-mention-bac', methods=['GET'])
def get_nb_etudiants_mention_bac():
    data = requests.get(API_URL + "records?select=mention_bac").json()
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)


