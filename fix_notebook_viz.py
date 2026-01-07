import json

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "web-visualization",
    "metadata": {},
    "outputs": [],
    "source": [
     "import json\n",
     "import webbrowser\n",
     "import os\n",
     "\n",
     "# Chargement des données filtrées\n",
     "try:\n",
     "    with open(\"data-filtered.json\", \"r\", encoding=\"utf-8\") as f:\n",
     "        data = json.load(f)\n",
     "except FileNotFoundError:\n",
     "    print(\"Le fichier data-filtered.json n'existe pas. Veuillez lancer la cellule précédente.\")\n",
     "    data = {}\n",
     "\n",
     "# Préparation des données pour le Graphique (Chart.js)\n",
     "regions = list(data.keys())\n",
     "counts = list(data.values())\n",
     "\n",
     "# Création du contenu HTML\n",
     "html_content = f\"\"\"\n",
     "<!DOCTYPE html>\n",
     "<html lang=\"fr\">\n",
     "<head>\n",
     "    <meta charset=\"UTF-8\">\n",
     "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n",
     "    <title>Visualisation des Salles de Cinéma</title>\n",
     "    <script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script>\n",
     "    <style>\n",
     "        body {{ font-family: sans-serif; padding: 20px; }}\n",
     "        .container {{ width: 80%; margin: auto; }}\n",
     "        h1 {{ text-align: center; }}\n",
     "    </style>\n",
     "</head>\n",
     "<body>\n",
     "    <div class=\"container\">\n",
     "        <h1>Nombre de Salles de Cinéma par Région</h1>\n",
     "        <canvas id=\"myChart\"></canvas>\n",
     "    </div>\n",
     "\n",
     "    <script>\n",
     "        const ctx = document.getElementById('myChart').getContext('2d');\n",
     "        const myChart = new Chart(ctx, {{\n",
     "            type: 'bar',\n",
     "            data: {{\n",
     "                labels: {json.dumps(regions)},\n",
     "                datasets: [{{\n",
     "                    label: 'Nombre de salles',\n",
     "                    data: {json.dumps(counts)},\n",
     "                    backgroundColor: 'rgba(54, 162, 235, 0.6)',\n",
     "                    borderColor: 'rgba(54, 162, 235, 1)',\n",
     "                    borderWidth: 1\n",
     "                }}]\n",
     "            }},\n",
     "            options: {{\n",
     "                scales: {{\n",
     "                    y: {{\n",
     "                        beginAtZero: true\n",
     "                    }}\n",
     "                }}\n",
     "            }}\n",
     "        }});\n",
     "    </script>\n",
     "</body>\n",
     "</html>\n",
     "\"\"\"\n",
     "\n",
     "# Sauvegarde du fichier HTML\n",
     "html_filename = \"visualisation.html\"\n",
     "with open(html_filename, \"w\", encoding=\"utf-8\") as f:\n",
     "    f.write(html_content)\n",
     "\n",
     "print(f\"Page web générée : {html_filename}\")\n",
     "\n",
     "# Ouverture automatique dans le navigateur\n",
     "webbrowser.open('file://' + os.path.realpath(html_filename))"
    ]
}

with open('explications.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Append if not detected
source_start = new_cell['source'][0]
found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and len(cell['source']) > 0 and cell['source'][0] == source_start:
        found = True
        break

if not found:
    nb['cells'].append(new_cell)
    with open('explications.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook updated: Visualisation cell appended.")
else:
    print("Visualisation cell already present.")
