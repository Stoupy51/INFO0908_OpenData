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

#########################
# Fonctions générales #
#########################

def fetch_data(query):
    """
    Lance la requête à l'API et retourne les résultats.
    La limite des requêtes est de 100 résultats par requête, il faut donc parfois faire plusieurs requêtes pour récupérer tous les résultats.
    Args:
        query (str): la requête à envoyer à l'API
    Returns:
        list: la liste des résultats
    """
    offset = 0
    results = []
    while True:
        response = requests.get(f"{API_URL}records?{query}&limit=100&offset={offset}").json()
        results += response["results"]
        if len(response["results"]) < 100:
            break
        offset += 100
    return results

# retourne le dataset entier sous forme de json
@app.route('/api/json', methods=['GET'])
def get_all_data():
    data  = requests.get("https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcours-et-reussite-des-bacheliers-en-licence/exports/json?lang=fr&timezone=Europe%2FBerlin").json()
    return jsonify(data)                                                                                                                                      

#########################
# Les listes #
#########################

# Récupérer la liste des différentes grandes disciplines
@app.route('/api/gd_discipline', methods=['GET'])
def get_gd_disciplines():
    data = fetch_data("select=gd_discipline_lib")
    disciplines = [row['gd_discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer la liste des différentes disciplines
@app.route('/api/discipline', methods=['GET'])
def get_disciplines():
    data = fetch_data("select=discipline_lib")
    disciplines = [row['discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer la liste des types de bac
@app.route('/api/types-bac', methods=['GET'])
def get_types_bac():
    data = fetch_data("select=serie_bac_lib")
    types_bac = [row['serie_bac_lib'] for row in data]
    return jsonify(list(set(types_bac)))

# Récupérer la liste des différentes mentions au Bac
@app.route('/api/mentions-bac', methods=['GET'])
def get_mentions_bac():
    data = fetch_data("select=mention_bac_lib")
    mentions = [row['mention_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

#################################
# Répartition des étudiants #
#################################

# récupérer le nb d’hommes et de femmes
@app.route('/api/nb-hommes-femmes/', methods=['GET'], defaults={'groupby': ""})
@app.route('/api/nb-hommes-femmes/<string:groupby>', methods=['GET'])
def get_nb_hommes(groupby):
    """
    Récupère le nombre d'hommes et de femmes. Si groupby n'est pas spécifi, retourne le nombre total d'hommes et de femmes. 
    Sinon, retourne le nombre d'hommes et de femmes regroupé par la colonne groupby.
    Les valeurs supportées pour groupby sont:
    - "gd_discipline"
    - "discipline"
    - "bac"
    - "mention_bac"
    Args:
        groupby (str): la colonne à grouper
    Returns:
        json: le nombre
    """

    assert groupby in ["", "gd_discipline", "discipline", "bac", "mention_bac"], "Valeur incorrecte de group_by"

    if groupby == "":
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
        elif groupby == "gd_discipline":
            groupby = "gd_discipline_lib"
        elif groupby == "discipline":
            groupby = "discipline_lib"

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

# récupérer le nombre d’étudiants par grandes disciplines
@app.route('/api/nb-etudiants-par-gd_discipline', methods=['GET'])
def get_nb_etudiants_par_gd_discipline():
    data = fetch_data("select=gd_discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=gd_discipline_lib")
    result = {row['gd_discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# récupérer le nombre d’étudiants par disciplines
@app.route('/api/nb-etudiants-par-discipline', methods=['GET'])
def get_nb_etudiants_par_discipline():
    data = fetch_data("select=discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=discipline_lib")
    result = {row['discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par type de bac
@app.route('/api/nb-etudiants-par-type-bac', methods=['GET'])
def get_nb_etudiants_par_type_bac():
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par mention au bac
@app.route('/api/nb-etudiants-par-mention-bac', methods=['GET'])
def get_nb_etudiants_par_mention_bac():
    data = fetch_data("select=mention_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

#################################
# Passage en L2 et réorientation #
#################################

# récupérer le nombre d’étudiant passant en L2 en 1 an / en 2 ans / le nombre d’étudiants n’étant pas passer en L2
@app.route('/api/passage-l2-stats', methods=['GET'])
def get_passage_l2_stats():
    data = fetch_data("select=passage_en_l2_1_an,passage_en_l2_2_ans,effectif_neobacheliers_passage")
    result = {
        'passage_en_l2_1_an': int(sum(filter(None,[row['passage_en_l2_1_an'] for row in data]))),
        'passage_en_l2_2_ans': int(sum(filter(None,[row['passage_en_l2_2_ans'] for row in data]))),
        'pas_passe': sum(filter(None,[row['effectif_neobacheliers_passage'] for row in data]))
    }
    result['pas_passe'] = int(result['pas_passe'] - (result['passage_en_l2_1_an'] + result['passage_en_l2_2_ans']))
    return jsonify(result)

# Passage en L2 (1 an, 2 ans, pas passe, taux de passage) par sexe
@app.route('/api/passage-l2-par-sexe', methods=['GET'])
def get_passage_l2_par_sexe():
    data = fetch_data("select=sexe_lib,SUM(passage_en_l2_1_an),SUM(passage_en_l2_2_ans),SUM(effectif_neobacheliers_passage)&group_by=sexe_lib")
    result = {row['sexe_lib']: {
        'passage_en_l2_1_an': int(row['SUM(passage_en_l2_1_an)']),
        'passage_en_l2_2_ans': int(row['SUM(passage_en_l2_2_ans)']),
        'pas_passe': int(row['SUM(effectif_neobacheliers_passage)']) - (int(row['SUM(passage_en_l2_1_an)']) + int(row['SUM(passage_en_l2_2_ans)'])),
        'taux_passage': (int(row['SUM(passage_en_l2_1_an)']) + int(row['SUM(passage_en_l2_2_ans)'])) / int(row['SUM(effectif_neobacheliers_passage)']) * 100
    } for row in data}
    return jsonify(result)

# récupérer le nombre de passage en L2 en fonction du type de bac
@app.route('/api/passage-l2-par-bac', methods=['GET'])
def get_passage_l2_par_bac():
    data = fetch_data("select=serie_bac_lib,SUM(passage_en_l2_1_2_ans)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: row['SUM(passage_en_l2_1_2_ans)'] for row in data}
    return jsonify(result)

# Nombre d’étudiants passant en DUT après 1 an / 2 ans de licence
@app.route('/api/passage-dut', methods=['GET'])
def get_passage_dut():
    data = fetch_data("select=SUM(reorientation_en_dut_1_an),SUM(reorientation_en_dut_2_ans)")
    result = {
        "après 1 an": data[0]['SUM(reorientation_en_dut_1_an)'],
        "après 2 ans": data[0]['SUM(reorientation_en_dut_2_ans)']
    }
    return jsonify(result)

##########################
# Réussite en licence #
##########################

# nombre d’étudiant obtenant la licence en 3 ans / 4 ans / jamais
@app.route('/api/reussite-licence', methods=['GET'])
def get_reussite_licence():
    data = fetch_data("select=reussite_3_ans,reussite_4_ans,effectif_neobacheliers_reussite")
    result = {
        'en 3 ans': int(sum(filter(None,[row['reussite_3_ans'] for row in data]))),
        'en 4 ans': int(sum(filter(None,[row['reussite_4_ans'] for row in data]))),
        'pas_reussi': sum(filter(None,[row['effectif_neobacheliers_reussite'] for row in data]))
    }
    result['pas_reussi'] = int(result['pas_reussi'] - (result['en 3 ans'] + result['en 4 ans']))
    return jsonify(result)

# Calculer le taux de réussite en licence par grandes disciplines
@app.route('/api/taux-reussite-par-gd_discipline', methods=['GET'])
def get_taux_reussite_par_gd_discipline():
    data = fetch_data("select=gd_discipline_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=gd_discipline_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['gd_discipline_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par discipline
@app.route('/api/taux-reussite-par-discipline', methods=['GET'])
def get_taux_reussite_par_discipline():
    data = fetch_data("select=discipline_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=discipline_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['discipline_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par mention au bac
@app.route('/api/taux-reussite-par-mention-bac', methods=['GET'])
def get_taux_reussite_par_mention_bac():
    data = fetch_data("select=mention_bac_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=mention_bac_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)'] 
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['mention_bac_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par type de bac
@app.route('/api/taux-reussite-par-type-bac', methods=['GET'])
def get_taux_reussite_par_type_bac():
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=serie_bac_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['serie_bac_lib']] = round(taux,2)
    return jsonify(result)

##########################
# Redoublement #
##########################

# Récupérer le nombre d’étudiants ayant redoublé par grandes discipline
@app.route('/api/redoublement-par-gd_discipline', methods=['GET'])
def get_redoublement_par_gd_discipline():
    data = fetch_data("select=gd_discipline_lib,SUM(redoublement_en_l1)&group_by=gd_discipline_lib")
    result = {row['gd_discipline_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par discipline
@app.route('/api/redoublement-par-discipline', methods=['GET'])
def get_redoublement_par_discipline():
    data = fetch_data("select=discipline_lib,SUM(redoublement_en_l1)&group_by=discipline_lib")
    result = {row['discipline_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par type de bac
@app.route('/api/redoublement-par-type-bac', methods=['GET'])
def get_redoublement_par_type_bac():
    data = fetch_data("select=serie_bac_lib,SUM(redoublement_en_l1)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par mention au bac
@app.route('/api/redoublement-par-mention-bac', methods=['GET'])
def get_redoublement_par_mention_bac():
    data = fetch_data("select=mention_bac_lib,SUM(redoublement_en_l1)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)


