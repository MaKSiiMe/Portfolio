# Plan de Développement Détaillé pour votre Moteur de Jeu Pokémon TCG Pocket

Voici une proposition de plan détaillé, étape par étape, pour vous guider dans la création de votre moteur de jeu Pokémon TCG Pocket en Python, en utilisant LemonTCG comme base. Ce plan est conçu pour être progressif et vous permettre de construire votre moteur de manière structurée.

## Phase 1 : Fondations et Configuration

### Étape 1 : Définition Précise des Objectifs et Prérequis (Rappel et Affinement)

*   **Objectif principal :** Créer un moteur Python pour Pokémon TCG Pocket capable de gérer la logique complète du jeu, sans interface graphique initialement, et compatible avec Gymnasium pour l'entraînement d'un agent IA.
*   **Fonctionnalités clés à implémenter (liste non exhaustive à affiner) :**
    *   Gestion des types de cartes Pokémon (Pokémon de base, Évolution, V, VMAX, VSTAR, etc.), Dresseur (Supporter, Objet, Stade), Énergie.
    *   Gestion des zones de jeu : Deck, Main, Pokémon Actif, Banc, Pile de Défausse, Cartes Récompense, Zone Perdue (si applicable à Pocket).
    *   Mécaniques de jeu : Pioche, attachement d'énergie, évolution, mise en jeu de Pokémon, utilisation d'objets et supporters, attaques (dégâts, effets), K.O., prise de récompenses, conditions de victoire/défaite.
    *   Gestion des statuts spéciaux (Empoisonné, Brûlé, Endormi, Paralysé, Confus).
    *   Effets des cartes (talents Pokémon, effets des cartes Dresseur, effets des attaques).
*   **Prérequis techniques :**
    *   Environnement Python 3 configuré.
    *   Connaissance de base de la programmation orientée objet en Python.
    *   Compréhension des règles de Pokémon TCG Pocket.

### Étape 2 : Installation, Configuration et Prise en Main de LemonTCG

*   **Cloner le dépôt LemonTCG :** `git clone https://github.com/Zitronenjoghurt/LemonTCG.git`
*   **Créer un environnement virtuel** pour votre projet et y installer les dépendances de LemonTCG (et les vôtres au fur et à mesure, comme Gymnasium).
*   **Explorer la structure du code de LemonTCG :** Prenez le temps de bien comprendre les répertoires principaux (`lemon_tcg`, `entities`, `event`, `game.py`, `context.py`) et les classes de base (`Card`, `Player`, `Deck`, `Board`, `GameState`, le système d'événements).
*   **Exécuter les exemples ou tests** s'il y en a dans LemonTCG pour voir son fonctionnement de base (même si le projet est "WORK IN PROGRESS").

## Phase 2 : Modélisation des Éléments Spécifiques à Pokémon TCG Pocket

### Étape 3 : Conception et Adaptation des Structures de Données pour les Cartes Pokémon

*   **Étendre la classe `Card` de LemonTCG :**
    *   Définissez une nouvelle classe (par exemple, `PokemonCard`) qui hérite de `lemon_tcg.entities.card.Card` ou la compose.
    *   Ajoutez les attributs spécifiques aux cartes Pokémon : nom, PV (Points de Vie), type (Feu, Eau, Psy, etc.), stade d'évolution (Base, Niveau 1, Niveau 2, V, VMAX...), attaques (nom, coût en énergie, dégâts, effets textuels), talent (nom, description), faiblesse, résistance, coût de retraite.
    *   Créez des classes similaires pour les cartes Dresseur (`TrainerCard` avec des sous-types comme `SupporterCard`, `ItemCard`, `StadiumCard`) et les cartes Énergie (`EnergyCard` avec des sous-types comme Énergie de base, Énergie spéciale).
*   **Définir le format de stockage des données des cartes :** LemonTCG charge les cartes depuis des fichiers JSON. Définissez la structure JSON pour vos cartes Pokémon, Dresseur et Énergie.
*   **Implémenter le chargement des cartes Pokémon :** Adaptez ou étendez la méthode `load_from_id` pour charger vos nouvelles structures de cartes.

### Étape 4 : Modélisation du Plateau et des Zones de Jeu Pokémon

*   **Adapter la classe `Board` de LemonTCG ou créer une nouvelle classe `PokemonBoard` :**
    *   Définissez les zones spécifiques : Pokémon Actif (1 emplacement), Banc (typiquement 5 emplacements), Pile de Défausse, Cartes Récompense (nombre défini), Deck.
    *   Pensez à comment représenter les cartes attachées (par exemple, les Énergies sur un Pokémon, les Outils Pokémon).
*   **Gérer les transitions de cartes entre les zones :** Implémentez des méthodes pour déplacer les cartes (piocher du Deck vers la Main, jouer un Pokémon de la Main vers le Banc ou l'Actif, défausser une carte, prendre une Récompense, etc.).

## Phase 3 : Implémentation de la Logique de Jeu

### Étape 5 : Implémentation de la Logique de Base du Tour et des Phases de Jeu

*   **Définir la structure d'un tour de jeu Pokémon :**
    *   Début du tour (pioche, effets de début de tour).
    *   Phase principale : actions du joueur (jouer des Pokémon de base, attacher une énergie, faire évoluer, jouer des cartes Dresseur, utiliser des talents, battre en retraite).
    *   Phase d'attaque (déclarer l'attaque, appliquer les dégâts et effets).
    *   Fin du tour (vérification des K.O., effets de fin de tour).
*   **Adapter ou étendre `GameState` et `Game` de LemonTCG :**
    *   Intégrez la notion de joueur actif, le comptage des tours, et l'état actuel de la phase de jeu.
    *   Implémentez la logique de passage d'une phase à l'autre et d'un joueur à l'autre.

### Étape 6 : Ajout et Test des Actions de Base du Joueur

*   **Implémenter les actions fondamentales :**
    *   Piocher une carte.
    *   Jouer un Pokémon de base sur le Banc.
    *   Promouvoir un Pokémon du Banc vers le Pokémon Actif.
    *   Attacher une carte Énergie à un Pokémon.
    *   Faire évoluer un Pokémon.
    *   Jouer une carte Dresseur (Objet, Supporter simple pour commencer).
    *   Battre en retraite.
*   **Utiliser le système d'événements de LemonTCG** pour signaler ces actions et permettre à d'autres parties du jeu de réagir (par exemple, un talent qui se déclenche quand une énergie est attachée).
*   **Commencer à écrire des tests unitaires** pour chaque action afin de vérifier leur bon fonctionnement.

### Étape 7 : Développement de la Logique des Combats et des Effets de Cartes Complexes

*   **Implémenter le système de combat :**
    *   Calcul des dégâts (prise en compte de la Faiblesse et de la Résistance).
    *   Application des effets des attaques (dégâts supplémentaires, statuts spéciaux, pioche de cartes, défausse d'énergie, etc.).
    *   Gestion des K.O. et prise des cartes Récompense.
*   **Implémenter les statuts spéciaux :** Logique pour Empoisonné, Brûlé, Endormi, Paralysé, Confus et leurs effets à chaque tour.
*   **Gérer les talents Pokémon et les effets des cartes Dresseur plus complexes :** C'est souvent la partie la plus longue et la plus délicate. Abordez-les progressivement, carte par carte ou par type d'effet.
    *   Pensez à un système flexible pour définir et exécuter ces effets (par exemple, des fonctions ou des classes dédiées à chaque effet, déclenchées par le système d'événements).
*   **Conditions de victoire et de défaite :** Implémentez la vérification (plus de cartes Récompense à prendre, plus de Pokémon en jeu, deck vide au moment de piocher).

## Phase 4 : Intégration de l'Intelligence Artificielle et Finalisation

### Étape 8 : Intégration d'une Interface Compatible Gymnasium pour l'IA

*   **Définir l'environnement Gymnasium (`gym.Env`) :**
    *   **Espace d'observation (`observation_space`) :** Déterminez quelles informations de `GameState` seront visibles par l'agent IA (main du joueur, Pokémon en jeu et leurs états, défausse, récompenses restantes, etc.). Représentez cet état de manière numérique ou structurée.
    *   **Espace d'action (`action_space`) :** Définissez toutes les actions possibles qu'un agent peut prendre (jouer une carte spécifique de sa main, choisir une attaque d'un Pokémon, etc.). Cela peut être un espace discret avec un grand nombre d'actions possibles, ou un espace plus structuré (par exemple, choisir un type d'action, puis les paramètres de cette action).
    *   **Méthode `step(action)` :** Prend une action de l'agent, l'applique au moteur de jeu, calcule la récompense (par exemple, +1 pour avoir pris une carte Récompense, -1 pour avoir perdu un Pokémon, 0 sinon), retourne la nouvelle observation, la récompense, si la partie est terminée (`done`), et des informations supplémentaires (`info`).
    *   **Méthode `reset()` :** Réinitialise le jeu pour une nouvelle partie et retourne l'observation initiale.
    *   **Méthode `render()` (optionnel pour le terminal) :** Affiche l'état du jeu dans le terminal pour le débogage ou l'observation humaine.
*   **Connecter le moteur de jeu à l'interface Gymnasium :** Le moteur doit exposer des fonctions pour que l'environnement Gymnasium puisse obtenir l'état du jeu, envoyer des actions, et être notifié des résultats.

### Étape 9 : Validation, Tests Approfondis et Documentation du Moteur

*   **Tests unitaires :** Écrivez des tests pour chaque module, classe, et fonction critique, en particulier pour la logique des règles et les effets des cartes.
*   **Tests d'intégration :** Testez des scénarios de jeu complets pour vous assurer que les différentes parties du moteur fonctionnent correctement ensemble.
*   **Jouer contre soi-même ou un agent simple :** Créez un agent IA très basique (par exemple, qui joue des actions aléatoires valides) pour tester le flux de jeu via l'interface Gymnasium.
*   **Documentation du code :** Commentez votre code (docstrings pour les classes et fonctions) pour expliquer son fonctionnement.
*   **Documentation utilisateur/développeur :** Rédigez un README expliquant comment utiliser le moteur, comment ajouter de nouvelles cartes, et comment interagir avec l'interface Gymnasium.

### Étape 10 : (Optionnel) Préparation d'un Guide de Déploiement et d'Utilisation

*   Si vous prévoyez de partager votre moteur, expliquez comment l'installer, le configurer, et lancer une partie ou un entraînement d'IA.

## Conseils Généraux pour le Projet

*   **Commencez simple :** N'essayez pas d'implémenter toutes les cartes et tous les effets dès le début. Commencez avec un sous-ensemble de cartes et de mécaniques, puis étendez progressivement.
*   **Utilisez la gestion de version (Git) :** Sauvegardez votre travail régulièrement et utilisez des branches pour développer de nouvelles fonctionnalités.
*   **Modularité :** Concevez votre code de manière modulaire pour faciliter les tests, la maintenance et les évolutions futures.
*   **Tests continus :** Écrivez des tests au fur et à mesure que vous développez, pas seulement à la fin.
*   **Référencez les règles officielles :** Gardez les règles de Pokémon TCG Pocket à portée de main pour vous assurer de l'exactitude de votre implémentation.
*   **Statut "WORK IN PROGRESS" de LemonTCG :** Soyez prêt à devoir potentiellement corriger ou compléter des parties de la bibliothèque LemonTCG elle-même si vous rencontrez des limitations ou des bugs.

Ce plan est une feuille de route. N'hésitez pas à l'adapter en fonction de vos découvertes et de l'évolution de votre projet. Bon développement ! J'espère que ce plan détaillé vous sera utile.

