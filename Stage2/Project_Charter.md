# 🌟 Project Charter – Portfolio Project

## 0. 🎯 Project Objectives

**✨ Purpose:**
The goal of this project is to build an **AI-driven system** capable of **evaluating and optimizing decks** for **Pokémon TCG Pocket** by learning from **simulated gameplay outcomes**. This initiative serves as a hands-on application of **reinforcement learning** in the context of a **simplified trading card game**, where the **AI agent** improves through **self-play** without relying on predefined strategies or datasets. The project also includes the development of a **minimal game engine** to simulate battles, a **deck scoring system**, and a **web dashboard** that allows users to **explore**, **compare**, and **visualize** the performance of different decks. This end-to-end solution will help the team strengthen their skills in **AI training workflows**, **game logic implementation**, **data management**, and **full-stack web development**.


**SMART Objectives:**
[Smart Objective - Define Project Objectives](https://mm.tt/map/3705342687?t=fVm3arspiu)

1. By the end of the development phase, create an AI agent that can autonomously play at least 100 games and improve deck performance based on win/loss outcomes using reinforcement learning.
2. Within 12 weeks, develop and integrate a web dashboard that displays the top 3 optimized decks with real-time performance metrics.
3. Ensure that the game engine simulates at least 90% of all valid game states defined by simplified Pokémon TCG Pocket rules before the MVP presentation.

---

## 1. Stakeholders and Team Roles

### Stakeholders

| Stakeholder Type | Name / Description                              | Role / Interest in the Project                                   |
| ---------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Internal         | Maxime (Team Member)                            | Responsible for game engine development and AI training          |
| Internal         | Badr (Team Member)                              | In charge of web development and database integration            |
| Internal         | Holberton Instructors & Reviewers               | Ensure educational alignment and evaluate deliverables           |
| External         | Target Users (TCG players, game AI enthusiasts) | End-users interested in watching or interacting with AI gameplay |

### Team Roles

| Role                  | Assigned To     | Responsibilities                                                                 |
| --------------------- | --------------- | -------------------------------------------------------------------------------- |
| Project Manager       | Maxime          | Organizes timeline, ensures coordination and delivery of milestones              |
| Game & AI Developer   | Maxime          | Designs the game logic, implements and trains the reinforcement learning agent   |
| Fullstack Developer   | Badr            | Builds the web interface and manages UI/UX                                       |
| Database Manager      | Maxime & Badr   | Designs and maintains the database used to store decks and game results          |

---

## 2. 📦 Project Scope

### ✅ In-Scope

- Development of a **simplified Pokémon TCG Pocket game engine**
- **Reinforcement learning agent** that plays the game and learns deck performance
- **Web frontend** to visualize AI matches and access deck rankings
- **Database** for storing cards, decks, and game outcomes

### ❌ Out-of-Scope

- Multiplayer online features
- Integration with Pokémon TCG Pocket APIs or assets
- Complex card effects outside the simplified ruleset
- Mobile application development

---

## 3. ⚠️ Risks and Mitigation Strategies

| Risk                                                        | Likelihood | Impact | Mitigation Strategy                                                                             |
| ----------------------------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------------------              |
| Lack of experience in reinforcement learning implementation | Medium     | High   | Dedicate time for studying RL concepts and use libraries like Stable Baselines3                 |
| Underestimation of time needed for AI training              | High       | High   | Start with simplified rules and run smaller training iterations early                           |
| Incompatibility or bugs between frontend and backend        | Medium     | Medium | Establish regular integration checkpoints and API contracts                                     |
| Scope creep with advanced game mechanics                    | Medium     | High   | Define and freeze game rules early; track all requested changes                                 |
| Limited dataset for AI evaluation                           | High       | Medium | Use self-play and synthetic data generation to build a sufficient training dataset              |
| Lack of important features right from the start.            | High       | Low    | Study the structure of similar databases (such as Pokédex online) and plan a clear data model.  |
| Difficulty managing a large map database.                   | Medium     | High   | Use a scalable cloud service like Firebase or MongoDB or similar to manage data efficiently.    |
| Lack of experience in the web domain                        | Medium     | Medium | Establish regular integration checkpoints and API contracts                                     |

---

## 4. 🗓️ High-Level Plan

| Stage                       | Timeline (Weeks) | Key Deliverables                                              |
| --------------------------- | ---------------- | ------------------------------------------------------------- |
| Stage 1: Idea Development   | Week 1–2         | MVP idea, simplified rules, early design choices              |
| Stage 2: Project Charter    | Week 3–4         | Project Charter document with all sections completed          |
| Stage 3: Technical Planning | Week 5–6         | Game engine implementation plan, AI strategy, database schema |
| Stage 4: MVP Development    | Week 7–10        | Game engine, trained AI agent, frontend and backend features  |
| Stage 5: Project Closure    | Week 11–12       | Final testing, documentation, and presentation                |

---

## 5. Document Sharing

Final document to be submitted via Holberton Intranet with links to code repository and presentation slides once completed.

> This Project Charter was created by Maxime and Badr for the Holberton Portfolio Project – Stage 2.
