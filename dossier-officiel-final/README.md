# SAE 15 - Traitement de données : Établissements Cinématographiques

Projet réalisé dans le cadre de la formation **BUT Réseaux & Télécommunications**.

**Auteurs :**
*   **Yanni Delattre-Balcer**
*   **Briac Le Meillat**

---

## 📝 Présentation du projet

Ce projet a pour objectif d'automatiser la récupération, le traitement et la visualisation de données ouvertes (Open Data). Nous avons choisi d'analyser les **établissements cinématographiques en France** à partir des données de `data.culture.gouv.fr`.

Le système permet de :
1.  **Télécharger** automatiquement les données CSV à jour.
2.  **Traiter** et nettoyer les données (agrégation par région, calcul du nombre d'écrans et de fauteuils).
3.  **Visualiser** les résultats sous forme de graphiques via une interface Web locale ou via l'API QuickChart.

## 🚀 Guide d'utilisation

### Prérequis

Assurez-vous d'avoir Python 3 installé. Les bibliothèques tierces nécessaires sont :
*   `requests`
*   `matplotlib`

Installation des dépendances :
```bash
pip install -r requirements.txt
# Ou manuellement :
pip install requests matplotlib
```

### Exécution

Pour lancer le programme principal (qui exécutera séquentiellement tous les scripts) :

```bash
python main.py
```

Un menu interactif vous proposera deux modes :
1.  **Graphique simple (QuickChart)** : Génère des URL de graphiques via l'API QuickChart.io et les ouvre dans votre navigateur.
2.  **Interface web complète** : Lance un serveur web local affichant un tableau de bord complet avec statistiques et graphiques.

---

## 📂 Architecture technique

### 0. Point d'entrée (`main.py`)
*   **Rôle** : Chef d'orchestre global.
*   **Fonction** : Exécute séquentiellement l'extraction, la transformation et la visualisation pour garantir un flux de données à jour.

### 1. Extraction (`scraper-data.py`)
*   **Source** : API Data Culture Gouv (fichier CSV).
*   **Objectif** : Récupère le fichier `etablissements-cinematographiques.csv`.
*   **Technique** : Utilisation de la librairie `requests`. Gestion des erreurs HTTP (codes 200/404).

### 2. Transformation (`formater-data.py`)
*   **Entrée** : Le fichier CSV brut.
*   **Traitement** : 
    *   Lecture et parsing CSV.
    *   Agrégation des données par région administrative.
    *   Calcul des sommes (écrans, fauteuils, nombre de cinémas).
    *   Génération de graphiques statiques avec `matplotlib` (pour le mode Web local).
*   **Sortie** : Fichier `formatted-etablissements-cinematographiques.json`.

### 3. Visualisation (`visualizer-data.py`)
*   **Rôle** : Interface utilisateur.
*   **Fonctionnalités** :
    *   **Mode QuickChart** : Envoie les données agrégées à `quickchart.io` pour générer le rendu.
    *   **Mode Web** : Serveur HTTP (`http.server`) servant une page HTML5/CSS3 moderne avec tableau de bord.

---

## 📊 Aperçu Visuel

![Dashboard](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171011.png)

![Graphique](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171049.png)

![Liste](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171107.png)

---

## 👥 Répartition des tâches

Pour la répartition des tâches, nous avons réalisé un diagramme de Gantt que voici :

![Diagramme de Gantt](diagramme-de-gantt.png)

### Technologies utilisées

- Python 3
- requests
- csv
- json
- matplotlib as plt
- base64
- BytesIO from io
- os
- sys
- webbrowser
- subprocess
- time

Pour le bonus (interface web) :
- http.server
- socketserver
- threading

### Réalisations de Yanni Delattre-Balcer
*   **Planification** : Élaboration du **Diagramme de Gantt** pour la gestion de projet.
*   **Scraping** : Conception du script `scraper-data.py` (utilisation de `requests`).
*   **Formatage (Partie 1)** : Structure initiale de `formater-data.py` (lecture CSV).
*   **Gestion GitLab** : Co-versionnage du projet.
*   **Présentation** : Co-réalisation du diaporama.

### Réalisations de Briac Le Meillat
*   **Gestion GitLab** : Initialisation, configuration et co-versionnage du projet.
*   **Formatage (Partie 2)** : Finalisation de `formater-data.py`, gestion des erreurs et cohérence des données.
*   **Visualisation / Web** : Intégration de l'API **QuickChart**  afin de visualiser dans le navigateur les graphiques des données (`visualizer-data.py`).
*   **Main** : Conception du script `main.py`, point d'entrée du programme, permettant d'exécuter les scripts en séquence.
*   **Présentation** : Co-réalisation du diaporama.
*   **Bonus** : Développement de l'interface web (`visualizer-data.py`).

**Travail commun** : Analyse initiale, tests complets et finalisation du Livrable.

## 📂 Détails des scripts

### 1. Extraction (`scraper-data.py`) : réalisé par Yanni Delattre-Balcer
#### Objectif
Récupérer automatiquement le fichier CSV des établissements cinématographiques depuis l'API **data.gouv.fr**.

#### Bibliothèques utilisées
*   **requests** : Envoi de la requête HTTP GET pour télécharger le fichier.

#### Fonctionnement du script
1.  Envoie une requête au serveur open data.
2.  Vérifie le code de statut (200 OK).
3.  Ecrit le contenu brut dans `etablissements-cinematographiques.csv`.
4.  Gère les erreurs de connexion éventuelles.

---

### 2. Transformation (`formater-data.py`) : réalisé par Yanni Delattre-Balcer & Briac Le Meillat
#### Objectif
Nettoyer le fichier CSV, agréger les données par région et générer les graphiques statiques pour le Web.

#### Bibliothèques utilisées
*   **csv** : Lecture et parsing du fichier brut.
*   **json** : Export des données structurées.
*   **matplotlib** : Génération des graphiques (barres) pour le mode hors-ligne/web local.
*   **base64 / io** : Encodage des images générées directement dans le JSON.

#### Fonctionnement du script
1.  Lit le fichier CSV ligne par ligne.
2.  **Agrégation** : Somme les écrans, fauteuils et cinémas pour chaque région administrative.
3.  **Nettoyage** : Utilise `try/except` pour ignorer les valeurs corrompues ou manquantes.
4.  **Génération Graphique** : Crée 3 graphiques avec Matplotlib, les convertit en Base64.
5.  **Export** : Sauvegarde le tout (stats + images) dans `formatted-etablissements-cinematographiques.json`.

---

### 3. Visualisation (`visualizer-data.py`) : réalisé par Briac Le Meillat
#### Objectif
Offrir une interface utilisateur complète (Console + Web) pour consulter les résultats.

#### Bibliothèques utilisées
*   **requests** : Appel à l'API **QuickChart** (pour le mode graphique simple).
*   **webbrowser** : Ouverture automatique du navigateur.
*   **Interface Web (Bonus) -> http.server / socketserver** : Création du serveur web local.
*   **Interface Web (Bonus) -> threading** : Gestion des tâches en arrière-plan sans bloquer l'interface.

#### Fonctionnement du script
*   **Mode Graphique Simple** : Lit le JSON et appelle l'API QuickChart pour afficher les courbes dans le navigateur.
*   **Mode Interface Web (Bonus)** :
    1.  Lance un serveur HTTP local (Port 8000).
    2.  Sert une page HTML5/CSS3 moderne ("Dashboard").
    3.  Affiche les statistiques et injecte les graphiques Base64 générés par le formateur.

---

### 4. Orchestration (`main.py`) : réalisé par Briac Le Meillat
#### Objectif
Point d'entrée unique qui automatise toute la chaîne de traitement.

#### Bibliothèques utilisées
*   **subprocess** : Exécution séquentielle des scripts Python externes.
*   **time** : Mesure de la performance (temps d'exécution).

#### Fonctionnement du script
1.  Lance `scraper-data.py` (Extraction).
2.  Lance `formater-data.py` (Transformation).
3.  Lance `visualizer-data.py` (Visualisation).
4.  Gère l'arrêt propre (Ctrl+C) et les erreurs d'exécution pour chaque étape.
