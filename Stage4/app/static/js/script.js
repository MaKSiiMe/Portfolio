import { startGame, getGameState, playTurnAPI, drawCardsAPI, playCardAPI, chooseColorAPI } from './api.js';

let gameId = null;
let playerIdx = 0;
let currentColor = null;

function parseCard(cardStr) {
    if (!cardStr) return null;
    const parts = cardStr.split(' ');
    if (parts.length === 2) return { color: parts[0], value: parts[1] };
    if (parts.length === 3) return { color: parts[0], value: parts[1] + ' ' + parts[2] };
    return { color: 'black', value: cardStr };
}

function renderHand(cards) {
    const handDiv = document.getElementById("hand");
    handDiv.innerHTML = '';
    cards.forEach((cardStr, idx) => {
        const card = parseCard(cardStr);
        const div = document.createElement("div");
        div.className = `card ${card.color.toLowerCase()}`;
        div.textContent = card.value;
        div.onclick = () => tryPlayCard(idx);
        handDiv.appendChild(div);
    });
}

function renderTopCard(cardStr) {
    const zone = document.getElementById("top-card");
    zone.innerHTML = '';
    if (!cardStr) return;
    const card = parseCard(cardStr);
    const div = document.createElement("div");
    div.className = `card ${card.color.toLowerCase()}`;
    div.textContent = card.value;
    zone.appendChild(div);
}

function renderBotHand(cards) {
    const botDiv = document.getElementById("bot-hand");
    botDiv.innerHTML = '';
    cards.forEach(() => {
        const div = document.createElement("div");
        div.className = "card-back";
        div.textContent = "🂠";
        botDiv.appendChild(div);
    });
}

// Démarre une partie
document.getElementById("start-btn").addEventListener("click", async () => {
    const result = await startGame();
    console.log("startGame result:", result);
    if (result.error) return alert(result.error);
    if (!result.game_id) {
        alert("Erreur: game_id manquant dans la réponse !");
        return;
    }
    gameId = result.game_id;
    playerIdx = 0;
    updateGameState();
});

// Pioche une carte
document.getElementById("draw-btn").addEventListener("click", async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    const result = await drawCardsAPI(gameId, playerIdx, 1);
    console.log("drawCardsAPI result:", result);
    if (result.error) return alert(result.error);
    updateGameState();
});

async function tryPlayCard(cardIdx) {
    const stateRes = await getGameState(gameId);
    console.log("getGameState (tryPlayCard):", stateRes);
    if (stateRes.error) return alert(stateRes.error);
    const state = stateRes;
    const hand = state.hands[playerIdx];
    const cardStr = hand[cardIdx];
    const card = parseCard(cardStr);

    if (card.value.startsWith("Wild")) {
        document.getElementById("color-choice").style.display = 'flex';
        window.pendingWild = { cardIdx, cardStr };
        return;
    }

    const playRes = await playCardAPI(gameId, playerIdx, cardStr);
    console.log("playCardAPI result:", playRes);
    if (playRes.error) return alert(playRes.error);
    updateGameState();
}

document.querySelectorAll(".color-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
        if (!window.pendingWild) return;
        const { cardIdx, cardStr } = window.pendingWild;
        const chosenColor = btn.dataset.color.charAt(0).toUpperCase() + btn.dataset.color.slice(1);
        const playRes = await playCardAPI(gameId, playerIdx, cardStr);
        console.log("playCardAPI (wild) result:", playRes);
        if (playRes.error) return alert(playRes.error);
        // Ici, pas de chooseColorAPI car ton backend ne gère pas ce endpoint dans cette version
        document.getElementById("color-choice").style.display = 'none';
        window.pendingWild = null;
        updateGameState();
    });
});

async function updateGameState() {
    if (!gameId) return;
    const result = await getGameState(gameId);
    console.log("getGameState result:", result);
    if (result.error) return alert(result.error);
    const state = result;
    currentColor = state.current_color;
    renderHand(state.hands[playerIdx]);
    renderTopCard(state.discard_pile[state.discard_pile.length - 1]);
    renderBotHand(state.hands[1]);
    // Pas de gestion du gagnant ici car pas dans l'état retourné
}

window.addEventListener("DOMContentLoaded", () => {
    updateGameState();
});