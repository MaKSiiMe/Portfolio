import numpy as np

# Simulate the updated constants and encodings
COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = list(range(1, 10))
SPECIAL_CARDS = ['+2', 'Reverse', 'Skip']
WILD_CARDS = [f"Wild {color}" for color in COLORS] + [f"Wild +4 {color}" for color in COLORS]
ALL_CARDS = [f"{color} {number}" for color in COLORS for number in range(0, 10)] + \
            [f"{color} {special}" for color in COLORS for special in SPECIAL_CARDS] + \
            WILD_CARDS
CARD2IDX = {card: idx for idx, card in enumerate(ALL_CARDS)}
IDX2CARD = {idx: card for card, idx in CARD2IDX.items()}
TOTAL_CARDS = len(ALL_CARDS)

# Define the functions
def normalize_card(card: str) -> str:
    if 'Wild' in card:
        parts = card.split()
        if parts[0] in COLORS:
            return " ".join(parts)
    return card

def encode_card(card_str: str) -> int:
    return CARD2IDX[normalize_card(card_str)]

def decode_card(card_id: int) -> str:
    if card_id not in IDX2CARD:
        raise KeyError(f"Card ID '{card_id}' not found in IDX2CARD")
    return IDX2CARD[card_id]

def encode_hand(hand: list) -> np.ndarray:
    vec = np.zeros(len(CARD2IDX), dtype=np.float32)
    for card in hand:
        norm_card = normalize_card(card)
        if norm_card in CARD2IDX:
            vec[CARD2IDX[norm_card]] += 1
    return vec

def decode_hand(encoded_hand: list) -> list:
    return [decode_card(idx) for idx, count in enumerate(encoded_hand) if count > 0]

def decode_action(index: int) -> str:
    if index == TOTAL_CARDS:
        return "DRAW"
    return decode_card(index)

# Create sample hand and test encoding/decoding
sample_hand = ["Red 3", "Green +2", "Wild +4 Blue"]
encoded = encode_hand(sample_hand)
decoded = decode_hand(encoded)

encoded, decoded, decode_action(TOTAL_CARDS), decode_action(5)  # example decode

