
# Imports
from .shared_import import *

# Récupérer la liste des différentes grandes disciplines
@app.route('/api/liste/gd_discipline', methods=['GET'])
def get_gd_disciplines() -> list[str]:
    """ Récupère la liste des différentes grandes disciplines

    Returns:
        list[str]: la liste des différentes grandes disciplines
    Examples:
        >>> requests.get(f"http://localhost:5000/api/liste/gd_discipline").json()
        ['Santé', "Sciences et sciences de l'ingénieur", 'Droit, gestion, économie, AES', 'Lettres, langues et sciences humaines', 'STAPS']
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
        >>> requests.get(f"http://localhost:5000/api/liste/discipline").json()
        ['Pluridisciplinaire lettres, langues, sciences humaines', 'Lettres, sciences du langage, arts', 'STAPS', 'Sciences fondamentales et applications', 'Pluridisciplinaire sciences', 'Sciences humaines et sociales', 'Droit, sciences politiques', 'Administration économique et sociale', 'Sciences économiques, gestion', 'Médecine', 'Langues', "Sciences de la vie, de la terre et de l'univers"]
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
        >>> requests.get(f"http://localhost:5000/api/liste/secteurs_disciplinaire").json()[:10]
        ['Sciences économiques', 'Mécanique, génie mécanique', 'Sciences juridiques', 'Pluridisciplinaire sciences', 'Langues étrangères appliquées', 'Sciences politiques', 'Géographie', 'Technologie et sciences industrielles', 'Administration économique et sociale', 'Pluridisciplinaire droit, sciences politiques']
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
        >>> requests.get(f"http://localhost:5000/api/liste/types_bac").json()
        ['BAC STMG', 'BAC S', 'BAC L', 'BAC ES', 'BAC technologique hors STMG', 'BAC professionnel']
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
        >>> requests.get(f"http://localhost:5000/api/liste/mentions_bac").json()
        ['Passable premier groupe', 'Assez bien', 'Très bien', 'Bien', 'Inconnue', 'Passable deuxième groupe']
    """
    data = fetch_data("select=mention_bac_lib")
    mentions = [row['mention_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

# Récupérer la liste des différents ages au bac
@app.route('/api/liste/age_au_bac', methods=['GET'])
def get_age_au_bac() -> list[str]:
    """ Récupère la liste des différents âges à l'obtention du bac

    Returns:
        list[str]: la liste des différentes âges à l'obtention au Bac
    Examples:
        >>> sorted(requests.get(f"http://localhost:5000/api/liste/age_au_bac").json())
        ["A l'heure ou en avance", "En retard d'un an", "En retard de plus d'un an", 'Non pris en compte']
    """
    data = fetch_data("select=age_au_bac_lib")
    mentions = [row['age_au_bac_lib'] for row in data]
    return jsonify(list(set(mentions)))

# Récupérer la liste des différents sexualités
@app.route('/api/liste/sexe', methods=['GET'])
def get_sexe() -> list[str]:
    """ Récupère la liste des différentes séxualités

    Returns:
        list[str]: la liste des différentes séxualités
    Examples:
        >>> requests.get(f"http://localhost:5000/api/liste/sexe").json()
        ['Homme', 'Femme']
    """
    data = fetch_data("select=sexe_lib")
    mentions = [row['sexe_lib'] for row in data]
    return jsonify(list(set(mentions)))

