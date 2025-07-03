const API_BASE = "http://localhost:5000/api";

export function startGame() {
  return fetch(`${API_BASE}/start_game`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ num_players: 2 })
  }).then(res => res.json());
}

export function getGameState(gameId) {
  return fetch(`${API_BASE}/game_state/${gameId}`).then(res => res.json());
}

export function drawCardAPI(gameId, playerIdx) {
  return fetch(`${API_BASE}/draw_cards`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, count: 1 })
  }).then(res => res.json());
}

export function playCardAPI(gameId, playerIdx, card) {
  return fetch(`${API_BASE}/play_card`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, card })
  }).then(res => res.json());
}

// ✅ Ajoute cette fonction pour jouer le tour du bot
export function botPlayAPI(gameId) {
  return fetch(`${API_BASE}/bot_play?game_id=${gameId}`, {
    method: "POST"
  }).then(res => res.json());
}