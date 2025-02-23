
# Imports
from .shared_import import *

# récupérer le nb d’hommes et de femmes
@app.route('/api/nb-hommes-femmes/', methods=['GET'], defaults={'groupby': ""})
@app.route('/api/nb-hommes-femmes/<string:groupby>', methods=['GET'])
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
def get_nb_etudiants_par_gd_discipline() -> dict:
    """ Récupère le nombre d'étudiants par grandes disciplines

    Returns:
        dict: le nombre d'étudiants par grandes disciplines
    """
    data = fetch_data("select=gd_discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=gd_discipline_lib")
    result = {row['gd_discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# récupérer le nombre d’étudiants par disciplines
@app.route('/api/nb-etudiants-par-discipline', methods=['GET'])
def get_nb_etudiants_par_discipline() -> dict:
    """ Récupère le nombre d'étudiants par disciplines

    Returns:
        dict: le nombre d'étudiants par disciplines
    """
    data = fetch_data("select=discipline_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=discipline_lib")
    result = {row['discipline_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par type de bac
@app.route('/api/nb-etudiants-par-type-bac', methods=['GET'])
def get_nb_etudiants_par_type_bac() -> dict:
    """ Récupère le nombre d'étudiants par type de bac

    Returns:
        dict: le nombre d'étudiants par type de bac
    """
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants par mention au bac
@app.route('/api/nb-etudiants-par-mention-bac', methods=['GET'])
def get_nb_etudiants_par_mention_bac() -> dict:
    """ Récupère le nombre d'étudiants par mention au bac

    Returns:
        dict: le nombre d'étudiants par mention au bac
    """
    data = fetch_data("select=mention_bac_lib,SUM(effectif_neobacheliers_passage),SUM(effectif_neobacheliers_reussite)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(sum(filter(None,[row['SUM(effectif_neobacheliers_passage)'],row['SUM(effectif_neobacheliers_reussite)']]))) for row in data}
    return jsonify(result)

