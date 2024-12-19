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
