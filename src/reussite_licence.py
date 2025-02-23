
# Imports
from .shared_import import *

# Nombre d’étudiant obtenant la licence en 3 ans / 4 ans / pas réussi
@app.route('/api/reussite_licence', methods=['GET'])
def get_reussite_licence() -> dict:
    """ Récupérer le nombre d'étudiants obtenant la licence en 3 ans / 4 ans / pas réussi

    Returns:
        dict: le nombre d'étudiants obtenant la licence en 3 ans / 4 ans / pas réussi
    Examples:
        >>> requests.get(f"{OUR_API}/api/reussite_licence").json()
    """
    data = fetch_data("select=reussite_3_ans,reussite_4_ans,effectif_neobacheliers_reussite")
    result = {
        'en 3 ans': int(sum(filter(None,[row['reussite_3_ans'] for row in data]))),
        'en 4 ans': int(sum(filter(None,[row['reussite_4_ans'] for row in data]))),
        'pas_reussi': sum(filter(None,[row['effectif_neobacheliers_reussite'] for row in data]))
    }
    result['pas_reussi'] = int(result['pas_reussi'] - (result['en 3 ans'] + result['en 4 ans']))
    return jsonify(result)

# Calculer le taux de réussite en licence par grandes disciplines
@app.route('/api/taux_reussite_licence/gd_discipline', methods=['GET'])
def get_taux_reussite_par_gd_discipline() -> dict:
    """ Calculer le taux de réussite en licence par grandes disciplines

    Returns:
        dict: le taux de réussite en licence par grandes disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/taux_reussite_licence/gd_discipline").json()
    """
    data = fetch_data("select=gd_discipline_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=gd_discipline_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['gd_discipline_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par discipline
@app.route('/api/taux_reussite_licence/discipline', methods=['GET'])
def get_taux_reussite_par_discipline() -> dict:
    """ Calculer le taux de réussite en licence par discipline

    Returns:
        dict: le taux de réussite en licence par discipline
    Examples:
        >>> requests.get(f"{OUR_API}/api/taux_reussite_licence/discipline").json()
    """
    data = fetch_data("select=discipline_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=discipline_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['discipline_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par mention au bac
@app.route('/api/taux_reussite_licence/mention_bac', methods=['GET'])
def get_taux_reussite_par_mention_bac() -> dict:
    """ Calculer le taux de réussite en licence par mention au bac

    Returns:
        dict: le taux de réussite en licence par mention au bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/taux_reussite_licence/mention_bac").json()
    """
    data = fetch_data("select=mention_bac_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=mention_bac_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)'] 
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['mention_bac_lib']] = round(taux,2)
    return jsonify(result)

# Calculer le taux de réussite en licence par type de bac
@app.route('/api/taux_reussite_licence/type_bac', methods=['GET'])
def get_taux_reussite_par_type_bac() -> dict:
    """ Calculer le taux de réussite en licence par type de bac

    Returns:
        dict: le taux de réussite en licence par type de bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/taux_reussite_licence/type_bac").json()
    """
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=serie_bac_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['serie_bac_lib']] = round(taux,2)
    return jsonify(result)

