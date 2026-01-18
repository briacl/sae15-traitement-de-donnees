# Explications : Script de Visualisation (`visualizer-data.py`)

Ce fichier détaille le fonctionnement du script d'interface utilisateur.

## 📌 Rôle global
Ce script est la "vitrine" du projet. Il propose un menu interactif et deux modes de visualisation :
1.  **Mode Simple** : Utilise l'API externe QuickChart.
2.  **Mode Web** : Un serveur web local complet avec tableau de bord et rafraîchissement en temps réel.

---

## 🔍 Explication détaillée (Ligne par Ligne)

### 1. Le Serveur Web

```python
309: class VizHandler(http.server.SimpleHTTPRequestHandler):
```
On crée notre propre gestionnaire de requêtes web en héritant du gestionnaire standard de Python. C'est ici qu'on définit comment le serveur réagit aux demandes du navigateur.

```python
326:     def do_GET(self):
341:         elif self.path == "/api/dashboard":
345:                 html = self.generate_dashboard_html(stats_json)
```
Si le navigateur demande la page `/api/dashboard`, on charge le JSON généré par le formateur et on construit dynamiquement le HTML (grâce à la fonction `generate_dashboard_html` ligne 362) pour inclure les chiffres et les graphiques à jour.

```python
354:         elif self.path == "/":
358:             html = self.generate_index_html()
```
Si on va à la racine (`/`), on affiche la page d'accueil (le bouton "Lancer l'analyse"). La fonction `generate_index_html` (ligne 421) contient tout le HTML/CSS de cette page.

### 2. Le Threading (Tâche de fond)

```python
271: def run_process_async():
292:         subprocess.run([sys.executable, scraper_script], check=True)
299:         subprocess.run([sys.executable, formater_script], check=True)
```
Pour l'interface Web (bouton "Lancer l'analyse"), on ne veut pas que le site "gèle" pendant le téléchargement.
On utilise donc cette fonction qui lance le scraper puis le formateur.

```python
315:             t = threading.Thread(target=run_process_async)
316:             t.start()
```
Dans `do_POST` (ligne 312), quand on clique sur le bouton, cette fonction est lancée dans un **Thread séparé** (fil d'exécution parallèle). Le serveur peut donc répondre "OK j'ai commencé" immédiatement à l'utilisateur, tout en travaillant en arrière-plan.

### 3. Mode Console & QuickChart (L'option 1)

```python
33: def afficher_graphique_simple():
```
Cette fonction gère le "Mode 1" du menu.

```python
168:         response1 = requests.post("https://quickchart.io/chart/create", json={"chart": chart_data_salles})
```
Ici, on n'utilise pas Matplotlib en local. On envoie nos données (les étiquettes et les valeurs) à l'API **QuickChart.io**.
C'est un service web qui prend des données JSON et nous renvoie l'URL d'une image générée.

```python
188:             webbrowser.open(url1)
```
Dès qu'on reçoit l'URL de QuickChart, on demande au système d'exploitation d'ouvrir le navigateur par défaut pour afficher l'image.

### 4. Le Menu Principal

```python
230: def menu_principal():
237:             choix = input("\nVotre choix (1, 2 ou 3) : ").strip()
```
Une simple boucle infinie (`while True`) qui attend l'entrée utilisateur pour diriger vers la fonction `afficher_graphique_simple()` ou `afficher_interface_web()`.

### 5. Génération HTML (Le "Front-End")

```python
381:         return f"""
382:             <div class="result-section fade-in">
...
400:                     <img src="{chart_url_salles}" ...>
```
Dans `generate_dashboard_html`, on utilise une f-string géante pour écrire le code HTML. Remarquez la ligne 400 : on injecte `chart_url_salles` (notre image Base64 créée par le formateur) directement dans la balise `<img>`. C'est ce qui permet d'afficher le graphique sans avoir besoin de fichier image externe.
