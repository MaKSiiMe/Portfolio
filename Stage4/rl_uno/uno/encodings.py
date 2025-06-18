from .constants import COLORS, VALUES, SPECIAL_CARDS, WILD_CARDS

ALL_CARDS = []
for color in COLORS:
    ALL_CARDS.append(f"{color} 0")
    for v in VALUES:
        ALL_CARDS.append(f"{color} {v}")
    for s in SPECIAL_CARDS:
        ALL_CARDS.append(f"{color} {s}")
ALL_CARDS.extend(WILD_CARDS)

CARD2IDX = {card: idx for idx, card in enumerate(ALL_CARDS)}
IDX2CARD = {idx: card for card, idx in CARD2IDX.items()}
