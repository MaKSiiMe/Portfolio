# Project Charter – Portfolio Project (Stage 2)

## 0. Project Objectives

**Purpose:**
The goal of this project is to develop an AI-powered system capable of analyzing and optimizing decks for Pokémon TCG Pocket. This project provides a practical application of reinforcement learning within the context of a card game, enhancing understanding of AI training, data management, and game engine development.

**SMART Objectives:**

1. Implement a functional game engine that simulates Pokémon TCG Pocket mechanics by Week 6.
2. Develop and train a reinforcement learning model capable of playing the game and ranking decks by Week 10.
3. Build a frontend interface that allows users to view AI matches and explore deck rankings by Week 12.

---

## 1. Stakeholders and Team Roles

### Stakeholders

| Stakeholder Type | Name / Description                              | Role / Interest in the Project                                   |
| ---------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Internal         | Maxime (Team Member)                            | Responsible for game engine development and AI training          |
| Internal         | Badr (Team Member)                              | In charge of frontend development and database integration       |
| Internal         | Holberton Instructors & Reviewers               | Ensure educational alignment and evaluate deliverables           |
| External         | Target Users (TCG players, game AI enthusiasts) | End-users interested in watching or interacting with AI gameplay |

### Team Roles

| Role                 | Assigned To   | Responsibilities                                                               |
| -------------------- | ------------- | ------------------------------------------------------------------------------ |
| Project Manager      | Maxime        | Organizes timeline, ensures coordination and delivery of milestones            |
| AI/Backend Developer | Maxime        | Designs the game logic, implements and trains the reinforcement learning agent |
| Frontend Developer   | Badr          | Builds the web interface and manages UI/UX                                     |
| Database Manager     | Maxime & Badr | Designs and maintains the database used to store decks and game results        |

---

## 2. Project Scope

### In-Scope

* Development of a simplified Pokémon TCG Pocket game engine
* Reinforcement learning agent that plays the game and learns deck performance
* Web frontend to visualize AI matches and access deck rankings
* Database for storing cards, decks, and game outcomes

### Out-of-Scope

* Multiplayer online features
* Integration with official Pokémon TCG APIs or assets
* Complex card effects outside the simplified ruleset
* Mobile application development

---

## 3. Risks and Mitigation Strategies

| Risk                                                        | Likelihood | Impact | Mitigation Strategy                                                                |
| ----------------------------------------------------------- | ---------- | ------ | ---------------------------------------------------------------------------------- |
| Lack of experience in reinforcement learning implementation | Medium     | High   | Dedicate time for studying RL concepts and use libraries like Stable Baselines3    |
| Underestimation of time needed for AI training              | High       | High   | Start with simplified rules and run smaller training iterations early              |
| Incompatibility or bugs between frontend and backend        | Medium     | Medium | Establish regular integration checkpoints and API contracts                        |
| Scope creep with advanced game mechanics                    | Medium     | High   | Define and freeze game rules early; track all requested changes                    |
| Limited dataset for AI evaluation                           | High       | Medium | Use self-play and synthetic data generation to build a sufficient training dataset |

---

## 4. High-Level Plan

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
