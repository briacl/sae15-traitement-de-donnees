# Explications : Script de Formatage (`formater-data.py`)

Ce fichier détaille le fonctionnement du script de transformation des données.

## 📌 Rôle global
Ce script correspond à l'étape **Transform** du pipeline ETL. Il lit les données brutes (CSV), les nettoie, les agrège par région, et prépare déjà les visualisations pour l'interface web (en générant des images encodées en Base64).

---

## 🔍 Explication détaillée (Ligne par Ligne)

### 1. Importations et Initialisation

```python
1: import csv
2: import json
4: import matplotlib.pyplot as plt
6: import base64
8: from io import BytesIO
```
*   `csv` & `json` : Pour lire la source et écrire la destination.
*   `matplotlib.pyplot` : Pour dessiner les graphiques (histogrammes).
*   `base64` & `BytesIO` : Astuce technique pour sauvegarder les images directement dans le texte du fichier JSON (sous forme de chaîne de caractères) plutôt que dans des fichiers `.png` séparés. Cela facilite le transport des données vers le site web.

```python
12: data_par_region = {}
13: total_cinemas = 0
```
On prépare un dictionnaire vide qui va servir d'accumulateur pour nos calculs d'agrégation.

### 2. Lecture et Agrégation (Le coeur du script)

```python
16: with open('etablissements-cinematographiques.csv', 'r', encoding='utf-8') as f:
19:     reader = csv.DictReader(f, delimiter=';')
```
On ouvre le fichier brut. `DictReader` est très pratique : il permet d'accéder aux colonnes par leur nom (ex: `row['ecrans']`) plutôt que par leur index (ex: `row[14]`). **Attention** : le fichier source utilise des points-virgules `;`.

```python
22:     for row in reader:
24:         region = row.get('region_administrative')
34:             data_par_region[region] = {'ecrans': 0, 'fauteuils': 0, 'cinemas': 0}
```
On parcourt chaque cinéma un par un. Si on rencontre une nouvelle région, on l'initialise dans notre dictionnaire avec des compteurs à 0.

```python
35:             try:
37:                 data_par_region[region]['ecrans'] += float(ecrans)
38:                 data_par_region[region]['fauteuils'] += float(fauteuils)
39:                 data_par_region[region]['cinemas'] += 1
41:             except ValueError:
43:                 pass
```
**Gestion d'erreur (Robustesse)** : On additionne les valeurs. Le `try...except ValueError` est crucial. Si une ligne du CSV est malformée (ex: "cinq" au lieu de "5" écrans), le programme ne plantera pas ; il ignorera juste cette valeur erronée.

### 3. Nettoyage final des données

```python
46: formatted = {
47:     region: {
48:         'ecrans': int(values['ecrans']), 
...
52:     for region, values in data_par_region.items()
53: }
```
Une "Dictionary Comprehension" pour nettoyer le résultat : on convertit tous les totaux en entiers (plus propre que des nombres à virgule `.0`) pour le fichier final.

### 4. Les Tops 5

```python
61: top_regions_ecrans = sorted(formatted.items(), key=lambda x: x[1]['ecrans'], reverse=True)[:5]
```
On trie notre dictionnaire agrégé pour extraire les "champions".
*   `sorted` : Trie la liste.
*   `key=...` : Dit de trier selon le nombre d'écrans.
*   `reverse=True` : Du plus grand au plus petit.
*   `[:5]` : On ne garde que les 5 premiers.

### 5. Génération des Graphiques (Matplotlib)

```python
72: plt.figure(figsize=(12, 6))
73: plt.bar(regions_all, cinemas_counts, color='#e74c3c')
```
On configure un graphique en barres classique.

```python
80: buffer1 = BytesIO()
81: plt.savefig(buffer1, format='png', dpi=100)
83: image_base64_salles = base64.b64encode(buffer1.read()).decode('utf-8')
```
**L'astuce "Base64"** :
1.  On ne sauve pas sur le disque dur, mais dans la mémoire vive (`BytesIO`).
2.  On demande à Matplotlib de "sauvegarder" l'image dans cette mémoire.
3.  On encode le contenu de cette image binaire en une longue chaîne de texte (Base64).
4.  C'est cette chaîne qu'on mettra dans le JSON. Le navigateur saura la décoder pour afficher l'image.

*Cette logique est répétée 3 fois pour les 3 graphiques (Régions, Écrans, Fauteuils).*

### 6. Export Final JSON

```python
129: output_data = {
130:     "stats": { ... },
138:     "chart_url_salles": chart_url_salles, ...
141:     "regions_data": formatted
142: }
```
On assemble tout : les statistiques brutes + les images encodées.

```python
148: with open(output_filename, 'w', encoding='utf-8') as out:
149:     json.dump(output_data, out, ensure_ascii=False, indent=2)
```
On écrit le fichier `formatted-etablissements-cinematographiques.json`. C'est ce fichier "propre" et complet qui sera lu par le visualiseur. `ensure_ascii=False` permet de garder les accents lisibles dans le fichier JSON.
