# Stage 1 Report – Portfolio Project

## 0. Team Formation Overview

- **Student Name:** [TRUEL Maxime](https://github.com/MaKSiiMe), [DIDI Badr](https://github.com/saru3450)
- **Team:**
- **Role:** 
  - Badr: Fullstack Developer
  - Maxime: Project Manager, AI Developer
- **Personal Objectives:**
  - Learn new technologies related to artificial intelligence and gaming.
  - Build a creative and potentially useful project.
  - Deepen knowledge in reinforcement learning.
  - Deepen knowledge in web developement

- **Technologies to Explore:**
  - Python (main programming language)
  - PyTorch or TensorFlow
  - OpenAI Gym (to structure the environment)
  - Front-End (CSS, Tailwind, JS) for result visualization
  - Back-End (flask, Python)

---

## 1. Research and Brainstorming

### Method Used:
- Individual brainstorming based on personal interests (AI, gaming, strategy)
- Feasibility and impact analysis
- [Mind Mapping](https://mm.tt/map/3695024987?t=tDBVLK82R3)
- [SCAMPER Framework](https://mm.tt/map/3695079337?t=D1vzNQwlVK)

---

## 2. Ideas Explored

### Idea 1: Train an AI to Play Pokémon TCG
- **Summary:** Build a reinforcement learning agent that learns to play Pokémon Trading Card Game (TCG) and improves through self-play.
- ✅ Pros:
  - Challenging and exciting project to explore RL
  - Can evolve into a deck recommender or strategy tester
- ❌ Cons:
  - Full game simulation is complex
  - Requires strong foundation in AI and math

---

### Idea 2: Deck Battle Simulator
- **Summary:** Develop a simplified engine to simulate automatic battles between decks based on game rules.
- ✅ Pros:
  - Easier to implement
  - Can be used to test AI later
- ❌ Cons:
  - No dynamic decision-making
  - Lacks learning or adaptation

---

### Idea 3: Deck Analysis Dashboard
- **Summary:** Create a web dashboard to compare decks using different metrics (cost, win rate, type efficiency, etc.)
- ✅ Pros:
  - Visual, useful for players
  - Good for learning frontend development
- ❌ Cons:
  - Requires clean and reliable external data
  - No AI or learning component

---

### Idea 4: AI-Generated Optimal Decks
- **Summary:** Use AI to generate competitive decks based on a specific goal (e.g., countering another deck).
- ✅ Pros:
  - Very innovative
  - Can be adapted to other card games
- ❌ Cons:
  - Very complex (combinatorial problem)
  - Requires a lot of iterations and testing

---

## 3. Decision and Refinement

### 🎯 Selected MVP: Train an AI to Play Pokémon TCG

#### Main Objective:
> Develop an AI that learns to play the Pokémon Trading Card Game using reinforcement learning to identify winning strategies and discover the most effective decks.

#### Problem It Solves:
- Helps players better understand what makes a deck or strategy strong.
- Could provide a tool for testing or recommending decks.
- Provides a learning sandbox for AI developers and game theorists.

#### Target Users:
- Pokémon TCG players
- AI developers and learners
- Gaming and e-sports community

#### Key Features:
- Simplified game environment for training
- AI agent using RL (Q-learning, PPO, or similar)
- Match analysis system (win rate, mistakes, key cards)
- (Optional) Visualization of AI progression over time

#### Opportunities:
- Can be extended to other card games (e.g., Magic, Yu-Gi-Oh!)
- Potential for an educational tool
- Could become a deck recommendation API

#### Challenges:
- Building a simplified but realistic game engine
- Choosing and tuning the right learning algorithm
- Training time and computing resources
- Balancing game mechanics and abstraction level

---

## 4. Idea Development Documentation

### Process Summary:

1. **Brainstormed** based on personal passions (AI + gaming)
2. **Explored 4 ideas** with pros and cons
3. **Selected** the most ambitious and educational idea
4. **Outlined** next steps and expected challenges

---

## Next Step (for Stage 2):

- Build a simplified version of the Pokémon TCG (core rules, attacks, decks)
- Choose the most suitable RL library (e.g., Stable Baselines, Ray RLlib)
- Begin training and tracking AI performance over time

---
