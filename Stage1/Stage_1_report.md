# Stage 1 Report – Portfolio Project

## 0. Team Formation Overview

- **Team Name:** Team Name

- **Student Name:** [TRUEL Maxime](https://github.com/MaKSiiMe), [DIDI Badr](https://github.com/saru3450)

- **Role:**
  - Maxime: Project Manager, AI Developer, Game Developer
  - Badr: Fullstack Developer, Frontend & Backend Web Developer
  - Both: Responsible for database design and integration

- **Personal Objectives:**
  - Learn and apply reinforcement learning in a real-world context
  - Develop a simplified game engine from scratch
  - Explore full-stack web development for visualization and interaction
  - Build a product that is both innovative and technically challenging
  - Work effectively as a team in a collaborative software development process
  - <!-- Rajoute ce que tu veux ici -->

- **Communication & Collaboration**
  - Slack, Discord, Github

- **Technologies to Explore:**
  - Python (main programming language)
  - PyTorch or TensorFlow
  - OpenAI Gym (to structure the environment)
  - Front-End (CSS, Tailwind, JS) for result visualization
  - Back-End (flask, Python, JS)
  - <!-- Rajoute ce que tu veux ici -->

---

## 1. Research and Brainstorming

### Method Used:
- Brainstorming based on personal interests (Blockchain, AI, gaming, sport)
- Feasibility and impact analysis
- [Mind Mapping - Initial Idea Exploration](https://mm.tt/map/3695024987?t=tDBVLK82R3)
- [SCAMPER Framework - Idea Refinement](https://mm.tt/map/3695079337?t=D1vzNQwlVK)

---

## 2. Ideas Explored

### Idea 1: TAO Delegation Dashboard for Bittensor
- **Summary:** Create a web application to help TAO holders delegate their tokens across multiple Bittensor subnets, with performance analytics and an easy-to-use interface.
- ✅ Pros:
  - Useful for the Bittensor community
  - Real use case with personal relevance
  - Web-focused, with data visualization and backend
- ❌ Cons:
  - Niche audience
  - Limited AI component

---

### Idea 2: Train an AI to Play Pokémon TCG
- **Summary:** Build a reinforcement learning agent that learns to play Pokémon Trading Card Game (TCG) and improves through self-play.
- ✅ Pros:
  - Applicable to a wide audience
  - Good use case for machine learning and frontend development
  - Can include voice or chatbot interaction
- ❌ Cons:
  - Competitive space with many existing apps
  - Complex backend logic for personalization and safety

---

### Idea 3: AI-Powered Fitness Assistant

- 🌟 Idée 1 : Tableau de Bord pour le Classement des Decks
Description :
- Créer un tableau de bord web qui affiche les decks Pokémon TCG avec leurs statistiques (taux de victoire, popularité, performances contre des decks spécifiques).

- Fonctionnalité :
	- Classement des decks par performance.
	- Filtres pour sélectionner les decks par type, coût énergétique, ou autre c
	- Graphiques interactifs (barres, radar) pour visualiser les données.

- Conséquence :
	- Nécessite une intégration backend pour récupérer les données calculées par l’IA.
	- Ajoute une valeur directe pour les joueurs en fournissant des insights visuels clairs.
	- L’interface devra être conçue avec une attention particulière à l’ergonomie et à la responsivité (mobile/desktop).

🌟 Idée 2 : Simulateur de Matchs Simplifiés
Description :
	- Créer une interface où les utilisateurs peuvent configurer des matchs entre deux decks et voir les résultats simulés, basés sur les calculs de l'IA.

Fonctionnalités :

	- Sélection des decks par l’utilisateur via un menu déroulant.
	- Résumé des résultats de match (deck gagnant, points forts, cartes clés).

	- Historique des matchs simulés pour comparaison.

Conséquences :

	- Besoin d’une API connectée à la logique de l’IA pour exécuter les simulations.
	- Peut nécessiter des animations ou des visuels pour rendre les matchs plus engageants.
	- Outil pratique pour les utilisateurs cherchant à optimiser leurs stratégies.

🌟 Idée 3 : Créateur de Deck Interactif
Description :
	- Un outil permettant aux utilisateurs de construire leurs propres decks directement sur le site, avec des recommandations et des analyses fournies par l’IA.

Fonctionnalités :

	- Bibliothèque de cartes avec options de recherche et filtres.
	- Recommandations automatiques basées sur la compatibilité des cartes.
	- Feedback en temps réel sur la puissance du deck construit.

Conséquences :

	- Demande une base de données pour stocker et gérer les cartes disponibles.
	- Améliore l’engagement en permettant aux utilisateurs de personnaliser leur expérience.
	- Crée un pont direct entre l’IA et les joueurs via des suggestions intelligentes.

🌟 Idée 4 : Visualisation de la Progression de l’IA
Description :
	- Développer une page dédiée où les utilisateurs peuvent voir comment l’IA s’améliore au fil du temps (statistiques de victoire, stratégies émergentes, etc.).

Fonctionnalités :

	- Courbes de progression des performances de l’IA (ex. : taux de victoire).
	- Répartition des stratégies gagnantes et évolution des choix de cartes.
	- Section "Did You Know?" montrant des faits intéressants sur le processus d’apprentissage de l’IA.

Conséquences :

	- Ajoute une dimension éducative au projet.
	- Nécessite une connexion constante avec les données générées par l’IA.
	- Peut inclure des animations et graphiques pour rendre l’information engageante

🌟 Idée 5 : Communauté et Partage
Description :
	- Créer une section pour que les utilisateurs partagent leurs decks, leurs idées, et leurs expériences.

Fonctionnalités :

	- Système de partage de decks avec évaluations par la communauté.
	- Commentaires et discussions sur chaque deck.
	- Page de profil utilisateur montrant les decks favoris ou partagés.

Conséquences :

	- Renforce l’engagement communautaire.
	- Nécessite une base de données et une gestion des utilisateurs.
	- Complément idéal pour un projet axé sur un jeu compétitif.

---

| Idea Element                                                            | Feasibility | Potential Impact | Technical Alignment | Scalability | Risks / Constraints                                    |
|-------------------------------------------------------------------------|-------------|------------------|---------------------|-------------|--------------------------------------------------------|
| **Objective**                                                           |             |                  |                     |             |                                                        |
| Learn new AI/ML technologies                                            | 5/5         | 5/5              | 5/5                 | 4/5         | Steep learning curve                                   |
| Create a useful tool for Pokémon TCG players                            | 5/5         | 5/5              | 4/5                 | 5/5         | Needs user feedback to be effective                    |
| Experiment with reinforcement learning                                  | 4/5         | 5/5              | 5/5                 | 4/5         | Complex to set up and optimize                         |
| **Game Understanding**                                                  |             |                  |                     |             |                                                        |
| Rules of Pokémon TCG                                                    | 4/5         | 3/5              | 5/5                 | 4/5         | Detailed and sometimes unclear rules                   |
| Deck structure (types, energy, trainers)                                | 5/5         | 4/5              | 4/5                 | 4/5         | May vary across expansions                             |
| Match format (1v1, rounds, win conditions)                              | 4/5         | 4/5              | 4/5                 | 4/5         | Needs simplification for MVP                           |
| Existing deck tiers/meta                                                | 5/5         | 4/5              | 4/5                 | 4/5         | Might change over time                                 |
| **AI Approaches**                                                       |             |                  |                     |             |                                                        |
| Reinforcement Learning – Self-play                                      | 4/5         | 5/5              | 5/5                 | 4/5         | Training stability and simulation speed                |
| Reinforcement Learning – Reward function (win, damage, cards drawn…)    | 3/5         | 5/5              | 5/5                 | 4/5         | Designing a good reward system is hard                 |
| Supervised Learning – Train on historical match data (if available)     | 3/5         | 4/5              | 5/5                 | 4/5         | Data might be hard to find                             |
| Heuristics / Monte Carlo Tree Search                                    | 4/5         | 3/5              | 4/5                 | 3/5         | May not scale to full game complexity                  |
| **Technical Stack**                                                     |             |                  |                     |             |                                                        |
| Game engine simulator – Build from scratch                              | 3/5         | 4/5              | 5/5                 | 4/5         | Time-consuming                                         |
| Game engine simulator – Use simplified rules                            | 5/5         | 4/5              | 4/5                 | 4/5         | Might limit realism of AI                              |
| Programming language (Python, Unity ML Agents…)                         | 5/5         | 4/5              | 5/5                 | 5/5         | Easy to implement but must be consistent across team   |
| AI frameworks (TensorFlow, PyTorch, Gym…)                               | 5/5         | 5/5              | 5/5                 | 5/5         | Well-documented but need to choose best fit            |
| Dataset (scraped games, simulated matches, etc.)                        | 4/5         | 4/5              | 4/5                 | 4/5         | Needs preprocessing and cleaning                       |
| **Output & UX**                                                         |             |                  |                     |             |                                                        |
| Deck ranking                                                            | 5/5         | 5/5              | 4/5                 | 5/5         | Needs accurate win-rate tracking                       |
| Win rate vs meta decks                                                  | 4/5         | 5/5              | 4/5                 | 5/5         | Requires benchmark opponents                           |
| Recommendation system                                                   | 4/5         | 5/5              | 4/5                 | 5/5         | Needs interpretability                                 |
| Web dashboard                                                           | 5/5         | 5/5              | 4/5                 | 5/5         | Must be simple and intuitive                           |
| Visual feedback (graphs, decklists…)                                    | 5/5         | 4/5              | 4/5                 | 5/5         | Depends on frontend polish                             |
| **Challenges**                                                          |             |                  |                     |             |                                                        |
| Complex rules and randomness                                            | 3/5         | 4/5              | 5/5                 | 3/5         | Adds variance and training instability                 |
| Simulation speed                                                        | 3/5         | 3/5              | 5/5                 | 3/5         | Could slow down training drastically                   |
| Data availability                                                       | 3/5         | 4/5              | 4/5                 | 4/5         | Might need synthetic generation                        |
| Game engine development                                                 | 4/5         | 4/5              | 5/5                 | 4/5         | Core component; can delay whole project                |
| **Potential Extensions**                                                |             |                  |                     |             |                                                        |
| Apply to other card games (Hearthstone, Magic, Yu-Gi-Oh)                | 3/5         | 5/5              | 4/5                 | 5/5         | Only feasible after a successful MVP                   |
| API for players to test custom decks                                    | 4/5         | 5/5              | 4/5                 | 5/5         | Requires backend stability and auth                    |
| Adaptive AI opponent for training                                       | 4/5         | 5/5              | 4/5                 | 5/5         | Depends on training progress                           |

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
