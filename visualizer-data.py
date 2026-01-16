#!/usr/bin/env python3
"""
visualizer-data.py

Code dont chaque ligne est expliquée, produisant le même résultat que viz_server.py.
Ce script lance un serveur web local pour afficher les données des cinémas.
"""

# On importe le module http.server qui permet de créer un serveur web simple
import http.server
# On importe socketserver pour gérer les connexions TCP (réseau)
import socketserver
# On importe le module json pour manipuler les données au format JSON
import json
# On importe le module os pour interagir avec le système d'exploitation (fichiers, chemins)
import os
# On importe subprocess pour lancer d'autres scripts python (process_data.py)
import subprocess
# On importe webbrowser pour ouvrir automatiquement la page dans le navigateur
import webbrowser
# On importe threading pour exécuter le traitement en parallèle sans bloquer le serveur
import threading
# On importe sys pour accéder aux informations sur l'interpréteur Python actuel
import sys

# On définit le port sur lequel le serveur va écouter (8000 est standard pour le dév)
PORT = 8000
# On définit le nom du fichier qui contiendra les statistiques finales générées par process_data.py
STATS_FILE = "cinemas_stats.json"
# On définit le nom du fichier qui sert à suivre la progression du traitement
PROGRESS_FILE = "progress.json"

# --- Nettoyage initial ---
# Le script doit s'assurer de démarrer avec un état propre
# On vérifie si un fichier de progression existe déjà d'une exécution précédente
if os.path.exists(PROGRESS_FILE):
    # Si le fichier existe, on le supprime pour éviter d'afficher des données obsolètes
    os.remove(PROGRESS_FILE)


# --- Définition de la fonction de traitement en arrière-plan ---
def run_process_async():
    """Lance process_data.py en arrière-plan."""
    # Cette fonction sera exécutée dans un fil d'exécution séparé (thread)
    # On utilise subprocess.run pour exécuter le script process_data.py comme si on le tapait dans le terminal
    # sys.executable est le chemin vers l'interpréteur Python actuel, assure qu'on utilise le même environnement
    subprocess.run([sys.executable, "process_data.py"])


# --- Définition de la classe de gestion des requêtes HTTP ---
# Cette classe hérite de http.server.SimpleHTTPRequestHandler pour gérer les fichiers statiques de base
class VizHandler(http.server.SimpleHTTPRequestHandler):
    
    # Cette méthode est appelée automatiquement quand le serveur reçoit une requête POST
    # Les requêtes POST sont utilisées ici pour envoyer des commandes au serveur (comme "démarrer")
    def do_POST(self):
        # On vérifie l'URL demandée par le navigateur
        if self.path == "/api/start":
            # Si l'URL est "/api/start", cela signifie que l'utilisateur a cliqué sur le bouton
            
            # On prépare un nouveau thread (processus léger) qui exécutera la fonction run_process_async
            t = threading.Thread(target=run_process_async)
            # On démarre ce thread. Cela permet au serveur de répondre immédiatement sans attendre la fin du traitement
            t.start()
            
            # On prépare la réponse HTTP pour dire au navigateur que c'est bon (code 200 = OK)
            self.send_response(200)
            # On spécifie que le contenu de la réponse est du JSON
            self.send_header("Content-type", "application/json")
            # On termine l'écriture des en-têtes
            self.end_headers()
            # On envoie le corps de la réponse : un petit JSON confirmant le démarrage
            self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))
        else:
            # Si l'adresse n'est pas reconnue, on renvoie une erreur 404 (Non trouvé)
            self.send_error(404)

    # Cette méthode est appelée automatiquement quand le serveur reçoit une requête GET
    # Les requêtes GET sont utilisées pour demander des pages ou des données
    def do_GET(self):
        # Cas 1 : Le navigateur demande l'état d'avancement du traitement
        if self.path == "/api/progress":
            # On prépare une réponse OK (200)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            # On initialise les données par défaut (si le fichier n'existe pas encore)
            data = {"step": "En attente...", "percentage": 0}
            
            # On regarde si le fichier de progression a été créé par process_data.py
            if os.path.exists(PROGRESS_FILE):
                try:
                    # On ouvre le fichier en lecture
                    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                        # On charge le contenu JSON dans la variable data
                        data = json.load(f)
                except:
                    # Si on n'arrive pas à lire (ex: fichier en cours d'écriture), on garde les valeurs par défaut
                    pass
            
            # On envoie les données au navigateur
            self.wfile.write(json.dumps(data).encode("utf-8"))
            
        # Cas 2 : Le navigateur demande le tableau de bord final (les résultats)
        elif self.path == "/api/dashboard":
            # On vérifie si le fichier de statistiques final existe
            if os.path.exists(STATS_FILE):
                # On ouvre le fichier de stats
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    stats_json = json.load(f)
                
                # On appelle notre méthode interne pour générer le HTML à partir de ces donnnées
                html = self.generate_dashboard_html(stats_json)
                
                # On envoie la réponse HTML
                self.send_response(200)
                # Notez le charset utf-8 pour bien gérer les accents
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                # Si le fichier de stats n'existe pas, on renvoie une erreur 404
                self.send_error(404)

        # Cas 3 : Le navigateur demande la page d'accueil (l'URL racine "/")
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            # On génère le code HTML complet de la page d'accueil
            html = self.generate_index_html()
            self.wfile.write(html.encode("utf-8"))
        
        # Cas par défaut : Pour tout autre fichier (CSS, JS externe, images...)
        else:
            # On laisse la classe parente (SimpleHTTPRequestHandler) essayer de trouver le fichier sur le disque
            super().do_GET()

    # --- Méthode utilitaire pour créer le HTML du tableau de bord ---
    def generate_dashboard_html(self, data):
        # On extrait les données utiles du dictionnaire
        stats = data.get("stats", {})
        chart_url = data.get("chart_url", "")
        
        # On formate les nombres pour avoir des espaces entre les milliers (ex: 1 000)
        total_cinemas = f"{stats.get('total_cinemas', 0):,}".replace(",", " ")
        total_ecrans = f"{stats.get('total_ecrans', 0):,}".replace(",", " ")
        total_fauteuils = f"{stats.get('total_fauteuils', 0):,}".replace(",", " ")
        source = stats.get("source", "Inconnue")
        
        # On construit dynamiquement la liste HTML des meilleures régions
        top_regions_html = ""
        # La boucle parcourt la liste des régions (nom, nombre)
        for reg, count in stats.get("top_regions", []):
            top_regions_html += f"<li><strong>{reg}</strong> : {count} cinémas</li>"

        # On retourne une chaîne de caractères contenant le HTML (f-string pour insérer les variables)
        return f"""
            <div class="result-section fade-in">
                <div class="container">
                    <div class="card">
                        <h2>Total Cinémas</h2>
                        <p>{total_cinemas}</p>
                    </div>
                    <div class="card">
                        <h2>Total Écrans</h2>
                        <p>{total_ecrans}</p>
                    </div>
                    <div class="card">
                        <h2>Total Fauteuils</h2>
                        <p>{total_fauteuils}</p>
                    </div>
                </div>

                <div class="chart-container">
                    <h2>Top 5 Régions (Nombre d'établissements)</h2>
                    <img src="{chart_url}" alt="Graphique Top 5 Régions">
                </div>
                
                <div class="list-container">
                    <h2>Détail Top 5</h2>
                    <ul>
                        {top_regions_html}
                    </ul>
                </div>

                <div class="footer">
                    <p>Source : {source}</p>
                    <p><a href="https://data.culture.gouv.fr/explore/dataset/etablissements-cinematographiques/" target="_blank">Voir le jeu de données original</a></p>
                </div>
            </div>
        """

    # --- Méthode utilitaire pour créer la page d'accueil ---
    def generate_index_html(self):
        # Cette fonction retourne tout le code HTML, CSS et JS de la page principale
        # C'est une grosse chaîne multi-lignes
        return """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAE 15 - Analyse Cinémas</title>
            <style>
                /* CSS intégré pour ne pas dépendre de fichiers externes */
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
                .main-wrapper { width: 100%; max-width: 900px; padding: 20px; text-align: center; }
                h1 { color: #2c3e50; margin-bottom: 10px; font-size: 2.5em; }
                h3 { color: #7f8c8d; font-weight: normal; margin-top: 0; margin-bottom: 40px; font-size: 1.2em; }
                
                #start-section { margin-top: 20px; }
                button { background-color: #3498db; color: white; border: none; padding: 15px 40px; font-size: 1.3em; border-radius: 50px; cursor: pointer; transition: transform 0.2s, background 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                button:hover { background-color: #2980b9; transform: translateY(-2px); }
                
                #progress-section { display: none; width: 100%; max-width: 600px; margin: 0 auto; }
                .progress-bar-container { width: 100%; background-color: #e0e0e0; border-radius: 15px; overflow: hidden; height: 30px; margin-top: 15px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); }
                .progress-bar { width: 0%; height: 100%; background-color: #27ae60; transition: width 0.5s ease; text-align: center; color: white; line-height: 30px; font-weight: bold; font-size: 0.9em; }
                #step-text { font-size: 1.1em; color: #555; margin-bottom: 5px; min-height: 1.2em; }
                
                .result-section { width: 100%; text-align: left; }
                .container { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 30px; justify-content: center; }
                .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); flex: 1; min-width: 200px; text-align: center; }
                .card h2 { margin: 0; font-size: 1.1em; color: #95a5a6; text-transform: uppercase; letter-spacing: 1px; }
                .card p { font-size: 2.5em; font-weight: bold; margin: 10px 0 0; color: #2c3e50; }
                
                .chart-container { text-align: center; margin-top: 40px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
                img { max-width: 100%; height: auto; border-radius: 8px; }
                
                .list-container { margin-top: 20px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
                ul { list-style-type: none; padding: 0; }
                li { padding: 12px; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; }
                li:last-child { border-bottom: none; }
                .footer { text-align: center; margin-top: 50px; color: #95a5a6; font-size: 0.85em; }
                
                .fade-in { animation: fadeIn 0.8s ease-out; }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            </style>
        </head>
        <body>
            <div class="main-wrapper">
                <h1>SAE 15 - Briac Le Meillat & Yanni Delattre Balcer</h1>
                <h3>Analyse des données Data.Gouv - Cinémas</h3>
                
                <!-- Section Démarrage -->
                <div id="start-section">
                    <button onclick="startProcess()">🚀 Lancer l'analyse</button>
                </div>
                
                <!-- Section Progression -->
                <div id="progress-section">
                    <div id="step-text">Initialisation...</div>
                    <div class="progress-bar-container">
                        <div id="progress-bar" class="progress-bar">0%</div>
                    </div>
                </div>
                
                <!-- Section Dashboard (sera remplie par JS) -->
                <div id="dashboard-section"></div>
            </div>

            <script>
                // --- Javascript côté client ---

                // Fonction appelée quand on clique sur le bouton start
                function startProcess() {
                    // On masque le bouton
                    document.getElementById('start-section').style.display = 'none';
                    // On affiche la barre de progression
                    document.getElementById('progress-section').style.display = 'block';
                    
                    // On envoie une requête POST au serveur pour dire "vas-y lance !"
                    fetch('/api/start', { method: 'POST' })
                        .then(() => pollProgress()); // Si ça marche, on commence à surveiller
                }
                
                // Fonction qui demande l'état d'avancement toutes les 500ms
                function pollProgress() {
                    const interval = setInterval(() => {
                        fetch('/api/progress')
                            .then(res => res.json())
                            .then(data => {
                                // Mise à jour de l'affichage (texte et largeur de la barre)
                                document.getElementById('step-text').innerText = data.step;
                                document.getElementById('progress-bar').style.width = data.percentage + '%';
                                document.getElementById('progress-bar').innerText = data.percentage + '%';
                                
                                // Si c'est fini (100%), on arrête et on charge la suite
                                if (data.percentage >= 100) {
                                    clearInterval(interval);
                                    setTimeout(loadDashboard, 1000);
                                }
                            });
                    }, 500);
                }
                
                // Fonction pour aller chercher le dashboard final généré par le serveur
                function loadDashboard() {
                    fetch('/api/dashboard')
                        .then(res => res.text())
                        .then(html => {
                            // On cache la progression
                            document.getElementById('progress-section').style.display = 'none';
                            // On injecte le HTML reçu dans la page
                            document.getElementById('dashboard-section').innerHTML = html;
                        });
                }
            </script>
        </body>
        </html>
        """

# --- Exécution du serveur ---

# On affiche un message dans la console pour dire que le serveur démarre
print(f"Serveur interactif démarré sur http://localhost:{PORT}")

# On tente d'ouvrir le navigateur par défaut automatiquement
try:
    webbrowser.open(f"http://localhost:{PORT}")
except:
    # Si l'ouverture échoue, ce n'est pas grave, l'utilisateur peut y aller manuellement
    pass

# On crée l'instance du serveur TCP
# ("" signifie écouter sur toutes les interfaces locales, PORT est le port choisi)
# VizHandler est notre classe qui gère comment répondre aux requêtes
try:
    with socketserver.TCPServer(("", PORT), VizHandler) as httpd:
        # On lance la boucle infinie qui attend les connexions
        # Le programme bloquera ici tant qu'on ne l'arrête pas (Ctrl+C)
        httpd.serve_forever()
except KeyboardInterrupt:
    # Si l'utilisateur appuie sur Ctrl+C, on capture l'interruption pour quitter proprement
    print("\nArrêt du serveur.")
except Exception as e:
    # Si une autre erreur survient (port déjà utilisé par exemple)
    print(f"\nErreur lors du démarrage du serveur : {e}")

