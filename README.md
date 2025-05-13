# Portfolio Project


### MVP Description
For the MVP, we aim to build a simplified AI-powered tool that helps analyze and rank Pokémon TCG decks. The project includes a custom game engine that simulates basic matches using simplified rules, enabling automated testing between different decks. This allows us to evaluate deck performance over many simulated games.

A web dashboard will present key insights such as win rates, deck comparisons, and visual feedback (graphs, match summaries, etc.). The goal is to provide a helpful assistant for players to better understand which decks perform well, and why.


### Arboréscence


Team Rocket/
|-- pokemon_tcg_engine/      # Le cœur de votre moteur Pokémon TCG Pocket
|   |-- __init__.py
|   |-- cards/               # Vos classes de cartes Pokémon, Dresseur, Énergie
|   |   |-- __init__.py
|   |   |-- base_card.py       # Peut-être une classe de base pour vos cartes, utilisant/étendant Card de LemonTCG
|   |   |-- pokemon_card.py
|   |   |-- trainer_card.py
|   |   |-- energy_card.py
|   |-- game_elements/       # Logique du plateau, zones de jeu, joueur spécifique à Pokémon
|   |   |-- __init__.py
|   |   |-- board.py           # Représentation du plateau Pokémon (Actif, Banc, etc.)
|   |   |-- player_state.py    # État spécifique d'un joueur Pokémon (main, défausse, récompenses)
|   |-- game_logic/          # Règles du jeu, gestion des tours, phases, actions, effets
|   |   |-- __init__.py
|   |   |-- turn_manager.py
|   |   |-- action_resolver.py # Gère la résolution des actions (jouer carte, attaquer)
|   |   |-- effect_engine.py   # Moteur pour appliquer les effets des cartes
|   |   |-- rule_checks.py     # Fonctions pour vérifier la validité des actions
|   |-- game_state.py        # L'état global d'une partie de Pokémon TCG
|   |-- constants.py         # Constantes du jeu (taille max du banc, etc.)
|
|-- gym_env/                 # Votre environnement Gymnasium
|   |-- __init__.py
|   |-- pokemon_pocket_env.py  # Classe héritant de gym.Env
|
|-- card_definitions/        # Fichiers de données pour vos cartes (par ex. JSON)
|   |-- pokemon/
|   |-- trainer/
|   |-- energy/
|
|-- lemon_tcg_lib/           # Où vous placez le code source de LemonTCG
|   |-- lemon_tcg/           # Le répertoire 'lemon_tcg' copié depuis le dépôt de Zitronenjoghurt
|   |   |-- __init__.py
|   |   |-- entities/
|   |   |-- event/
|   |   |-- ... (reste de la structure de LemonTCG)
|
|-- tests/                   # Vos tests unitaires et d'intégration
|   |-- test_cards.py
|   |-- test_game_logic.py
|   |-- test_gym_env.py
|
|-- main.py                  # Un script principal pour lancer une partie, des tests, etc.
|-- requirements.txt         # Dépendances (Gymnasium, Pydantic si pas déjà inclus par LemonTCG)
|-- README.md                # Description de votre projet