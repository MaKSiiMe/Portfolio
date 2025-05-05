from card import PokemonCard, Attack, Talent, SupporterCard
from player import Player
from game import Game

# Définir quelques attaques
tackle = Attack(name="Tackle", cost=["Colorless"], damage=30)
fire_blast = Attack(name="Fire Blast", cost=["Fire"], damage=60, effect="Burns the opponent")

# Talents
regeneration = Talent(name="Regeneration", effect="Heal 10 HP at the beginning of your turn")

# Pokémon
bulbasaur = PokemonCard(
    name="Bulbasaur", hp=60, evolution="Base", attacks=[tackle],
    pokemon_type="Plant", talent=regeneration
)

charmander = PokemonCard(
    name="Charmander", hp=50, evolution="Base", attacks=[fire_blast],
    pokemon_type="Fire"
)

# Supporter
erika = SupporterCard(name="Erika", effect="Draw 2 cards")

# Créer les decks
deck1 = [bulbasaur, erika]
deck2 = [charmander, erika]

# Créer les joueurs
player1 = Player(name="Maxime", deck=deck1)
player2 = Player(name="Badr", deck=deck2)

# Lancer le jeu
game = Game(player1, player2)
game.start_game()

# Simuler quelques tours
game.play_turn()  # Tour de Maxime
game.play_turn()  # Tour de Badr
