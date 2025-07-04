from app.models.uno.rules import is_playable

class RuleBasedAgent:
    def choose_action(self, game_state: dict, player_idx: int) -> int:
        """
        Choisit la première carte jouable, sinon pioche.
        Args:
            game_state (dict): état brut du jeu (Game.get_state())
            player_idx (int): index du joueur courant

        Returns:
            int: index dans la main à jouer, ou None pour piocher
        """
        hand = game_state["hands"][player_idx]
        top_card = game_state["discard_pile"][-1]
        current_color = game_state.get("current_color", None)

        for idx, card in enumerate(hand):
            if is_playable(card, top_card, current_color):
                return idx  # <-- index dans la main, PAS encode_card(card)

        return None  # Aucun coup jouable, donc pioche
