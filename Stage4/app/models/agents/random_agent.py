def choose_action(env, obs):
    """
    Chooses a random action from the environment's action space.
    """
    return env.action_space.sample()
