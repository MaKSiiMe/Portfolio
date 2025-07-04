import numpy as np
from stable_baselines3 import PPO

from app.models.envs.uno_env import UnoEnv

model_path = "Stage4/app/models/agents/ppo/ppo_uno"
model = PPO.load(model_path)

env = UnoEnv(n_players=2)

ppo_wins = 0
random_wins = 0
draws = 0

for _ in range(100):
    obs = env.reset()
    done = False

    while not done:
        if env.game.current_player == 0:
            # PPO agent
            action, _ = model.predict(obs, deterministic=True)
        else:
            # Random agent
            valid_actions = env.valid_actions()
            action = np.random.choice(valid_actions)

        obs, reward, done, info = env.step(action)

    if reward > 0:
        ppo_wins += 1
    elif reward < 0:
        random_wins += 1
    else:
        draws += 1

print("Résultats après 100 parties :")
print(f"PPO wins     : {ppo_wins}")
print(f"Random wins  : {random_wins}")
print(f"Draws        : {draws}")
