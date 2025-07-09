import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from tqdm import trange
import numpy as np
from stable_baselines3 import PPO
from app.models.envs.uno_env import UnoEnv
from app.models.agents.random_agent import random_agent_fn

N_GAMES = 100
ppo_wins = 0
random_wins = 0
draws = 0

# Load trained PPO model
model_path = "Stage4/app/models/agents/ppo/ppo_uno_pre_final_1751828262.zip"
model = PPO.load(model_path)

for i in trange(N_GAMES, desc="Evaluating"):
    # Create environment with a random opponent
    env = UnoEnv(opponent_agent_fn=random_agent_fn)
    obs, _ = env.reset()

    done = False
    while not done:
        if env.game.current_player == 0:
            # PPO agent's turn
            action, _ = model.predict(obs, deterministic=True)
            action = action.item()
        else:
            # Random agent's turn
            state = env.game.get_state()
            action = random_agent_fn(env, state)

        obs, _, done, _, _ = env.step(action)

    winner = env.game.get_winner()
    if winner == 0:
        ppo_wins += 1
    elif winner == 1:
        random_wins += 1
    else:
        print(f"[❌ No winner] Game ended after {env.step_count} steps.")
        draws += 1

    print(f"Final hands: PPO={len(env.game.hands[0])} cards, Random={len(env.game.hands[1])} cards")


# Print results
print("🎯 Evaluation over", N_GAMES, "games:")
print("PPO agent wins:", ppo_wins)
print("Random agent wins:", random_wins)
print("Draws or invalid:", N_GAMES - ppo_wins - random_wins)
print("PPO win rate:", round((ppo_wins / N_GAMES) * 100, 2), "%")
