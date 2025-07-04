# train_ppo.py

import os
import sys
import time
import argparse
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from app.models.envs.uno_env import UnoEnv

logging.basicConfig(level=logging.INFO)
log_dir = f"./Stage4/app/logs/ppo/run_{int(time.time())}"

# Argument CLI
parser = argparse.ArgumentParser()
parser.add_argument("--timesteps", type=int, default=500_000, help="Nombre de pas d'entraînement PPO")
args = parser.parse_args()

# Crée un environnement Gym compatible SB3
def make_env():
    return UnoEnv(opponent_agent_fn=None)

env = DummyVecEnv([make_env])

# Crée le modèle PPO avec TensorBoard activé
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    tensorboard_log=log_dir
)

# Entraîne le modèle
model.learn(total_timesteps=args.timesteps)

# Sauvegarde le modèle
save_path = "Stage4/app/models/agents/ppo"
os.makedirs(save_path, exist_ok=True)
model.save(os.path.join(save_path, "ppo_uno"))

print(f"✅ Modèle entraîné ({args.timesteps} étapes) et sauvegardé dans {save_path}")
