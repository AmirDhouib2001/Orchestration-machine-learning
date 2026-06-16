"""API d'inférence FastAPI pour le meilleur modèle League of Legends."""
from __future__ import annotations

import logging
import os
import pandas as pd
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import mlflow
import mlflow.sklearn

from src.config import MLFLOW_TRACKING_URI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

ml: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Charge automatiquement le MEILLEUR modèle depuis MLflow au démarrage de l'API."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    # 1. On cherche l'expérience "League_of_Legends_Models"
    experiment = mlflow.get_experiment_by_name("League_of_Legends_Models")
    if not experiment:
        logger.error("L'expérience est introuvable. Avez-vous lancé train_optuna.py ?")
        yield
        return
        
    # 2. Requête MLflow : "Donne moi le modèle qui a le meilleur score F1"
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1 DESC"],
        max_results=1
    )
    
    if runs.empty:
        logger.error("Aucun entraînement trouvé.")
        yield
        return
        
    best_run_id = runs.iloc[0].run_id
    best_f1 = runs.iloc[0]["metrics.f1"]
    best_run_name = runs.iloc[0].get("tags.mlflow.runName", "Modèle Inconnu")
    
    logger.info(f"🏆 Chargement du meilleur modèle ({best_run_name}, F1: {best_f1:.3f})")
    
    # 3. Chargement du modèle original sklearn directement depuis MLflow !
    ml["model"] = mlflow.sklearn.load_model(f"runs:/{best_run_id}/model")
    ml["model_info"] = {"model_name": best_run_name, "f1_score": best_f1}
    
    yield
    ml.clear()


app = FastAPI(title="League of Legends API", version="1.0.0", lifespan=lifespan)


# -------------------------------------------------------------------------
# Étape 1 & 2 : Schémas Pydantic (Entrée et Sortie)
# -------------------------------------------------------------------------
class Features(BaseModel):
    # Variables numériques
    blueWardsPlaced: float = Field(..., ge=0)
    blueWardsDestroyed: float = Field(..., ge=0)
    blueKills: float = Field(..., ge=0)
    blueDeaths: float = Field(..., ge=0)
    blueAssists: float = Field(..., ge=0)
    blueTotalGold: float = Field(..., ge=0)
    blueTotalExperience: float = Field(..., ge=0)
    blueGoldDiff: float = Field(...)
    blueExperienceDiff: float = Field(...)
    redWardsPlaced: float = Field(..., ge=0)
    redWardsDestroyed: float = Field(..., ge=0)
    redKills: float = Field(..., ge=0)
    redDeaths: float = Field(..., ge=0)
    redAssists: float = Field(..., ge=0)
    redTotalGold: float = Field(..., ge=0)
    redTotalExperience: float = Field(..., ge=0)
    
    # Variables catégorielles
    blueFirstBlood: int = Field(..., ge=0, le=1)
    blueDragons: int = Field(..., ge=0, le=5)
    blueHeralds: int = Field(..., ge=0, le=2)
    redFirstBlood: int = Field(..., ge=0, le=1)
    redDragons: int = Field(..., ge=0, le=5)
    redHeralds: int = Field(..., ge=0, le=2)

    model_config = {
        "json_schema_extra": {
            "example": {
                "blueWardsPlaced": 15, "blueWardsDestroyed": 2, "blueKills": 5, "blueDeaths": 3,
                "blueAssists": 4, "blueTotalGold": 16000, "blueTotalExperience": 18000,
                "blueGoldDiff": 1000, "blueExperienceDiff": 500,
                "redWardsPlaced": 12, "redWardsDestroyed": 1, "redKills": 3, "redDeaths": 5,
                "redAssists": 2, "redTotalGold": 15000, "redTotalExperience": 17500,
                "blueFirstBlood": 1, "blueDragons": 1, "blueHeralds": 0,
                "redFirstBlood": 0, "redDragons": 0, "redHeralds": 0
            }
        }
    }


class PredictionOut(BaseModel):
    prediction: int
    probability: float
    message: str


# -------------------------------------------------------------------------
# Étape 4 & 5 : Endpoints
# -------------------------------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOut)
def predict(features: Features) -> PredictionOut:
    model = ml.get("model")
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
        
    # Transformation du JSON en DataFrame
    row = pd.DataFrame([features.model_dump()])
    
    # Prédiction
    proba = float(model.predict_proba(row)[0, 1])
    pred = int(proba >= 0.5)
    
    msg = "Victoire Équipe Bleue !" if pred == 1 else "Défaite Équipe Bleue..."
    
    return PredictionOut(prediction=pred, probability=round(proba, 4), message=msg)


# Bonus S12-5
@app.get("/model-info")
def model_info() -> dict:
    """Renvoie les informations du modèle MLflow actuellement en mémoire."""
    if "model_info" in ml:
        return ml["model_info"]
    raise HTTPException(status_code=503, detail="Modèle non chargé")
