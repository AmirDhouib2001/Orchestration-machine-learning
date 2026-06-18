"""Frontend Streamlit : tester l'API de classification League of Legends.

L'URL de l'API est lue depuis la variable d'environnement API_URL.
"""
from __future__ import annotations

import os
from pathlib import Path
import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Prediction LoL", layout="wide")

# Injection de CSS pour le theme League of Legends
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cinzel', serif;
        color: #C89B3C !important;
        text-shadow: 1px 1px 2px #000000;
    }
    
    .stApp {
        background-color: #0A1428;
        color: #F0E6D2;
    }
    
    .stButton>button {
        background-color: #1E2328;
        color: #C89B3C;
        border: 2px solid #C89B3C;
        border-radius: 0px;
        font-family: 'Cinzel', serif;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #C89B3C;
        color: #0A1428;
        border-color: #F0E6D2;
        box-shadow: 0 0 10px #C89B3C;
    }
    
    .stTextInput>div>div>input {
        background-color: #010A13;
        color: #F0E6D2;
        border: 1px solid #785A28;
    }
    
    .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #010A13;
        color: #F0E6D2;
        border: 1px solid #785A28;
    }
    
    .sidebar .sidebar-content {
        background-color: #010A13;
        border-right: 2px solid #785A28;
    }
    
    hr {
        border-color: #785A28;
    }
    
    .success-text {
        color: #00BFFF;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .error-text {
        color: #FF4500;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("League of Legends - Prediction de Victoire - par Amir DHOUIB")

with st.sidebar:
    st.markdown("### Realise par : Amir DHOUIB")
    st.markdown("---")
    
    st.header("Liens Utiles")
    st.link_button("Voir le README (Projet GitHub)", "https://github.com/AmirDhouib2001/Orchestration-machine-learning#readme")
    st.link_button("Dashboard MLflow", "http://158.178.195.9:5000")
    
    st.markdown("---")
    st.header("API FastAPI")
    st.link_button("Tester l'API (Swagger UI)", "http://158.178.195.9:8000/docs")
    if st.button("Afficher les Endpoints"):
        st.session_state.show_api_details = not st.session_state.get("show_api_details", False)
        
    if st.session_state.get("show_api_details", False):
        st.info("""
        **Endpoints Disponibles :**
        - `GET /health` : Verifie si l'API est en ligne.
        - `GET /model-info` : Retourne le modele MLflow actuellement charge.
        - `POST /predict` : Recoit les caracteristiques en JSON et retourne la prediction.
        
        *(La documentation Swagger complete de l'API est accessible sur le port 8000 via `/docs`)*
        """)

api_url = st.text_input("URL de l'API (Reseau Interne Docker)", value=API_URL)

predict_tab, about_tab = st.tabs(["Prediction", "A Propos du Projet"])

with predict_tab:
    st.subheader("Saisir les statistiques de la partie (a 10 minutes)")

    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='color: #00BFFF !important;'>Equipe Bleue</h3>", unsafe_allow_html=True)
            blueWardsPlaced = st.number_input("Wards Placees", min_value=0, value=15)
            blueWardsDestroyed = st.number_input("Wards Detruites", min_value=0, value=2)
            blueKills = st.number_input("Kills", min_value=0, value=5)
            blueDeaths = st.number_input("Morts", min_value=0, value=5)
            blueAssists = st.number_input("Assistances", min_value=0, value=5)
            blueTotalGold = st.number_input("Total Gold", min_value=0, value=15000)
            blueTotalExperience = st.number_input("Total Exp", min_value=0, value=15000)
            blueFirstBlood = st.selectbox("First Blood ?", [1, 0])
            blueDragons = st.selectbox("Dragons tues", [0, 1, 2])
            blueHeralds = st.selectbox("Herauts tues", [0, 1])
            
        with col2:
            st.markdown("<h3 style='color: #FF4500 !important;'>Equipe Rouge</h3>", unsafe_allow_html=True)
            redWardsPlaced = st.number_input("Wards Placees (Rouge)", min_value=0, value=15)
            redWardsDestroyed = st.number_input("Wards Detruites (Rouge)", min_value=0, value=2)
            redKills = st.number_input("Kills (Rouge)", min_value=0, value=5)
            redDeaths = st.number_input("Morts (Rouge)", min_value=0, value=5)
            redAssists = st.number_input("Assistances (Rouge)", min_value=0, value=5)
            redTotalGold = st.number_input("Total Gold (Rouge)", min_value=0, value=15000)
            redTotalExperience = st.number_input("Total Exp (Rouge)", min_value=0, value=15000)
            redFirstBlood = st.selectbox("First Blood ? (Rouge)", [0, 1])
            redDragons = st.selectbox("Dragons tues (Rouge)", [0, 1, 2])
            redHeralds = st.selectbox("Herauts tues (Rouge)", [0, 1])
            
        blueGoldDiff = blueTotalGold - redTotalGold
        blueExperienceDiff = blueTotalExperience - redTotalExperience

        submitted = st.form_submit_button("Lancer la Prediction")

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
            st.subheader("Resultat de la Prediction")
            
            col_res1, col_res2 = st.columns(2)
            
            if result["prediction"] == 1:
                col_res1.markdown("<p class='success-text'>VICTOIRE : L'equipe BLEUE a le plus de chances de gagner.</p>", unsafe_allow_html=True)
            else:
                col_res1.markdown("<p class='error-text'>DEFAITE : L'equipe BLEUE va perdre (Victoire Rouge).</p>", unsafe_allow_html=True)
                
            proba_bleue = result['probability']
            col_res2.metric("Probabilite de Victoire Bleue", f"{proba_bleue*100:.1f} %")
            st.progress(proba_bleue)
            
        except httpx.HTTPError as exc:
            st.error(f"Appel a l'API impossible : {exc}")

with about_tab:
    st.subheader("Informations sur le Projet")
    readme_path = Path(__file__).resolve().parents[1] / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("Le fichier README.md est introuvable.")
