import random
import time
import sys

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = list(range(1, 10))  # Cartes de 1 à 9 (deux fois par couleur)
SPECIAL_CARDS = ['+2', 'Reverse', 'Skip']
CARDS_PER_PLAYER = 7
NUM_PLAYERS = 2
PLAYER_NAMES = [f"Joueur {i}" for i in range(NUM_PLAYERS)]

def create_deck(seed=None):
    deck = []

    # Cartes 0 : 1 par couleur
    for color in COLORS:
        deck.append(f"{color} 0")

    # Cartes 1 à 9 : 2 par couleur
    for color in COLORS:
        for value in VALUES:
            deck.append(f"{color} {value}")
            deck.append(f"{color} {value}")

    # Cartes spéciales couleur : 2 par type et par couleur
    for color in COLORS:
        for special in SPECIAL_CARDS:
            deck.extend([f"{color} {special}"] * 2)

    # Jokers (sans couleur)
    deck.extend(['Black Wild'] * 4)
    deck.extend(['Black +4'] * 4)

    # Mélange
    if seed is not None:
        random.seed(seed)
    else:
        random.seed(time.time())
    random.shuffle(deck)
    return deck

def is_playable(card, top_card):
    card_parts = card.split()
    top_parts = top_card.split()

    # Wilds are always playable
    if card_parts[0] == 'Black':
        return True

    return card_parts[0] == top_parts[0] or card_parts[1] == top_parts[1]

def print_hand(player_idx, hand):
    print(f"{PLAYER_NAMES[player_idx]}: {hand}")

def print_board(turn, current_player, top_card):
    print(f"\nTour {turn} - Tour de {PLAYER_NAMES[current_player]}")
    print(f"Carte du dessus: {top_card}")

def main(seed=None):
    if seed is None and len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print("Usage : python main.py [seed]")
            sys.exit(1)

    deck = create_deck(seed)
    hands = [deck[i * CARDS_PER_PLAYER:(i + 1) * CARDS_PER_PLAYER] for i in range(NUM_PLAYERS)]
    deck = deck[CARDS_PER_PLAYER * NUM_PLAYERS:]
    discard_pile = [deck.pop()]
    turn = 0
    current_player = 0
    consecutive_passes = 0
    draw_two_next = 0
    draw_four_next = 0
    skip_next = False
    direction = 1
    skip_current_player = False

    while all(len(hand) > 0 for hand in hands):
        print_board(turn, current_player, discard_pile[-1])
        print_hand(current_player, hands[current_player])

        # Si le joueur doit piocher 4 cartes et passer son tour
        if draw_four_next:
            for _ in range(4):
                if deck:
                    hands[current_player].append(deck.pop())
            print(f"{PLAYER_NAMES[current_player]} pioche 4 cartes (effet +4)")
            draw_four_next = 0
            skip_current_player = True  # il passe son tour

        # Si le joueur doit piocher 2 cartes et passer son tour
        elif draw_two_next > 0:
            cards_to_draw = 2 * draw_two_next
            for _ in range(cards_to_draw):
                if deck:
                    hands[current_player].append(deck.pop())
                else:
                    print(f"{PLAYER_NAMES[current_player]} aurait dû piocher {cards_to_draw} cartes mais la pioche est vide")
                    break
            print(f"{PLAYER_NAMES[current_player]} pioche {cards_to_draw} cartes (effet +2)")
            draw_two_next = 0
            skip_current_player = True  # il passe son tour

        # Si le joueur doit passer son tour à cause d'un Skip ou Reverse (2 joueurs)
        elif skip_next:
            print(f"{PLAYER_NAMES[current_player]} est passé (Skip)")
            skip_next = False
            skip_current_player = True

        # Si le joueur doit passer son tour (lié aux effets ci-dessus)
        if skip_current_player:
            skip_current_player = False
            consecutive_passes = 0
            current_player = (current_player + direction) % NUM_PLAYERS
            turn += 1
            continue

        # Sinon, le joueur peut jouer s'il a une carte jouable
        playable_cards = [card for card in hands[current_player] if is_playable(card, discard_pile[-1])]

        if playable_cards:
            card_to_play = playable_cards[0]
            hands[current_player].remove(card_to_play)
            discard_pile.append(card_to_play)
            print(f"{PLAYER_NAMES[current_player]} joue {card_to_play}")
            consecutive_passes = 0

            # Gestion des effets spéciaux
            if "+2" in card_to_play:
                draw_two_next += 1  # empile les +2 si plusieurs se suivent
            elif "Skip" in card_to_play:
                skip_next = True
            elif "Reverse" in card_to_play:
                if NUM_PLAYERS == 2:
                    # À 2 joueurs, Reverse = Skip
                    skip_next = True
                else:
                    direction *= -1
                    print("Sens de jeu inversé !")
            elif "Wild" in card_to_play and "+4" not in card_to_play:
                new_color = random.choice(COLORS)
                discard_pile[-1] = f"{new_color} Wild"
                print(f"{PLAYER_NAMES[current_player]} change la couleur en {new_color}")
            elif "+4" in card_to_play:
                new_color = random.choice(COLORS)
                discard_pile[-1] = f"{new_color} Wild +4"
                draw_four_next += 1  # empile les +4 si plusieurs se suivent
                print(f"{PLAYER_NAMES[current_player]} change la couleur en {new_color} et inflige +4")

        else:
            # Pas de carte jouable : pioche une carte si possible
            if deck:
                drawn_card = deck.pop()
                hands[current_player].append(drawn_card)
                print(f"{PLAYER_NAMES[current_player]} pioche une carte")
                consecutive_passes = 0
            else:
                print(f"{PLAYER_NAMES[current_player]} ne peut pas piocher, le paquet est vide")
                consecutive_passes += 1

        if consecutive_passes >= NUM_PLAYERS:
            print("\nAucun joueur ne peut jouer, le paquet est vide. Match nul.")
            return

        # Passage au joueur suivant et incrément du tour
        current_player = (current_player + direction) % NUM_PLAYERS
        turn += 1

    winner = next(i for i, hand in enumerate(hands) if len(hand) == 0)
    print(f"\n{PLAYER_NAMES[winner]} a gagné !")

if __name__ == "__main__":
    main()
