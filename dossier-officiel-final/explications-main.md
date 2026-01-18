# Explications : Script Principal (`main.py`)

Ce fichier détaille le fonctionnement du "Chef d'orchestre" du projet.

## 📌 Rôle global
C'est le point d'entrée unique. Il simplifie la vie de l'utilisateur : une seule commande (`python main.py`) suffit pour tout lancer dans le bon ordre. Il garantit que le pipeline est respecté : on n'essaie pas de visualiser des données qui n'ont pas encore été téléchargées.

---

## 🔍 Explication détaillée (Ligne par Ligne)

### 1. Robustesse des chemins

```python
12:     base_dir = os.path.dirname(os.path.abspath(__file__))
15:     scraper_script = os.path.join(base_dir, "scraper-data.py")
```
**Important** : On ne fait pas juste `scraper-data.py`. On calcule le chemin absolu du dossier où se trouve le script.
Pourquoi ? Si l'utilisateur lance le script depuis un autre dossier (ex: `python dossier/main.py`), Python pourrait ne pas trouver les autres fichiers. Avec cette méthode, peu importe d'où on lance la commande, le script retrouvera toujours ses "petits frères".

### 2. Exécution Séquentielle

```python
24:         subprocess.run([sys.executable, scraper_script], check=True)
```
C'est la commande clé du script : `subprocess.run`.
*   `sys.executable` : C'est le chemin vers l'interpréteur Python actuel (celui qui exécute `main.py`). Cela garantit qu'on utilise le même environnement (et donc les mêmes librairies installées) pour les sous-scripts.
*   `check=True` : Si le script `scraper` plante (renvoie une erreur), `main.py` s'arrête immédiatement et lève une exception. Cela évite l'effet "domino" (essayer de formater un fichier qui n'a pas été téléchargé).

```python
25:         print(f"✓ Extraction terminée en {time.time() - start_time:.2f}s.")
```
On utilise `time.time()` pour chronométrer chaque étape. C'est un petit bonus "pro" qui permet de voir quel script prend du temps (performance).

### 3. Gestion globale des erreurs

```python
37:     except subprocess.CalledProcessError as e:
38:         print(f"\nUne erreur est survenue lors de l'exécution d'un script : {e}")
39:         sys.exit(1)
```
On intercepte les erreurs de tous les sous-scripts ici.
*   `sys.exit(1)` : On quitte proprement le programme en signalant au système d'exploitation que ça s'est mal passé (code de retour 1).

```python
43:     except KeyboardInterrupt:
44:         print("\n\nArrêt de la procédure par l'utilisateur.")
```
Permet à l'utilisateur de faire "Ctrl+C" à tout moment pour tout arrêter proprement, sans voir un gros message d'erreur rouge illisible ("Traceback").
