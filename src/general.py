
# Imports
from .shared_import import *

# Route pour récupérer le dataset entier sous forme de json
@app.route('/api/json', methods=['GET'])
def get_all_data() -> list[dict]:
    """ Récupère le dataset entier sous forme de json

    Returns:
        dict: le dataset entier sous forme de json
    Examples:
        >>> requests.get(f"{OUR_API}/api/json").json()[0]["age_au_bac"]
        'R2'
    """
    data: list[dict] = requests.get(f"{API_URL}/exports/json?lang=fr&timezone=Europe%2FBerlin").json()
    return jsonify(data)

