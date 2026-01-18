# Explications : Script de Scrapping (`scraper-data.py`)

Ce fichier détaille le fonctionnement du script d'extraction des données.

## 📌 Rôle global
Ce script est responsable de la **première étape** du pipeline ETL (Extract, Transform, Load). Son but est simple : se connecter à l'API Data Culture Gouv et télécharger les dernières données brutes disponibles au format CSV.

---

## 🔍 Explication détaillée (Ligne par Ligne)

```python
1: # On utilise la librairie requests afin de faire la requête http...
2: import requests
```
**Ligne 2** : On importe `requests`. C'est LA librairie standard en Python pour discuter avec des serveurs web. Elle nous permet de faire des appels HTTP (comme un navigateur) facilement.

```python
5: url = "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv"
```
**Ligne 5** : On définit l'URL cible. C'est l'adresse précise ("Endpoint") fournie par data.gouv.fr qui génère le fichier CSV des cinémas.

```python
8: response = requests.get(url)
```
**Ligne 8** : C'est ici que l'action se passe. `requests.get(url)` envoie une requête de type GET au serveur. Le script s'arrête ici tant que le serveur n'a pas répondu. La réponse complète (contenu, code statut, en-têtes) est stockée dans la variable `response`.

```python
11: if response.status_code == 200:
```
**Ligne 11** : On vérifie le code de statut HTTP.
*   **200** signifie "OK" (Tout s'est bien passé).
*   Si c'est 404 (Not Found) ou 500 (Erreur Serveur), on passera dans le `else`.

```python
14:     filename = f"etablissements-cinematographiques.csv"
```
**Ligne 14** : On prépare le nom du fichier de sortie. On utilise une f-string (même s'il n'y a pas de variable ici) pour définir le nom du fichier local où on va sauvegarder les données.

```python
18:     with open(filename, "w", encoding="utf-8") as f:
19:         # Et on écrit directement dans le fichier le contenu de la var response
20:         f.write(response.text)
```
**Ligne 18** : On ouvre le fichier en mode écriture (`"w"` pour write) et on force l'encodage `utf-8` pour éviter les problèmes d'accents.
*   L'instruction `with` est très importante : elle garantit que le fichier sera correctement fermé même si une erreur survient pendant l'écriture.
**Ligne 20** : On prend tout le texte reçu du serveur (`response.text`) et on l'injecte tel quel dans notre fichier local.

```python
23:     print(f"Données téléchargées et enregistrées dans {filename}")
```
**Ligne 23** : On informe l'utilisateur que tout s'est bien passé.

```python
25: else:
27:     print(f"Erreur lors de la requête : {response.status_code}")
```
**Ligne 25-27** : Si le serveur a répondu par une erreur (ex: 404), on affiche le code d'erreur pour aider au débogage, au lieu de planter silencieusement ou de créer un fichier vide.
