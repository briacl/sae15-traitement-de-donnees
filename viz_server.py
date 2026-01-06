#!/usr/bin/env python3
"""
viz_server.py

Serveur HTTP interactif avec suivi de progression pour process_data.py.
"""
import http.server
import socketserver
import json
import os
import subprocess
import webbrowser
import threading
import sys
import shutil

PORT = 8000
STATS_FILE = "cinemas_stats.json"
PROGRESS_FILE = "progress.json"

# Nettoyage initial
if os.path.exists(PROGRESS_FILE):
    os.remove(PROGRESS_FILE)

def run_process_async():
    """Lance process_data.py en arrière-plan."""
    # On utilise sys.executable pour être sûr d'utiliser le même interpréteur
    subprocess.run([sys.executable, "process_data.py"])

class VizHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/start":
            # Lancement du thread
            t = threading.Thread(target=run_process_async)
            t.start()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "started"}).encode("utf-8"))
        else:
            self.send_error(404)

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
            # Renvoie le HTML du dashboard final (fragment)
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
            # Page d'accueil avec JS pour l'interactivité
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

    def generate_index_html(self):
        return """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SAE 15 - Analyse Cinémas</title>
            <style>
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
                
                /* Styles dashboard injectés */
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
                
                <div id="start-section">
                    <button onclick="startProcess()">🚀 Lancer l'analyse</button>
                </div>
                
                <div id="progress-section">
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
                    
                    fetch('/api/start', { method: 'POST' })
                        .then(() => pollProgress());
                }
                
                function pollProgress() {
                    const interval = setInterval(() => {
                        fetch('/api/progress')
                            .then(res => res.json())
                            .then(data => {
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
                    fetch('/api/dashboard')
                        .then(res => res.text())
                        .then(html => {
                            document.getElementById('progress-section').style.display = 'none';
                            document.getElementById('dashboard-section').innerHTML = html;
                        });
                }
            </script>
        </body>
        </html>
        """

def main():
    print(f"Serveur interactif démarré sur http://localhost:{PORT}")
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        pass

    with socketserver.TCPServer(("", PORT), VizHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur.")

if __name__ == "__main__":
    main()
