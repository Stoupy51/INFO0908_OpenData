
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
    """
    data = fetch_data("select=mention_bac_lib,SUM(redoublement_en_l1)&group_by=mention_bac_lib")
    result = {row['mention_bac_lib']: int(row['SUM(redoublement_en_l1)']) for row in data}
    return jsonify(result)

