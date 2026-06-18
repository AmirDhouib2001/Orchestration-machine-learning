"""Frontend Streamlit : tester l'API de classification League of Legends.

L'URL de l'API est lue depuis la variable d'environnement API_URL.
"""
from __future__ import annotations

import os

from pathlib import Path

import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Prédiction LoL", layout="wide")
st.title("League of Legends - Prédiction de Victoire (Équipe Bleue) - par Amir DHOUIB")

with st.sidebar:
    st.header("🔗 Liens Utiles")
    st.link_button("📖 Voir le README (Projet GitHub)", "https://github.com/AmirDhouib2001/Orchestration-machine-learning#readme")
    st.link_button("📈 Dashboard MLflow", "http://158.178.195.9:5000")
    
    st.markdown("---")
    st.header("⚙️ API FastAPI")
    if st.button("Afficher les Endpoints"):
        st.session_state.show_api_details = not st.session_state.get("show_api_details", False)
        
    if st.session_state.get("show_api_details", False):
        st.info("""
        **Endpoints Disponibles :**
        - `GET /health` : Vérifie si l'API est en ligne.
        - `GET /model-info` : Retourne le modèle MLflow actuellement chargé en mémoire.
        - `POST /predict` : Reçoit les caractéristiques en JSON et retourne la prédiction.
        
        *(La documentation Swagger complète de l'API est accessible sur le port 8000 via `/docs`)*
        """)

api_url = st.text_input("URL de l'API (Réseau Interne Docker)", value=API_URL)

predict_tab, about_tab = st.tabs(["🔮 Prédiction", "📖 À Propos du Projet"])

with predict_tab:
    st.subheader("Saisir les statistiques de la partie (à 10 minutes)")

    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔵 Équipe Bleue")
            blueWardsPlaced = st.number_input("Wards Placées", min_value=0, value=15)
            blueWardsDestroyed = st.number_input("Wards Détruites", min_value=0, value=2)
            blueKills = st.number_input("Kills", min_value=0, value=5)
            blueDeaths = st.number_input("Morts", min_value=0, value=5)
            blueAssists = st.number_input("Assistances", min_value=0, value=5)
            blueTotalGold = st.number_input("Total Gold", min_value=0, value=15000)
            blueTotalExperience = st.number_input("Total Exp", min_value=0, value=15000)
            blueFirstBlood = st.selectbox("First Blood ?", [1, 0])
            blueDragons = st.selectbox("Dragons tués", [0, 1, 2])
            blueHeralds = st.selectbox("Hérauts tués", [0, 1])
            
        with col2:
            st.markdown("### 🔴 Équipe Rouge")
            redWardsPlaced = st.number_input("Wards Placées (Rouge)", min_value=0, value=15)
            redWardsDestroyed = st.number_input("Wards Détruites (Rouge)", min_value=0, value=2)
            redKills = st.number_input("Kills (Rouge)", min_value=0, value=5)
            redDeaths = st.number_input("Morts (Rouge)", min_value=0, value=5)
            redAssists = st.number_input("Assistances (Rouge)", min_value=0, value=5)
            redTotalGold = st.number_input("Total Gold (Rouge)", min_value=0, value=15000)
            redTotalExperience = st.number_input("Total Exp (Rouge)", min_value=0, value=15000)
            redFirstBlood = st.selectbox("First Blood ? (Rouge)", [0, 1])
            redDragons = st.selectbox("Dragons tués (Rouge)", [0, 1, 2])
            redHeralds = st.selectbox("Hérauts tués (Rouge)", [0, 1])
            
        # Variables calculées automatiquement (différences)
        blueGoldDiff = blueTotalGold - redTotalGold
        blueExperienceDiff = blueTotalExperience - redTotalExperience

        submitted = st.form_submit_button("Lancer la Prédiction 🔮")

    if submitted:
        payload = {
            "blueWardsPlaced": float(blueWardsPlaced),
            "blueWardsDestroyed": float(blueWardsDestroyed),
            "blueKills": float(blueKills),
            "blueDeaths": float(blueDeaths),
            "blueAssists": float(blueAssists),
            "blueTotalGold": float(blueTotalGold),
            "blueTotalExperience": float(blueTotalExperience),
            "blueGoldDiff": float(blueGoldDiff),
            "blueExperienceDiff": float(blueExperienceDiff),
            "redWardsPlaced": float(redWardsPlaced),
            "redWardsDestroyed": float(redWardsDestroyed),
            "redKills": float(redKills),
            "redDeaths": float(redDeaths),
            "redAssists": float(redAssists),
            "redTotalGold": float(redTotalGold),
            "redTotalExperience": float(redTotalExperience),
            "blueFirstBlood": int(blueFirstBlood),
            "blueDragons": int(blueDragons),
            "blueHeralds": int(blueHeralds),
            "redFirstBlood": int(redFirstBlood),
            "redDragons": int(redDragons),
            "redHeralds": int(redHeralds)
        }
        
        try:
            response = httpx.post(f"{api_url}/predict", json=payload, timeout=10.0)
            response.raise_for_status()
            result = response.json()
            
            st.markdown("---")
            st.subheader("Résultat de la Prédiction")
            
            col_res1, col_res2 = st.columns(2)
            
            # Affichage visuel du résultat (S14bis-3)
            if result["prediction"] == 1:
                col_res1.success("🏆 L'équipe BLEUE a le plus de chances de gagner !")
            else:
                col_res1.error("💀 L'équipe BLEUE va perdre (Victoire Rouge).")
                
            proba_bleue = result['probability']
            col_res2.metric("Probabilité de Victoire Bleue", f"{proba_bleue*100:.1f} %")
            st.progress(proba_bleue)
            
        except httpx.HTTPError as exc:
            st.error(f"Appel à l'API impossible : {exc}")

with about_tab:
    st.subheader("Informations sur le Projet")
    readme_path = Path(__file__).resolve().parents[1] / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("Le fichier README.md est introuvable à cet emplacement.")
