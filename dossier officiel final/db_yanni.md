# Portfolio SAE 105 - Traitement de données

**Nom :** Delattre-Balcer  
**Prénom :** Yanni  
**Formation :** BUT Réseaux & Télécommunications

## Présentation du projet

Dans le cadre de la SAE 105, j'ai travaillé en binôme avec Briac Le Meillat sur un projet de traitement de données portant sur les établissements cinématographiques en France. Nous avons développé des scripts Python permettant d'extraire des données via une API, de les formater et de les visualiser.

Le projet consiste en une chaîne de traitement automatisée qui télécharge un fichier CSV depuis le site data.culture.gouv.fr, l'analyse par région, puis génère des visualisations via une interface web.

## Compétences mises en œuvre

### AC13.02 - Lire, exécuter, corriger et modifier un programme

**Mise en œuvre :** J'ai conçu et développé le script de récupération des données (`scraper-data.py`). J'ai utilisé la bibliothèque `requests` pour automatiser l'extraction du fichier CSV et j'ai intégré une gestion d'erreurs pour vérifier la validité de la réponse du serveur avant l'écriture du fichier.

### AC13.03 - Traduire un algorithme, dans un langage et pour un environnement donné

**Mise en œuvre :** J'ai réalisé la première moitié du travail de formatage dans le script `formater-data.py`. J'ai mis en place la structure de lecture du fichier CSV avec `csv.DictReader` et l'extraction initiale des données nécessaires comme les régions, les écrans et les fauteuils.

### AC13.04 - Connaître l'architecture et les technologies d'un site Web

**Mise en œuvre :** En collaboration avec mon binôme, j'ai conçu le **diaporama** de présentation pour la soutenance. J'ai également participé à l'élaboration de l'interface d'affichage web pour exposer les résultats de nos analyses de manière graphique.

### AC13.06 - S'intégrer dans un environnement propice au développement et au travail collaboratif

**Mise en œuvre :** J'ai assuré la planification du projet en créant le **diagramme de Gantt**. Cela nous a permis d'organiser nos 10 tâches principales, du paramétrage de l'équipe jusqu'à la démonstration finale, en respectant les délais impartis entre le 4 et le 16 janvier 2026.

**Répartition du travail :**
- **Moi :** Script de récupération (scraper), Diagramme de Gantt, Diaporama, 1ère moitié du formatage.
- **Briac :** Mise en ligne GitLab, Affichage Web, Cohérence du formatage, Diaporama.
- **Commun :** Analyse, Tests et Finalisation.

## Ressources mobilisées

### R1.07 - Fondamentaux de la programmation
Programmation en Python, utilisation de bibliothèques externes (`requests`) et gestion des structures de données comme les dictionnaires.

### R1.15 - Gestion de projet
Création d'un diagramme de Gantt pour planifier les étapes du projet et suivre l'avancement des tâches du binôme.

## Tableau récapitulatif des compétences

| Compétence | Code| Justification |
|------------|------|---------------|
| Lire, exécuter, corriger et modifier un programme | AC13.02 | Développement du script de récupération API Python |
| Traduire un algorithme dans un langage donné | AC13.03 | Implémentation de la structure initiale de traitement CSV |
| Connaître l'architecture et les technologies Web | AC13.04 | Création du diaporama et aide à l'interface d'affichage |
| S'intégrer dans un environnement collaboratif | AC13.06 | Gestion du planning via le diagramme de Gantt |

---

## Ressources mobilisées - Détail

| Ressource | Utilisation dans le projet |
|-----------|---------------------------|
| R1.07 - Programmation | Utilisation de Python pour l'automatisation et le traitement | 
| R1.09 - Technologies Web | Compréhension des requêtes HTTP GET pour l'API | 
| R1.15 - Gestion de projet | Planification temporelle via Gantt |