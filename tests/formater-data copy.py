import csv
import json
import urllib.parse

# Initialisation d'un dictionnaire vide pour stocker les résultats par région
# Clé : Nom de la région, Valeur : Dictionnaire {'cinemas': count, 'ecrans': total_ecrans, 'fauteuils': total_fauteuils}.
data_par_region = {}

# Variables pour les totaux globaux
total_cinemas_global = 0
total_ecrans_global = 0
total_fauteuils_global = 0

# Ouverture du fichier CSV 'etablissements-cinematographiques.csv' en mode lecture ('r') avec encodage UTF-8.
with open('etablissements-cinematographiques.csv', 'r', encoding='utf-8') as f:
    # Création d'un lecteur CSV qui interprète la première ligne comme des en-têtes (clés de dictionnaire).
    # Le délimiteur est le point-virgule ';'.
    reader = csv.DictReader(f, delimiter=';')
    
    # Boucle sur chaque ligne du fichier CSV.
    for row in reader:
        # Récupération de la valeur de la colonne 'region_administrative'.
        region = row.get('region_administrative')
        # Récupération de la valeur de la colonne 'ecrans'.
        ecrans_str = row.get('ecrans')
        # Récupération de la valeur de la colonne 'fauteuils'.
        fauteuils_str = row.get('fauteuils')
        
        # Vérification si les valeurs existent (non vides).
        if region and ecrans_str and fauteuils_str:
            try:
                ecrans = float(ecrans_str)
                fauteuils = float(fauteuils_str)
                
                # Mise à jour des totaux globaux
                total_cinemas_global += 1
                total_ecrans_global += ecrans
                total_fauteuils_global += fauteuils

                # Si la région n'est pas encore dans notre dictionnaire, on l'ajoute
                if region not in data_par_region:
                    data_par_region[region] = {'cinemas': 0, 'ecrans': 0, 'fauteuils': 0}
                
                # Mise à jour des données régionales
                data_par_region[region]['cinemas'] += 1
                data_par_region[region]['ecrans'] += ecrans
                data_par_region[region]['fauteuils'] += fauteuils
                
            except ValueError:
                # Si la conversion échoue (ex: donnée corrompue), on ignore cette erreur et on passe à la suite.
                pass

# Calcul du Top 5 des régions par nombre de cinémas
# On transforme le dictionnaire en une liste de tuples (region, count) triée
top_regions = sorted(
    [(reg, data['cinemas']) for reg, data in data_par_region.items()],
    key=lambda x: x[1],
    reverse=True
)[:5]

# Préparer les résultats au format attendu par le visualizer
formatted_output = {
    "stats": {
        "total_cinemas": int(total_cinemas_global),
        "total_ecrans": int(total_ecrans_global),
        "total_fauteuils": int(total_fauteuils_global),
        "source": "Data.Gouv (CSV)",
        "top_regions": top_regions
    },
    # On garde les données détaillées si besoin pour d'autres usages
    "details": {
        region: {
            'cinemas': data['cinemas'],
            'ecrans': int(data['ecrans']), 
            'fauteuils': int(data['fauteuils'])
        } 
        for region, data in data_par_region.items()
    },
    # URL placeholder pour le graphique (non généré par ce script, mais nécessaire pour le template)
    "chart_url": "https://quickchart.io/chart?c=" + urllib.parse.quote(json.dumps({
        "type": "bar",
        "data": {
            "labels": [r[0] for r in top_regions],
            "datasets": [{
                "label": "Nombre de cinémas",
                "data": [r[1] for r in top_regions]
            }]
        }
    }))
}

# Nom du fichier de sortie demandé par l'utilisateur (JSON).
output_filename = 'formatted-etablissements-cinematographiques.json'

# Écriture du JSON avec encodage UTF-8 et indentation pour lisibilité.
with open(output_filename, 'w', encoding='utf-8') as out:
    json.dump(formatted_output, out, ensure_ascii=False, indent=2)

# Affichage des résultats finaux pour information.
print("Statistiques générées :")
print(f"Total Cinémas : {int(total_cinemas_global)}")
print(f"Total Écrans : {int(total_ecrans_global)}")
print(f"Total Fauteuils : {int(total_fauteuils_global)}")
print("\nTop 5 Régions :")
for reg, count in top_regions:
    print(f"- {reg} : {count} cinémas")

print(f"\nFichier JSON écrit : {output_filename}")