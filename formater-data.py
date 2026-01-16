import csv
import json

# Initialisation d'un dictionnaire vide pour stocker les résultats.
# Clé : Nom de la région, Valeur : Nombre total d'écrans.
data_par_region = {}

# Ouverture du fichier CSV 'etablissements_cinematographiques.csv' en mode lecture ('r') avec encodage UTF-8.
with open('etablissements_cinematographiques.csv', 'r', encoding='utf-8') as f:
    # Création d'un lecteur CSV qui interprète la première ligne comme des en-têtes (clés de dictionnaire).
    # Le délimiteur est le point-virgule ';'.
    reader = csv.DictReader(f, delimiter=';')
    
    # Boucle sur chaque ligne du fichier CSV.
    for row in reader:
        # Récupération de la valeur de la colonne 'region_administrative'.
        region = row.get('region_administrative')
        # Récupération de la valeur de la colonne 'ecrans'.
        ecrans = row.get('ecrans')
        
        # Vérification si les deux valeurs existent (non vides).
        if region and ecrans:
            # Si la région n'est pas encore dans notre dictionnaire, on l'ajoute avec une valeur initiale de 0.
            if region not in data_par_region:
                data_par_region[region] = 0
            try:
                # On essaie de convertir le nombre d'écrans en nombre flottant (float), puis on l'ajoute au total de la région.
                data_par_region[region] += float(ecrans)
            except ValueError:
                # Si la conversion échoue (ex: donnée corrompue), on ignore cette erreur et on passe à la suite.
                pass

# Préparer les résultats sous forme d'entiers pour sauvegarde.
formatted = {region: int(nb_ecrans) for region, nb_ecrans in data_par_region.items()}

# Nom du fichier de sortie demandé par l'utilisateur (JSON).
output_filename = 'formatted_etablissements_cinematographiques.json'

# Écriture du JSON avec encodage UTF-8 et indentation pour lisibilité.
with open(output_filename, 'w', encoding='utf-8') as out:
    json.dump(formatted, out, ensure_ascii=False, indent=2)

# Affichage des résultats finaux pour information.
for region, nb_ecrans in formatted.items():
    print(f"{region} : {nb_ecrans} salles")

print(f"Fichier JSON écrit : {output_filename}")