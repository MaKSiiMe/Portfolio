from app.models.uno.encodings import IDX2CARD, ALL_CARDS

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
