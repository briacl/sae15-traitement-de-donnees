#!/usr/bin/env python3
"""
process_data.py

Récupère les données des cinémas en France (Data Culture), calcule des statistiques
(par région), et génère un graphique via QuickChart.

Usage:
  python process_data.py
"""
import requests
import csv
import io
import json
import statistics
from collections import Counter
from urllib.parse import quote
import time # Ajout pour simulation délai si trop rapide

# Nouveau fichier pour communiquer l'avancement
PROGRESS_FILE = "progress.json"

# URL du CSV (Établissements cinématographiques)
CSV_URL = "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"

def report_progress(step, percentage):
    """Ecrit l'état d'avancement dans un fichier JSON."""
    data = {
        "step": step,
        "percentage": percentage,
        "timestamp": time.time()
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    # Petit délai pour que l'animation soit visible (optionnel)
    if percentage < 100:
        time.sleep(0.5)

def fetch_csv(url):
    """Télécharge le contenu CSV depuis l'URL."""
    report_progress("Connexion aux serveurs Data.Gouv...", 10)
    print(f"Téléchargement des données depuis {url}...")
    try:
        response = requests.get(url, timeout=30)
        report_progress("Téléchargement en cours...", 30)
        response.raise_for_status()
        response.encoding = 'utf-8' 
        report_progress("Téléchargement terminé.", 50)
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None

def process_data(csv_text):
    """Parse le CSV et calcule les agrégations."""
    report_progress("Analyse des données...", 60)
    if not csv_text:
        return None

    f = io.StringIO(csv_text)
    reader = csv.DictReader(f, delimiter=';')
    
    records = list(reader)
    if not records:
        return None
        
    total_cinemas = len(records)
    print(f"\nNombre total de cinémas récupérés : {total_cinemas}")

    # Helper pour trouver une clé insensible à la casse / accent
    def get_value_fuzzy(record, candidates):
        # 1. Exact match attempt
        for c in candidates:
            if c in record:
                return record[c]
        
        # 2. Case insensitive match
        keys = list(record.keys())
        for c in candidates:
            for k in keys:
                if c.lower() in k.lower():
                    return record[k]
        return None

    # Agrégations
    region_counts = Counter()
    total_ecrans = 0
    total_fauteuils = 0
    
    cinemas_valid = 0
    
    # Simulation traitement long si beaucoup de données
    
    for r in records:
        # Récupération Région
        reg = get_value_fuzzy(r, ['région administrative', 'régioncnc', 'region'])
        if not reg: 
            reg = "Inconnu"
        
        region_counts[reg] += 1
        
        # Récupération Ecrans
        ec = get_value_fuzzy(r, ['écrans', 'ecrans', 'nombre d\'écrans', 'ecran'])
        try:
            val = int(float(ec)) if ec else 0
            total_ecrans += val
        except (ValueError, TypeError):
            pass

        # Récupération Fauteuils
        ft = get_value_fuzzy(r, ['fauteuils', 'nombre de fauteuils', 'fauteuil'])
        try:
            val = int(float(ft)) if ft else 0
            total_fauteuils += val
        except (ValueError, TypeError):
            pass
            
        cinemas_valid += 1
    
    report_progress("Calcul des statistiques terminé.", 75)

    print(f"Nombre de cinémas traités : {cinemas_valid}")
    print(f"Total écrans : {total_ecrans}")
    print(f"Total fauteuils : {total_fauteuils}")
    
    # Top 5 Régions
    top_5_regions = region_counts.most_common(5)
    print("\nTop 5 des régions par nombre de cinémas :")
    for reg, count in top_5_regions:
        print(f"  - {reg} : {count}")
    
    return {
        "top_regions": top_5_regions,
        "total_cinemas": total_cinemas,
        "total_ecrans": total_ecrans,
        "total_fauteuils": total_fauteuils,
        "source": "Data Culture - Établissements cinématographiques"
    }

def generate_quickchart_url(data):
    """Génère l'URL QuickChart pour visualiser le Top 5 Régions."""
    report_progress("Génération du graphique...", 85)
    if not data or not data.get("top_regions"):
        return None

    top_5 = data["top_regions"]
    labels = [item[0] for item in top_5]
    values = [item[1] for item in top_5]

    # Configuration du graphique
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Nombre de cinémas",
                "data": values,
                "backgroundColor": "rgba(255, 99, 132, 0.5)",
                "borderColor": "rgb(255, 99, 132)",
                "borderWidth": 1
            }]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Top 5 Régions - Nombre de Cinémas"
            },
            "plugins": {
                "datalabels": {
                    "anchor": "end",
                    "align": "top"
                }
            }
        }
    }

    # Sérialisation et encodage
    json_config = json.dumps(chart_config)
    encoded_config = quote(json_config)
    url = f"https://quickchart.io/chart?c={encoded_config}"
    report_progress("Graphique prêt.", 95)
    return url

def main():
    report_progress("Démarrage du processus...", 0)
    csv_content = fetch_csv(CSV_URL)
    if csv_content:
        results = process_data(csv_content)
        if results:
            chart_url = generate_quickchart_url(results)
            print(f"\n--- Résultat Final ---")
            print(f"Données traitées avec succès.")
            print(f"Lien vers le graphique : {chart_url}")
            
            # Sauvegarder le JSON final
            output_data = {
                "stats": results,
                "chart_url": chart_url
            }
            with open("cinemas_stats.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print("Fichier 'cinemas_stats.json' généré.")
            
    report_progress("Terminé !", 100)

if __name__ == "__main__":
    main()
