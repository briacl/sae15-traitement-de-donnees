# On va utiliser la librairie requests afin de faire la requête http vers le site qui nous intrésse, afin d'en récupérer des données
import requests

# On définit l'adresse où se trouve le fichier à télécharger
url = "https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/exports/csv"

# Via une requête http de type get, on (python) contacte le serveur et récupère la réponse, on place le tout dans la var response
response = requests.get(url)

# Ici on va d'abord mettre en place la gestion d'erreur, si code = 200 alors ça marche, sinon il nous affiche le code erreur, ex 404 pour not found
if response.status_code == 200:

    # Définition du nom du fichier
    filename = f"etablissements_cinematographiques.csv"


    # On ouvre (ou créer si inexistant) un fichier pour écrire le contenu
    with open(filename, "w", encoding="utf-8") as f:
        # Et on écrit directement dans le fichier le contenu de la var response
        f.write(response.text)

    # On affiche que la procédure a aboutie
    print(f"Données téléchargées et enregistrées dans {filename}")

else:
    # On affiche qu'une erreur s'est produite, et on précise laquelle
    print(f"Erreur lors de la requête : {response.status_code}")
