#!/usr/bin/env python3

from player import Player
from card import PokemonCard, SupporterCard

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.current_player_index = 0
        self.turn_count = 0
        self.is_over = False
        self.winner = None

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def opponent(self) -> Player:
        return self.players[1 - self.current_player_index]

    def start_game(self):
        for player in self.players:
            player.draw_starting_hand()
            # Assign active Pokémon and optionally bench Pokémon
            for card in player.hand[:]:
                if isinstance(card, PokemonCard):
                    player.set_active_pokemon(card)
                    break

    def play_turn(self):
        player = self.players[self.current_player_index]
        opponent = self.players[1 - self.current_player_index]

        print(f"\n--- Tour de {player.name} ---")
        player.reset_turn_flags()
        player.draw_card()

        # Vérifiez si un supporter peut être joué
        for card in player.hand:
            if isinstance(card, SupporterCard):
                player.play_supporter(card)
                break

        # Attacher de l'énergie à l'actif
        if player.active_pokemon:
            player.attach_energy(player.active_pokemon)

            # Utilisation du talent (si dispo)
            if player.active_pokemon.talent and not player.active_pokemon.talent.used_this_turn:
                print(f"{player.name} utilise le Talent de {player.active_pokemon.name} : {player.active_pokemon.talent.effect}")
                player.active_pokemon.talent.used_this_turn = True

            # Utiliser première attaque possible
            for attack in player.active_pokemon.attacks:
                if player.active_pokemon.energy_attached >= len(attack.cost):
                    print(f"{player.name} utilise l'attaque {attack.name} de {player.active_pokemon.name}")
                    opponent.take_damage(attack.damage)
                    break

        # Vérifier victoire
        if player.victory_points >= 3:
            print(f"\n🏆 {player.name} remporte la partie avec {player.victory_points} points!")
            self.is_over = True
            return

        # Fin du tour
        self.current_player_index = 1 - self.current_player_index

    def check_knockouts(self):
        for player in self.players:
            if player.active_pokemon and player.active_pokemon.is_knocked_out():
                print(f"{player.active_pokemon.name} is knocked out!")
                self.opponent.gain_point(player.active_pokemon)
                player.discard_pile.append(player.active_pokemon)
                player.active_pokemon = None  # À remplacer par un remplacement réel plus tard

    def check_victory(self):
        for player in self.players:
            if player.has_won():
                self.is_over = True
                self.winner = player
                print(f"\n{player.name} wins the game with {player.victory_points} points!")

    def end_turn(self):
        self.current_player_index = 1 - self.current_player_index
        self.turn_count += 1
