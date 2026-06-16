"""Client de test pour interroger l'API FastAPI (League of Legends)."""

from __future__ import annotations

import argparse
import json
import logging
import httpx

from src.config import TARGET
from src.data import load_data

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

N_SAMPLES = 3
DEFAULT_API_URL = "http://127.0.0.1:8000"


def build_payloads(n: int = N_SAMPLES) -> list[dict]:
    """Extrait n exemples au hasard du jeu de données pour tester l'API."""
    logger.info("Chargement du jeu de données pour extraire des exemples...")
    df = load_data()

    # On retire la variable cible (blueWins) car c'est ce que l'API doit deviner !
    features = df.drop(columns=[TARGET])
    sample = features.sample(n=n, random_state=42)

    return [json.loads(row.to_json()) for _, row in sample.iterrows()]


def main() -> None:
    """Point d'entrée principal du client."""
    parser = argparse.ArgumentParser(description="Test client pour l'API LoL")
    parser.add_argument(
        "--url",
        default=DEFAULT_API_URL,
        help="URL de base de l'API (ex: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()

    payloads = build_payloads()

    logger.info("Connexion à l'API sur %s ...", args.url)
    with httpx.Client(base_url=args.url, timeout=10.0) as client:
        # 1. Vérification de la santé de l'API (Endpoint /health)
        try:
            health = client.get("/health")
            logger.info("✅ GET /health -> %s %s", health.status_code, health.json())
        except httpx.ConnectError:
            logger.error(
                "❌ Impossible de contacter l'API. N'oublie pas de lancer 'uvicorn src.api:app --reload' dans un autre terminal !"
            )
            return

        # 2. Vérification du modèle chargé (Endpoint /model-info)
        info = client.get("/model-info")
        logger.info("🧠 GET /model-info -> %s %s", info.status_code, info.json())

        # 3. Test de prédiction sur les exemples extraits (Endpoint /predict)
        print("\n" + "-" * 50)
        for i, payload in enumerate(payloads, 1):
            response = client.post("/predict", json=payload)

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    f"🔮 PRÉDICTION #{i} : {data['message']} (Proba: {data['probability']:.1%})"
                )
            else:
                logger.error(
                    f"❌ Erreur de prédiction #{i} : {response.status_code} {response.text}"
                )
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
