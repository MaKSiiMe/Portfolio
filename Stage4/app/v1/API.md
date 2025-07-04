# 🎮 UNO Game API Documentation

This API allows you to manage UNO games via simple HTTP requests (JSON).
All responses are in JSON format.

---

## Table of Contents

* [Start a New Game](#start-a-new-game)
* [Get Current Game State](#get-current-game-state)
* [Play a Turn](#play-a-turn)
* [Draw Cards](#draw-cards)
* [Choose Color](#choose-color)
* [Get Scores](#get-scores)
* [Delete a Game](#delete-a-game)
* [Check Card Playability](#check-card-playability)
* [Error Handling](#error-handling)
* [Tips](#tips)

---

## Start a New Game

**POST** `/api/start_game`

**Request body:**

```json
{
  "num_players": 2,
  "seed": 42,                // Optional, default: random
  "agent_type": "rulesbased" // Optional, default: "rulesbased". Choices: "rulesbased", "random", "ppo"
}
```

**Response (success):**

```json
{
  "success": true,
  "data": {
    "game_id": "abcd-1234-...",
    "agent_type": "rulesbased",
    "message": "Game started vs rulesbased agent",
    "discard_pile": "Yellow +2",
    "hands": [7, 7],
    "state": { ... } // full game state
  },
  "error": null
}
```

---

## Get Current Game State

**GET** `/api/game_state/<game_id>`

**Response:**

```json
{
  "success": true,
  "data": {
    "state": {
      "num_players": 2,
      "hands": [["Blue 1", ...], ["Red 3", ...]],
      "discard_pile": ["Yellow +2"],
      "current_player": 0,
      "current_color": "Yellow",
      "deck_size": 93,
      "direction": 1,
      "turn": 0,
      "cards_left": [7, 7],
      "winner": null
    }
  },
  "error": null
}
```

---

## Play a Turn

**POST** `/api/play_turn`

**Request body:**

```json
{
  "game_id": "abcd-1234-...",
  "human_input": 0      // Optional: index of the card in the current player's hand, or null if AI/autoplay (default)
}
```

**Examples:**

* Human plays the 1st card in their hand:

  ```json
  { "game_id": "abcd-1234-...", "human_input": 0 }
  ```
* Let the agent/AI choose automatically:

  ```json
  { "game_id": "abcd-1234-..." }
  ```

  or

  ```json
  { "game_id": "abcd-1234-...", "human_input": null }
  ```

**Response (success):**

```json
{
  "success": true,
  "data": {
    "state": { ... },           // updated game state
    "winner": null,             // index of winner if game over, else null
    "scores": null              // final scores if game over, else null
  },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "human_input out of bounds"
}
```

---

## Draw Cards

**POST** `/api/draw_cards`

**Request body:**

```json
{
  "game_id": "abcd-1234-...",
  "player_idx": 0,
  "count": 1         // Optional, default: 1
}
```

**Response (success):**

```json
{
  "success": true,
  "data": {
    "state": { ... },           // updated game state
    "warning": "No more cards left to draw." // (optional, only if deck and discard are empty)
  },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "Game is already over"
}
```

---

## Choose Color

**POST** `/api/choose_color`

**Request body:**

```json
{
  "game_id": "abcd-1234-...",
  "color": "Red"     // Must be one of: "Red", "Blue", "Green", "Yellow"
}
```

**Response (success):**

```json
{
  "success": true,
  "data": { "current_color": "Red" },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "Invalid color: Purple"
}
```

---

## Get Scores

**GET** `/api/get_scores/<game_id>`

**Response (success):**

```json
{
  "success": true,
  "data": {
    "scores": [86, 107]
  },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "Invalid game_id"
}
```

---

## Delete a Game

**DELETE** `/api/delete_game/<game_id>`

**Response (success):**

```json
{
  "success": true,
  "data": {
    "message": "Game abcd-1234 deleted."
  },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "Invalid game_id"
}
```

---

## Check Card Playability

**POST** `/api/is_playable`

**Request body:**

```json
{
  "card": "Red 5",
  "top_card": "Yellow +2",
  "current_color": "Red"
}
```

**Response (success):**

```json
{
  "success": true,
  "data": { "playable": true },
  "error": null
}
```

**Response (error):**

```json
{
  "success": false,
  "data": {},
  "error": "Field 'current_color' must be a non-empty string"
}
```

---

## Error Handling

All errors are returned with `success: false`, an explicit `error` message, and `data: {}`.

**Example error response:**

```json
{
  "success": false,
  "data": {},
  "error": "Invalid game_id"
}
```

---

## Tips

* All requests and responses use JSON format.
* You can use `fetch`, `axios`, `requests` (Python), etc. to interact with the API.
* The full game state is returned in the `state` key of responses.
* Always check the `success` field before processing the data.

---
