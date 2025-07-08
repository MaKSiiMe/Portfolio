# train_ppo.py

import os
import sys
import time
import argparse
import logging

# Ajout du chemin racine pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback

from app.models.envs.uno_env import UnoEnv
from app.models.agents.rules_agent import RuleBasedAgent
from app.models.agents.random_agent import RandomAgent

# 📜 Logging
logging.basicConfig(level=logging.INFO)

# 🧪 Logger TensorBoard
log_dir = f"./Stage4/app/logs/ppo/run_{int(time.time())}"
os.makedirs(log_dir, exist_ok=True)
new_logger = configure(log_dir, ["stdout", "tensorboard"])

# 🎛️ Argument CLI
parser = argparse.ArgumentParser()
parser.add_argument("--timesteps", type=int, default=3_000_000, help="Nombre de pas d'entraînement PPO")
args = parser.parse_args()

# ⚙️ Fabrique l’environnement avec Monitor
def make_env(seed=0, max_steps=200):
    def _init():
        env = UnoEnv(seed=seed, max_steps=max_steps)
        return Monitor(env)
    return _init

env = DummyVecEnv([make_env(seed=i) for i in range(4)])

# 🤖 Création du modèle PPO
"""
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    learning_rate=0.0001,
    ent_coef=0.01,
    target_kl=0.03,
)
"""

model = PPO.load("Stage4/app/models/agents/ppo/ppo_uno_pre_final_1751828262.zip", env=env)

model.set_logger(new_logger)

# ⏱️ Entraînement principal (98% du total)
total_timesteps = args.timesteps
pre_save_timesteps = int(0.98 * total_timesteps)

# 💾 Callback pour checkpoints réguliers
checkpoint_callback = CheckpointCallback(
    save_freq=100_000,
    save_path="./Stage4/app/models/agents/ppo_checkpoints/",
    name_prefix="ppo_uno"
)

# model.learn(total_timesteps=pre_save_timesteps, callback=checkpoint_callback)
model.learn(total_timesteps=3_000_000)


# 💾 Sauvegarde intermédiaire
timestamp = int(time.time())
save_path = "Stage4/app/models/agents/ppo"
os.makedirs(save_path, exist_ok=True)
intermediate_save_path = f"{save_path}/ppo_uno_pre_final_{timestamp}"
model.save(intermediate_save_path)
print(f"💾 Modèle sauvegardé avant la dernière update dans {intermediate_save_path}")

# 🎯 Derniers 2% d'entraînement
model.learn(total_timesteps=total_timesteps - pre_save_timesteps, reset_num_timesteps=False)

# 📦 Sauvegarde finale
final_save_path = f"{save_path}/ppo_uno"
model.save(final_save_path)
print(f"✅ Modèle entraîné ({args.timesteps} étapes) et sauvegardé dans {final_save_path}")
