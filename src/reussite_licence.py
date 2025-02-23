
# Imports
from .shared_import import *

# Nombre d’étudiant obtenant la licence en 3 ans / 4 ans / pas réussi
@app.route('/api/reussite_licence', methods=['GET'])
def get_reussite_licence() -> dict:
    """ Récupérer le nombre d'étudiants obtenant la licence en 3 ans / 4 ans / pas réussi

    Returns:
        dict: le nombre d'étudiants obtenant la licence en 3 ans / 4 ans / pas réussi
    Examples:
        >>> requests.get(f"http://localhost:5000/api/reussite_licence").json()
        {'en 3 ans': 41922, 'en 4 ans': 18624, 'pas_reussi': 87295}
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
        >>> requests.get(f"http://localhost:5000/api/taux_reussite_licence/gd_discipline").json()
        {'Droit, gestion, économie, AES': 40.88, 'Lettres, langues et sciences humaines': 42.46, 'STAPS': 40.1, 'Santé': 75.76, "Sciences et sciences de l'ingénieur": 37.38}
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
        >>> requests.get(f"http://localhost:5000/api/taux_reussite_licence/discipline").json()
        {'Administration économique et sociale': 27.17, 'Droit, sciences politiques': 44.53, 'Langues': 39.86, 'Lettres, sciences du langage, arts': 43.95, 'Médecine': 75.76, 'Pluridisciplinaire lettres, langues, sciences humaines': 50.7, 'Pluridisciplinaire sciences': 38.2, 'STAPS': 40.1, "Sciences de la vie, de la terre et de l'univers": 40.12, 'Sciences fondamentales et applications': 34.52, 'Sciences humaines et sociales': 43.6, 'Sciences économiques, gestion': 39.77}
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
        >>> requests.get(f"http://localhost:5000/api/taux_reussite_licence/mention_bac").json()
        {'Assez bien': 54.82, 'Bien': 69.76, 'Inconnue': 26.7, 'Passable deuxième groupe': 18.6, 'Passable premier groupe': 32.62, 'Très bien': 76.82}
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
        >>> requests.get(f"http://localhost:5000/api/taux_reussite_licence/type_bac").json()
        {'BAC ES': 52.1, 'BAC L': 46.67, 'BAC S': 52.12, 'BAC STMG': 14.07, 'BAC professionnel': 4.96, 'BAC technologique hors STMG': 18.15}
    """
    data = fetch_data("select=serie_bac_lib,SUM(effectif_neobacheliers_reussite),SUM(reussite_3_4_ans)&group_by=serie_bac_lib")
    result = {}
    for row in data:
        total = row['SUM(effectif_neobacheliers_reussite)']
        reussis = row['SUM(reussite_3_4_ans)']
        taux = (reussis / total) * 100 if total else 0
        result[row['serie_bac_lib']] = round(taux,2)
    return jsonify(result)

