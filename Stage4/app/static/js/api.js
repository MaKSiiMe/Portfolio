const API_BASE = "http://localhost:5000/api";

export function startGame(agentType = "rulesbased") {
    return fetch(`${API_BASE}/start_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_players: 2, agent_type: agentType })
    }).then(res => res.json());
}

export function getGameState(gameId) {
    return fetch(`${API_BASE}/game_state/${gameId}`)
        .then(res => res.json());
}

export function playTurnAPI(gameId, humanInput = null) {
    const body = { game_id: gameId };
    if (humanInput !== null && humanInput !== undefined) {
        body.human_input = humanInput;
    }
    return fetch(`${API_BASE}/play_turn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    }).then(res => res.json());
}

export function drawCardsAPI(gameId, playerIdx, count = 1) {
    return fetch(`${API_BASE}/draw_cards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, count })
    }).then(res => res.json());
}

export function chooseColorAPI(gameId, color) {
    return fetch(`${API_BASE}/choose_color`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, color })
    }).then(res => res.json());
}