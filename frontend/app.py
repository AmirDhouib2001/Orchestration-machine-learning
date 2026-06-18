"""Frontend Streamlit : tester l'API de classification League of Legends.

L'URL de l'API est lue depuis la variable d'environnement API_URL.
"""
from __future__ import annotations

import os
from pathlib import Path
import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LoL Predictor", layout="wide", initial_sidebar_state="expanded")

# Injection de CSS pour le theme League of Legends moderne (Copie de la maquette)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@300;400;600&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b111a !important; /* Fond tres sombre */
        color: #A0AEC0;
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: #121824 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Text Input (API URL) */
    .stTextInput>div>div>input {
        background-color: #1a2332;
        color: #FFFFFF;
        border: 1px solid #2d3748;
        border-radius: 6px;
        font-family: monospace;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px 0px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #A0AEC0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF;
        border-bottom: 3px solid #C89B3C !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1a2332;
        color: #A0AEC0;
        border: 1px solid #2d3748;
        border-radius: 6px;
        transition: all 0.2s ease;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        border-color: #C89B3C;
        color: #C89B3C;
        background-color: rgba(200, 155, 60, 0.1);
    }
    
    /* Primary Submit Button */
    [data-testid="stFormSubmitButton"]>button {
        background: linear-gradient(90deg, #005a82 0%, #0088c2 100%);
        color: white;
        border: none;
        font-weight: 600;
        font-size: 16px;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 15px;
    }
    [data-testid="stFormSubmitButton"]>button:hover {
        background: linear-gradient(90deg, #0088c2 0%, #005a82 100%);
        color: white;
        box-shadow: 0 0 15px rgba(0, 191, 255, 0.4);
        border: none;
    }
    
    /* Link buttons in sidebar */
    a[data-testid="baseLinkButton"] {
        width: 100%;
    }
    a[data-testid="baseLinkButton"] > p {
        width: 100%;
    }
    
    /* Number Inputs */
    .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #121824;
        color: #FFFFFF;
        border: 1px solid #1e293b;
        border-radius: 6px;
    }
    
    /* Section Titles in forms */
    .category-title {
        color: #C89B3C;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: -15px;
    }
    
    /* Gold accent button for Swagger */
    .gold-btn > button {
        border-color: #C89B3C !important;
        color: #C89B3C !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 40px; margin-top: 10px;">
        <div style="background: linear-gradient(135deg, #C89B3C 0%, #785A28 100%); color: #0A1428; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 20px; font-family: 'Inter', sans-serif;">LP</div>
        <div>
            <div style="font-weight: 800; font-size: 16px; color: #FFFFFF; letter-spacing: 0.5px;">LoL Predictor</div>
            <div style="font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px;">Realise par Amir Dhouib</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 11px; font-weight: 600; color: #718096; letter-spacing: 1px; margin-bottom: 10px;'>LIENS UTILES</div>", unsafe_allow_html=True)
    st.link_button("README (GitHub)", "https://github.com/AmirDhouib2001/Orchestration-machine-learning#readme")
    st.link_button("Dashboard MLflow", "http://158.178.195.9:5000")
    
    st.markdown("<br><div style='font-size: 11px; font-weight: 600; color: #718096; letter-spacing: 1px; margin-bottom: 10px;'>API FASTAPI</div>", unsafe_allow_html=True)
    st.link_button("Tester l'API (Swagger)", "http://158.178.195.9:8000/docs")
    
    st.markdown("<div class='gold-btn'>", unsafe_allow_html=True)
    if st.button("Afficher les endpoints"):
        st.session_state.show_api_details = not st.session_state.get("show_api_details", False)
    st.markdown("</div>", unsafe_allow_html=True)
        
    if st.session_state.get("show_api_details", False):
        st.info("""
        **Endpoints Disponibles :**
        - `GET /health` : Verifie si l'API est en ligne.
        - `GET /model-info` : Retourne le modele MLflow.
        - `POST /predict` : Prediction.
        """)

# ----------------- HEADER -----------------
col_title, col_api = st.columns([3, 1])
with col_title:
    st.markdown("<div style='font-size: 12px; color: #C89B3C; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;'>League of Legends - Win Predictor</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top: -10px; font-size: 36px;'>Prediction de l'equipe gagnante</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color: #718096; font-size: 14px; margin-bottom: 30px;'>Saisissez les statistiques des deux equipes a la 10e minute. La probabilite de victoire se mettra a jour apres lancement.</div>", unsafe_allow_html=True)

with col_api:
    st.markdown("<div style='font-size: 10px; color: #718096; text-transform: uppercase; font-weight: 600; margin-bottom: 5px;'>URL de l'API (Reseau Docker)</div>", unsafe_allow_html=True)
    api_url = st.text_input("API", value=API_URL, label_visibility="collapsed")

predict_tab, about_tab = st.tabs(["Prediction", "A propos du projet"])

with predict_tab:
    
    # Espace reserve pour le resultat de la prediction (Top Bar)
    result_container = st.empty()
    
    # Ligne d'en-tete pour les statistiques
    st.markdown("""
        <div style='margin-top: 30px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;'>
            <div style='font-size: 18px; font-weight: 600; color: #FFFFFF;'>Statistiques de la partie <span style='color: #718096; font-weight: 400; font-size: 14px;'>a 10 minutes</span></div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("predict_form"):
        col1, col2 = st.columns(2)
        
        # --- EQUIPE BLEUE ---
        with col1:
            st.markdown("""
                <div style='background: linear-gradient(180deg, rgba(0, 140, 255, 0.05) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(0, 140, 255, 0.2); border-radius: 12px; padding: 25px; box-shadow: 0 0 30px rgba(0, 140, 255, 0.02);'>
                    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
                        <div style='width: 10px; height: 10px; border-radius: 50%; background-color: #008CFF; box-shadow: 0 0 10px #008CFF;'></div>
                        <div style='font-size: 18px; font-weight: 600; color: #FFFFFF;'>Equipe Bleue</div>
                    </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='category-title'>Combat</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            blueKills = c1.number_input("KILLS", min_value=0, value=5, key="bk")
            blueDeaths = c2.number_input("MORTS", min_value=0, value=5, key="bd")
            blueAssists = st.number_input("ASSISTANCES", min_value=0, value=5, key="ba")
            
            st.markdown("<div class='category-title'>Economie</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            blueTotalGold = c1.number_input("OR TOTAL", min_value=0, value=15000, key="bg")
            blueTotalExperience = c2.number_input("EXP TOTAL", min_value=0, value=15000, key="bexp")
            blueFirstBlood = st.selectbox("PREMIER SANG (FIRST BLOOD)", [1, 0], key="bfb")
            
            st.markdown("<div class='category-title'>Objectifs</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            blueDragons = c1.selectbox("DRAGONS", [0, 1, 2], key="bdr")
            blueHeralds = c2.selectbox("HERAUTS", [0, 1], key="bh")
            
            st.markdown("<div class='category-title'>Vision</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            blueWardsPlaced = c1.number_input("WARDS PLACEES", min_value=0, value=15, key="bwp")
            blueWardsDestroyed = c2.number_input("WARDS DETRUITES", min_value=0, value=2, key="bwd")
            
            st.markdown("</div>", unsafe_allow_html=True)

        # --- EQUIPE ROUGE ---
        with col2:
            st.markdown("""
                <div style='background: linear-gradient(180deg, rgba(255, 70, 85, 0.05) 0%, rgba(0,0,0,0) 100%); border: 1px solid rgba(255, 70, 85, 0.2); border-radius: 12px; padding: 25px; box-shadow: 0 0 30px rgba(255, 70, 85, 0.02);'>
                    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
                        <div style='width: 10px; height: 10px; border-radius: 50%; background-color: #FF4655; box-shadow: 0 0 10px #FF4655;'></div>
                        <div style='font-size: 18px; font-weight: 600; color: #FFFFFF;'>Equipe Rouge</div>
                    </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='category-title'>Combat</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            redKills = c1.number_input("KILLS", min_value=0, value=5, key="rk")
            redDeaths = c2.number_input("MORTS", min_value=0, value=5, key="rd")
            redAssists = st.number_input("ASSISTANCES", min_value=0, value=5, key="ra")
            
            st.markdown("<div class='category-title'>Economie</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            redTotalGold = c1.number_input("OR TOTAL", min_value=0, value=15000, key="rg")
            redTotalExperience = c2.number_input("EXP TOTAL", min_value=0, value=15000, key="rexp")
            redFirstBlood = st.selectbox("PREMIER SANG (FIRST BLOOD)", [0, 1], key="rfb")
            
            st.markdown("<div class='category-title'>Objectifs</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            redDragons = c1.selectbox("DRAGONS", [0, 1, 2], key="rdr")
            redHeralds = c2.selectbox("HERAUTS", [0, 1], key="rh")
            
            st.markdown("<div class='category-title'>Vision</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            redWardsPlaced = c1.number_input("WARDS PLACEES", min_value=0, value=15, key="rwp")
            redWardsDestroyed = c2.number_input("WARDS DETRUITES", min_value=0, value=2, key="rwd")
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("LANCER LA PREDICTION")

    if submitted:
        blueGoldDiff = blueTotalGold - redTotalGold
        blueExperienceDiff = blueTotalExperience - redTotalExperience
        
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
            
            proba_bleue = result['probability']
            proba_rouge = 1.0 - proba_bleue
            
            # Injection de la progress bar dans le result_container tout en haut
            html_bar = f"""
            <div style="background-color: #121824; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; justify-content: space-between; font-family: 'Teko', sans-serif; margin-bottom: 5px;">
                    <span style="color: #008CFF; font-size: 20px; font-weight: 600; letter-spacing: 1px;">EQUIPE BLEUE<br><span style="font-size: 32px;">{proba_bleue*100:.0f}%</span></span>
                    <span style="color: #FF4655; font-size: 20px; font-weight: 600; text-align: right; letter-spacing: 1px;">EQUIPE ROUGE<br><span style="font-size: 32px;">{proba_rouge*100:.0f}%</span></span>
                </div>
                <div style="width: 100%; height: 12px; background-color: #FF4655; border-radius: 6px; overflow: hidden; display: flex; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);">
                    <div style="width: {proba_bleue*100}%; height: 100%; background-color: #008CFF; transition: width 0.5s ease-in-out; border-right: 2px solid #ffffff;"></div>
                </div>
                <div style="text-align: center; margin-top: 15px; color: #A0AEC0; font-size: 14px;">
                    <span style="color: {'#008CFF' if proba_bleue > 0.5 else '#FF4655'};">&#x25CF;</span> 
                    <b>{'Equipe Bleue' if proba_bleue > 0.5 else 'Equipe Rouge'}</b> favorite - {max(proba_bleue, proba_rouge)*100:.0f}% de confiance
                </div>
            </div>
            """
            result_container.markdown(html_bar, unsafe_allow_html=True)
            
        except httpx.HTTPError as exc:
            st.error(f"Erreur API : {exc}")

with about_tab:
    st.subheader("Informations sur le Projet")
    readme_path = Path(__file__).resolve().parents[1] / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.warning("Le fichier README.md est introuvable.")
