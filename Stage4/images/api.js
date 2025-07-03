const API_URL = "/api";
let gameId = null;
let playerIndex = 0; // joueur humain toujours 0

async function startGame(numPlayers = 2) {
    const res = await fetch(`${API_URL}/start_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_players: numPlayers })
    });
    const data = await res.json();
    gameId = data.game_id;
    return data;
}

async function getGameState() {
    const res = await fetch(`${API_URL}/game_state/${gameId}`);
    return await res.json();
}

async function playTurn(card) {
    const res = await fetch(`${API_URL}/play_turn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, human_input: card })
    });
    return await res.json();
}

async function drawCard() {
    const res = await fetch(`${API_URL}/draw_cards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ game_id: gameId, player_idx: playerIndex, count: 1 })
    });
    return await res.json();
}

