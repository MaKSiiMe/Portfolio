# 🎮 UNO Game API Documentation

This API allows you to manage UNO games via simple HTTP requests (JSON).  
All responses are in JSON format.

---

## Table of Contents

- [Start a New Game](#start-a-new-game)
- [Get Current Game State](#get-current-game-state)
- [Play a Card](#play-a-card)
- [Draw Cards](#draw-cards)
- [Delete a Game](#delete-a-game)
- [Check Card Playability](#check-card-playability)
- [Error Handling](#error-handling)
- [Tips](#tips)

---

## Start a New Game

**POST** `/api/start_game`

**Request body:**
```json
{
  "num_players": 2,
  "agent_type": "rulesbased" // or "random", "ppo" (optional, default: "rulesbased")
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

## Play a Card

**POST** `/api/play_card`

**Request body:**
```json
{
  "game_id": "abcd-1234-...",
  "player_idx": 0,
  "card": "Red 5"
}
```

**Response (success):**
```json
{
  "success": true,
  "data": {
    "state": { ... } // updated game state
  },
  "error": null
}
```

**Response (error):**
```json
{
  "success": false,
  "data": {},
  "error": "Card is not playable"
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
  "count": 1
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "state": { ... } // updated game state
  },
  "error": null
}
```

---

## Delete a Game

**DELETE** `/api/delete_game/<game_id>`

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Game abcd-1234 deleted."
  },
  "error": null
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

**Response:**
```json
{
{
    "data": {
        "playable": true
    },
    "error": null,
    "success": true
}
}
```

---

## Error Handling

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

- All requests and responses use JSON format.
- You can use `fetch`, `axios`, `requests` (Python), etc. to interact with the API.
- Full game states are returned in the `state` key of responses.
