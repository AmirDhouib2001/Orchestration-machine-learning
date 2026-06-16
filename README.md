# Projet d'Orchestration MLOps : Prédiction de Victoire sur League of Legends

## Le Dataset : League of Legends (High Diamond 10min)

Pour ce projet de classification binaire, j'ai choisi le monde de l'e-sport et plus particulièrement le jeu vidéo **League of Legends (LoL)**.

### Quelle est la problématique ?
Dans une partie de LoL, deux équipes de 5 joueurs s'affrontent (l'équipe **Bleue** contre l'équipe **Rouge**). Les parties durent souvent 30 à 45 minutes, mais les premières minutes sont souvent décisives.

**Notre question :** *Peut-on deviner à 100% quelle équipe va gagner la partie simplement en regardant les statistiques à la minute 10 ?*

### De quoi s'agit-il dans les données ?
Le jeu de données regroupe environ 10 000 parties jouées par les meilleurs joueurs du monde (niveau Diamant/Master). Toutes les données sont arrêtées exactement à **10 minutes de jeu**.

* **La Cible (Ce qu'on veut prédire) :** `blueWins`
  * `1` = L'équipe Bleue finit par remporter la partie entière.
  * `0` = L'équipe Rouge finit par remporter la partie entière.

* **Les Variables (Les indices utilisés par notre modèle) :**
  Pour prédire la victoire, le modèle regarde la situation des deux équipes à la minute 10. Parmi les variables principales, on retrouve :
  - **L'économie :** `blueTotalGold`, `redTotalGold` (l'argent amassé par l'équipe).
  - **Les Kills :** `blueKills`, `redKills` (les éliminations des adversaires).
  - **L'expérience :** `blueTotalExperience` (la progression des personnages).
  - **La vision du jeu :** `blueWardsPlaced` (les balises de vision posées sur la carte).
  - **Les objectifs :** `blueDragons`, `blueFirstBlood` (les monstres ou le premier kill récupérés).

---

## Le Workflow Technique (Pipeline)

Pour mener ce projet à bien, voici la "Stack technique" mise en place au fil des séances :

1. **MLflow :** Pour garder une trace de chaque entraînement, comparer les modèles (ex: Random Forest vs XGBoost) et conserver le meilleur (Model Registry).
2. **Optuna :** Pour exécuter des centaines d'entraînements automatiquement afin de trouver la configuration parfaite.
3. **Docker :** Pour conteneuriser le code et garantir qu'il s'exécute toujours de la même façon.
4. **FastAPI & Streamlit :** Pour créer une API et un site web permettant aux utilisateurs d'entrer les statistiques d'une partie et d'obtenir une prédiction en direct.
5. **Airflow :** Pour planifier une routine qui ré-entraîne le modèle tous les lundis avec de potentielles nouvelles données.

---

## Avancement du Projet

### Configuration et Préparation des Données
- Mise en place d'un environnement virtuel Python propre et gestion des dépendances via `uv`.
- Création d'un dossier `src/` pour centraliser la logique métier.
- Configuration du projet (`config.py`) pour intégrer le dataset League of Legends.
- `data.py` : Chargement, nettoyage des doublons, suppression de l'identifiant inutile (`gameId`) et séparation Train/Test.
- `features.py` : Création d'un `Pipeline` pour ajouter des synergies métier (Gold*XP, etc.) avant de standardiser les données (`StandardScaler`, `OneHotEncoder`).

### Entraînement Baseline (MLflow)
- **`train.py`** : Entraînement d'un premier modèle simple (`LogisticRegression`) avec suivi **MLflow** (enregistrement des paramètres, des scores et sauvegarde de la matrice de confusion en image).

### Optimisation par Grille (GridSearchCV)
- **`train_models.py`** : Entraînement de 3 modèles (`LogisticRegression`, `RandomForest`, `XGBoost`) optimisés via **GridSearchCV** (avec `mlflow.sklearn.autolog()` pour tracer chaque essai sur l'interface web).

### Optimisation Intelligente (Optuna)
- **`train_optuna.py`** : Optimisation bayésienne de ces mêmes modèles via **Optuna**. Seul le modèle "Champion" est enregistré dans MLflow pour garder le tableau de bord propre et permettre une comparaison directe avec le GridSearch.

### Déploiement via API (FastAPI)
- **`api.py`** : Création d'une API REST robuste avec **FastAPI** pour effectuer des prédictions en direct.
- **Chargement intelligent** : L'API se connecte automatiquement à la base **MLflow** au démarrage, recherche l'entraînement ayant le meilleur F1-score, et charge ce modèle directement en mémoire (zéro manipulation manuelle de `.joblib` !).
- **Validation (Pydantic)** : Sécurisation de l'API en forçant les utilisateurs à envoyer un JSON contenant exactement les 22 variables attendues, avec des contraintes mathématiques (pas de chiffres négatifs, etc.).
- **Endpoints** : `/predict` pour obtenir la prédiction (Victoire/Défaite + probabilité) et `/model-info` pour vérifier le nom du modèle actuellement utilisé par l'API.
