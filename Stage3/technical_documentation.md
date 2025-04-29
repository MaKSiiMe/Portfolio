# Technical Documentation - AI Agent for Pokémon TCG Deck Optimization

## 1. System Architecture Overview

The project will consist of three main components:

```plaintext
+------------------------+
| 1. AI Agent             |
| - Model training        |
| - Match simulation      |
| - Deck evaluation logic |
+-----------+-------------+
            |
            v
+------------------------+
| 2. Data Management      |
| - Decks database        |
| - Match history storage |
| - Basic stats tracking  |
+-----------+-------------+
            |
            v
+------------------------+
| 3. Visualization Layer  |
| - Web or CLI dashboard  |
| - Deck rankings         |
| - Training progress     |
+------------------------+
```

---

## 2. Main Technologies

| Component             | Technology Suggestion          |
|:--------------------- |:------------------------------ |
| AI Agent              | Python (with PyTorch or simple custom training) |
| Data Management       | CSV files or lightweight SQLite DB |
| Visualization Layer   | CLI (Rich library for pretty tables) or Flask + basic HTML/CSS dashboard |

---

## 3. AI Agent: Design Choices

| Feature                    | Approach                          |
|:--------------------------- |:--------------------------------- |
| AI technique                | Reinforcement learning (basic Q-learning or policy iteration) |
| State representation        | Current deck composition and simplified battle situation |
| Action space                | Possible deck modifications or deck selections |
| Reward function             | Win/loss outcome of simulated matches |
| Training loop               | Self-play between random decks, agent updates its preferences |

---

## 4. Simplifications for MVP

- Limited number of cards (e.g., 20–30 cards only, not the full Pokémon TCG database).
- Simplified battle logic (abstract the game to "deck A wins deck B" based on deck strength).
- Static rules (no real-time battle actions, focus only on *deck vs deck* outcome).

---

## 5. Database Structure (if needed)

- **Decks**:
    - ID
    - List of cards
    - Current score (win ratio)

- **Matches**:
    - Match ID
    - Deck A vs Deck B
    - Winner

---

## 6. Visualization Features

- **Deck Rankings**: Table or bar chart of the best-performing decks
- **Training Progress**: Display win ratios over time
- **Basic Interface**:
    - CLI option: Use `Rich` (Python package for tables, progress bars)
    - Web option: Flask + HTML page + Chart.js for graphs

---

# Example of Visual Interface

## CLI Dashboard Example

```plaintext
=========================
  Best Performing Decks
=========================

Rank | Deck ID | Win Rate
-----+--------+---------
  1  |  #12   | 82%
  2  |  #8    | 77%
  3  |  #4    | 70%
  4  |  #15   | 66%

Training Iterations Completed: 500
```

## Web Dashboard Example

- Graph (bar chart) showing deck winrates
- Table listing each deck and its performance

---

# Recommended Technologies

| If you want to...         | Use...                                  |
|:----------------------|:-------------------------------------------|
| Console display       | Python + `rich` library (for pretty tables and progress bars) |
| Mini Web Dashboard     | Flask + HTML (optionally Bootstrap + Chart.js) |

---

# Next Steps

- [ ] Create a basic Python training loop for the AI agent
- [ ] Set up data saving in CSV or SQLite
- [ ] Build a simple CLI or web dashboard to visualize results

---

**Note:** I can also prepare for you:
- A basic AI agent training script
- A minimal Flask app example for visualizing your project

Just tell me if you want it!

