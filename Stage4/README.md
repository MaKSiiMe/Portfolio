# 🎮 UNO Game Engine – Python

## Overview

This project provides an **automated UNO game simulation** in Python, without a graphical interface. It allows you to run a game between several virtual players, displaying the progress in the terminal. The goal is to offer a simple, readable, and easily modifiable engine.

## Main Features

- Simulates a UNO game between 2 to 10 players (3 players by default).
- Follows the main UNO rules:
  - Deals 7 cards to each player.
  - Manages the draw and discard piles.
  - Supports special cards: +2, +4, Color Change, Reverse, Skip.
  - Players automatically play the first valid card in their hand.
  - If a player cannot play, they draw a card.
- Displays the game progress in the terminal (played cards, effects, winner).

## Project Structure

```
.
├── main.py        # Main script: runs a complete automated UNO game
└── README.md      # This file
```

## Usage

### Prerequisites

- Python 3.10 or higher
- No external packages required

### Start a Game

In the terminal, run:

```bash
python main.py
```

- By default, the game is played with 3 automated players.
- To set a random seed (for reproducibility), you can pass an argument :

```bash
python main.py 42
```

## Implemented Rules

- **Gameplay** : Each player takes turns. If they cannot play, they draw a card.
- **Special cards** :
  - `+2` : The next player draws 2 cards and skips their turn.
  - `+4` : The next player draws 4 cards, skips their turn, and the color changes randomly.
  - `Wild` : Allows changing the color (chosen randomly).
  - `Reverse` : Reverses the direction of play (acts as Skip with 2 players).
  - `Skip` : The next player skips their turn.
- **End of game** : The first player with no cards wins. If no one can play and the draw pile is empty, the game is declared a draw.

## Example Output

```
Turn 0 - Joueur 0's turn
Top card: Blue 5
Joueur 0: ['Red 2', 'Blue 7', 'Yellow +2', ...]
Joueur 0 plays Blue 7
...
Joueur 2 draws a card
...
Joueur 1 has won !
```

## Customization

- Change the `NUM_PLAYERS` variable in `main.py` to set the number of players (max 10).
- Player behavior is automated (no human interaction).

## Limitations & Improvements

- No human player (fully automated).
- No advanced strategies or AI.
- No unit tests or graphical interface.
