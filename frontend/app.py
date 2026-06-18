import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json

st.set_page_config(layout="wide", page_title="LoL Predictor", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    iframe {border: none; width: 100%; height: 100vh;}
</style>
""", unsafe_allow_html=True)

readme_path = Path(__file__).resolve().parents[1] / "README.md"
readme_content = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

# Safe JSON dump for the README content
readme_json = json.dumps(readme_content)

html_code = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>LoL Predictor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        html, body {{ margin: 0; padding: 0; height: 100%; }}
        body {{ background: #070A12; font-family: 'Barlow', system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
        input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {{ -webkit-appearance: none; margin: 0; }}
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,.09); border-radius: 8px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        @keyframes pulseDot {{ 0%, 100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
        [v-cloak] {{ display: none; }}
        
        .markdown-body {{
            color: #A8B0C2;
            font-size: 15px;
            line-height: 1.7;
        }}
        .markdown-body h1, .markdown-body h2, .markdown-body h3 {{
            color: #E6EAF2;
            font-family: 'Rajdhani', sans-serif;
            margin-top: 24px;
        }}
        .markdown-body a {{ color: #5FB0FF; text-decoration: none; }}
        .markdown-body a:hover {{ text-decoration: underline; }}
        .markdown-body code {{ background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }}
        .markdown-body pre {{ background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; overflow-x: auto; border: 1px solid rgba(255,255,255,0.05); }}
        .markdown-body pre code {{ background: transparent; padding: 0; }}
    </style>
</head>
<body>
<div id="app" v-cloak style="--accent: #C9A227; display: flex; height: 100vh; width: 100%; overflow: hidden; background: radial-gradient(1200px 700px at 78% -8%, rgba(46,155,255,.10), transparent 60%), radial-gradient(1000px 600px at 12% 110%, rgba(255,84,104,.08), transparent 55%), #070A12; color: #E6EAF2;">

  <!-- SIDEBAR -->
  <aside style="width: 262px; flex: none; height: 100%; display: flex; flex-direction: column; gap: 26px; padding: 26px 22px; background: linear-gradient(180deg,#0A0E1A,#080B14); border-right: 1px solid rgba(255,255,255,.06);">
    <div style="display: flex; align-items: center; gap: 11px;">
      <div style="width: 34px; height: 34px; border-radius: 9px; flex: none; background: linear-gradient(140deg, var(--accent, #C9A227), #7d6418); display: flex; align-items: center; justify-content: center; font-family: 'Rajdhani'; font-weight: 700; color: #0A0E1A; font-size: 17px;">LP</div>
      <div style="line-height: 1.1;">
        <div style="font-family: 'Rajdhani'; font-weight: 700; font-size: 15px; letter-spacing: .02em;">LoL Predictor</div>
        <div style="font-size: 11px; color: #7C859A;">Réalisé par Amir Dhouib</div>
      </div>
    </div>

    <div>
      <div style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #5C6679; margin-bottom: 11px;">Liens utiles</div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <a href="https://github.com/AmirDhouib2001/Orchestration-machine-learning" target="_blank" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 10px 13px; border-radius: 10px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.06); color: #C8D0E0; text-decoration: none; font-size: 13px; font-weight: 500;" onmouseover="this.style.background='rgba(255,255,255,.07)'; this.style.borderColor='rgba(255,255,255,.12)';" onmouseout="this.style.background='rgba(255,255,255,.035)'; this.style.borderColor='rgba(255,255,255,.06)';">README (GitHub)<span style="color: #5C6679;">↗</span></a>
        <a :href="mlflowUrl" target="_blank" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 10px 13px; border-radius: 10px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.06); color: #C8D0E0; text-decoration: none; font-size: 13px; font-weight: 500;" onmouseover="this.style.background='rgba(255,255,255,.07)'; this.style.borderColor='rgba(255,255,255,.12)';" onmouseout="this.style.background='rgba(255,255,255,.035)'; this.style.borderColor='rgba(255,255,255,.06)';">Dashboard MLflow<span style="color: #5C6679;">↗</span></a>
        <div style="position: relative;" @mouseover="showAirflowTooltip = true" @mouseleave="showAirflowTooltip = false">
            <a :href="airflowUrl" target="_blank" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 10px 13px; border-radius: 10px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.06); color: #C8D0E0; text-decoration: none; font-size: 13px; font-weight: 500;" onmouseover="this.style.background='rgba(255,255,255,.07)'; this.style.borderColor='rgba(255,255,255,.12)';" onmouseout="this.style.background='rgba(255,255,255,.035)'; this.style.borderColor='rgba(255,255,255,.06)';">Dashboard Airflow<span style="color: #5C6679;">↗</span></a>
            <div v-show="showAirflowTooltip" style="position: absolute; left: 105%; top: 50%; transform: translateY(-50%); background: #1C2333; color: #E6EAF2; padding: 6px 10px; border-radius: 6px; font-size: 11px; white-space: nowrap; border: 1px solid rgba(255,255,255,.1); box-shadow: 0 4px 12px rgba(0,0,0,.3); z-index: 100;">
                User: <strong>admin</strong><br>Pass: <strong>admin</strong>
            </div>
        </div>
      </div>
    </div>

    <div>
      <div style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #5C6679; margin-bottom: 11px;">API FastAPI</div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <a :href="swaggerUrl" target="_blank" style="display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 10px 13px; border-radius: 10px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.06); color: #C8D0E0; text-decoration: none; font-size: 13px; font-weight: 500;" onmouseover="this.style.background='rgba(255,255,255,.07)'; this.style.borderColor='rgba(255,255,255,.12)';" onmouseout="this.style.background='rgba(255,255,255,.035)'; this.style.borderColor='rgba(255,255,255,.06)';">Tester l'API (Swagger)<span style="color: #5C6679;">↗</span></a>
      </div>
    </div>

    <div style="margin-top: auto; padding: 13px; border-radius: 11px; background: rgba(46,155,255,.06); border: 1px solid rgba(46,155,255,.16);">
      <div style="font-size: 11px; color: #9FB6D6; line-height: 1.5;">Modèle entraîné sur les statistiques à <strong style="color: #fff;">10 minutes</strong> de parties classées.</div>
    </div>
  </aside>

  <main style="flex: 1; min-width: 0; height: 100%; overflow: auto;">

    <header style="padding: 34px 40px 0;">
      <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; flex-wrap: wrap;">
        <div>
          <div style="font-family: 'Rajdhani'; font-weight: 600; font-size: 12px; letter-spacing: .22em; text-transform: uppercase; color: var(--accent, #C9A227); margin-bottom: 8px;">League of Legends · Win Predictor</div>
          <h1 style="margin: 0; font-family: 'Rajdhani'; font-weight: 700; font-size: 38px; line-height: 1.05; letter-spacing: -.01em; color: #F2F5FB;">Prédiction de l'équipe gagnante</h1>
          <p style="margin: 9px 0 0; color: #8A93A6; font-size: 14px; max-width: 560px;">Saisissez les statistiques des deux équipes à la 10ᵉ minute. La probabilité de victoire se met à jour en temps réel.</p>
        </div>
        <div style="flex: none; width: 300px; max-width: 100%;">
          <label style="display: block; font-size: 11px; letter-spacing: .04em; text-transform: uppercase; color: #7C859A; font-weight: 600; margin-bottom: 7px;">URL de l'API (FastAPI)</label>
          <input v-model="apiUrl" style="width: 100%; height: 42px; padding: 0 14px; background: #0C1322; border: 1px solid rgba(255,255,255,.09); border-radius: 10px; color: #C8D0E0; font-family: 'IBM Plex Mono', monospace; font-size: 13px; outline: none;" onfocus="this.style.borderColor='var(--accent, #C9A227)';" onblur="this.style.borderColor='rgba(255,255,255,.09)';">
        </div>
      </div>

      <div style="display: flex; gap: 4px; margin-top: 24px; border-bottom: 1px solid rgba(255,255,255,.07);">
        <button @click="tab = 'prediction'" :style="tab === 'prediction' ? tabOn : tabBase">Prédiction</button>
        <button @click="tab = 'models'" :style="tab === 'models' ? tabOn : tabBase">Modèles Entraînés</button>
        <button @click="tab = 'about'" :style="tab === 'about' ? tabOn : tabBase">À propos du projet</button>
      </div>
    </header>

    <div v-if="tab === 'prediction'">
      <div style="position: sticky; top: 0; z-index: 6; padding: 18px 40px; background: rgba(8,11,20,.82); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,.07);">
        <div style="display: flex; align-items: center; gap: 28px;">
          <div style="flex: none; min-width: 120px;">
            <div style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #5FB0FF;">Équipe Bleue</div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-weight: 600; font-size: 32px; color: #5FB0FF; line-height: 1;">{{{{ bluePct }}}}%</div>
          </div>

          <div style="flex: 1; min-width: 0;">
            <div style="position: relative; height: 14px; border-radius: 999px; overflow: hidden; background: linear-gradient(90deg,#7a2b33,#FF5468); box-shadow: inset 0 0 0 1px rgba(255,255,255,.06);">
              <div :style="{{ width: bluePct + '%', position: 'absolute', left: 0, top: 0, bottom: 0, background: 'linear-gradient(90deg,#1F6FCB,#3FA0FF)', transition: 'width .45s cubic-bezier(.4,0,.2,1)' }}"></div>
              <div :style="{{ left: bluePct + '%', position: 'absolute', top: '-3px', bottom: '-3px', width: '2px', background: '#F2F5FB', boxShadow: '0 0 8px rgba(255,255,255,.7)', transition: 'left .45s cubic-bezier(.4,0,.2,1)' }}"></div>
            </div>
            <div style="display: flex; justify-content: center; margin-top: 11px;">
              <div style="display: flex; align-items: center; gap: 9px; padding: 6px 15px; border-radius: 999px; background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08);">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: var(--accent, #C9A227); animation: pulseDot 1.6s infinite;"></span>
                <span style="font-size: 13px; color: #C8D0E0;"><strong :style="{{ color: favoriteColor, fontWeight: 700 }}">{{{{ favoriteLabel }}}}</strong> favorite · {{{{ confidence }}}}% de confiance</span>
              </div>
            </div>
          </div>

          <div style="flex: none; min-width: 120px; text-align: right;">
            <div style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #FF7B88;">Équipe Rouge</div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-weight: 600; font-size: 32px; color: #FF7B88; line-height: 1;">{{{{ redPct }}}}%</div>
          </div>
        </div>
      </div>

      <div style="padding: 26px 40px 56px;">
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 18px; flex-wrap: wrap;">
          <h2 style="margin: 0; font-family: 'Rajdhani'; font-weight: 700; font-size: 20px; letter-spacing: .01em; color: #E6EAF2;">Statistiques de la partie <span style="color: #5C6679; font-weight: 600; font-size: 15px;">· à 10 minutes</span></h2>
          <div style="display: flex; gap: 9px;">
            <button v-if="error" style="height: 38px; padding: 0 16px; border-radius: 9px; background: rgba(255,84,104,.1); border: 1px solid rgba(255,84,104,.2); color: #FF5468; font-family: 'Barlow'; font-size: 13px; font-weight: 600;">⚠️ Erreur API</button>
            <button @click="loadExample" style="height: 38px; padding: 0 16px; border-radius: 9px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1); color: #C8D0E0; font-family: 'Barlow'; font-size: 13px; font-weight: 600; cursor: pointer;" onmouseover="this.style.background='rgba(255,255,255,.09)';" onmouseout="this.style.background='rgba(255,255,255,.05)';">Charger un exemple</button>
            <button @click="resetData" style="height: 38px; padding: 0 16px; border-radius: 9px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1); color: #C8D0E0; font-family: 'Barlow'; font-size: 13px; font-weight: 600; cursor: pointer;" onmouseover="this.style.background='rgba(255,255,255,.09)';" onmouseout="this.style.background='rgba(255,255,255,.05)';">Réinitialiser</button>
            <button @click="doPredict" style="height: 38px; padding: 0 20px; border-radius: 9px; background: var(--accent, #C9A227); border: none; color: #0A0E1A; font-family: 'Barlow'; font-size: 14px; font-weight: 700; cursor: pointer;">{{{{ loading ? 'Calcul...' : 'Prédire' }}}}</button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 22px;">

          <!-- ÉQUIPE BLEUE -->
          <section style="border-radius: 16px; padding: 22px; background: linear-gradient(180deg, rgba(31,111,203,.10), rgba(12,19,34,.6)); border: 1px solid rgba(63,160,255,.22); box-shadow: 0 22px 60px -30px rgba(63,160,255,.55);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <span style="width: 11px; height: 11px; border-radius: 50%; background: #3FA0FF; box-shadow: 0 0 10px #3FA0FF;"></span>
                <span style="font-family: 'Rajdhani'; font-weight: 700; font-size: 19px; letter-spacing: .02em; color: #9FCBFF;">Équipe Bleue</span>
              </div>
              <span style="font-family: 'IBM Plex Mono', monospace; font-size: 14px; color: #5FB0FF;">{{{{ bluePct }}}}%</span>
            </div>
            
            <div v-for="group in statGroups" :key="'b-'+group.title" style="margin-top: 16px;">
              <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 11px;">
                <span style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--accent, #C9A227);">{{{{ group.title }}}}</span>
                <span style="flex: 1; height: 1px; background: rgba(255,255,255,.07);"></span>
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 11px;">
                <div v-for="f in group.items" :key="'b-'+f.key" style="display: flex; flex-direction: column; gap: 6px;">
                  <span style="font-size: 11px; letter-spacing: .03em; text-transform: uppercase; color: #8A93A6; font-weight: 600;">{{{{ f.label }}}}</span>
                  <div style="display: flex; align-items: center; height: 40px; background: #0A1120; border: 1px solid rgba(255,255,255,.08); border-radius: 10px; overflow: hidden;">
                    <button @click="bump('blue', f.key, -(f.step||1))" style="width: 38px; height: 100%; flex: none; background: transparent; border: none; color: #8A93A6; font-size: 20px; cursor: pointer; line-height: 1;" onmouseover="this.style.background='rgba(255,255,255,.06)'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#8A93A6';">−</button>
                    <input type="number" v-model.number="blue[f.key]" style="flex: 1; min-width: 0; width: 100%; background: transparent; border: none; color: #E6EAF2; text-align: center; font-family: 'IBM Plex Mono', monospace; font-size: 15px; font-weight: 500; outline: none;">
                    <button @click="bump('blue', f.key, (f.step||1))" style="width: 38px; height: 100%; flex: none; background: transparent; border: none; color: #8A93A6; font-size: 18px; cursor: pointer; line-height: 1;" onmouseover="this.style.background='rgba(255,255,255,.06)'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#8A93A6';">+</button>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- ÉQUIPE ROUGE -->
          <section style="border-radius: 16px; padding: 22px; background: linear-gradient(180deg, rgba(203,40,56,.10), rgba(12,19,34,.6)); border: 1px solid rgba(255,84,104,.22); box-shadow: 0 22px 60px -30px rgba(255,84,104,.5);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <span style="width: 11px; height: 11px; border-radius: 50%; background: #FF5468; box-shadow: 0 0 10px #FF5468;"></span>
                <span style="font-family: 'Rajdhani'; font-weight: 700; font-size: 19px; letter-spacing: .02em; color: #FFB0B8;">Équipe Rouge</span>
              </div>
              <span style="font-family: 'IBM Plex Mono', monospace; font-size: 14px; color: #FF7B88;">{{{{ redPct }}}}%</span>
            </div>
            
            <div v-for="group in statGroups" :key="'r-'+group.title" style="margin-top: 16px;">
              <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 11px;">
                <span style="font-family: 'Rajdhani'; font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--accent, #C9A227);">{{{{ group.title }}}}</span>
                <span style="flex: 1; height: 1px; background: rgba(255,255,255,.07);"></span>
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 11px;">
                <div v-for="f in group.items" :key="'r-'+f.key" style="display: flex; flex-direction: column; gap: 6px;">
                  <span style="font-size: 11px; letter-spacing: .03em; text-transform: uppercase; color: #8A93A6; font-weight: 600;">{{{{ f.label }}}}</span>
                  <div style="display: flex; align-items: center; height: 40px; background: #0A1120; border: 1px solid rgba(255,255,255,.08); border-radius: 10px; overflow: hidden;">
                    <button @click="bump('red', f.key, -(f.step||1))" style="width: 38px; height: 100%; flex: none; background: transparent; border: none; color: #8A93A6; font-size: 20px; cursor: pointer; line-height: 1;" onmouseover="this.style.background='rgba(255,255,255,.06)'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#8A93A6';">−</button>
                    <input type="number" v-model.number="red[f.key]" style="flex: 1; min-width: 0; width: 100%; background: transparent; border: none; color: #E6EAF2; text-align: center; font-family: 'IBM Plex Mono', monospace; font-size: 15px; font-weight: 500; outline: none;">
                    <button @click="bump('red', f.key, (f.step||1))" style="width: 38px; height: 100%; flex: none; background: transparent; border: none; color: #8A93A6; font-size: 18px; cursor: pointer; line-height: 1;" onmouseover="this.style.background='rgba(255,255,255,.06)'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#8A93A6';">+</button>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>

    <div v-if="tab === 'models'" style="padding: 34px 40px 56px; max-width: 960px;">
      <h2 style="margin: 0 0 14px; font-family: 'Rajdhani'; font-weight: 700; font-size: 24px; color: #E6EAF2;">Modèles Entraînés (MLflow)</h2>
      
      <!-- Active Model -->
      <div style="margin-bottom: 24px; padding: 18px; border-radius: 12px; background: rgba(201,162,39,.1); border: 1px solid rgba(201,162,39,.3);">
         <h3 style="margin: 0 0 8px; font-family: 'Rajdhani'; color: var(--accent, #C9A227);">Modèle Actif (en production)</h3>
         <div v-if="activeModel" style="color: #E6EAF2; font-size: 15px;">
             <strong>Nom :</strong> {{{{ activeModel.model_name }}}}<br>
             <strong>F1-Score :</strong> {{{{ activeModel.f1_score.toFixed(4) }}}}
         </div>
         <div v-else style="color: #A8B0C2; font-size: 14px;">Chargement du modèle actif...</div>
      </div>
      
      <!-- All Models List -->
      <h3 style="margin: 0 0 12px; font-family: 'Rajdhani'; color: #E6EAF2;">Historique des entraînements</h3>
      <div v-if="modelsList.length > 0" style="background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.07); border-radius: 12px; overflow: hidden;">
          <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; color: #C8D0E0;">
              <thead>
                  <tr style="background: rgba(255,255,255,.05); border-bottom: 1px solid rgba(255,255,255,.1);">
                      <th style="padding: 12px 16px; font-weight: 600;">Nom du Modèle</th>
                      <th style="padding: 12px 16px; font-weight: 600;">F1-Score</th>
                      <th style="padding: 12px 16px; font-weight: 600;">Accuracy</th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="(m, i) in modelsList" :key="m.run_id" :style="i !== modelsList.length - 1 ? 'border-bottom: 1px solid rgba(255,255,255,.05);' : ''">
                      <td style="padding: 12px 16px; font-family: 'IBM Plex Mono', monospace; font-size: 13px;">{{{{ m.name }}}}</td>
                      <td style="padding: 12px 16px; color: #5FB0FF; font-weight: 600;">{{{{ m.f1_score.toFixed(4) }}}}</td>
                      <td style="padding: 12px 16px; color: #9FB6D6;">{{{{ m.accuracy.toFixed(4) }}}}</td>
                  </tr>
              </tbody>
          </table>
      </div>
      <div v-else style="color: #A8B0C2; font-size: 14px;">Chargement des modèles ou aucun modèle trouvé...</div>
    </div>

    <div v-if="tab === 'about'" style="padding: 34px 40px 56px; max-width: 960px;">
      <div class="markdown-body" v-html="parsedReadme"></div>
    </div>

  </main>
</div>

<script>
const {{ createApp, ref, computed, onMounted, watch }} = Vue;

const DEFAULTS = {{
  kills: 5, deaths: 5, assists: 5,
  gold: 15000, cs: 200, avgLevel: 6,
  towers: 0, dragons: 0, heralds: 0,
  wardsPlaced: 15, wardsDestroyed: 2,
  firstBlood: 0
}};

const EXAMPLE_BLUE = {{ kills: 8, deaths: 3, assists: 11, gold: 17200, cs: 225, avgLevel: 7, towers: 2, dragons: 1, heralds: 1, wardsPlaced: 19, wardsDestroyed: 4, firstBlood: 1 }};
const EXAMPLE_RED  = {{ kills: 3, deaths: 8, assists: 4, gold: 14600, cs: 198, avgLevel: 6, towers: 0, dragons: 0, heralds: 0, wardsPlaced: 13, wardsDestroyed: 1, firstBlood: 0 }};

const STAT_GROUPS = [
  {{ title: 'Combat',    items: [ {{key: 'kills', label: 'Kills'}}, {{key: 'deaths', label: 'Morts'}}, {{key: 'assists', label: 'Assistances'}} ] }},
  {{ title: 'Économie',  items: [ {{key: 'gold', label: 'Or total', step: 500}}, {{key: 'cs', label: 'CS (minions)', step: 5}}, {{key: 'avgLevel', label: 'Niveau moyen'}} ] }},
  {{ title: 'Objectifs', items: [ {{key: 'towers', label: 'Tours détruites'}}, {{key: 'dragons', label: 'Dragons'}}, {{key: 'heralds', label: 'Hérauts'}}, {{key: 'firstBlood', label: 'Premier Sang (0=Non, 1=Oui)'}} ] }},
  {{ title: 'Vision',    items: [ {{key: 'wardsPlaced', label: 'Wards placées'}}, {{key: 'wardsDestroyed', label: 'Wards détruites'}} ] }},
];

// Inject the README markdown string
const rawReadme = {readme_json};

createApp({{
  setup() {{
    const tab = ref('prediction');
    const apiUrl = ref('http://localhost:8000');
    const blue = ref({{ ...DEFAULTS, firstBlood: 1 }});
    const red = ref({{ ...DEFAULTS }});
    
    const bluePct = ref(50);
    const redPct = ref(50);
    const loading = ref(false);
    const error = ref(false);
    
    const activeModel = ref(null);
    const modelsList = ref([]);
    
    const parsedReadme = computed(() => marked.parse(rawReadme));
    
    const fetchModelsData = async () => {{
        try {{
            const resInfo = await fetch(`${{apiUrl.value}}/model-info`);
            if (resInfo.ok) {{
                activeModel.value = await resInfo.json();
            }}
            
            const resModels = await fetch(`${{apiUrl.value}}/models`);
            if (resModels.ok) {{
                const data = await resModels.json();
                modelsList.value = data.models || [];
            }}
        }} catch (e) {{
            console.error("Erreur chargement MLflow:", e);
        }}
    }};
    
    onMounted(() => {{
        // Get the host from the parent window if possible, else fallback to window.location
        let host = 'localhost';
        try {{
            host = window.parent.location.hostname || window.location.hostname || 'localhost';
        }} catch (e) {{
            host = window.location.hostname || 'localhost';
        }}
        apiUrl.value = `http://${{host}}:8000`;
        
        fetchModelsData();
    }});

    const statGroups = STAT_GROUPS;

    const bump = (team, key, delta) => {{
      const obj = team === 'blue' ? blue.value : red.value;
      obj[key] = Math.max(0, (Number(obj[key]) || 0) + delta);
    }};

    const doPredict = async () => {{
        loading.value = true;
        error.value = false;
        
        const payload = {{
            blueWardsPlaced: blue.value.wardsPlaced,
            blueWardsDestroyed: blue.value.wardsDestroyed,
            blueKills: blue.value.kills,
            blueDeaths: blue.value.deaths,
            blueAssists: blue.value.assists,
            blueTotalGold: blue.value.gold,
            blueTotalExperience: blue.value.gold, 
            blueGoldDiff: blue.value.gold - red.value.gold,
            blueExperienceDiff: (blue.value.avgLevel - red.value.avgLevel) * 1000,
            redWardsPlaced: red.value.wardsPlaced,
            redWardsDestroyed: red.value.wardsDestroyed,
            redKills: red.value.kills,
            redDeaths: red.value.deaths,
            redAssists: red.value.assists,
            redTotalGold: red.value.gold,
            redTotalExperience: red.value.gold,
            blueFirstBlood: blue.value.firstBlood,
            blueDragons: blue.value.dragons,
            blueHeralds: blue.value.heralds,
            redFirstBlood: red.value.firstBlood,
            redDragons: red.value.dragons,
            redHeralds: red.value.heralds
        }};

        try {{
            const res = await fetch(`${{apiUrl.value}}/predict`, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }});
            if (!res.ok) throw new Error('API Error');
            const data = await res.json();
            const pBlue = data.probability;
            bluePct.value = Math.round(pBlue * 100);
            redPct.value = 100 - bluePct.value;
        }} catch (e) {{
            console.error(e);
            error.value = true;
            calculateDummyScore();
        }} finally {{
            loading.value = false;
        }}
    }};
    
    const calculateDummyScore = () => {{
        const b = blue.value;
        const r = red.value;
        const score =
            0.00085 * (b.gold - r.gold)
          + 0.55    * (b.avgLevel - r.avgLevel)
          + 0.016   * (b.cs - r.cs)
          + 0.16    * (b.kills - r.kills)
          + 0.10    * (r.deaths - b.deaths)
          + 0.04    * (b.assists - r.assists)
          + 0.55    * (b.towers - r.towers)
          + 0.75    * (b.dragons - r.dragons)
          + 0.55    * (b.heralds - r.heralds)
          + 0.03    * (b.wardsPlaced - r.wardsPlaced)
          + 0.05    * (b.wardsDestroyed - r.wardsDestroyed);

        const p = 1 / (1 + Math.exp(-score));
        bluePct.value = Math.round(p * 100);
        redPct.value = 100 - bluePct.value;
    }};

    const resetData = () => {{
      blue.value = {{ ...DEFAULTS, firstBlood: 1 }};
      red.value = {{ ...DEFAULTS, firstBlood: 0 }};
      bluePct.value = 50;
      redPct.value = 50;
    }};

    const loadExample = () => {{
      blue.value = {{ ...EXAMPLE_BLUE }};
      red.value = {{ ...EXAMPLE_RED }};
      doPredict();
    }};

    const blueFav = computed(() => bluePct.value >= 50);
    const confidence = computed(() => Math.max(bluePct.value, redPct.value));
    const favoriteLabel = computed(() => blueFav.value ? 'Équipe Bleue' : 'Équipe Rouge');
    const favoriteColor = computed(() => blueFav.value ? '#5FB0FF' : '#FF7B88');

    const tabBase = "height: 42px; padding: 0 18px; background: transparent; border: none; border-bottom: 2px solid transparent; margin-bottom: -1px; font-family: 'Rajdhani'; font-weight: 700; font-size: 15px; letter-spacing: .03em; cursor: pointer; color: #7C859A;";
    const tabOn = "height: 42px; padding: 0 18px; background: transparent; border: none; border-bottom: 2px solid var(--accent, #C9A227); margin-bottom: -1px; font-family: 'Rajdhani'; font-weight: 700; font-size: 15px; letter-spacing: .03em; cursor: pointer; color: #F2F5FB;";

    const mlflowUrl = computed(() => {{
        let host = 'localhost';
        try {{ host = window.parent.location.hostname || window.location.hostname || 'localhost'; }} catch (e) {{ host = window.location.hostname || 'localhost'; }}
        return `http://${{host}}:5000`;
    }});
    
    const swaggerUrl = computed(() => {{
        let host = 'localhost';
        try {{ host = window.parent.location.hostname || window.location.hostname || 'localhost'; }} catch (e) {{ host = window.location.hostname || 'localhost'; }}
        return `http://${{host}}:8000/docs`;
    }});

    const airflowUrl = computed(() => {{
        let host = 'localhost';
        try {{ host = window.parent.location.hostname || window.location.hostname || 'localhost'; }} catch (e) {{ host = window.location.hostname || 'localhost'; }}
        return `http://${{host}}:8080`;
    }});
    
    const showAirflowTooltip = ref(false);

    return {{
      tab, apiUrl, blue, red,
      bluePct, redPct, loading, error,
      statGroups, activeModel, modelsList,
      bump, doPredict, resetData, loadExample,
      blueFav, confidence, favoriteLabel, favoriteColor,
      tabBase, tabOn, mlflowUrl, swaggerUrl, airflowUrl, showAirflowTooltip, parsedReadme
    }};
  }}
}}).mount('#app');
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
