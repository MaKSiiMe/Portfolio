from app.models.uno.rules import is_playable
from app.models.uno.encodings import CARD2IDX
from app.models.uno.utils import encode_card, TOTAL_CARDS

class RuleBasedAgent:
    def __call__(self, env, obs):
        player_idx = env.game.current_player
        game_state = env.game.get_state()
        action = self.choose_action(game_state, player_idx)
        if env.verbose:
            print(f"[RuleBasedAction] player {player_idx} -> action {action}")
        return action

    def choose_action(self, game_state, player_idx):
        """
        Choisit la première carte jouable, sinon pioche.
        Args:
            game_state (dict): état brut du jeu (Game.get_state())
            player_idx (int): index du joueur courant

        Returns:
            int: action (0-107 pour jouer une carte, 108 = piocher)
        """
        hand = game_state["hands"][player_idx]
        top_card = game_state["discard_pile"][-1]
        current_color = game_state.get("current_color", None)

        for card in hand:
            if is_playable(card, top_card, current_color):
                return encode_card(card)

        return TOTAL_CARDS
