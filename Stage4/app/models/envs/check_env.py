from stable_baselines3.common.env_checker import check_env

from app.models.envs.uno_env import UnoEnv

if __name__ == "__main__":
    env = UnoEnv()
    check_env(env, warn=True)
