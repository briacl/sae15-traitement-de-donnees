# Readme

Ceci est un projet de SAE15 réalisé dans le cadre de la formation BUT Réseaux & Télécommunications, dont l'objectif est de savoir traiter des données.

Ce projet a été réalisé entièrement en python

# Explications : Scraper et Visualisation de Données Cinéma

Ce document détaille le fonctionnement de l'application, qui se compose de deux scripts principaux :
1.  **`process_data.py`** : Le moteur de récupération et d'analyse des données.
2.  **`viz_server.py`** : L'interface web interactive pour lancer l'analyse et visualiser les résultats.

---

## 1. Le Moteur : `process_data.py`

Ce script est responsable de la logique métier "lourde".

### Fonctionnement Global
1.  **Extract** : Téléchargement du CSV depuis *data.culture.gouv.fr*.
2.  **Transform** : Analyse des colonnes, nettoyage des données (conversion texte -> nombre), et agrégations (comptage par région).
3.  **Load** : Génération d'un fichier de résultats (`cinemas_stats.json`) et d'un graphique (lien QuickChart).

### Points Clés du Code
- **`fetch_csv(url)`** :
    - Utilise `requests` pour récupérer les données.
    - **Gestion d'erreur** : En cas de pépin réseau, il catche l'exception.
    - **Progression** : Appelle `report_progress()` pour dire "J'en suis à l'étape téléchargement".
- **`process_data(csv_text)`** :
    - **DictReader** : Lit le CSV en mode dictionnaire pour plus de facilité.
    - **Fuzzy Matching (`get_value_fuzzy`)** : Une fonction intelligente qui trouve les colonnes même si leur nom change légèrement ("écrans" vs "Nombre d'écrans").
    - **Boucle Principale** : Parcourt tous les cinémas, incrémente les compteurs de région, et additionne fauteuils/écrans.
- **`report_progress(step, percentage)`** :
    - C'est le lien avec le serveur web. Il écrit l'état actuel (ex: "Analyse en cours...", 60%) dans un petit fichier `progress.json`.

---

## 2. L'Interface Web : `viz_server.py`

Ce script lance un serveur web local accessible via `http://localhost:8000`.

### Fonctionnement Global
- Il sert une page HTML d'accueil ("Landing Page").
- Il permet de déclencher l'exécution de `process_data.py`.
- Il surveille l'avancement et met à jour la page en temps réel.
- Il affiche le tableau de bord final.

### Architecture Technique
- **`http.server`** : Utilise la librairie standard Python pour créer un serveur HTTP sans dépendance externe (comme Flask/Django).
- **Gestion des Requêtes (`VizHandler`)** :
    - `GET /` : Renvoie le code HTML/CSS/JS de la page principale.
    - `POST /api/start` : Lance le script `process_data.py` dans un processus séparé (via `subprocess`) pour ne pas bloquer le serveur.
    - `GET /api/progress` : Lit le fichier `progress.json` écrit par le script de traitement et renvoie le JSON au navigateur.
    - `GET /api/dashboard` : Une fois fini, lit `cinemas_stats.json` et génère le code HTML des résultats.

### Interface (Frontend)
- **HTML/CSS** : Tout est inclus dans le script Python (`generate_index_html`).
- **Design** : Utilisation de Flexbox pour centrer les éléments, d'ombres portées ("Card UI") et d'une barre de progression animée.
- **Javascript** :
    - `pollProgress()` : Une fonction qui interroge le serveur toutes les 500ms (`setInterval`) pour mettre à jour la barre de chargement.

---

## 3. Flux d'Exécution Complet

1.  L'utilisateur ouvre **http://localhost:8000**.
2.  Il clique sur **"Lancer l'analyse"**.
3.  Le serveur lance `process_data.py` en arrière-plan.
4.  Le navigateur demande "Où en est-on ?" (`/api/progress`) chaque demi-seconde.
5.  `process_data.py` met à jour `progress.json` au fur et à mesure (10%... 30%... 100%).
6.  Quand la progression atteint 100%, l'interface charge automatiquement le rapport final (`/api/dashboard`).
