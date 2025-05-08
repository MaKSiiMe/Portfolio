# 📘 Glossaire et Concepts Clés - Reinforcement Learning pour Jeux de Cartes

## Table des Matières
1. [🧠 Concepts Fondamentaux](#-concepts-fondamentaux)
2. [📦 Algorithmes de RL](#-algorithmes-de-rl)
3. [🏗 Architectures de Réseaux](#-architectures-de-réseaux)
4. [🔧 AutoML / AutoRL et Optimisation](#-automl--autorrl-et-optimisation)
5. [⚙️ Environnements et Outils](#️-environnements-et-outils)
6. [📖 Définitions plus détaillées](#-définitions-plus-détaillées)

---

## 🧠 Concepts Fondamentaux

| Terme                          | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **[MDP (Markov Decision Process)](#01-mdp-markov-decision-process)** | Modélisation mathématique d’un environnement de décision avec états, actions, transitions, récompenses.  |
| **[Reward shaping](#02-reward-shaping)**                             | Modification de la fonction de récompense pour guider l’apprentissage plus efficacement.                 |
| **[Curriculum learning](#03-curriculum-learning)**                   | Apprentissage progressif, débutant par des tâches faciles.                                               |
| **[Self-play](#04-self-play)**                                       | L’agent joue contre lui-même ou ses versions précédentes pour apprendre.                                 |
| **[Policy](#05-policy)**                                             | Fonction déterminant l’action à prendre selon l’état. Peut être déterministe ou stochastique.            |
| **[Value Function](#06-value-function)**                             | Fonction estimant la récompense attendue d’un état ou d’une action donnée.                               |
| **[Exploration vs Exploitation](#07-exploration-vs-exploitation)**   | Dilemme entre exploiter les connaissances acquises ou explorer de nouvelles stratégies.                  |
| **[Hyperparameters](#08-hyperparameters)**                           | Paramètres définis avant l’entraînement (learning rate, gamma, epsilon, etc.).                           |
| **[Discount Factor](#09-discount-factor)**                           | Contrôle l’importance des récompenses futures.                                                           |
| **[Episode](#10-episode)**                                           | Une séquence complète d’interactions entre l’agent et l’environnement.                                   |
| **[State Space](#11-state-space)**                                   | Ensemble de tous les états possibles de l’environnement.                                                 |
| **[Action Space](#12-action-space)**                                 | Ensemble de toutes les actions possibles dans un état donné.                                             |


---

## 📦 Algorithmes de RL

| Algorithme                     | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **[DQN (Deep Q-Network)](#05-dqn-deep-q-network)**                     | Réseau de neurones apprenant une fonction Q(s, a) pour des environnements discrets. |
| **[PPO (Proximal Policy Optimization)](#06-ppo-proximal-policy-optimization)** | Algorithme acteur-critique stable et performant. |
| **[A2C / A3C](#07-a2c--a3c-advantage-actor-critic--asynchronous-a2c)** | Versions synchrones/asynchrones de l’acteur-critique. |
| **[MCTS (Monte Carlo Tree Search)](#08-mcts-monte-carlo-tree-search)**  | Recherche séquentielle pour explorer les meilleures actions à prendre. |
| **[AlphaZero / MuZero](#09-alphazero--muzero)**                         | Algos combinant MCTS, RL profond et self-play (MuZero apprend même les règles). |

---

## 🏗 Architectures de Réseaux

| Architecture                   | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **[MLP (Multi-Layer Perceptron)](#10-mlp-multi-layer-perceptron)**       | Réseau de neurones dense classique. |
| **[LSTM (Long Short-Term Memory)](#11-lstm-long-short-term-memory)**     | Réseau récurrent pour séquences (ex : ordre de draft). |
| **[CNN (Convolutional Neural Network)](#12-cnn-convolutional-neural-network)** | Peut extraire des patterns sur des séquences de cartes. |
| **[Transformer](#13-transformer)**                                      | Réseau à attention, puissant sur séquences longues. |
| **[GNN (Graph Neural Network)](#14-gnn-graph-neural-network)**          | Encode des relations structurelles (ex : cartes interconnectées). |

---

## 🔧 AutoML / AutoRL et Optimisation

| Terme / Outil                  | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **[AutoML](#15-automl-automated-machine-learning)**                     | Automatisation du choix de modèle, tuning et architecture. |
| **[AutoRL](#16-autorrl-automated-reinforcement-learning)**              | Application d’AutoML au RL (paramètres, rewards, architectures). |
| **[NAS (Neural Architecture Search)](#17-nas-neural-architecture-search)** | Recherche automatique des meilleures architectures de réseau. |
| **[Ray Tune](#18-ray-tune)**                                           | Librairie de tuning d’hyperparamètres à grande échelle. |
| **[Optuna / HyperOpt / Nevergrad](#19-optuna--hyperopt--nevergrad)**    | Librairies pour optimiser automatiquement les hyperparamètres. |

---

## ⚙️ Environnements et Outils

| Outil                           | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| **[OpenAI Gym / Gymnasium](#20-openai-gym--gymnasium)**                  | Standard pour implémenter des environnements RL. |
| **[RLCard](#21-rlcard)**                                               | Environnements RL pour jeux de cartes (UNO, Blackjack, etc.). |
| **[PettingZoo](#22-pettingzoo)**                                        | Environnements multi-agents (ex : 2 joueurs). |
| **[Stable-Baselines3 (SB3)](#23-stable-baselines3-sb3)**                | Implémentations prêtes à l’emploi des algos de RL. |
| **[RLlib](#24-rllib-ray)**                                             | Librairie distribuée pour entraînement RL à grande échelle. |

---

## 📖 Définitions plus détaillées

### 01. MDP (Markov Decision Process)
<details>
<summary>Voir la définition</summary>

Un MDP est un cadre mathématique qui décrit comment un agent interagit avec un environnement à travers:
- **S (States)** : les états du jeu (ex : contenu du deck, main actuelle, PV des Pokémon actifs)
- **A (Actions)** : les actions disponibles (ex : choisir une carte à ajouter au deck, lancer une attaque)
- **P (Transitions)** : les probabilités de passer d’un état à un autre après une action
- **R (Reward)** : le score ou feedback reçu
- **γ (Gamma)** : un facteur de pondération pour les récompenses futures

🧪 **Application à ton projet** :
- État = composition actuelle du deck + résumé des performances passées
- Action = ajouter/retirer une carte du deck
- Récompense = victoire/défaite ou score de performance du deck en match simulé

🧠 **Avantage** : Fournit une base formelle claire pour modéliser ton problème d’optimisation de deck comme un processus d’apprentissage par renforcement.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 02. Reward Shaping
<details>
<summary>Voir la définition</summary>

C’est l’art d’ajuster la fonction de récompense pour faciliter l’apprentissage. Au lieu de ne récompenser qu’à la victoire, on donne aussi des récompenses intermédiaires.

🧪 **Application à ton projet** :
- Donner une petite récompense si un deck fait plus de dégâts moyens par partie
- Donner un bonus si une carte ajoutée augmente le taux de victoire
- Donner une pénalité si le deck dépasse la limite autorisée de doublons ou devient moins polyvalent

🧠 **Avantage** : Accélère l’apprentissage et évite que l’IA stagne ou apprenne des comportements sous-optimaux.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 03. Curriculum Learning
<details>
<summary>Voir la définition</summary>

On commence l’entraînement sur des tâches simples, puis on augmente la difficulté progressivement, comme dans un programme scolaire.

🧪 **Application à ton projet** :
- Phase 1 : L’IA optimise un deck avec 5 cartes fixes et ne peut changer qu’1 ou 2 cartes
- Phase 2 : L’IA a un choix libre sur 15 cartes parmi un pool limité
- Phase 3 : L’IA peut construire un deck complet avec toute la base de données

🧠 **Avantage** : Rend l’apprentissage plus stable et progressif, surtout dans des environnements complexes à forte combinatoire comme Pokémon TCG Pocket.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 04. Self-play
<details>
<summary>Voir la définition</summary>

L’agent joue contre lui-même ou ses versions précédentes, ce qui permet d’apprendre sans supervision externe.

🧪 **Application à ton projet** :
- L’IA construit un deck, puis joue des parties contre un adversaire IA entraîné précédemment
- Tu peux faire évoluer ce second adversaire au fil du temps, pour forcer l’IA à s’adapter à des decks toujours plus performants

🧠 **Avantage** : Permet un entraînement autonome et indéfini, en générant des adversaires dynamiques adaptés au niveau de l’agent.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 05. DQN (Deep Q-Network)
<details>
<summary>Voir la définition</summary>

Un algorithme qui apprend à estimer la valeur Q(s, a), c’est-à-dire la qualité d’une action a dans un état s. Il utilise un réseau de neurones pour approximer cette fonction.

🧪 **Application à ton projet** :
- L’état pourrait être la composition actuelle du deck
- L’action serait ajouter, retirer ou remplacer une carte
- Le réseau apprend quelles actions mènent aux meilleurs taux de victoire

🧠 **Avantage** : bien adapté si tu as un espace d’action discret (ex : pool limité de cartes).

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 06. PPO (Proximal Policy Optimization)
<details>
<summary>Voir la définition</summary>

Un algorithme acteur-critique qui apprend directement une politique (π) pour choisir des actions, tout en restant proche de la politique précédente (d’où "proximal").

🧪 **Application à ton projet** :
- Ton IA peut apprendre une distribution de choix de cartes, au lieu de choisir toujours la même
- Elle s’ajuste progressivement pour éviter les comportements instables

🧠 **Avantage** : Très utilisé, stable, et compatible avec des architectures plus complexes comme des [Transformers](#13-transformer) ou [GNNs](#14-gnn-graph-neural-network). Utile pour entraîner des politiques stochastiques.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 07. A2C / A3C (Advantage Actor-Critic / Asynchronous A2C)
<details>
<summary>Voir la définition</summary>

Algorithmes avec deux réseaux :
- Acteur : choisit l’action
- Critique : estime la valeur de l’état
La version A3C entraîne plusieurs agents en parallèle.

🧪 **Application à ton projet** :
- Tu peux entraîner plusieurs agents avec des decks différents en parallèle et agréger leur apprentissage
- Parfait pour accélérer l’entraînement via [self-play](#04-self-play) en parallèle

🧠 **Avantage** : Très rapide à entraîner sur CPU et efficace pour les tâches complexes avec beaucoup de bruit dans la récompense (comme des résultats de match).

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 08. MCTS (Monte Carlo Tree Search)
<details>
<summary>Voir la définition</summary>

Une méthode basée sur la simulation qui construit un arbre de décisions en explorant les branches les plus prometteuses.
Elle simule des jeux jusqu’au bout pour estimer la valeur d’une action.

🧪 **Application à ton projet** :
- Utilisé pour tester différents choix de decks, en simulant des parties pour chaque branche
- Peut aider à sélectionner les meilleures actions de construction ou même les meilleures stratégies de jeu

🧠 **Avantage** : Très utile au début du projet, quand tu n’as pas encore de modèle appris. Peut aussi être combiné avec un réseau de valeur (comme dans [AlphaZero)](#09-alphazero--muzero)).

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 09. AlphaZero / MuZero
<details>
<summary>Voir la définition</summary>

AlphaZero combine [self-play](#04-self-play), [MCTS](#08-mcts-monte-carlo-tree-search) et deep learning.
MuZero va plus loin : il n’a pas besoin de connaître les règles du jeu à l’avance. Il apprend un modèle interne de l’environnement.

🧪 **Application à ton projet** :
- L’IA apprend à construire un deck sans savoir explicitement pourquoi certaines cartes sont fortes
- Elle s’appuie uniquement sur les résultats de simulation et apprend les "règles" de succès implicitement

🧠 **Avantage** : Très puissant dans des environnements complexes ou imparfaitement connus (comme Pokémon TCG Pocket où les synergies entre cartes ne sont pas toujours évidentes).

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 10. MLP (Multi-Layer Perceptron)
<details>
<summary>Voir la définition</summary>

Un réseau dense classique, composé de plusieurs couches entièrement connectées (fully connected). C’est la base des réseaux neuronaux.

🧪 **Application à ton projet** :
- Entrée : représentation vectorielle du deck (par exemple, un vecteur binaire indiquant quelles cartes sont présentes)
- Utilisé pour prédire la valeur du deck (ex : taux de victoire estimé)

🧠 **Avantage** : Simple, rapide à entraîner, suffisant si tes données sont bien structurées et peu séquentielles.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 11. LSTM (Long Short-Term Memory)
<details>
<summary>Voir la définition</summary>

Un type de réseau récurrent (RNN) conçu pour mémoriser les séquences avec dépendances à long terme.

🧪 **Application à ton projet** :
- Peut être utilisé si tu veux apprendre à construire un deck carte après carte, en tenant compte de l’ordre
- Utile pour prédire la synergie d’une carte ajoutée en fonction des cartes précédemment sélectionnées

🧠 **Avantage** : Gère très bien les données séquentielles, par exemple pour apprendre une logique de draft ou de combo.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 12. CNN (Convolutional Neural Network)
<details>
<summary>Voir la définition</summary>

Initialement conçu pour les images, mais utilisable pour capturer des motifs locaux dans des séquences, grâce aux filtres convolutifs.

🧪 **Application à ton projet** :
- Peut détecter des motifs ou combinaisons fréquentes de cartes dans les decks gagnants
- Entrée : représentation linéaire ou matricielle des cartes, classées par type, rareté, coût, etc.

🧠 **Avantage** : Très bon pour détecter des synergies locales (par exemple, des mini-combos de 2 ou 3 cartes).

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 13. Transformer
<details>
<summary>Voir la définition</summary>

Un réseau basé sur le mécanisme d’attention, permettant d’analyser de longues séquences en parallèle sans récurrence.

🧪 **Application à ton projet** :
- Traiter un deck comme une séquence de cartes, et apprendre quelles cartes interagissent entre elles via des mécanismes d’attention
- Peut servir à générer un deck complet token par token, comme GPT génère du texte mot par mot

🧠 **Avantage** : Idéal pour capturer des relations complexes et non locales entre cartes dans un deck.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 14. GNN (Graph Neural Network)
<details>
<summary>Voir la définition</summary>

Les réseaux de neurones pour graphes apprennent à partir de structures où les entités (nœuds) sont connectées (arêtes), comme un réseau de synergies.

🧪 **Application à ton projet** :
- Chaque carte = un nœud
- Une synergie ou interaction = une arête entre deux cartes
- Le réseau apprend à évaluer un deck en fonction de la structure de ses synergies

🧠 **Avantage** : Le plus adapté si tu veux représenter la structure interne d’un deck comme un graphe de synergies, de types, ou d’effets complémentaires.

[⬆ Retour à la table des matières](#table-des-matières)


</details>

---

### 15. AutoML (Automated Machine Learning)
<details>
<summary>Voir la définition</summary>

AutoML désigne l'ensemble des techniques qui permettent d'automatiser tout ou partie du processus de conception d'un modèle de machine learning, de la préparation des données jusqu’au choix du modèle et de ses hyperparamètres.

🧪 **Application à ton projet** :
- Tu peux automatiser le choix du meilleur modèle pour prédire la force d’un deck ou pour sélectionner des cartes
- Exemple : essayer automatiquement [MLP](#10-mlp-multi-layer-perceptron), [CNN (Convolutional Neural Network)](#12-cnn-convolutional-neural-network), [LSTM](#11-lstm-long-short-term-memory), etc., sur une tâche comme "évaluer un deck"

🧠 **Avantage** : Tu gagnes du temps et tu laisses l’outil explorer ce que tu ne soupçonnes même pas, surtout utile en début de projet.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 16. AutoRL (Automated Reinforcement Learning)
<details>
<summary>Voir la définition</summary>

Une branche d’AutoML spécialisée dans le RL : elle vise à automatiser le choix de l’algorithme RL, de la politique, du [Reward shaping](#02-reward-shaping), des hyperparamètres et de l’architecture réseau.

🧪 **Application à ton projet** :
- Ton environnement IA (le jeu Pokémon TCG Pocket) est entièrement simulable, donc parfait pour une exploration auto-entretenue
- Exemple : tu veux tester automatiquement [PPO](#06-ppo-proximal-policy-optimization), [DQN](#05-dqn-deep-q-network), [A2C](#07-a2c--a3c-advantage-actor-critic--asynchronous-a2c) avec différentes architectures ([MLP](#10-mlp-multi-layer-perceptron), [LSTM](#11-lstm-long-short-term-memory), [GNN](#14-gnn-graph-neural-network)), et différentes fonctions de récompense (winrate, diversité du deck, synergies...)

🧠 **Avantage** : Laisse ton IA apprendre quelle stratégie de RL est la meilleure pour ton jeu, au lieu de tout faire manuellement.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 17. NAS (Neural Architecture Search)
<details>
<summary>Voir la définition</summary>

Technique d’AutoML qui cherche automatiquement la meilleure architecture de réseau de neurones pour une tâche donnée. Peut être combinée avec RL, évolution génétique, ou recherche bayésienne.

🧪 **Application à ton projet** :
- Tu veux qu’un moteur NAS teste et découvre si une architecture [Transformer](#13-transformer), hybride [CNN](#12-cnn-convolutional-neural-network)+[MLP](#10-mlp-multi-layer-perceptron) ou [GNN](#14-gnn-graph-neural-network) fonctionne le mieux pour prédire l’efficacité d’un deck ou pour prendre des décisions de construction
- Cela peut aussi t’aider à concevoir le policy network de ton agent RL automatiquement

🧠 **Avantage** : Tu n’as pas besoin de deviner l’architecture idéale pour ton modèle de deckbuilder — elle est découverte automatiquement.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 18. Ray Tune
<details>
<summary>Voir la définition</summary>

Un framework d’optimisation d’hyperparamètres à grande échelle, très utilisé dans les pipelines de RL. Intègre facilement des algos de recherche (Bayesian, grid search, PBT, etc.) et peut gérer des milliers d’expériences en parallèle.

🧪 **Application à ton projet** :
- Tu peux utiliser Ray Tune pour lancer des dizaines de versions de ton agent PPO avec des combinaisons différentes de :
    - learning rate
    - γ (discount factor)
    - batch size
    - structure du réseau (nombre de couches, etc.)

🧠 **Avantage** : Tu peux trouver rapidement les meilleurs réglages en profitant de la parallélisation (CPU ou GPU) et de l’intégration avec des frameworks comme PyTorch, RLlib, etc.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 19. Optuna / HyperOpt / Nevergrad
<details>
<summary>Voir la définition</summary>

Trois outils open-source d’optimisation d’hyperparamètres :
- Optuna : recherche bayésienne et TPE (Tree-structured Parzen Estimator)
- HyperOpt : orienté statistiques bayésiennes également
- Nevergrad (by Facebook) : basé sur des stratégies d’optimisation sans gradient, très utile en contexte RL

🧪 **Application à ton projet** :
- Tu peux les utiliser pour trouver automatiquement la meilleure configuration d’un agent RL ou d’un modèle d’évaluation de deck ([MLP](#10-mlp-multi-layer-perceptron) par ex.)
- Exemple : tuning de ton algorithme PPO avec Optuna pour tester des dizaines de combinaisons automatiquement

🧠 **Avantage** : Simple à intégrer dans ton code Python, rapide et efficace pour des petits comme des grands projets.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 20. OpenAI Gym / Gymnasium
<details>
<summary>Voir la définition</summary>

- OpenAI Gym est l’interface standard pour les environnements RL, proposée par OpenAI.
- Gymnasium est son fork officiel maintenu activement depuis 2022, car Gym n’est plus mis à jour.

🧪 **Application à ton projet** :
- Tu peux créer un environnement Pokémon TCG Pocket en suivant le format Gymnasium :
    ```python
    class PokeDeckEnv(gym.Env):
        def step(self, action): ...
        def reset(self): ...
        def render(self): ...
    ```
- Cela te permettra de l’utiliser avec n’importe quelle librairie RL compatible Gym (comme SB3, [Ray RLlib](#24-rllib-ray)...)

🧠 **Avantage** : Standardisation = intégration facile avec des dizaines d’outils, visualisation simple, outils de debug inclus.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 21. RLCard
<details>
<summary>Voir la définition</summary>

Un framework open-source pour l’entraînement d’agents RL dans les jeux de cartes (Texas Hold’em, Uno, Blackjack...), développé par l’université de Fudan.

🧪 **Application à ton projet** :
- RLCard offre des environnements multi-agents avec gestion des règles, du piochement, des actions valides, etc.
- Tu peux t’en inspirer pour structurer ton environnement Pokémon TCG Pocket de façon modulaire :
    - gestion des états de la main
    - deck simulé
    - actions comme "poser carte", "faire évoluer", etc.

🧠 **Avantage** : Tu gagnes du temps en réutilisant des mécaniques propres aux jeux de cartes, déjà codées et testées.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 22. PettingZoo
<details>
<summary>Voir la définition</summary>

Une librairie Python dédiée aux environnements RL multi-agents, compatible avec [Gymnasium](#20-openai-gym--gymnasium).

🧪 **Application à ton projet** :
- Si tu veux simuler deux agents IA qui s’affrontent, PettingZoo est fait pour toi :
    - Chaque joueur est un agent
    - Tu peux faire apprendre les deux agents en parallèle ou en opposition

🧠 **Avantage** : Permet de former ton IA contre des adversaires dynamiques, au lieu d’un bot statique. C’est idéal pour l’optimisation de decks face à un méta-jeu évolutif.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 23. Stable-Baselines3 (SB3)
<details>
<summary>Voir la définition</summary>

Une implémentation stable, modulaire et bien documentée des principaux algorithmes de RL ([DQN](#05-dqn-deep-q-network), [PPO](#06-ppo-proximal-policy-optimization), [A2C / A3C](#07-a2c--a3c-advantage-actor-critic--asynchronous-a2c)...) basée sur PyTorch.

🧪 **Application à ton projet** :
- Une fois ton environnement Gym prêt, tu peux directement l’entraîner avec SB3 :
```python
from stable_baselines3 import PPO
model = PPO("MlpPolicy", poke_env, verbose=1)
model.learn(total_timesteps=100_000)
```

🧠 **Avantage** : Rapide à déployer, excellente documentation, plugins pour TensorBoard, checkpoints, callbacks personnalisés...

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---

### 24. RLlib (Ray)
<details>
<summary>Voir la définition</summary>

Une plateforme RL industrielle et distribuée, intégrée à l’écosystème Ray. Permet de lancer des expériences RL à grande échelle, avec support pour la parallélisation, les multi-agents, et l’AutoRL.

🧪 **Application à ton projet** :
- Idéal si tu veux entraîner plusieurs agents deckbuilders en parallèle, ou lancer des recherches d’hyperparamètres avec [Ray Tune](#18-ray-tune)
- Tu peux l’utiliser pour du training multi-joueur où chaque IA explore des stratégies différentes

🧠 **Avantage** : Puissant, scalable, prêt pour le cloud. C’est l’outil parfait pour passer d’un prototype local à un entraînement massif.

[⬆ Retour à la table des matières](#table-des-matières)

</details>

---
