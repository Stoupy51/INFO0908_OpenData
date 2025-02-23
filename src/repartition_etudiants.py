
# Imports
from .shared_import import *

# récupérer le nb d’hommes et de femmes
@app.route('/api/nb_hommes_femmes', methods=['GET'], defaults={'groupby': ""})
@app.route('/api/nb_hommes_femmes/<string:groupby>', methods=['GET'])
def get_nb_hommes(groupby: str) -> dict:
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
        json: le nombre d'hommes et de femmes
    Examples:
        >>> requests.get(f"{OUR_API}/api/nb_hommes_femmes").json()
        {'femmes': 181739, 'hommes': 125868}
        >>> requests.get(f"{OUR_API}/api/nb_hommes_femmes/gd_discipline").json()
        {'Droit, gestion, économie, AES': {'femmes': 62742, 'hommes': 43048}, 'Lettres, langues et sciences humaines': {'femmes': 90630, 'hommes': 35942}, 'STAPS': {'femmes': 6806, 'hommes': 19274}, 'Santé': {'femmes': 30, 'hommes': 24}, "Sciences et sciences de l'ingénieur": {'femmes': 21531, 'hommes': 27580}}
        >>> requests.get(f"{OUR_API}/api/nb_hommes_femmes/discipline").json()["Administration économique et sociale"]
        {'femmes': 8912, 'hommes': 6350}
        >>> requests.get(f"{OUR_API}/api/nb_hommes_femmes/bac").json()
        {'BAC ES': {'femmes': 56000, 'hommes': 36196}, 'BAC L': {'femmes': 46807, 'hommes': 12717}, 'BAC S': {'femmes': 37515, 'hommes': 42679}, 'BAC STMG': {'femmes': 14661, 'hommes': 13013}, 'BAC professionnel': {'femmes': 15950, 'hommes': 13511}, 'BAC technologique hors STMG': {'femmes': 10806, 'hommes': 7752}}
        >>> requests.get(f"{OUR_API}/api/nb_hommes_femmes/mention_bac").json()
        {'Assez bien': {'femmes': 50947, 'hommes': 31443}, 'Bien': {'femmes': 23755, 'hommes': 11253}, 'Inconnue': {'femmes': 5878, 'hommes': 4218}, 'Passable deuxième groupe': {'femmes': 24558, 'hommes': 22183}, 'Passable premier groupe': {'femmes': 68352, 'hommes': 53543}, 'Très bien': {'femmes': 8249, 'hommes': 3228}}
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
@app.route('/api/nb_etudiants/gd_discipline', methods=['GET'])
def get_nb_etudiants_par_gd_discipline() -> dict:
    """ Récupère le nombre d'étudiants par grandes disciplines

    Returns:
        dict: le nombre d'étudiants par grandes disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/nb_etudiants/gd_discipline").json()
        {'Droit, gestion, économie, AES': 105790, 'Lettres, langues et sciences humaines': 126572, 'STAPS': 26080, 'Santé': 54, "Sciences et sciences de l'ingénieur": 49111}
    """
    data = fetch_data("select=gd_discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=gd_discipline_lib")
    result = {row['gd_discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# récupérer le nombre d’étudiants par disciplines
@app.route('/api/nb_etudiants/discipline', methods=['GET'])
def get_nb_etudiants_par_discipline() -> dict:
    """ Récupère le nombre d'étudiants par disciplines

    Returns:
        dict: le nombre d'étudiants par disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/nb_etudiants/discipline").json()
        {'Administration économique et sociale': 15262, 'Droit, sciences politiques': 62922, 'Langues': 42667, 'Lettres, sciences du langage, arts': 23879, 'Médecine': 54, 'Pluridisciplinaire lettres, langues, sciences humaines': 1159, 'Pluridisciplinaire sciences': 12380, 'STAPS': 26080, "Sciences de la vie, de la terre et de l'univers": 16165, 'Sciences fondamentales et applications': 20566, 'Sciences humaines et sociales': 58867, 'Sciences économiques, gestion': 27606}
    """
    data = fetch_data("select=discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=discipline_lib")
    result = {row['discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par type de bac
@app.route('/api/nb_etudiants/type_bac', methods=['GET'])
def get_nb_etudiants_par_type_bac() -> dict:
    """ Récupère le nombre d'étudiants par type de bac

    Returns:
        dict: le nombre d'étudiants par type de bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/nb_etudiants/type_bac").json()
        {'BAC ES': 92196, 'BAC L': 59524, 'BAC S': 80194, 'BAC STMG': 27674, 'BAC professionnel': 29461, 'BAC technologique hors STMG': 18558}
    """
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par mention au bac
@app.route('/api/nb_etudiants/mention_bac', methods=['GET'])
def get_nb_etudiants_par_mention_bac() -> dict:
    """ Récupère le nombre d'étudiants par mention au bac

    Returns:
        dict: le nombre d'étudiants par mention au bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/nb_etudiants/mention_bac").json()
        {'Assez bien': 82390, 'Bien': 35008, 'Inconnue': 10096, 'Passable deuxième groupe': 46741, 'Passable premier groupe': 121895, 'Très bien': 11477}
    """
    data = fetch_data("select=mention_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

