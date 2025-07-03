const API_BASE = "http://localhost:5000/api";

// Lance une nouvelle partie
export function startGame(agentType = "rulesbased") {
    return fetch(`${API_BASE}/start_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_players: 2, agent_type: agentType })
    }).then(res => res.json());
}

// Récupère l'état du jeu
export function getGameState(gameId) {
    return fetch(`${API_BASE}/game_state/${gameId}`)
        .then(res => res.json());
}

// Joue un tour (pour le joueur humain)
export function playTurnAPI(gameId, humanInput) {
    return fetch(`${API_BASE}/play_turn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, human_input: humanInput })
    }).then(res => res.json());
}

// Pioche une carte
export function drawCardsAPI(gameId, playerIdx, count = 1) {
    return fetch(`${API_BASE}/draw_cards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, count })
    }).then(res => res.json());
}

// Joue une carte
export function playCardAPI(gameId, playerIdx, card) {
    return fetch(`${API_BASE}/play_card`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, card })
    }).then(res => res.json());
}

// Change la couleur courante (pour les Wild)
export function chooseColorAPI(gameId, color) {
    return fetch(`${API_BASE}/choose_color`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, color })
    }).then(res => res.json());
}

// Vérifie si une carte est jouable
export function isPlayableAPI(card, topCard, currentColor) {
    return fetch(`${API_BASE}/is_playable`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ card, top_card: topCard, current_color: currentColor })
    }).then(res => res.json());
}
