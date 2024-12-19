# Projet Proteus

## Diagramme fonctionnel

- **Entrée 230V AC** : Il s'agit de l'entrée principale, généralement une tension alternative de 230V provenant du réseau.
- **Protection** : Ce bloc protège le circuit contre les surtensions, les surintensités, ou d'autres anomalies électriques.
- **Redressement** : Cette étape convertit la tension alternative (AC) en tension continue (DC).
- **Filtrage** : Après le redressement, cette étape lisse la tension pour réduire les ondulations et fournir une tension DC stable.
- **Découpage de puissance** : C'est ici que la tension continue est découpée en impulsions à haute fréquence grâce à un système de modulation (PWM). Cela permet une régulation et une conversion efficaces de l'énergie.
- **Transformateur** : Ce composant convertit la tension découpée à la fréquence souhaitée et ajuste la tension pour correspondre aux besoins du circuit de sortie.
- **Retour** : Ce chemin de rétroaction fournit des informations sur la sortie au système de contrôle (PWM), permettant d'ajuster le découpage de puissance pour maintenir la stabilité.
- **PWM (Modulation de largeur d'impulsion)** : Ce bloc génère des signaux d'impulsions pour commander le découpage de puissance en fonction des données de rétroaction.
- **Sortie (Source)** : C'est la tension ou le courant final, utilisé pour alimenter une charge ou un appareil.


https://github.com/user-attachments/assets/279c424c-68a0-4bd7-84c4-b62d18692735

## Résultats de l'oscilloscope

**Canal A (Jaune) – Tension secteur redressée (bloc "Redressement")**
- **Observation** : La forme d’onde jaune est une sinusoïde redressée double alternance.
- **Lien fonctionnel** :
  - Elle provient du pont de diodes.
  - Le signal correspond à la tension secteur 220 V redressée sans filtrage 
complet.
  - Cette tension sert d’entrée à l’étage de découpage de puissance.

**Canal B (Rose) – Tension après filtrage (bloc "Filtrage")**
- **Observation** : La forme d’onde rose est une sinusoïde lissée avec peu d’ondulations.
  - Cette tension résulte du condensateur de filtrage placé après le pont de 
diodes.
  - Elle représente une tension continue partiellement lissée utilisée pour 
alimenter le découpage PWM.

**Canal C (Bleu) – Tension de sortie du transformateur (bloc "Transformateur")**
- **Observation** : La forme d’onde bleue est une sinusoïde tronquée ou modulée.
- **Lien fonctionnel** :
  - Le signal est généré après le transformateur haute fréquence, où le découpage 
PWM influence la forme.
  - Cela montre une conversion de tension à travers le transformateur.
 
**Canal D (Vert) – Signal de rétroaction (bloc "Régulation")**
- **Observation** : Le signal vert est un signal carré ou numérique.
- **Lien fonctionnel** :
  - Il représente la rétroaction de la sortie vers le circuit de commande PWM.
  - Ce signal ajuste dynamiquement la largeur des impulsions pour réguler la 
tension en sortie.

## Comment Exécuter le Projet

Suivez ces étapes pour exécuter le projet localement :

### Prérequis

Assurez-vous d'avoir Proteus installé sur votre machine :

- [Proteus](https://www.labcenter.com/downloads/)

### Exécution Locale

1. **Cloner le Référentiel**:
   - Exécutez `git clone https://github.com/votre-utilisateur/movie-app.git` pour cloner le projet.

2. **Lancement du projet**:
   - Exécutez `start` pour démarrer le projet avec Proteus.




