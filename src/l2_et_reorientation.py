
# Imports
from .shared_import import *

# Récupérer le nombre d’étudiant passant en L2 en 1 an / en 2 ans / le nombre d’étudiants n’étant pas passer en L2
@app.route('/api/passage_l2/stats', methods=['GET'])
def get_passage_l2_stats() -> dict:
    """ Récupérer le nombre d’étudiant passant en L2 en 1 an / en 2 ans / le nombre d’étudiants n’étant pas passer en L2

    Returns:
        dict: le nombre d'étudiants passant en L2 en 1 an / en 2 ans / le nombre d'étudiants n'étant pas passer en L2
    Examples:
        >>> requests.get(f"{OUR_API}/api/passage_l2/stats").json()
    """
    data = fetch_data("select=passage_en_l2_1_an,passage_en_l2_2_ans,effectif_neobacheliers_passage")
    result = {
        'passage_en_l2_1_an': int(sum(filter(None,[row['passage_en_l2_1_an'] for row in data]))),
        'passage_en_l2_2_ans': int(sum(filter(None,[row['passage_en_l2_2_ans'] for row in data]))),
        'pas_passe': sum(filter(None,[row['effectif_neobacheliers_passage'] for row in data]))
    }
    result['pas_passe'] = int(result['pas_passe'] - (result['passage_en_l2_1_an'] + result['passage_en_l2_2_ans']))
    return jsonify(result)

# Passage en L2 (1 an, 2 ans, pas passe, taux de passage) par sexe
@app.route('/api/passage_l2/sexe', methods=['GET'])
def get_passage_l2_par_sexe() -> dict:
    """ Récupérer le nombre d'étudiants passant en L2 en 1 an / en 2 ans / le nombre d'étudiants n'étant pas passer en L2 par sexe

    Returns:
        dict: le nombre d'étudiants passant en L2 en 1 an / en 2 ans / le nombre d'étudiants n'étant pas passer en L2 par sexe
    Examples:
        >>> requests.get(f"{OUR_API}/api/passage_l2/sexe").json()
    """
    data = fetch_data("select=sexe_lib,SUM(passage_en_l2_1_an),SUM(passage_en_l2_2_ans),SUM(effectif_neobacheliers_passage)&group_by=sexe_lib")
    result = {row['sexe_lib']: {
        'passage_en_l2_1_an': int(row['SUM(passage_en_l2_1_an)']),
        'passage_en_l2_2_ans': int(row['SUM(passage_en_l2_2_ans)']),
        'pas_passe': int(row['SUM(effectif_neobacheliers_passage)']) - (int(row['SUM(passage_en_l2_1_an)']) + int(row['SUM(passage_en_l2_2_ans)'])),
        'taux_passage': (int(row['SUM(passage_en_l2_1_an)']) + int(row['SUM(passage_en_l2_2_ans)'])) / int(row['SUM(effectif_neobacheliers_passage)']) * 100
    } for row in data}
    return jsonify(result)

# Récupérer le nombre de passage en L2 en fonction du type de bac
@app.route('/api/passage_l2/bac', methods=['GET'])
def get_passage_l2_par_bac() -> dict:
    """ Récupérer le nombre de passage en L2 en fonction du type de bac

    Returns:
        dict: le nombre de passage en L2 en fonction du type de bac
    Examples:
        >>> requests.get(f"{OUR_API}/api/passage_l2/bac").json()
    """
    data = fetch_data("select=serie_bac_lib,SUM(passage_en_l2_1_2_ans)&group_by=serie_bac_lib")
    result = {row['serie_bac_lib']: row['SUM(passage_en_l2_1_2_ans)'] for row in data}
    return jsonify(result)

# Nombre d’étudiants passant en DUT après 1 an / 2 ans de licence
@app.route('/api/passage_dut', methods=['GET'])
def get_passage_dut() -> dict:
    """ Récupérer le nombre d'étudiants passant en DUT après 1 an / 2 ans de licence

    Returns:
        dict: le nombre d'étudiants passant en DUT après 1 an / 2 ans de licence
    Examples:
        >>> requests.get(f"{OUR_API}/api/passage_dut").json()
    """
    data = fetch_data("select=SUM(reorientation_en_dut_1_an),SUM(reorientation_en_dut_2_ans)")
    result = {
        "après 1 an": data[0]['SUM(reorientation_en_dut_1_an)'],
        "après 2 ans": data[0]['SUM(reorientation_en_dut_2_ans)']
    }
    return jsonify(result)

