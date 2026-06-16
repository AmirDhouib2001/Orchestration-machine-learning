"""Entraînement et comparaison de plusieurs modèles avec GridSearchCV."""

from __future__ import annotations

import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, roc_auc_score
from xgboost import XGBClassifier

from src.config import MLFLOW_TRACKING_URI
from src.data import load_data, split
from src.features import build_preprocessor


def build_pipeline(classifier) -> Pipeline:
    """Crée un pipeline combinant le préprocesseur et un modèle donné."""
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("clf", classifier),
        ]
    )


def train_and_log(
    run_name: str,
    pipeline: Pipeline,
    param_grid: dict,
    x_train,
    y_train,
    x_test,
    y_test,
):
    """Effectue un GridSearchCV, évalue le meilleur modèle et log tout dans MLflow."""
    with mlflow.start_run(run_name=run_name):
        print(f"--- Entraînement de {run_name} ---")

        # Recherche des meilleurs paramètres (GridSearchCV)
        grid_search = GridSearchCV(
            estimator=pipeline, param_grid=param_grid, scoring="f1", cv=3, n_jobs=-1
        )

        grid_search.fit(x_train, y_train)

        best_model = grid_search.best_estimator_

        proba = best_model.predict_proba(x_test)[:, 1]
        preds = (proba >= 0.5).astype(int)

        metrics = {
            "f1": float(f1_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
        }

        print(f"✅ Meilleurs paramètres : {grid_search.best_params_}")
        print(
            f"✅ Scores -> f1: {metrics['f1']:.3f}, roc_auc: {metrics['roc_auc']:.3f}\n"
        )

        # Enregistrement dans MLflow
        mlflow.log_params(grid_search.best_params_)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(best_model, artifact_path="model")


def main():
    df = load_data()
    x_train, x_test, y_train, y_test = split(df)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("League_of_Legends_Models")

    mlflow.sklearn.autolog()

    # ---------------------------------------------------------
    # Modèle 1 : Logistic Regression (La Baseline)
    # ---------------------------------------------------------
    lr_pipe = build_pipeline(LogisticRegression(max_iter=1000))
    lr_params = {
        "clf__C": [0.01, 0.1, 1.0, 10.0]  # Régularisation
    }
    train_and_log(
        "LogisticRegression_Optimized",
        lr_pipe,
        lr_params,
        x_train,
        y_train,
        x_test,
        y_test,
    )

    # ---------------------------------------------------------
    # Modèle 2 : Random Forest
    # ---------------------------------------------------------
    rf_pipe = build_pipeline(RandomForestClassifier(random_state=42))
    rf_params = {
        "clf__n_estimators": [50, 100],  # Nombre d'arbres
        "clf__max_depth": [None, 5, 10],  # Profondeur des arbres
    }
    train_and_log(
        "RandomForest_Optimized", rf_pipe, rf_params, x_train, y_train, x_test, y_test
    )

    # ---------------------------------------------------------
    # Modèle 3 : XGBoost
    # ---------------------------------------------------------
    xgb_pipe = build_pipeline(XGBClassifier(eval_metric="logloss", random_state=42))
    xgb_params = {
        "clf__n_estimators": [50, 100],  # Nombre d'arbres
        "clf__max_depth": [3, 5],  # Profondeur
        "clf__learning_rate": [0.01, 0.1],  # Vitesse d'apprentissage
    }
    train_and_log(
        "XGBoost_Optimized", xgb_pipe, xgb_params, x_train, y_train, x_test, y_test
    )


if __name__ == "__main__":
    main()
