# SAE 15 - Traitement et Visualisation de Données : Cinémas

**Auteurs** : Briac Le Meillat & Yanni Delattre Balcer

## 📝 Description

Ce projet a pour objectif d'analyser les données publiques des établissements cinématographiques en France. Il propose une chaîne complète de traitement de données :
1.  **Extraction** : Récupération des données depuis l'API du Ministère de la Culture ou via des fichiers CSV.
2.  **Transformation** : Nettoyage, conversion en JSON et agrégation statistique (nombre de salles par région).
3.  **Visualisation** : Génération automatique d'un tableau de bord Web interactif.

Le tout est orchestré par un serveur Python local capable de gérer ces tâches en arrière-plan.

---

## 🚀 Installation

Assurez-vous d'avoir **Python 3.x** installé sur votre machine.

Les dépendances principales sont incluses dans la bibliothèque standard (`http.server`, `json`, `csv`, `subprocess`, `threading`), excepté `requests` pour la partie téléchargement API.

```bash
pip install requests
```

---

## 📚 Guide d'Utilisation du Code

Ce projet a été conçu étape par étape. Voici le détail de chaque module.

### 1. Récupération des Données

Nous utilisons l'API de `data.culture.gouv.fr` pour obtenir les dernières données à jour.

```python
import requests

url = "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv"
response = requests.get(url)

if response.status_code == 200:
    filename = "etablissements_cinematographiques"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Données téléchargées : {filename}")
else:
    print(f"Erreur : {response.status_code}")
```

### 2. Conversion et Nettoyage (CSV vers JSON)

Les données brutes peuvent être au format CSV ou Texte. Nous les convertissons en JSON pour faciliter leur manipulation.

```python
import csv
import json

data_json_csv = []
with open("data-etablissements-cinematographiques.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";") 
    for row in reader:
        data_json_csv.append(row)

with open("data-etablissements-cinematographiques.json", "w", encoding="utf-8") as f:
    json.dump(data_json_csv, f, indent=4, ensure_ascii=False)
```

### 3. Analyse Statistique

Nous analysons ensuite le nombre de salles (écrans) par région administrative.

```python
salles_par_region = {}

# Lecture et agrégation
with open("data-etablissements-cinematographiques.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        region = row["region_administrative"]
        # Conversion sécurisée en entier
        nb_ecrans = int(float(row["ecrans"]))
        
        if region in salles_par_region:
            salles_par_region[region] += nb_ecrans
        else:
            salles_par_region[region] = nb_ecrans

# Sauvegarde des résultats filtrés
with open("data-filtered.json", "w", encoding="utf-8") as f:
    json.dump(salles_par_region, f, indent=4, ensure_ascii=False)
```

### 4. Application Web Interactive

Pour rendre le projet convivial, nous avons développé un **serveur Web Python** qui offre une interface graphique.

#### Architecture du Serveur (`VizHandler`)

Le serveur gère plusieurs routes API :
- `POST /api/start` : Lance le traitement (`run_process_async`) dans un thread séparé pour ne pas bloquer l'interface.
- `GET /api/progress` : Renvoie l'avancement du traitement en temps réel.
- `GET /api/dashboard` : Génère et renvoie le tableau de bord HTML une fois le traitement terminé.

#### Gestion Asynchrone

L'exécution des scripts de traitement se fait via `subprocess` dans un thread dédié :

```python
def run_process_async():
    """Lance la pipeline de données en arrière-plan."""
    current_dir = os.getcwd()
    script_dir = os.path.join(current_dir, "tests")
    
    scraper_script = os.path.join(script_dir, "scraper-data copy.py")
    formater_script = os.path.join(script_dir, "formater-data copy.py")
    
    try:
        # Lancement séquentiel des scripts
        subprocess.run([sys.executable, scraper_script], check=True)
        subprocess.run([sys.executable, formater_script], check=True)
        # ... mise à jour de la progression ...
    except Exception as e:
        print(f"Erreur : {e}")
```

#### Démarrage

Pour lancer l'application finale, exécutez simplement le script principal. Le navigateur s'ouvrira automatiquement.

```python
PORT = 8000
with socketserver.TCPServer(("", PORT), VizHandler) as httpd:
    print(f"Serveur démarré sur http://localhost:{PORT}")
    httpd.serve_forever()
```

---

## 📊 Résultat

Une fois l'analyse terminée, vous obtenez un **Tableau de Bord** comprenant :
- Les chiffres clés (Total cinémas, écrans, fauteuils).
- Un graphique interactif des Top 5 régions.
- Une liste détaillée des données.

---
*Projet réalisé dans le cadre de la SAE 15.*
