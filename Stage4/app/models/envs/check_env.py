import sys
import os
from stable_baselines3.common.env_checker import check_env

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from app.models.envs.uno_env import UnoEnv

if __name__ == "__main__":
    env = UnoEnv()
    check_env(env, warn=True)
