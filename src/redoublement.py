
# Imports
from .shared_import import *

# Récupérer le nombre d’étudiants ayant redoublé par grandes discipline
@app.route('/api/redoublement/gd_discipline', methods=['GET'])
def get_redoublement_par_gd_discipline() -> dict:
    """ Récupérer le nombre d’étudiants ayant redoublé par grandes discipline

    Returns:
        dict: le nombre d'étudiants ayant redoublé par grandes discipline
    Examples:
        >>> requests.get(f"{OUR_API}/api/redoublement/gd_discipline").json()
        {'Droit, gestion, économie, AES': 17728, 'Lettres, langues et sciences humaines': 16375, 'STAPS': 4527, 'Santé': 2, "Sciences et sciences de l'ingénieur": 7760}
    """
    data = fetch_data("select=gd_discipline_lib,SUM(redoublement_en_l1)&group_by=gd_discipline_lib")
    result = {row['gd_discipline_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par discipline
@app.route('/api/redoublement/discipline', methods=['GET'])
def get_redoublement_par_discipline() -> dict:
    """ Récupérer le nombre d’étudiants ayant redoublé par discipline

    Returns:
        dict: le nombre d'étudiants ayant redoublé par discipline
    Examples:
        >>> requests.get(f"{OUR_API}/api/redoublement/discipline").json()
        {'Administration économique et sociale': 2559, 'Droit, sciences politiques': 11202, 'Langues': 6009, 'Lettres, sciences du langage, arts': 2667, 'Médecine': 2, 'Pluridisciplinaire lettres, langues, sciences humaines': 121, 'Pluridisciplinaire sciences': 1871, 'STAPS': 4527, "Sciences de la vie, de la terre et de l'univers": 2522, 'Sciences fondamentales et applications': 3367, 'Sciences humaines et sociales': 7578, 'Sciences économiques, gestion': 3967}
    """
    data = fetch_data("select=discipline_lib,SUM(redoublement_en_l1)&group_by=discipline_lib")
    result = {row['discipline_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par type de bac
@app.route('/api/redoublement/type_bac', methods=['GET'])
def get_redoublement_par_type_bac() -> dict:
    """ Récupérer le nombre d’étudiants ayant redoublé par type de bac

    Returns:
        dict: le nombre d'étudiants ayant redoublé par type de bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/redoublement/type_bac").json()
        {'BAC ES': 12738, 'BAC L': 9415, 'BAC S': 10352, 'BAC STMG': 5079, 'BAC professionnel': 5286, 'BAC technologique hors STMG': 3522}
    """
    data = fetch_data("select=serie_bac_lib,SUM(redoublement_en_l1)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

# Récupérer le nombre d’étudiants ayant redoublé par mention au bac
@app.route('/api/redoublement/mention_bac', methods=['GET'])
def get_redoublement_par_mention_bac() -> dict:
    """ Récupérer le nombre d’étudiants ayant redoublé par mention au bac

    Returns:
        dict: le nombre d'étudiants ayant redoublé par mention au bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/redoublement/mention_bac").json()
        {'Assez bien': 10409, 'Bien': 2392, 'Inconnue': 1376, 'Passable deuxième groupe': 9935, 'Passable premier groupe': 21772, 'Très bien': 508}
    """
    data = fetch_data("select=mention_bac_lib,SUM(redoublement_en_l1)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

