import random

def random_agent_fn(env, state):
    return env.action_space.sample()
