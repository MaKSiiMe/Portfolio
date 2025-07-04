class PPOAgent:
    """
    Placeholder for a Reinforcement Learning-based agent.
    Expects a trained policy to be loaded or defined.
    """

    def __init__(self, model_path):
        """
        Args:
            model: Trained policy or neural network (optional for now).
        """
        self.model = PPO.load(model_path)

    def choose_action(self, state, player_idx):
        """
        Selects an action based on the current observation.

        For now, raises NotImplementedError.
        """
        obs = encode_state(state, player_idx)
        action, _ = self.model.predict(obs)
        return int(action)
