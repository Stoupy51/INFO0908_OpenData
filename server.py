
# Imports
from src.shared_import import *
from src.general import *
#from src.lists import *
from src.repartition_etudiants import *
from src.l2_et_reorientation import *
from src.reussite_licence import *
from src.redoublement import *
from src.ml.prediction_reussite import *

# Liste des variables:
# gd_discipline
# gd_discipline_lib
# discipline
# discipline_lib
# sect_disciplinaire
# sect_disciplinaire_lib
# serie_bac
# serie_bac_lib
# age_au_bac
# age_au_bac_lib
# sexe
# sexe_lib
# mention_bac
# mention_bac_lib
# cohorte_passage
# effectif_neobacheliers_passage
# passage_en_l2_1_an
# redoublement_en_l1
# passage_en_l2_2_ans
# passage_en_l2_1_2_ans
# reorientation_en_dut_1_an
# reorientation_en_dut_2_ans
# reorientation_en_dut
# cohorte_reussite"
# effectif_neobacheliers_reussite
# reussite_3_ans
# reussite_4_ans
# reussite_3_4_ans

if __name__ == '__main__':
    #entrainer_modeles()

    for model_name in ["logistic", "rf"]:
        proba: float = predire_reussite({
            "gd_discipline": "Lettres, langues et sciences humaines",
            "discipline": "Langues",
            "sect_disciplinaire": "Langues et littératures étrangères",
            "serie_bac": "BAC STMG",
            "age_au_bac": "A l'heure ou en avance",
            "sexe": "Homme",
            "mention_bac": "Très bien",
            },
            model_name
        )
        stp.info(f"Probabilité de réussite ({model_name}): {proba}")
    #app.run(debug=True)


