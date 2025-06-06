"""
uno_env.py

UNO Gymnasium Environment

This module implements a custom Gymnasium environment for the UNO card game.
It wraps the core UNO engine to provide observations, actions, rewards, and environment dynamics for training AI agents.
"""

"""
uno_rl/envs/uno_env.py — L'environnement Gymnasium
C’est ici que tu crées la classe UnoEnv(gym.Env).
Elle encapsule une partie UNO 2 joueurs (IA + bot) en utilisant le moteur du dossier uno/.
Elle définit :
__init__: initialise un moteur de jeu UNO interne, définit observation_space et action_space
reset: démarre une nouvelle partie et renvoie l’observation initiale
step(action): applique une action du joueur IA, fait jouer le bot, retourne observation, reward, terminated, truncated, info
render: affiche l’état actuel du jeu
"""