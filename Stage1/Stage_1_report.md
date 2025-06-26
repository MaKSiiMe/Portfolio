# 🌟 Stage 1 Report – Portfolio Project

---

## 📋 0. Team Formation Overview

- **👥 Team Name:** Team Rocket

- **👤 Student Names:**
  - [TRUEL Maxime](https://github.com/MaKSiiMe) – Project Manager, AI Developer, Game Developer
  - [DIDI Badr](https://github.com/saru3450) – Fullstack Developer, Frontend & Backend Web Developer
  - **Shared Responsibility:** Database design and integration

- **🎯 Personal Objectives:**
  - 🚀 Learn and apply reinforcement learning in a real-world context
  - 🕹️ Develop a simplified game engine from scratch
  - 🌐 Explore full-stack web development for visualization and interaction
  - 💡 Build a product that is both innovative and technically challenging
  - 🤝 Work effectively as a team in a collaborative software development process

- **💬 Communication & Collaboration Tools:**
  - Slack, Discord, GitHub

- **🛠️ Technologies to Explore:**
  - Python (main programming language)
  - PyTorch or TensorFlow
  - OpenAI Gym (to structure the environment)
  - Front-End: CSS, Tailwind, JS (for result visualization)
  - Back-End: Flask, Python, JS

---

## 🔍 1. Research and Brainstorming

### 🧠 Method Used:
- 💡 Brainstorming based on personal interests (Blockchain, AI, gaming, sport)
- 📊 Feasibility and impact analysis
- 🗺️ [Mind Mapping - Initial Idea Exploration](https://mm.tt/map/3695024987?t=tDBVLK82R3)
- 🔍 [SCAMPER Framework - Idea Refinement](https://mm.tt/map/3695079337?t=D1vzNQwlVK)

---

## 💡 2. Ideas Explored

### 🃏 Idea 1: Train an AI to Play Pokémon TCG
- **Summary:** Build a reinforcement learning agent that learns to play Pokémon Trading Card Game (TCG) and improves through self-play.
- ✅ **Pros:**
  - Challenging and exciting project to explore RL
  - Can evolve into a deck recommender or strategy tester
  - Applicable to a wide audience
  - Good use case for machine learning and frontend development
- ❌ **Cons:**
  - Full game simulation is complex
  - Competitive space with many existing apps
  - Complex backend logic for personalization and safety

---

| Idea Element                                                            | Feasibility | Potential Impact | Technical Alignment | Scalability | Risks / Constraints                                    | Included in MVP ? | 
|-------------------------------------------------------------------------|-------------|------------------|---------------------|-------------|--------------------------------------------------------|-------------------|
| **Objective**                                                           |             |                  |                     |             |                                                        |                   |
| Learn new AI/ML technologies                                            | 5/5         | 5/5              | 5/5                 | 4/5         | Steep learning curve                                   | YES               |
| Create a useful tool for Pokémon TCG players                            | 5/5         | 5/5              | 4/5                 | 5/5         | Needs user feedback to be effective                    | YES               |
| Experiment with reinforcement learning                                  | 4/5         | 5/5              | 5/5                 | 4/5         | Complex to set up and optimize                         | YES               |
| **Game Understanding**                                                  |             |                  |                     |             |                                                        |                   |
| Rules of Pokémon TCG                                                    | 4/5         | 3/5              | 5/5                 | 4/5         | Detailed and sometimes unclear rules                   | YES (Simplified)  |
| Deck structure (types, energy, trainers)                                | 5/5         | 4/5              | 4/5                 | 4/5         | May vary across expansions                             | YES               |
| Match format (1v1, rounds, win conditions)                              | 4/5         | 4/5              | 4/5                 | 4/5         | Needs simplification for MVP                           | YES               |
| Existing deck tiers/meta                                                | 5/5         | 4/5              | 4/5                 | 4/5         | Might change over time                                 | YES               |
| **AI Approaches**                                                       |             |                  |                     |             |                                                        |                   |
| Reinforcement Learning – Self-play                                      | 4/5         | 5/5              | 5/5                 | 4/5         | Training stability and simulation speed                | YES               |
| Reinforcement Learning – Reward function (win, damage, cards drawn…)    | 3/5         | 5/5              | 5/5                 | 4/5         | Designing a good reward system is hard                 | YES (Simplified)  |
| Supervised Learning – Train on historical match data (if available)     | 3/5         | 4/5              | 5/5                 | 4/5         | Data might be hard to find                             | NO                |
| Heuristics / Monte Carlo Tree Search                                    | 4/5         | 3/5              | 4/5                 | 3/5         | May not scale to full game complexity                  | NO (Optional)     |
| **Technical Stack**                                                     |             |                  |                     |             |                                                        |                   |
| Game engine simulator – Build from scratch                              | 3/5         | 4/5              | 5/5                 | 4/5         | Time-consuming                                         | YES               |
| Game engine simulator – Use simplified rules                            | 5/5         | 4/5              | 4/5                 | 4/5         | Might limit realism of AI                              | YES               |
| Programming language (Python, Unity ML Agents…)                         | 5/5         | 4/5              | 5/5                 | 5/5         | Easy to implement but must be consistent across team   | YES               |
| AI frameworks (TensorFlow, PyTorch, Gym…)                               | 5/5         | 5/5              | 5/5                 | 5/5         | Well-documented but need to choose best fit            | YES               |
| Dataset (scraped games, simulated matches, etc.)                        | 4/5         | 4/5              | 4/5                 | 4/5         | Needs preprocessing and cleaning                       | NO                |
| **Output & UX**                                                         |             |                  |                     |             |                                                        |                   |
| Deck ranking                                                            | 5/5         | 5/5              | 4/5                 | 5/5         | Needs accurate win-rate tracking                       | YES               |
| Win rate vs meta decks                                                  | 4/5         | 5/5              | 4/5                 | 5/5         | Requires benchmark opponents                           | YES               |
| Recommendation system                                                   | 4/5         | 5/5              | 4/5                 | 5/5         | Needs interpretability                                 | NO                |
| Web dashboard                                                           | 5/5         | 5/5              | 4/5                 | 5/5         | Must be simple and intuitive                           | YES               |
| Visual feedback (graphs, decklists…)                                    | 5/5         | 4/5              | 4/5                 | 5/5         | Depends on frontend polish                             | YES               |
| AI Progress Visualization (victory statistics, emerging strategies...)  | 4/5         | 4/5              | 4/5                 | 4/5         | Requires access to training data, real-time stats...   | NO (Optional)     |
| **Challenges**                                                          |             |                  |                     |             |                                                        |                   |
| Complex rules and randomness                                            | 3/5         | 4/5              | 5/5                 | 3/5         | Adds variance and training instability                 | YES (Simplified)  |
| Simulation speed                                                        | 3/5         | 3/5              | 5/5                 | 3/5         | Could slow down training drastically                   | YES               |
| Data availability                                                       | 3/5         | 4/5              | 4/5                 | 4/5         | Might need synthetic generation                        | NO                |
| Game engine development                                                 | 4/5         | 4/5              | 5/5                 | 4/5         | Core component; can delay whole project                | YES               |
| **Potential Extensions**                                                |             |                  |                     |             |                                                        |                   |
| Apply to other card games (Hearthstone, Magic, Yu-Gi-Oh)                | 3/5         | 5/5              | 4/5                 | 5/5         | Only feasible after a successful MVP                   | NO                |
| API for players to test custom decks                                    | 4/5         | 5/5              | 4/5                 | 5/5         | Requires backend stability and auth                    | NO                |
| Adaptive AI opponent for training                                       | 4/5         | 5/5              | 4/5                 | 5/5         | Depends on training progress                           | NO                |
| Interactive Deck Builder                                                | 3/5         | 5/5              | 4/5                 | 5/5         | Needs card database and real-time feedback, complex UX | NO                |
| Simplified Match Simulator                                              | 4/5         | 4/5              | 4/5                 | 4/5         | Requires API, possible visual/animation challenges     | NO (Optional)     |
| Community & Sharing Platform (users profiles, decks, ideas, feedbacks)  | 3/5         | 5/5              | 3/5                 | 5/5         | User management, database, moderation...               | NO                |

---

## Evaluation Criteria Explanation

In this section, we explain the evaluation criteria used to assess the different components and ideas of our project. Each idea was rated from 1 (very poor) to 5 (excellent) on the following aspects:

---

### 🎯 1. Feasibility
**Definition:** How realistically can the idea be implemented within the MVP timeline and with the current team's skill set?

**Scoring Guide:**
- 5/5: Easily feasible with current skills and tools.
- 4/5: Requires some additional time or learning.
- 3/5: Technically possible but requires a significant amount of work or learning.
- 2/5: Very difficult or depends on external resources.
- 1/5: Almost impossible to achieve within the scope.

**Example:**  
"Build a simplified game engine from scratch" received a **3/5** because while it’s doable, it demands a lot of time and effort.

---

### 🌍 2. Potential Impact
**Definition:** What is the added value or usefulness of this idea? Will it impress users or contribute significantly to the final product?

**Scoring Guide:**
- 5/5: High impact; useful and/or impressive for users.
- 4/5: Good value but with limited visibility.
- 3/5: Interesting but not essential or very visible.
- 2/5: Limited usefulness.
- 1/5: Almost no visible benefit.

**Example:**  
"Deck ranking" got a **5/5** because it provides direct, useful, and visual feedback to TCG players.

---

### 🧠 3. Technical Alignment
**Definition:** How well does the idea align with the core technical goals of the project (AI, Machine Learning, RL, etc.)?

**Scoring Guide:**
- 5/5: Strong alignment with core AI goals (e.g., reinforcement learning).
- 4/5: Technically interesting and partially aligned.
- 3/5: Somewhat technical but not directly AI-related.
- 2/5: Low technical interest.
- 1/5: No technical relevance to the MVP.

**Example:**  
"Reinforcement learning with self-play" was rated **5/5**, as it’s central to the AI focus of the project.

---

### 🚀 4. Scalability
**Definition:** Can the idea be easily extended, improved, or generalized beyond the MVP?

**Scoring Guide:**
- 5/5: Highly extensible and reusable (e.g., can apply to other card games).
- 4/5: Evolves easily with a bit more development.
- 3/5: Limited scalability or usefulness beyond MVP.
- 2/5: Difficult to scale.
- 1/5: Not scalable at all.

**Example:**  
"Apply the agent to other card games" scored **5/5** since it naturally extends the current project logic.

---

### ⚠️ Risks / Constraints
This column highlights major risks or constraints for each idea. These are not scored numerically, but provide insight into:
- Time and complexity
- Lack of data
- Simulation performance
- Need for technical infrastructure or training time

---

Each idea from our mind map was evaluated with these criteria to guide our MVP development process and make strategic choices.



## 3. Decision and Refinement

### 🎯 Selected MVP: Train an AI to Play Pokémon TCG

#### **Main Objective:**
> Develop an AI that learns to play the Pokémon Trading Card Game using reinforcement learning to identify winning strategies and discover the most effective decks.

#### **MVP Description:**
For the MVP, we aim to build a simplified AI-powered tool that helps analyze and rank Pokémon TCG decks. The project includes:
- 🕹️ A custom game engine that simulates basic matches using simplified rules.
- 📊 A web dashboard presenting key insights such as win rates, deck comparisons, and visual feedback (graphs, match summaries, etc.).

#### **Problem It Solves:**
- Helps players better understand what makes a deck or strategy strong.
- Provides a learning sandbox for AI developers and game theorists.

#### **Target Users:**
- Pokémon TCG players
- AI developers and learners
- Gaming and e-sports community

#### **Key Features:**
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

## 📜 4. Idea Development Documentation

### **Process Summary:**
1. 💡 **Brainstormed** based on personal passions (AI + gaming)
2. 🔍 **Explored ideas** with pros and cons
3. ✅ **Selected** the most ambitious and educational idea
4. 🛠️ **Outlined** next steps and expected challenges
