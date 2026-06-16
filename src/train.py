"""Entrainement du modele de classification (baseline)."""

from __future__ import annotations

import argparse
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# TODO (S5-1) : importer mlflow et mlflow.sklearn
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline

from src.config import MODEL_DIR, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT
from src.data import load_data, split
from src.features import build_preprocessor


def build_model(c: float = 1.0, max_iter: int = 1000) -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("clf", LogisticRegression(C=c, max_iter=max_iter)),
        ]
    )


def train(c: float = 1.0, max_iter: int = 1000) -> dict:
    df = load_data()
    x_train, x_test, y_train, y_test = split(df)

    # TODO (S5-2) : configurer l'URI de tracking (mlflow.set_tracking_uri) et l'experience
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    # TODO (S5-3) : ouvrir un run englobant l'entrainement et l'evaluation (with mlflow.start_run())
    with mlflow.start_run(run_name="LogisticRegression_Baseline"):
        # --- Entraînement ---
        model = build_model(c=c, max_iter=max_iter)
        model.fit(x_train, y_train)

        # --- Évaluation ---
        proba = model.predict_proba(x_test)[:, 1]
        preds = (proba >= 0.5).astype(int)

        metrics = {
            "f1": float(f1_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
        }
        print(f"f1={metrics['f1']:.3f}  roc_auc={metrics['roc_auc']:.3f}")

        # TODO (S5-4) : logger les parametres (c, max_iter) avec mlflow.log_params
        mlflow.log_params({"C": c, "max_iter": max_iter})

        # TODO (S5-5) : logger les metriques (f1, roc_auc) avec mlflow.log_metrics
        mlflow.log_metrics(metrics)

        # TODO (S5-6) : logger le modele avec mlflow.sklearn.log_model
        mlflow.sklearn.log_model(model, artifact_path="model")

        # TODO (S5-7 bonus) : sauvegarder la matrice de confusion en image et la logger en artefact
        cm = confusion_matrix(y_test, preds)
        plt.figure(figsize=(6, 4))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Red Win", "Blue Win"],
            yticklabels=["Red Win", "Blue Win"],
        )
        plt.title("Matrice de Confusion")
        plt.ylabel("Vraie valeur")
        plt.xlabel("Prédiction")

        # Sauvegarde locale temporaire puis upload dans MLflow
        cm_path = "confusion_matrix.png"
        plt.savefig(cm_path)
        mlflow.log_artifact(cm_path)
        plt.close()  # Nettoyage de la mémoire
        Path(cm_path).unlink(missing_ok=True)  # Suppression de l'image locale

    # Sauvegarde locale du modèle classique
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--max-iter", type=int, default=1000)
    args = parser.parse_args()
    train(c=args.c, max_iter=args.max_iter)


if __name__ == "__main__":
    main()
