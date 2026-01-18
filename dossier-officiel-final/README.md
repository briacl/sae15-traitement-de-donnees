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

Pour lancer le programme principal (qui vérifiera et lancera les autres scripts si nécessaire) :

```bash
python visualizer-data.py
```

Un menu interactif vous proposera deux modes :
1.  **Graphique simple (QuickChart)** : Génère des URL de graphiques via l'API QuickChart.io et les ouvre dans votre navigateur.
2.  **Interface web complète** : Lance un serveur web local affichant un tableau de bord complet avec statistiques et graphiques.

---

## 📂 Architecture technique

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
*   **Rôle** : Chef d'orchestre et interface utilisateur.
*   **Fonctionnalités** :
    *   Vérifie l'existence des données ; lance le scraper/formater si besoin (`subprocess`).
    *   **Mode QuickChart** : Envoie les données agrégées à `quickchart.io` pour générer le rendu.
    *   **Mode Web** : Serveur HTTP (`http.server`) servant une page HTML5/CSS3 moderne avec tableau de bord.

---

## 📊 Aperçu Visuel

![Dashboard](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171011.png)

![Graphique](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171049.png)

![Liste](graph-for-readme/Capture%20d'%C3%A9cran%202026-01-17%20171107.png)