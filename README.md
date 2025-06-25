<h1 align="center">🎮 UNO Game Engine – Python</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
  <img src="https://img.shields.io/badge/Status-Automated%20Simulation-orange" />
</p>

<p align="center">
  <b>A simple, modular, fully automated UNO engine, ready for AI experiments!</b>
</p>

---

## 🚀 Overview

This project offers a **fully automated UNO game simulation** in Python, with no graphical interface. You can launch a game between several virtual players, with detailed progress displayed in the terminal. The goal: a simple, readable, and easily modifiable engine.

---

## 🏆 MVP Description

### From Pokémon TCG to UNO

The initial goal was to train an AI to play a simplified version of the Pokémon TCG Pocket game. However, even a basic trading card game turned out to be too time-consuming for this MVP.

To stay focused on the main objective — **training an AI to play a card game** — the project pivoted to a simplified version of **UNO**, enabling faster development while keeping the AI-oriented goal.

The MVP remains unchanged: build a functional game engine and train AI agents through self-play and simulation. Only the game's complexity has been reduced to save time and prioritize the AI phase.

> **Note:** The Pokémon TCG project is still ongoing as a personal side project alongside my AI/ML specialization.

---

## 🧩 Main Features

| Feature         | Description                                              |
|:--------------- |:--------------------------------------------------------|
| 👥 Players      | 2 to 10 virtual players (3 by default)                   |
| 🃏 UNO Rules    | Dealing, drawing, discard pile, special effects          |
| 🔄 Special Cards| +2, +4, Color change, Reverse, Skip                      |
| 🤖 AI           | Automatically plays the first valid card                 |
| 📺 Display      | Detailed progress in the terminal                        |
| 🏆 Victory      | Shows the winner or a draw                               |

---

## 📁 Project Structure

```
├── Stage4/
│   ├── app/
│   │   ├── models/                         # Core logic: game engine, agents, environments
│   │   │   ├── uno/                        # UNO game logic (rules, deck, display, utils)
│   │   │   │   ├── constants.py
│   │   │   │   ├── deck.py
│   │   │   │   ├── display.py
│   │   │   │   ├── rules.py
│   │   │   │   └── utils.py
│   │   │   ├── agents/                     # AI agents (random, rule-based, RL)
│   │   │   │   ├── random_agent.py
│   │   │   │   ├── rule_based_agent.py
│   │   │   │   └── rl_agent.py
│   │   │   └── envs/                       # Gymnasium environments for UNO
│   │   │       └── uno_env.py
│   │   ├── scripts/                        # Scripts for training, evaluation, and testing
│   │   │   ├── train.py
│   │   │   ├── evaluate.py
│   │   │   └── play_human.py
│   │   ├── static/                         # Static files for web demo (HTML, CSS, JS)
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── script.js
│   │   │   └── index.html
│   │   └── v1/                             # API routes (Flask blueprint)
│   │       └── routes.py
│   ├── run.py                              # CLI entry point for UNO game
│   ├── server.py                           # Flask server entry point
│   └── requirements.txt                    # Python dependencies
└── README.md
```
---

## ⚡️ Usage

### Prerequisites

- Python 3.10 or higher
- No external packages required

### Start a Game

```bash
python run.py
```

- By default, the game runs with 3 automated players.
- To set a random seed (for reproducibility):

```bash
python run.py 42
```

---

## 📜 Implemented Rules

- **Gameplay:** Each player takes turns. If they can't play, they draw a card.
- **Special cards:**
  - `+2`: Next player draws 2 cards and skips their turn.
  - `+4`: Next player draws 4 cards, skips their turn, and the color changes randomly.
  - `Wild`: Allows changing the color (chosen randomly).
  - `Reverse`: Reverses play direction (acts as Skip with 2 players).
  - `Skip`: Next player skips their turn.
- **End of round:** The first player with no cards wins the round. If no one can play and the draw pile is empty, the round is a draw.
- **Official UNO scoring:** The round winner scores the sum of points from all cards left in other players' hands. The game continues until a player reaches 500 points.

---

## 🎲 Example Output

```
=== Round 16 ===
First card: Blue 3

Turn 0 - Player 0's turn
Top card: Blue 3
Player 0: Red 5, Blue 5, Green 8, Blue Reverse, Wild +4, Yellow Skip, Green 2
Player 0 plays: Blue 5
```
```
Turn 42 - Player 0's turn
Top card: Red Skip
Player 0: Blue 7, Blue Reverse, Red +2, Green 6, Green 6
Player 0 plays: Red +2
```
```
The draw pile was empty: the discard pile has been shuffled to form a new draw pile.
```
```
🎉 Player 2 wins the round! 🎉

Remaining cards for other players:
Player 0: ['Red 7', 'Yellow 3']
Player 1: ['Yellow 6', 'Blue 4']

Player 2 earns 20 points.
```
```
Current scores:
Player 0: 466 points
Player 1: 510 points
Player 2: 204 points
```
```
🏆 Player 1 wins the game with 510 points in 16 rounds!
```

---

## 🛠️ Customization

- Change the `NUM_PLAYERS` variable in `run.py` to set the number of players (max 10).
- Change the `HUMAN_PLAYER_IDX = -1` variable in `run.py` to set the index of a human player (by default, no human player, -1 = fully automated simulation).
- Player behavior is automated (no human interaction by default, unless you enable a human player).

---

## ⚠️ Limitations & Improvement Ideas

- By default, there is no human player (`HUMAN_PLAYER_IDX = -1`), but you can enable one by changing this variable.
- No advanced strategy or AI yet.
- No unit tests or graphical interface.
- The code now follows PEP8 (pycodestyle) standards.

---

## 🧠 AI Roadmap

Before training an AI agent to play UNO, the engine must be modular and refactored. Here are the planned steps to support agent training, simulation, and evaluation.

<details>
<summary><b>See the full checklist</b></summary>

### 0. Official Scoring Mode
- [x] Add point calculation based on cards remaining in opponents' hands.
- [x] Track cumulative scores for each player.
- [x] End the game when a player reaches 500 points.
- [x] Display a scoreboard after each round.
- [x] Allow replaying rounds while preserving player scores.

### 1. Separate game logic from players
- [x] Create a `UnoGame` class to manage game state (`deck`, `discard_pile`, `hands`, `current_player`, etc.).
- [x] Implement `get_game_state()` to return a player's view.
- [x] Implement `play_turn(player_action)` to apply an action and update the state.

### 2. Create an Agent interface
- [ ] Define an abstract class `Agent` with the method `choose_action(game_state) -> action`.
- [x] Implement `HumanAgent` for console input.
- [x] Implement `RandomAgent` that randomly chooses a legal action.
- [ ] Attach an `Agent` instance per player (`self.agents = [...]`).

### 3. Encode states and actions
- [ ] Implement `encode_state(game_state)` to return a tensor or feature vector.
- [ ] Implement `decode_action(index)` if action space is discrete.
- [ ] Define the set of possible actions (playable cards + draw).

### 4. Simulation and logging
- [ ] Add a silent simulation mode (no print).
- [ ] Log each tuple `(state, action, reward, next_state, done)` per turn.
- [ ] Add a `run_episode()` method that returns the full log.

### 5. Define the reward function
- [ ] Implement `reward_function(state, action, next_state)`:
  - Small penalty each turn to encourage quick victory.
  - Large reward if the agent wins.
  - Penalty for illegal or null action.
- [ ] (Optional) Design other reward schemes.

### 6. Fully autonomous agent mode
- [x] Allow games where all players are autonomous agents.
- [ ] Support batch simulations over multiple episodes.
- [ ] Collect data for reinforcement or supervised learning.

### 7. Replay and trace saving
- [ ] Allow saving complete episodes in JSON or pickle.
- [ ] (Optional) Tools to replay an episode step by step.

### 8. Debug & visualization tools
- [ ] Add a `verbose` flag to display agent decisions.
- [x] Show cards played each turn for traceability.

---

### ✨ Bonus (Advanced Mechanics)
- [x] Refactor each special effect (`+2`, `Reverse`, etc.) into its own method.
- [ ] Write unit tests to validate effect handling.

</details>

---

<p align="center">
  <i>This engine lays the foundation for training and testing intelligent UNO agents!</i>
</p>
