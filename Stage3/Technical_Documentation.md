
# 📘 Technical Documentation – MVP UNO AI Game

---

## 1. 🎯 User Stories and Mockups

### User Stories (MoSCoW Prioritization)

| Priority | User Story |
|---------|------------|
| **Must Have** | As a player, I want to play a full UNO game against an AI, so that I can enjoy a solo game experience. |
| **Must Have** | As a developer, I want to simulate thousands of games, so that the AI can improve through training. |
| **Must Have** | As a player, I want to see the history of moves in a dashboard, so that I can understand the AI's strategy. |
| **Should Have** | As a tester, I want to select the AI’s difficulty level, so that I can evaluate different behaviors. |
| **Could Have** | As a player, I want to upload my game logs, so that I can analyze external gameplays. |

### Mockups

Wireframes for:
- Game View: card display, current player, action buttons.
- Dashboard: AI stats, win ratio, recent games.
(Mockups à créer avec Figma plus tard.)

---

## 2. 🧱 System Architecture

```
+-------------+          +---------------+          +---------------+
| Frontend UI | <------> |  FastAPI App  | <------> |   PostgreSQL  |
|  (optional) |          | (Python backend)         |    Database   |
+-------------+          +---------------+          +---------------+
                                   ↑
                                   |
                          +----------------+
                          |  AI Decision   |
                          | (RL or logic)  |
                          +----------------+
```

- **Frontend (optional)**: React or static HTML/JS dashboard.
- **Backend**: FastAPI, handles game logic and REST API.
- **AI Agent**: Trainable model or rule-based bot.
- **DB**: PostgreSQL, stores matches, player actions, training logs.

---

## 3. 🧩 Components, Classes, and Database Design

### Key Components & Classes

- `GameEngine`: manages the game flow (turns, actions, rules).
- `Player`: base class for human or AI players.
- `UNOCard`: represents each card (color, type, value).
- `DeckManager`: handles draw pile and discard pile.
- `AIPlayer`: inherits `Player`, adds decision logic.

### Database Schema (PostgreSQL)

```sql
Table: games
- id (PK)
- date_created
- result (win/loss/draw)
- total_turns

Table: actions
- id (PK)
- game_id (FK)
- player_type (human/ai)
- card_played
- turn_number

Table: ai_stats
- id (PK)
- model_version
- win_ratio
- total_games
```

---

## 4. 🔁 Sequence Diagrams

### Sequence 1: Player Plays a Turn

```
Player -> FastAPI -> GameEngine -> ValidateMove
                                   |
                        returns result (valid/invalid)
FastAPI -> DeckManager (if draw)
FastAPI -> DB (logs move)
```

### Sequence 2: AI Makes a Move

```
FastAPI -> AIPlayer -> GameStateAnalysis
                      -> ChooseAction
FastAPI -> GameEngine -> ApplyMove
FastAPI -> DB (logs move)
```

---

## 5. 🌐 API Specifications

### External APIs

Aucun appel externe requis (jeu auto-suffisant).

### Internal API Endpoints (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/game/start` | Initie une nouvelle partie |
| `POST` | `/game/play` | Envoie l’action du joueur |
| `GET`  | `/game/state` | Retourne l’état actuel du jeu |
| `POST` | `/game/ai` | Fait jouer l’IA |
| `GET`  | `/stats` | Récupère les performances de l’IA |
| `GET`  | `/history/{id}` | Récupère les logs d’une partie |

> 📦 Tous les échanges utilisent le format JSON.

---

## 6. 🛠️ SCM and QA Strategies

### SCM (Git)

- GitHub repository
- Branching:
  - `main` (prod)
  - `develop` (dev stable)
  - `feature/*`, `bugfix/*`, `hotfix/*`
- PR + code review obligatoire
- Commit messages conventionnels (`feat:`, `fix:`, etc.)

### QA Strategy

- `pytest` pour les tests unitaires et fonctionnels
- `test_game_engine.py`, `test_ai_behavior.py`, etc.
- Couverture de tests sur règles de jeu et IA
- Tests manuels avec Postman sur les endpoints
- GitHub Actions possible pour CI

---

## 7. ⚙️ Technical Justifications

| Décision | Justification |
|----------|---------------|
| **UNO vs Pokémon TCG** | Le jeu UNO simplifié permet un moteur de jeu stable en moins de temps. |
| **FastAPI** | Framework léger, rapide, parfait pour API RESTful. |
| **PostgreSQL** | Fiable et relationnel, idéal pour stocker des parties et actions. |
| **Python** | Langage commun pour IA et backend, facilite l’intégration. |
| **Git Flow** | Organisation claire entre dev, features, hotfixes. |
| **Tests automatisés** | Permet de valider les règles de manière fiable, indispensable pour IA. |
