"""Construction du pre-processing."""

from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer

from src.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def add_lol_synergies(X: pd.DataFrame) -> pd.DataFrame:
    """Crée de nouvelles colonnes basées sur la synergie de certaines statistiques."""
    X_out = X.copy()

    # 1. Effet 'Snowball' (Or * Expérience) : La puissance brute globale
    X_out["blueSnowball"] = X_out["blueTotalGold"] * X_out["blueTotalExperience"]
    X_out["redSnowball"] = X_out["redTotalGold"] * X_out["redTotalExperience"]

    # 2. Synergie d'Équipe (Kills * Assists) : Capacité à jouer groupé en teamfight
    X_out["blueTeamfight"] = X_out["blueKills"] * X_out["blueAssists"]
    X_out["redTeamfight"] = X_out["redKills"] * X_out["redAssists"]

    # 3. Contrôle de la Carte (Wards posées * Wards détruites)
    X_out["blueVisionControl"] = X_out["blueWardsPlaced"] * X_out["blueWardsDestroyed"]
    X_out["redVisionControl"] = X_out["redWardsPlaced"] * X_out["redWardsDestroyed"]

    return X_out


def build_preprocessor() -> Pipeline:
    new_numeric_features = NUMERIC_FEATURES + [
        "blueSnowball",
        "redSnowball",
        "blueTeamfight",
        "redTeamfight",
        "blueVisionControl",
        "redVisionControl",
    ]

    col_transformer = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), new_numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("synergies", FunctionTransformer(add_lol_synergies)),
            ("preprocessing", col_transformer),
        ]
    )
