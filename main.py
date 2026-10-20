# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import pandas as pd
import joblib
import os

# -----------------------------
# Charger le pipeline
# -----------------------------
pipeline_path = "xgb_pipeline_4feat.pkl"
if not os.path.exists(pipeline_path):
    raise FileNotFoundError(f"Pipeline non trouvé : {pipeline_path}")

pipeline = joblib.load(pipeline_path)

# Charger le dataset pour récupérer dynamiquement tous les quartiers
data_path = "data/train.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset non trouvé : {data_path}")

df_train = pd.read_csv(data_path)
valid_neigh = df_train["Neighborhood"].unique().tolist()

# -----------------------------
# Créer l’application FastAPI
# -----------------------------
app = FastAPI(title="API prédiction prix maisons")

# -----------------------------
# Classe d'entrée simplifiée
# -----------------------------
class HouseData(BaseModel):
    BedroomAbvGr: int
    GrLivArea: float
    YearBuilt: int
    Neighborhood: str

    @validator("Neighborhood")
    def check_neighborhood(cls, v):
        if v not in valid_neigh:
            raise ValueError(f"Quartier inconnu : {v}. Choisir parmi {valid_neigh}")
        return v

# -----------------------------
# Route de prédiction
# -----------------------------
@app.post("/predict")
def predict_price(data: HouseData):
    try:
        df = pd.DataFrame([data.dict()])
        pred = pipeline.predict(df)
        return {"PredictedPrice": float(pred[0])}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur serveur : " + str(e))

# -----------------------------
# Route d'accueil
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prédiction du prix des maisons!"}
