
# Imports
from ..shared_import import *
from ..general import *
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split  # Pour diviser les données
from sklearn.metrics import accuracy_score  # Pour évaluer le modèle
from sklearn.linear_model import LinearRegression  # Importer la régression linéaire
from sklearn.ensemble import RandomForestRegressor  # Importer la forêt aléatoire

# Constantes
MODELS_FOLDER: str = f"{ROOT}/models"
os.makedirs(MODELS_FOLDER, exist_ok=True)

## Objectif : faire un modèle de prédiction du taux de réussite d'un étudiant (score entre 0 et 1)
# Variables à utiliser
VARIABLES_UTILES: list[str] = [		# Variables qualitatives
	"gd_discipline_lib",
	"discipline_lib",
	"sect_disciplinaire_lib",
	"serie_bac_lib",
	"age_au_bac_lib",
	"sexe_lib",
	"mention_bac_lib",
]

# Fonction pour entrainer le modèle
@stp.handle_error(error_log=stp.LogLevels.ERROR_TRACEBACK)
def entrainer_modeles() -> None:
	""" Entraine le modèle de prédiction du taux de réussite d'un étudiant

	- Récupération des données
	- Préparation des données
	- Entrainement du modèle
	- Sauvegarde du modèle
	"""
	# Récupération des données
	json_data: list[dict] = get_all_data()
	data: pd.DataFrame = pd.DataFrame(json_data)
	data["taux_reussite"] = data["reussite_3_4_ans"] / data["effectif_neobacheliers_reussite"]	# Calcul du taux de réussite (nombre de réussite en 3-4 ans / nombre d"étudiants)

	# Ignorer les lignes avec des valeurs manquantes
	data = data.dropna()
	
	# Préparation des données
	X: pd.DataFrame = data[VARIABLES_UTILES]  # Variables indépendantes
	y: pd.Series = data["taux_reussite"]  # Variable dépendante

	# Convertir les variables qualitatives en variables numériques
	X_encoded: pd.DataFrame = pd.get_dummies(X)
	# Sauvegarder les colonnes pour pouvoir les réutiliser plus tard
	colonnes: list[str] = X_encoded.columns.tolist()
	joblib.dump(colonnes, f"{MODELS_FOLDER}/colonnes.pkl")

	# Diviser les données en ensembles d"entraînement et de test
	X_train: pd.DataFrame
	X_test: pd.DataFrame
	y_train: pd.Series
	y_test: pd.Series
	X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

	# Créer le modèle de régression linéaire et l'entraîner
	model_linear: LinearRegression = LinearRegression()
	model_linear.fit(X_train, y_train)

	# Évaluer le modèle de régression linéaire
	categorial_y_test: pd.Series = y_test.apply(lambda x: 1 if x > 0.5 else 0)
	y_pred_raw_linear: np.ndarray = model_linear.predict(X_test)
	y_pred_linear: np.ndarray = np.where(y_pred_raw_linear > 0.5, 1, 0)
	accuracy_linear: float = accuracy_score(categorial_y_test, y_pred_linear)
	stp.info(f"Accuracy (Linear Regression): {accuracy_linear}")

	# Créer le modèle de forêt aléatoire et l'entraîner
	model_rf: RandomForestRegressor = RandomForestRegressor(random_state=42)
	model_rf.fit(X_train, y_train)

	# Évaluer le modèle de forêt aléatoire
	y_pred_raw_rf: np.ndarray = model_rf.predict(X_test)
	y_pred_rf: np.ndarray = np.where(y_pred_raw_rf > 0.5, 1, 0)
	accuracy_rf: float = accuracy_score(categorial_y_test, y_pred_rf)
	stp.info(f"Accuracy (Random Forest): {accuracy_rf}")

	# Sauvegarde des modèles
	joblib.dump(model_linear, f"{MODELS_FOLDER}/linear.pkl")
	joblib.dump(model_rf, f"{MODELS_FOLDER}/rf.pkl")

# Fonction pour charger le modèle
def charger_modele(model_name: Literal["linear", "rf"]) -> tuple[Any, list[str]]:
	""" Charge le modèle de prédiction du taux de réussite d"un étudiant

	- Essaie de charger le modèle
	- Si le modèle n"est pas trouvé, entraine le modèle
	Returns:
		tuple[Any, list[str]]: Le modèle et la liste des colonnes pour l'encodage
	"""
	model_path: str = f"{MODELS_FOLDER}/{model_name}.pkl"
	colonnes_path: str = f"{MODELS_FOLDER}/colonnes.pkl"
	try:
		model: Any = joblib.load(model_path)
	except FileNotFoundError:
		entrainer_modeles()
		model: Any = joblib.load(model_path)
	colonnes: list[str] = joblib.load(colonnes_path)
	return model, colonnes

# Fonction pour prédire la reussite d"un étudiant
def predire_reussite(etudiant: dict, model_name: Literal["linear", "rf"]) -> float:
	""" Prédit le taux de réussite d"un étudiant

	- Chargement du modèle (si pas déjà chargé)
	- Prédiction
	"""
	model: Any
	colonnes: list[str]
	model, colonnes = charger_modele(model_name)

	# Préparation des données
	etudiant_df: pd.DataFrame = pd.DataFrame(etudiant)
	etudiant_encoded: pd.DataFrame = pd.get_dummies(etudiant_df)
	
	# S'assurer que toutes les colonnes nécessaires sont présentes
	for col in colonnes:
		if col not in etudiant_encoded.columns:
			etudiant_encoded[col] = 0
	
	# Réorganiser les colonnes dans le même ordre que lors de l'entrainement
	etudiant_encoded = etudiant_encoded[colonnes]

	# Prédiction
	prediction: float = model.predict(etudiant_encoded)[0]
	return prediction

