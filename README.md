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
│   │   ├── models/
│   │   │   ├── uno/
│   │   │   │   ├── constants.py
│   │   │   │   ├── deck.py
│   │   │   │   ├── display.py
│   │   │   │   ├── rules.py
│   │   │   │   ├── utils.py
│   │   │   │   └── __init__.py
│   │   │   ├── agents/
│   │   │   │   ├── human_agent.py
│   │   │   │   ├── random_agent.py
│   │   │   │   ├── rl_agent.py
│   │   │   │   ├── rule_based_agent.py
│   │   │   │   └── __init__.py
│   │   │   ├── envs/
│   │   │   │   ├── run_env.py
│   │   │   │   ├── test_env.py
│   │   │   │   ├── uno_env.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── scripts/
│   │   │   ├── train.py
│   │   │   ├── evaluate.py
│   │   │   └── play_human.py
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   ├── js/
│   │   │   │   └── script.js
│   │   │   └── index.html
│   │   ├── v1/
│   │   │   ├── routes.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── run.py
│   ├── server.py
│   └── requirements.txt
├── README.md
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

- By default, the game runs with 3 automated players.
- To set a random seed (for reproducibility):

```bash
python main.py 42
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
...
Turn 42 - Player 0's turn
Top card: Red Skip
Player 0: Blue 7, Blue Reverse, Red +2, Green 6, Green 6
Player 0 plays: Red +2
...
The draw pile was empty: the discard pile has been shuffled to form a new draw pile.
...
🎉 Player 2 wins the round! 🎉

Remaining cards for other players:
Player 0: ['Red 7', 'Yellow 3']
Player 1: ['Yellow 6', 'Blue 4']

Player 2 earns 20 points.
...
Current scores:
Player 0: 466 points
Player 1: 510 points
Player 2: 204 points

🏆 Player 1 wins the game with 510 points in 16 rounds!
```

---

## 🛠️ Customization

- Change the `NUM_PLAYERS` variable in `main.py` to set the number of players (max 10).
- Change the `HUMAN_PLAYER_IDX = -1` variable in `main.py` to set the index of a human player (by default, no human player, -1 = fully automated simulation).
- Player behavior is automated (no human interaction by default, unless you enable a human player).

---

## ⚠️ Limitations & Improvement Ideas

- By default, there is no human player (`HUMAN_PLAYER_IDX = -1`), but you can enable one by changing this variable.
- No advanced strategy or AI yet.
- No unit tests or graphical interface.
- The code now follows PEP8 (pycodestyle) standards.

---

## 🧠 Global Roadmap: Trainable & Playable UNO AI via Web Interface

This roadmap consolidates all required steps to:
- Build a modular and stable UNO game engine
- Train an AI agent using Gymnasium
- Allow a human player to play against the AI via a web interface

<details>
<summary><b>See the full checklist</b></summary>

### ✅ 1. Stabilize the Game Engine

- [x] Refactor game logic into a `Game` class
- [x] Handle all special effects: +2, +4, Wild, Reverse, Skip
- [x] Implement official scoring (end at 500 points, scoreboard, round accumulation)
- [x] Support multiple autonomous agents
- [ ] Refactor each special effect into a dedicated method
- [ ] Add basic unit tests for card effects
- [ ] Add a `verbose=False` mode to disable printouts
- [ ] Support fast simulation mode (no `input()`, no `print()`)

### 🤖 2. Implement AI Agents

- [ ] Create an abstract `Agent` or `BaseAgent` class with `choose_action(game_state)`
- [x] Implement `HumanAgent` (console-based)
- [x] Implement `RandomAgent`
- [x] Implement `RuleBasedAgent`
- [ ] Implement `RLAgent` (based on a trained model)
- [ ] Ensure all agents follow the same interface
- [ ] Assign an agent instance per player (`self.agents = [...]`)

### 🧩 3. Encode Game State and Actions

- [x] Implement `encode_state(game_state)` → vector/tensor
- [x] Define `action_space` (playable cards + draw)
- [x] Implement `decode_action(index)`
- [ ] Implement consistent `observation_space`
- [ ] Support encoding of `top_card`, `hand`, `nb_cards_others`, etc.

### 🔁 4. Gymnasium Environment `UnoEnv`

- [x] Implement `reset()` and `step()` with observation, reward, done, info
- [x] Handle `done=True` at end of round
- [ ] Integrate a reward function:
  - Win: +1 / Loss: -1
  - Turn penalty: -0.1
  - Optional: rewards for strategic moves
- [ ] Test environment thoroughly with basic agents

### 📈 5. Simulation & Data Collection

- [ ] Implement a complete `run_episode()` method
- [ ] Log each `(state, action, reward, next_state, done)`
- [ ] Add batch simulation mode (e.g. 1000 games)
- [ ] Save episodes (Pickle / JSON)
- [ ] Add a step-by-step replay/debug tool

### 🏋️‍♂️ 6. Train AI Agent

- [ ] Implement a `train.py` script (DQN or similar)
- [ ] Support classic RL training loop
- [ ] Save and load models (`.pt` / `.pth`)
- [ ] Document the training pipeline (README or notebook)

### 🌐 7. Flask Backend Integration

- [ ] Create API routes:
  - `POST /start` – start a game
  - `POST /play` – send human action
  - `GET /state` – get current state
  - `GET /play-ai` – make AI play
- [ ] Manage session state between requests
- [ ] Return clean JSON for frontend

### 🖥️ 8. Web Interface (Frontend)

- [ ] Display player's hand (text or image)
- [ ] Add buttons to: play card, draw, pass
- [ ] Show current top card and color
- [ ] Display score and winner at round end
- [ ] Automatically show AI move after each human move

### 🧪 9. UX, Debug, Validation

- [ ] Add debug mode (`verbose`, logs)
- [ ] Display current turn clearly
- [ ] Validate player actions on client side
- [ ] Add replay support for saved episodes

### 🚀 10. Deployment

- [ ] Dockerize the full project
- [ ] Deploy to Render / Railway / Fly.io
- [ ] Prepare public demo (GitHub page, video, etc.)

---

</details>

---

<p align="center">
  <i>This engine lays the foundation for training and testing intelligent UNO agents!</i>
</p>
