"""DAG Airflow - pipeline de re-entrainement du modele (squelette).

Seance 17 - TP Airflow
    Pipeline simple : preparation des donnees -> entrainement -> controle
    qualite. Completez les TODO (S17-n).
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)

# f1 minimal du modele entraine pour que le pipeline soit considere comme reussi.
QUALITY_THRESHOLD = 0.65

default_args = {
    "owner": "data-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def task_prepare_data(**context) -> None:
    from src.data import load_data
    load_data()
    logger.info("Données préparées et vérifiées avec succès.")


def task_train(**context) -> None:
    import os
    os.environ["MLFLOW_TRACKING_URI"] = "http://158.178.195.9:5000"
    os.environ["MLFLOW_EXPERIMENT"] = "League_of_Legends_Models"
    
    from src.train import train
    metrics = train()
    context["ti"].xcom_push(key="f1", value=metrics["f1"])


def task_check_quality(**context) -> None:
    f1 = context["ti"].xcom_pull(task_ids="train", key="f1")
    if f1 < QUALITY_THRESHOLD:
        raise ValueError(f"Qualité insuffisante: f1={f1:.3f} < seuil {QUALITY_THRESHOLD}")
    logger.info(f"Qualité OK : f1={f1:.3f}")


with DAG(
    dag_id="model_retraining",
    description="Prepare les donnees, reentraine le modele et controle sa qualite",
    schedule="0 3 * * 1",  # Tous les lundis à 3h du matin
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["classification", "training"],
) as dag:
    prepare = PythonOperator(task_id="prepare_data", python_callable=task_prepare_data)
    train_task = PythonOperator(task_id="train", python_callable=task_train)
    check = PythonOperator(task_id="check_quality", python_callable=task_check_quality)

    prepare >> train_task >> check
