from .constants import ALL_CARDS
from typing import Dict

# Index mappings
CARD2IDX: Dict[str, int] = {card: idx for idx, card in enumerate(ALL_CARDS)}
IDX2CARD: Dict[int, str] = {idx: card for card, idx in CARD2IDX.items()}
