import requests
import csv
import io

url = 'https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B'
r = requests.get(url)
f = io.StringIO(r.text)
reader = csv.DictReader(f, delimiter=';')
keys = list(reader)[0].keys()

print("--- Columns Found ---")
for k in keys:
    print(f"'{k}'")

print("\n--- Search Matches ---")
for k in keys:
    if 'cran' in k.lower():
        print(f"Screens match: {k}")
    if 'fauteuil' in k.lower():
        print(f"Seats match: {k}")
