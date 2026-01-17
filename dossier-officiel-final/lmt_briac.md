# Portfolio SAE 105 - Traitement de données

**Nom :** Le Meillat  
**Prénom :** Briac  
**Formation :** BUT Réseaux & Télécommunications

## Présentation du projet

Dans le cadre de la SAE 105, j'ai travaillé en binôme avec Yanni Delattre-Balcer sur un projet de traitement de données portant sur les établissements cinématographiques en France. Nous avons développé des scripts Python permettant d'extraire des données via une API, de les formater et de les visualiser.

Le projet consiste en une chaîne de traitement automatisée qui télécharge un fichier CSV depuis le site data.culture.gouv.fr, l'analyse par région, puis génère des visualisations via une interface web.

## Compétences mises en œuvre

### AC13.01 - Utiliser un système informatique et ses outils

**Mise en œuvre :** J'ai pris en charge la **mise en ligne et la configuration du projet sur GitLab**. J'ai assuré le versionnage du code et la gestion du dépôt pour permettre un travail collaboratif fluide avec mon binôme tout au long du projet.

### AC13.03 - Traduire un algorithme, dans un langage et pour un environnement donné

**Mise en œuvre :** J'ai effectué la seconde moitié du travail sur le script `formater-data.py`. J'ai systématiquement vérifié et complété la partie de Yanni pour garantir la cohérence de l'agrégation finale des données (écrans et fauteuils par région administrative).

### AC13.04 - Connaître l'architecture et les technologies d'un site Web

**Mise en œuvre :** J'ai été responsable de la **mise en ligne sur le Web** et de l'affichage des résultats. J'ai intégré l'API QuickChart pour transformer nos fichiers JSON en graphiques dynamiques et j'ai co-réalisé le diaporama de soutenance avec Yanni.

### AC13.05 - Choisir les mécanismes de gestion de données

**Mise en œuvre :** J'ai sécurisé le traitement des données dans `formater-data.py` en ajoutant des mécanismes de gestion d'erreurs (`try/except`) lors de la conversion des types de données. Cela a permis d'ignorer les données corrompues et de produire un fichier JSON final parfaitement structuré.

**Répartition du travail :**
- **Yanni :** Script de récupération (scraper), Diagramme de Gantt, Diaporama, 1ère moitié du formatage.
- **Moi :** Mise en ligne GitLab, Affichage Web, Cohérence du formatage, Diaporama.
- **Commun :** Analyse, Tests et Finalisation.

## Ressources mobilisées

### R1.09 - Introduction aux technologies Web
Mise en œuvre de l'affichage web et utilisation d'APIs tierces pour la génération automatisée de graphiques.

### R1.08 - Systèmes d'exploitation
Gestion du dépôt distant GitLab et utilisation des outils de ligne de commande pour le versionnage du projet.

## Tableau récapitulatif des compétences

| Compétence | Code| Justification |
|------------|------|---------------|
| Utiliser un système informatique et ses outils | AC13.01 | Configuration et gestion du dépôt GitLab |
| Traduire un algorithme dans un langage donné | AC13.03 | Finalisation et vérification de la cohérence du formatage |
| Connaître l'architecture et les technologies Web | AC13.04 | Mise en ligne web et intégration QuickChart |
| Choisir les mécanismes de gestion de données | AC13.05 | Gestion des erreurs de données et export JSON propre |

---

## Ressources mobilisées - Détail

| Ressource | Utilisation dans le projet |
|-----------|---------------------------|
| R1.08 - Systèmes d'exploitation | Utilisation de Git pour le travail en équipe | 
| R1.09 - Technologies Web | Intégration de services de visualisation (QuickChart) | 
| R1.15 - Gestion de projet | Collaboration et suivi des tâches assignées au binôme |