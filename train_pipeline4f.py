# train_pipeline.py

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib

# 1 Charger ton dataset
df = pd.read_csv("data/train.csv")  # Remplace par ton fichier CSV

# 2 Sélectionner les features et la cible
features = ["BedroomAbvGr", "GrLivArea", "YearBuilt", "Neighborhood"]
num_features = ["BedroomAbvGr", "GrLivArea", "YearBuilt"]
cat_features = ["Neighborhood"]
X = df[features]
y = df["SalePrice"]  # colonne cible

# 3 Créer le préprocesseur
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
])

# 4 Créer le pipeline complet
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", XGBRegressor())
])

# 5 Entraîner le pipeline
pipeline.fit(X, y)

# 6 Sauvegarder le pipeline
joblib.dump(pipeline, "xgb_pipeline_4feat.pkl")
print("Pipeline sauvegardé !")
