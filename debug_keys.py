import requests
import csv
import io

url = 'https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B'
r = requests.get(url)
r.encoding = 'utf-8'
f = io.StringIO(r.text)
reader = csv.DictReader(f, delimiter=';')
rec = list(reader)[0]

with open('debug_keys.txt', 'w', encoding='utf-8') as debug_f:
    for k, v in rec.items():
        debug_f.write(f"Key: '{k}' -> Value: '{v}'\n")
