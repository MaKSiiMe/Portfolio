<h1 align="center">🎮 UNO Game Engine – Python</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
  <img src="https://img.shields.io/badge/Status-Automated%20Simulation-orange" />
</p>

<p align="center">
  <b>An automated, simple, modular UNO game engine, ready for AI!</b>
</p>

---

## 🚀 Overview

This project offers an **automated UNO game simulation** in Python, without a graphical interface. It allows you to start a game between several virtual players, while displaying the progress in the terminal. The goal is to provide a simple, readable, and easily modifiable engine.

---

## 🧩 Main Features

| Feature | Description |
|:---|:---|
| 👥 Players | 2 to 10 virtual players (3 by default) |
| 🃏 UNO Rules | Dealing, drawing, discard pile, special effects |
| 🔄 Special Effects | +2, +4, Color change, Reverse, Skip |
| 🤖 Players | Automatically play the first valid card |
| 📺 Display | Detailed progress in the terminal |
| 🏆 Victory | Displays the winner or a draw |

---

## 📁 Project Structure

```
.
├── main.py        # Main script: launches an automated UNO game
└── README.md      # This file
```

---

## ⚡️ Usage

### Prerequisites

- Python 3.10 or higher
- No external packages required

### Start a Game

```bash
python main.py
```

- By default, the game is played with 3 automated players.
- To set a random seed (for reproducibility):

```bash
python main.py 42
```

---

## 📜 Implemented Rules

- **Gameplay**: Each player plays in turn. If they cannot play, they draw a card.
- **Special cards**:
  - `+2`: The next player draws 2 cards and skips their turn.
  - `+4`: The next player draws 4 cards, skips their turn, and the color changes randomly.
  - `Wild`: Allows changing the color (chosen randomly).
  - `Reverse`: Reverses the direction of play (acts as Skip with 2 players).
  - `Skip`: The next player skips their turn.
- **End of game**: The first player with no cards wins. If no one can play and the draw pile is empty, the game is a draw.

---

## 🎲 Example Output

```
Turn 0 - Player 0's turn
Top card: Blue 5
Player 0: ['Red 2', 'Blue 7', 'Yellow +2', ...]
Player 0 plays Blue 7
...
Player 2 draws a card
...
Player 1 has won!
```

---

## 🛠️ Customization

- Modify the `NUM_PLAYERS` variable in `main.py` to change the number of players (max 10).
- Player behavior is automated (no human interaction).

---

## ⚠️ Limitations & Improvement Ideas

- No human player (100% automated simulation).
- No advanced strategy or AI.
- No unit tests or graphical interface.

---

## 🧠 AI Agent Roadmap

Before training an AI agent to play UNO, the engine must be modular and refactored. Here are the steps to support agent training, simulation, and evaluation.

<details>
<summary><b>See the full checklist</b></summary>

### ✅ 1. Separate game logic from players
- [ ] Create a `UnoGame` class to manage game state (`deck`, `discard_pile`, `hands`, `current_player`, etc.).
- [ ] Implement `get_game_state()` to return a player's view.
- [ ] Implement `play_turn(player_action)` to apply an action and update the state.

### ✅ 2. Create an Agent interface
- [ ] Define an abstract class `Agent` with the method `choose_action(game_state) -> action`.
- [ ] Implement `HumanAgent` for console input.
- [ ] Implement `RandomAgent` that randomly chooses a legal action.
- [ ] Attach an `Agent` instance per player (`self.agents = [...]`).

### ✅ 3. Encode states and actions
- [ ] Implement `encode_state(game_state)` to return a tensor or feature vector.
- [ ] Implement `decode_action(index)` if action space is discrete.
- [ ] Define the set of possible actions (playable cards + draw).

### ✅ 4. Simulation and logging
- [ ] Add a silent simulation mode (no print).
- [ ] Log each tuple `(state, action, reward, next_state, done)` per turn.
- [ ] Add a `run_episode()` method that returns the full log.

### ✅ 5. Define the reward function
- [ ] Implement `reward_function(state, action, next_state)`:
  - Small penalty each turn to encourage quick victory.
  - Large reward if the agent wins.
  - Penalty for illegal or null action.
- [ ] (Optional) Design other reward schemes.

### ✅ 6. Fully autonomous agent mode
- [ ] Allow games where all players are autonomous agents.
- [ ] Support batch simulations over multiple episodes.
- [ ] Collect data for reinforcement or supervised learning.

### ✅ 7. Replay and trace saving
- [ ] Allow saving complete episodes in JSON or pickle.
- [ ] (Optional) Tools to replay an episode step by step.

### ✅ 8. Debug & visualization tools
- [ ] Add a `verbose` flag to display agent decisions.
- [ ] Show cards played each turn for traceability.

---

### ✨ Bonus (Advanced Mechanics)
- [ ] Refactor each special effect (`+2`, `Reverse`, etc.) into its own method.
- [ ] Write unit tests to validate effect handling.

</details>

---

<p align="center">
  <i>This engine lays the foundation for training and testing intelligent UNO agents!</i>
</p>
