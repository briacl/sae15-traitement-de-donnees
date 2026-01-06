import requests

r = requests.get("https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv")
r.encoding = 'utf-8'

with open ("data.txt", "w", encoding="utf-8") as f:
    f.write(r.text)

with open ("data.txt", "r", encoding="utf-8") as f:
    print(f.read())

