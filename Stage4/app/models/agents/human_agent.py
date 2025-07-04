from app.models.uno.encodings import IDX2CARD, ALL_CARDS
from app.models.uno.display import print_hand, print_board

def choose_action(env, obs):
    """
    Asks the human player for input via console.
    """
    print("\nYour hand:")
    for idx, encoded_card in enumerate(obs['hand']):
        if encoded_card == -1:
            continue
        print(f"{idx}: {ALL_CARDS[encoded_card]}")

    print(f"Top card: {IDX2CARD[obs['top_card']]}")
    
    action = input("Choose the index of the card to play, or 'd' to draw: ")
    if action.lower() == 'd':
        return env.action_space.n - 1
    try:
        return int(action)
    except ValueError:
        print("Invalid input. Drawing by default.")
        return env.action_space.n - 1

def ask_playable_choice(playable):
    """
    Ask the human to choose a playable card or draw.
    """
    print("Playable cards:", playable)
    while True:
        choice = input(f"Which card do you want to play? (0-{len(playable)-1} or 'p' to draw): ")
        if choice == 'p':
            return None
        elif choice.isdigit() and 0 <= int(choice) < len(playable):
            return int(choice)
        else:
            print("Invalid choice.")

def ask_draw():
    """
    Prompt when no playable cards.
    """
    input("No playable cards. Press Enter to draw...")
