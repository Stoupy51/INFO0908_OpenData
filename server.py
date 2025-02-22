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

# retourne le dataset entier sous forme de json
@app.route('/api/json', methods=['GET'])
def get_all_data():
    data  = requests.get("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcours-et-reussite-des-bacheliers-en-licence/exports/json?lang=fr&timezone=Europe%2FBerlin").json()
    return jsonify(data)

# récupérer le nb d’hommes et de femmes
@app.route('/api/nb-hommes-femmes/', methods=['GET'], defaults={'groupby': ""})
@app.route('/api/nb-hommes-femmes/<string:groupby>', methods=['GET'])
def get_nb_hommes(groupby):
    data_h = []
    data_f = []
    assert groupby in ["","gd_discipline", "bac", "mention_bac"], "Valeur incorrecte de group_by"

    if groupby == "":
        offset=0
        repetition = True
        while repetition:
            req_h = requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D1&limit=100&offset=" + str(offset)).json()
            data_h += req_h["results"]
            req_f = requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D2&limit=100&offset=" + str(offset)).json()
            data_f += req_f["results"]
            if len(req_h["results"]) < 100 and len(req_f["results"]) < 100: # on a atteint la fin
                repetition = False
            offset += 100
            
        somme_h = [sum(filter(None,[ligne["effectif_neobacheliers_passage"],ligne["effectif_neobacheliers_reussite"]])) for ligne in data_h]
        somme_h = sum(somme_h)
        somme_f = [sum(filter(None,[ligne["effectif_neobacheliers_passage"],ligne["effectif_neobacheliers_reussite"]])) for ligne in data_f]
        somme_f = sum(somme_f)
        resultat = {"hommes":int(somme_h), "femmes":int(somme_f)}
    else:
        if groupby == "bac":
            groupby = "serie_bac_lib"
        elif groupby == "mention_bac":
            groupby = "mention_bac_lib"

        repetition = True
        offset=0
        while repetition:
            req_h = requests.get(API_URL + "records?select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D1&group_by="+groupby+"&limit=100&offset=" + str(offset)).json()
            data_h += req_h["results"]
            req_f = requests.get(API_URL + "records?select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D2&group_by="+groupby+"&limit=100&offset=" + str(offset)).json()
            data_f += req_f["results"]
            if len(req_h["results"]) < 100 and len(req_f["results"]) < 100: # on a atteint la fin
                repetition = False
            offset += 100
        
        var = [ligne[groupby] for ligne in data_h]
        var += [ligne[groupby] for ligne in data_f]
        var = list(set(var))
        resultat = {d:{"hommes":0,"femmes":0} for d in var}
        for ligne in data_h:
            resultat[ligne[groupby]]["hommes"] = int(sum(filter(None,[ligne["SUM(effectif_neobacheliers_passage)"],ligne["SUM(effectif_neobacheliers_reussite)"]])))
        for ligne in data_f:
            resultat[ligne[groupby]]["femmes"] = int(sum(filter(None,[ligne["SUM(effectif_neobacheliers_passage)"],ligne["SUM(effectif_neobacheliers_reussite)"]])))

    return jsonify(resultat)


if __name__ == '__main__':
    app.run(debug=True)


