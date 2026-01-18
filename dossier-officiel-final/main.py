import subprocess
import sys
import os
import time

def main():
    print("============================================================")
    print("      SAE 15 - Lancement de la procédure complète")
    print("============================================================")

    # Obtenir le chemin du répertoire du script courant pour s'assurer qu'on exécute les fichiers du bon endroit
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Définition des chemins des scripts
    scraper_script = os.path.join(base_dir, "scraper-data.py")
    formater_script = os.path.join(base_dir, "formater-data.py")
    visualizer_script = os.path.join(base_dir, "visualizer-data.py")

    try:
        # Étape 1 : Extraction (Scraper)
        print("\n[1/3] Lancement de l'extraction des données (scraper-data.py)...")
        start_time = time.time()
        # On passe sys.executable pour utiliser le même interpréteur Python (celui du venv s'il est activé)
        subprocess.run([sys.executable, scraper_script], check=True)
        print(f"✓ Extraction terminée en {time.time() - start_time:.2f}s.")

        # Étape 2 : Transformation (Formater)
        print("\n[2/3] Lancement du traitement des données (formater-data.py)...")
        start_time = time.time()
        subprocess.run([sys.executable, formater_script], check=True)
        print(f"✓ Traitement terminé en {time.time() - start_time:.2f}s.")

        # Étape 3 : Visualisation (Visualizer)
        print("\n[3/3] Lancement de la visualisation (visualizer-data.py)...")
        subprocess.run([sys.executable, visualizer_script], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"\nUne erreur est survenue lors de l'exécution d'un script : {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\nFichier introuvable : {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nArrêt de la procédure par l'utilisateur.")
        sys.exit(0)

if __name__ == "__main__":
    main()
