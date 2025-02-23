
# Imports
from .shared_import import *

# Récupérer la liste des différentes grandes disciplines
@app.route('/api/gd_discipline', methods=['GET'])
def get_gd_disciplines() -> list[str]:
    """ Récupère la liste des différentes grandes disciplines

    Returns:
        list[str]: la liste des différentes grandes disciplines
    """
    data = fetch_data("select=gd_discipline_lib")
    disciplines = [row['gd_discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer la liste des différentes disciplines
@app.route('/api/discipline', methods=['GET'])
def get_disciplines() -> list[str]:
    """ Récupère la liste des différentes disciplines

    Returns:
        list[str]: la liste des différentes disciplines
    """
    data = fetch_data("select=discipline_lib")
    disciplines = [row['discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer la liste des types de bac
@app.route('/api/types-bac', methods=['GET'])
def get_types_bac() -> list[str]:
    """ Récupère la liste des types de bac

    Returns:
        list[str]: la liste des types de bac
    """
    data = fetch_data("select=serie_bac_lib")
    types_bac = [row['serie_bac_lib'] for row in data]
    return jsonify(list(set(types_bac)))

# Récupérer la liste des différentes mentions au Bac
@app.route('/api/mentions-bac', methods=['GET'])
def get_mentions_bac() -> list[str]:
    """ Récupère la liste des différentes mentions au Bac

    Returns:
        list[str]: la liste des différentes mentions au Bac
    """
    data = fetch_data("select=mention_bac_lib")
    mentions = [row['mention_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

