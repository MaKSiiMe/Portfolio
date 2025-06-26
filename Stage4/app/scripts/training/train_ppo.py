# train_ppo.py

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from app.models.envs.uno_env import UnoEnv
from app.models.agents.rules_agent import RuleBasedAgent


# Crée un environnement Gym compatible SB3
def make_env():
    return UnoEnv(opponent_agent_fn=None)

# Environnement vectorisé
env = DummyVecEnv([make_env])

# Crée le modèle PPO avec une politique adaptée aux observations complexes
model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs")

# Entraîne le modèle pendant 500_000 étapes
model.learn(total_timesteps=500_000)

# Sauvegarde le modèle
save_path = "./ppo_uno_model"
os.makedirs(save_path, exist_ok=True)
model.save(os.path.join(save_path, "ppo_uno"))

print(f"✅ Modèle entraîné et sauvegardé dans {save_path}")
