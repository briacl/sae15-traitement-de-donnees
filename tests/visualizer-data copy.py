# On importe le module http.server qui permet de créer un serveur web simple
import http.server
# On importe socketserver pour gérer les connexions TCP (réseau)
import socketserver
# On importe le module json pour manipuler les données au format JSON
import json
# On importe le module os pour les opérations système
import os
# On importe subprocess pour lancer des processus
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
STATS_FILE = "formatted-etablissements-cinematographiques.json"
# On définit le nom du fichier qui sert à suivre la progression du traitement
PROGRESS_FILE = "progress.json"

# Le script doit s'assurer de démarrer avec un état propre
# On vérifie si un fichier de progression existe déjà d'une exécution précédente
if os.path.exists(PROGRESS_FILE):
    # Si le fichier existe, on le supprime pour éviter d'afficher des données obsolètes
    os.remove(PROGRESS_FILE)

# --- Définition de la fonction de traitement en arrière-plan ---
def run_process_async():
    """Lance la pipeline de données (scraper + formateur) en arrière-plan."""
    # CORRECTION : Utilisation de os.getcwd() au lieu de __file__ pour les notebooks
    current_dir = os.getcwd()
    # On suppose que le dossier tests est dans le dossier courant
    script_dir = os.path.join(current_dir, "tests")
    
    # Chemins absolus vers les scripts 'copy'
    scraper_script = os.path.join(script_dir, "scraper-data copy.py")
    formater_script = os.path.join(script_dir, "formater-data copy.py")
    
    # Fonction helper pour mettre à jour le fichier de progression
    def update_progress(step, percentage):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump({"step": step, "percentage": percentage}, f)

    try:
        # 1. Démarrage
        update_progress("Démarrage du téléchargement...", 10)
        
        # 2. Lancement du scraper
        print(f"Lancement de {scraper_script}...")
        # check=True lève une exception si le script échoue
        subprocess.run([sys.executable, scraper_script], check=True)
        
        # 3. Transition
        update_progress("Formatage des données...", 50)
        
        # 4. Lancement du formateur
        print(f"Lancement de {formater_script}...")
        subprocess.run([sys.executable, formater_script], check=True)
        
        # 5. Fin
        update_progress("Traitement terminé !", 100)
        
    except Exception as e:
        print(f"Erreur durant le traitement : {e}")
        update_progress(f"Erreur : {e}", 0)


# Cette classe hérite de http.server.SimpleHTTPRequestHandler pour gérer les fichiers statiques de base
class VizHandler(http.server.SimpleHTTPRequestHandler):
    
    # Cette méthode est appelée automatiquement quand le serveur reçoit une requête POST
    def do_POST(self):
        if self.path == "/api/start":
            # Lancement du thread en arrière-plan
            t = threading.Thread(target=run_process_async)
            t.start()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))
        else:
            self.send_error(404)

    # Cette méthode est appelée automatiquement quand le serveur reçoit une requête GET
    def do_GET(self):
        if self.path == "/api/progress":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            
            data = {"step": "En attente...", "percentage": 0}
            if os.path.exists(PROGRESS_FILE):
                try:
                    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except:
                    pass
            self.wfile.write(json.dumps(data).encode("utf-8"))
            
        elif self.path == "/api/dashboard":
            if os.path.exists(STATS_FILE):
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    stats_json = json.load(f)
                html = self.generate_dashboard_html(stats_json)
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_error(404)

        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = self.generate_index_html()
            self.wfile.write(html.encode("utf-8"))
        else:
            super().do_GET()

    def generate_dashboard_html(self, data):
        stats = data.get("stats", {})
        chart_url = data.get("chart_url", "")
        
        total_cinemas = f"{stats.get('total_cinemas', 0):,}".replace(",", " ")
        total_ecrans = f"{stats.get('total_ecrans', 0):,}".replace(",", " ")
        total_fauteuils = f"{stats.get('total_fauteuils', 0):,}".replace(",", " ")
        source = stats.get("source", "Inconnue")
        
        top_regions_html = ""
        for reg, count in stats.get("top_regions", []):
            top_regions_html += f"<li><strong>{reg}</strong> : {count} cinémas</li>"

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
                    <h2>Top 5 Régions</h2>
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

    def generate_index_html(self):
        return """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAE 15 - Analyse Cinémas</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
                .main-wrapper { width: 100%; max-width: 900px; text-align: center; }
                h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
                h3 { color: #7f8c8d; font-weight: normal; margin-bottom: 40px; }
                button { background-color: #3498db; color: white; border: none; padding: 15px 40px; font-size: 1.3em; border-radius: 50px; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                button:hover { background-color: #2980b9; transform: translateY(-2px); }
                .progress-bar-container { width: 100%; background-color: #e0e0e0; border-radius: 15px; overflow: hidden; height: 30px; margin-top: 20px; }
                .progress-bar { width: 0%; height: 100%; background-color: #27ae60; transition: width 0.5s; text-align: center; color: white; line-height: 30px; font-weight: bold; }
                .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); flex: 1; min-width: 200px; margin: 10px; }
                .container { display: flex; flex-wrap: wrap; justify-content: center; margin-top: 30px; }
                ul { list-style: none; padding: 0; text-align: left; }
                li { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
            </style>
        </head>
        <body>
            <div class="main-wrapper">
                <h1>SAE 15 - Briac Le Meillat & Yanni Delattre Balcer</h1>
                <h3>Analyse des données Data.Gouv - Cinémas</h3>
                
                <div id="start-section">
                    <button onclick="startProcess()">🚀 Lancer l'analyse</button>
                </div>
                
                <div id="progress-section" style="display:none;">
                    <div id="step-text">Initialisation...</div>
                    <div class="progress-bar-container">
                        <div id="progress-bar" class="progress-bar">0%</div>
                    </div>
                </div>
                
                <div id="dashboard-section"></div>
            </div>

            <script>
                function startProcess() {
                    document.getElementById('start-section').style.display = 'none';
                    document.getElementById('progress-section').style.display = 'block';
                    fetch('/api/start', { method: 'POST' }).then(() => pollProgress());
                }
                
                function pollProgress() {
                    const interval = setInterval(() => {
                        fetch('/api/progress').then(res => res.json()).then(data => {
                            document.getElementById('step-text').innerText = data.step;
                            document.getElementById('progress-bar').style.width = data.percentage + '%';
                            document.getElementById('progress-bar').innerText = data.percentage + '%';
                            if (data.percentage >= 100) {
                                clearInterval(interval);
                                setTimeout(loadDashboard, 1000);
                            }
                        });
                    }, 500);
                }
                
                function loadDashboard() {
                    fetch('/api/dashboard').then(res => res.text()).then(html => {
                        document.getElementById('progress-section').style.display = 'none';
                        document.getElementById('dashboard-section').innerHTML = html;
                    });
                }
            </script>
        </body>
        </html>
        """

print(f"Serveur interactif démarré sur http://localhost:{PORT}")

# On tente d'ouvrir le navigateur par défaut automatiquement
try:
    webbrowser.open(f"http://localhost:{PORT}")
except:
    pass

try:
    # allow_reuse_address évite le problème du port bloqué si on relance vite
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), VizHandler) as httpd:
        # On lance la boucle infinie qui attend les connexions
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nArrêt du serveur.")
except Exception as e:
    print(f"\nErreur lors du démarrage du serveur : {e}")
