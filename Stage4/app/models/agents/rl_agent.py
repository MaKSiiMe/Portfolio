class RLAgent:
    """
    Placeholder for a Reinforcement Learning-based agent.
    Expects a trained policy to be loaded or defined.
    """

    def __init__(self, model=None):
        """
        Args:
            model: Trained policy or neural network (optional for now).
        """
        self.model = model

    def choose_action(self, obs):
        """
        Selects an action based on the current observation.

        For now, raises NotImplementedError.
        """
        raise NotImplementedError("RLAgent not implemented yet.")
