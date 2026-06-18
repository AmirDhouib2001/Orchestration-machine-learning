"""Entraînement et comparaison de plusieurs modèles avec Optuna."""

from __future__ import annotations

import optuna
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
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


def train_with_optuna(
    run_name: str, model_type: str, x_train, y_train, x_test, y_test, n_trials=10
):
    """Recherche des meilleurs hyperparamètres avec Optuna et log le meilleur modèle dans MLflow."""

    def objective(trial):
        """Fonction objectif qu'Optuna va essayer d'optimiser (maximiser le score)."""
        # 1. Optuna "suggère" des paramètres selon le modèle
        if model_type == "LogisticRegression":
            # float entre 0.01 et 10, échelle logarithmique
            c = trial.suggest_float("C", 0.01, 10.0, log=True)
            clf = LogisticRegression(C=c, max_iter=1000)

        elif model_type == "RandomForest":
            n_estimators = trial.suggest_categorical("n_estimators", [50, 100, 200])
            max_depth = trial.suggest_categorical("max_depth", [None, 5, 10])
            clf = RandomForestClassifier(
                n_estimators=n_estimators, max_depth=max_depth, random_state=42
            )

        elif model_type == "XGBoost":
            n_estimators = trial.suggest_categorical("n_estimators", [50, 100, 200])
            max_depth = trial.suggest_int("max_depth", 3, 7)
            learning_rate = trial.suggest_float("learning_rate", 0.01, 0.2, log=True)
            clf = XGBClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                eval_metric="logloss",
                random_state=42,
            )

        pipeline = build_pipeline(clf)

        score = cross_val_score(
            pipeline, x_train, y_train, cv=3, scoring="f1", n_jobs=-1
        ).mean()
        return score

    print(f"\n{'=' * 50}\n🚀 Lancement Optuna pour : {run_name}\n{'=' * 50}")

    study = optuna.create_study(direction="maximize")

    mlflow.sklearn.autolog(disable=True)

    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    print(f"\n🏆 Meilleurs paramètres trouvés : {best_params}")

    if model_type == "LogisticRegression":
        best_clf = LogisticRegression(C=best_params["C"], max_iter=1000)
    elif model_type == "RandomForest":
        best_clf = RandomForestClassifier(
            n_estimators=best_params["n_estimators"],
            max_depth=best_params["max_depth"],
            random_state=42,
        )
    elif model_type == "XGBoost":
        best_clf = XGBClassifier(
            n_estimators=best_params["n_estimators"],
            max_depth=best_params["max_depth"],
            learning_rate=best_params["learning_rate"],
            eval_metric="logloss",
            random_state=42,
        )

    best_pipeline = build_pipeline(best_clf)

    with mlflow.start_run(run_name=run_name):
        best_pipeline.fit(x_train, y_train)

        proba = best_pipeline.predict_proba(x_test)[:, 1]
        preds = (proba >= 0.5).astype(int)

        metrics = {
            "f1": float(f1_score(y_test, preds)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
        }
        print(
            f"📊 Scores sur le jeu de test -> f1: {metrics['f1']:.3f}, roc_auc: {metrics['roc_auc']:.3f}\n"
        )

        mlflow.log_params(best_params)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            best_pipeline,
            artifact_path="model",
            skops_trusted_types=["src.features.add_lol_synergies"],
        )


def main():
    df = load_data()
    x_train, x_test, y_train, y_test = split(df)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("League_of_Legends_Models")

    train_with_optuna(
        "LogisticRegression_Optuna",
        "LogisticRegression",
        x_train,
        y_train,
        x_test,
        y_test,
        n_trials=10,
    )
    train_with_optuna(
        "RandomForest_Optuna",
        "RandomForest",
        x_train,
        y_train,
        x_test,
        y_test,
        n_trials=10,
    )
    train_with_optuna(
        "XGBoost_Optuna", "XGBoost", x_train, y_train, x_test, y_test, n_trials=10
    )


if __name__ == "__main__":
    main()
