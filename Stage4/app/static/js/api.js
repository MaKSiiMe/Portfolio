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

// Joue un tour (pour le joueur humain OU le bot)
export function playTurnAPI(gameId, humanInput = null) {
    // humanInput : index de la carte à jouer OU null (pour le bot/autoplay)
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

// Pioche une carte
export function drawCardsAPI(gameId, playerIdx, count = 1) {
    return fetch(`${API_BASE}/draw_cards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, player_idx: playerIdx, count })
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