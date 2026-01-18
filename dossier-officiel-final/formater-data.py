import csv
import json
# On importe matplotlib pour les graphiques
import matplotlib.pyplot as plt
# On importe base64 pour encoder les images en base64
import base64
# On importe BytesIO pour les images, permet de stocker les images en mémoire
from io import BytesIO

# Initialisation d'un dictionnaire vide pour stocker les résultats.
# Clé : Nom de la région, Valeur : Nombre total d'écrans.
data_par_region = {}
total_cinemas = 0  # Compteur du nombre total de cinémas

# Ouverture du fichier CSV 'etablissements_cinematographiques.csv' en mode lecture ('r') avec encodage UTF-8.
with open('etablissements-cinematographiques.csv', 'r', encoding='utf-8') as f:
    # Création d'un lecteur CSV qui interprète la première ligne comme des en-têtes (clés de dictionnaire).
    # Le délimiteur est le point-virgule ';'.
    reader = csv.DictReader(f, delimiter=';')
    
    # Boucle sur chaque ligne du fichier CSV.
    for row in reader:
        # Récupération de la valeur de la colonne 'region_administrative'.
        region = row.get('region_administrative')
        # Récupération de la valeur de la colonne 'ecrans'.
        ecrans = row.get('ecrans')
        # Récupération de la valeur de la colonne 'fauteuils'.
        fauteuils = row.get('fauteuils')
        
        # Vérification si les deux valeurs existent (non vides).
        if region and ecrans:
            # Si la région n'est pas encore dans notre dictionnaire, on l'ajoute avec une valeur initiale de 0.
            if region not in data_par_region:
                data_par_region[region] = {'ecrans': 0, 'fauteuils': 0, 'cinemas': 0}
            try:
                # On essaie de convertir le nombre d'écrans en nombre flottant (float), puis on l'ajoute au total de la région.
                data_par_region[region]['ecrans'] += float(ecrans)
                data_par_region[region]['fauteuils'] += float(fauteuils)
                data_par_region[region]['cinemas'] += 1
                total_cinemas += 1  # Compter chaque établissement
            except ValueError:
                # Si la conversion échoue (ex: donnée corrompue), on ignore cette erreur et on passe à la suite.
                pass

# Préparer les résultats sous forme d'entiers pour sauvegarde.
formatted = {
    region: {
        'ecrans': int(values['ecrans']), 
        'fauteuils': int(values['fauteuils']),
        'cinemas': int(values['cinemas'])
    } 
    for region, values in data_par_region.items()
}

# Calculer les statistiques globales
# total_cinemas est maintenant calculé dans la boucle ci-dessus
total_ecrans = sum(v['ecrans'] for v in formatted.values())
total_fauteuils = sum(v['fauteuils'] for v in formatted.values())

# Obtenir le top 5 des régions par nombre d'écrans
top_regions_ecrans = sorted(formatted.items(), key=lambda x: x[1]['ecrans'], reverse=True)[:5]
top_regions_ecrans_list = [(region, data['ecrans']) for region, data in top_regions_ecrans]

# Obtenir le top 5 des régions par nombre de fauteuils
top_regions_fauteuils = sorted(formatted.items(), key=lambda x: x[1]['fauteuils'], reverse=True)[:5]
top_regions_fauteuils_list = [(region, data['fauteuils']) for region, data in top_regions_fauteuils]

# Créer le graphique 1 : Nombre de salles (régions) par région
regions_all = list(formatted.keys())
cinemas_counts = [1 for _ in regions_all]  # Chaque région = 1 cinéma dans ce contexte

plt.figure(figsize=(12, 6))
plt.bar(regions_all, cinemas_counts, color='#e74c3c')
plt.xlabel('Régions', fontsize=12)
plt.ylabel('Présence (région)', fontsize=12)
plt.title('Répartition des régions cinématographiques', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

buffer1 = BytesIO()
plt.savefig(buffer1, format='png', dpi=100)
buffer1.seek(0)
image_base64_salles = base64.b64encode(buffer1.read()).decode('utf-8')
plt.close()

chart_url_salles = f"data:image/png;base64,{image_base64_salles}"

# Créer le graphique 2 : Nombre d'écrans par région (top 5)
regions_names_ecrans = [region for region, _ in top_regions_ecrans]
ecrans_counts = [data['ecrans'] for _, data in top_regions_ecrans]

plt.figure(figsize=(12, 6))
plt.bar(regions_names_ecrans, ecrans_counts, color='#3498db')
plt.xlabel('Régions', fontsize=12)
plt.ylabel('Nombre d\'écrans', fontsize=12)
plt.title('Top 5 des régions par nombre d\'écrans', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

buffer2 = BytesIO()
plt.savefig(buffer2, format='png', dpi=100)
buffer2.seek(0)
image_base64_ecrans = base64.b64encode(buffer2.read()).decode('utf-8')
plt.close()

chart_url_ecrans = f"data:image/png;base64,{image_base64_ecrans}"

# Créer le graphique 3 : Nombre de fauteuils par région (top 5)
regions_names_fauteuils = [region for region, _ in top_regions_fauteuils]
fauteuils_counts = [data['fauteuils'] for _, data in top_regions_fauteuils]

plt.figure(figsize=(12, 6))
plt.bar(regions_names_fauteuils, fauteuils_counts, color='#2ecc71')
plt.xlabel('Régions', fontsize=12)
plt.ylabel('Nombre de fauteuils', fontsize=12)
plt.title('Top 5 des régions par nombre de fauteuils', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

buffer3 = BytesIO()
plt.savefig(buffer3, format='png', dpi=100)
buffer3.seek(0)
image_base64_fauteuils = base64.b64encode(buffer3.read()).decode('utf-8')
plt.close()

chart_url_fauteuils = f"data:image/png;base64,{image_base64_fauteuils}"

# Préparer le JSON final avec toutes les statistiques
output_data = {
    "stats": {
        "total_cinemas": total_cinemas,
        "total_ecrans": total_ecrans,
        "total_fauteuils": total_fauteuils,
        "source": "data.culture.gouv.fr",
        "top_regions_ecrans": top_regions_ecrans_list,
        "top_regions_fauteuils": top_regions_fauteuils_list
    },
    "chart_url_salles": chart_url_salles,
    "chart_url_ecrans": chart_url_ecrans,
    "chart_url_fauteuils": chart_url_fauteuils,
    "regions_data": formatted
}

# Nom du fichier de sortie demandé par l'utilisateur (JSON).
output_filename = 'formatted-etablissements-cinematographiques.json'

# Écriture du JSON avec encodage UTF-8 et indentation pour lisibilité.
with open(output_filename, 'w', encoding='utf-8') as out:
    json.dump(output_data, out, ensure_ascii=False, indent=2)

# Affichage des résultats finaux pour information.
print(f"Total de cinémas (régions): {total_cinemas}")
print(f"Total d'écrans: {total_ecrans}")
print(f"Total de fauteuils: {total_fauteuils}")
print("\nTop 5 régions par nombre d'écrans:")
for region, ecrans in top_regions_ecrans_list:
    print(f"  {region}: {ecrans} écrans")
print("\nTop 5 régions par nombre de fauteuils:")
for region, fauteuils in top_regions_fauteuils_list:
    print(f"  {region}: {fauteuils} fauteuils")

print(f"\nFichier JSON écrit : {output_filename}")