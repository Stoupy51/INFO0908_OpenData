
# Imports
from .shared_import import *

# Récupérer la liste des différentes grandes disciplines
@app.route('/api/liste/gd_discipline', methods=['GET'])
def get_gd_disciplines() -> list[str]:
    """ Récupère la liste des différentes grandes disciplines

    Returns:
        list[str]: la liste des différentes grandes disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/gd_discipline").json()
    """
    data = fetch_data("select=gd_discipline_lib")
    disciplines = [row['gd_discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer la liste des différentes disciplines
@app.route('/api/liste/discipline', methods=['GET'])
def get_disciplines() -> list[str]:
    """ Récupère la liste des différentes disciplines

    Returns:
        list[str]: la liste des différentes disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/discipline").json()
    """
    data = fetch_data("select=discipline_lib")
    disciplines = [row['discipline_lib'] for row in data]
    return jsonify(list(set(disciplines)))

# Récupérer le liste des différentes sect_disciplinaire
@app.route('/api/liste/secteurs_disciplinaire', methods=['GET'])
def get_secteurs_disciplinaires() -> list[str]:
    """ Récupère la liste des différents secteurs disciplinaires

    Returns:
        list[str]: la liste des différents secteurs disciplines
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/secteurs_disciplinaire").json()
    """
    data = fetch_data("select=sect_disciplinaire_lib")
    sect_disciplinaire = [row['sect_disciplinaire_lib'] for row in data]
    return jsonify(list(set(sect_disciplinaire)))

# Récupérer la liste des types de bac
@app.route('/api/liste/types_bac', methods=['GET'])
def get_types_bac() -> list[str]:
    """ Récupère la liste des types de bac

    Returns:
        list[str]: la liste des types de bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/types_bac").json()
    """
    data = fetch_data("select=serie_bac_lib")
    types_bac = [row['serie_bac_lib'] for row in data]
    return jsonify(list(set(types_bac)))

# Récupérer la liste des différentes mentions au Bac
@app.route('/api/liste/mentions_bac', methods=['GET'])
def get_mentions_bac() -> list[str]:
    """ Récupère la liste des différentes mentions au Bac

    Returns:
        list[str]: la liste des différentes mentions au Bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/mentions_bac").json()
    """
    data = fetch_data("select=mention_bac_lib")
    mentions = [row['mention_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

# Récupérer la liste des différents ages au bac
@app.route('/api/liste/age_au_bac', methods=['GET'])
def get_mentions_bac() -> list[str]:
    """ Récupère la liste des différents âges à l'obtention du bac

    Returns:
        list[str]: la liste des différentes âges à l'obtention au Bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/age_au_bac").json()
    """
    data = fetch_data("select=age_au_bac_lib")
    mentions = [row['age_au_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

# Récupérer la liste des différents sexualités
@app.route('/api/liste/sexe', methods=['GET'])
def get_mentions_bac() -> list[str]:
    """ Récupère la liste des différentes séxualités

    Returns:
        list[str]: la liste des différentes séxualités
    Examples:
        >>> requests.get(f"{OUR_API}/api/liste/sexe").json()
    """
    data = fetch_data("select=sexe_lib")
    mentions = [row['sexe_lib'] for row in data]
    return jsonify(list(set(mentions)))