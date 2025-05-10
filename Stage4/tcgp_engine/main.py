from card import PokemonCard, Attack, Talent, SupporterCard
from player import Player
from game import Game

# Définir quelques attaques
fouetLianes = Attack(name="Fouet Lianes", cost=["Colorless"], damage=40)
flammeche = Attack(name="Flammèche", cost=["Fire"], damage=30)

# Talents
regeneration = Talent(name="Regeneration", effect="Heal 10 HP at the beginning of your turn")

# Pokémon
bulbizarre = PokemonCard(
    name="Bulbizarre", hp=70, evolution="Base", attacks=[fouetLianes],
    pokemon_type="Plant"
)

salamèche = PokemonCard(
    name="Salamèche", hp=60, evolution="Base", attacks=[flammeche],
    pokemon_type="Fire"
)

# Supporter
erika = SupporterCard(name="Erika", effect="Draw 2 cards")

# Créer les decks
deck1 = [bulbizarre, erika]
deck2 = [salamèche, erika]

# Créer les joueurs
player1 = Player(name="Maxime", deck=deck1)
player2 = Player(name="Badr", deck=deck2)

# Lancer le jeu
game = Game(player1, player2)
game.start_game()

# Boucle de jeu principale
while not game.is_over:
    game.play_turn()
    game.check_knockouts()
    if game.is_game_over():
        break