import re
from flask import Flask, request, jsonify
import requests
import pandas as pd
import json

# Liste des variables:
# gd_discipline
# gd_discipline_lib
# discipline
# discipline_lib
# sect_disciplinaire
# sect_disciplinaire_lib
# serie_bac
# serie_bac_lib
# age_au_bac
# age_au_bac_lib
# sexe
# sexe_lib
# mention_bac
# mention_bac_lib
# cohorte_passage
# effectif_neobacheliers_passage
# passage_en_l2_1_an
# redoublement_en_l1
# passage_en_l2_2_ans
# passage_en_l2_1_2_ans
# reorientation_en_dut_1_an
# reorientation_en_dut_2_ans
# reorientation_en_dut
# cohorte_reussite"
# effectif_neobacheliers_reussite
# reussite_3_ans
# reussite_4_ans
# reussite_3_4_ans



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

# Fonction utilitaire pour récupérer les données avec pagination
def fetch_data(query):
    offset = 0
    results = []
    while True:
        response = requests.get(f"{API_URL}records?{query}&limit=100&offset={offset}").json()
        results += response["results"]
        if len(response["results"]) < 100:
            break
        offset += 100
    return results

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
        # while repetition:
        #     req_h = requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D1&limit=100&offset=" + str(offset)).json()
        #     data_h += req_h["results"]
        #     req_f = requests.get(API_URL + "records?select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D2&limit=100&offset=" + str(offset)).json()
        #     data_f += req_f["results"]
        #     if len(req_h["results"]) < 100 and len(req_f["results"]) < 100: # on a atteint la fin
        #         repetition = False
        #     offset += 100
        data_h = fetch_data("select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D1")
        data_f = fetch_data("select=effectif_neobacheliers_passage%2C%20effectif_neobacheliers_reussite&where=sexe%3D2")
            
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

        # repetition = True
        # offset=0
        # while repetition:
        #     req_h = requests.get(API_URL + "records?select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D1&group_by="+groupby+"&limit=100&offset=" + str(offset)).json()
        #     data_h += req_h["results"]
        #     req_f = requests.get(API_URL + "records?select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D2&group_by="+groupby+"&limit=100&offset=" + str(offset)).json()
        #     data_f += req_f["results"]
        #     if len(req_h["results"]) < 100 and len(req_f["results"]) < 100: # on a atteint la fin
        #         repetition = False
        #     offset += 100
        data_h = fetch_data("select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D1&group_by="+groupby)
        data_f = fetch_data("select=SUM(effectif_neobacheliers_passage)%2C%20SUM(effectif_neobacheliers_reussite)%2C%20"+groupby + "&where=sexe%3D2&group_by="+groupby)
        
        var = [ligne[groupby] for ligne in data_h]
        var += [ligne[groupby] for ligne in data_f]
        var = list(set(var))
        resultat = {d:{"hommes":0,"femmes":0} for d in var}
        for ligne in data_h:
            resultat[ligne[groupby]]["hommes"] = int(sum(filter(None,[ligne["SUM(effectif_neobacheliers_passage)"],ligne["SUM(effectif_neobacheliers_reussite)"]])))
        for ligne in data_f:
            resultat[ligne[groupby]]["femmes"] = int(sum(filter(None,[ligne["SUM(effectif_neobacheliers_passage)"],ligne["SUM(effectif_neobacheliers_reussite)"]])))

    return jsonify(resultat)


# récupérer la liste des différentes disciplines / grandes disciplines 

# récupérer le nombre d’étudiants par disciplines / grandes disciplines

# récupérer les d’étudiants par discipline et si ils ont réussi la licence -> calculer le taux de réussite en licence par discipline

# récupérer le nombre d’étudiants ayant redoublé par discipline

# récupérer la liste des différentes mentions au Bac

# récupérer le nombre d’étudiants par mention au bac

# récupérer pour chaque étudiant la mention au bac et s’il a réussi la licence 

# récupérer le nombre de passage en L2 en fonction du type de bac

# récupérer le nombre d’étudiant passant en L2 en 1 an / en 2 ans / le nombre d’étudiants n’étant pas passer en L2

# nombre d’étudiant obtenant la licence en 3 ans / 4 ans / jamais

# nombre étudiants passant en DUT après 1 an / après 2 ans de licence



if __name__ == '__main__':
    app.run(debug=True)


