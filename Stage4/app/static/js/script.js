import { startGame, getGameState, playTurnAPI, drawCardsAPI, chooseColorAPI } from './api.js';

let gameId = null;
let playerIdx = 0;
let currentColor = null;

function cardToString(card) {
    if (typeof card === "string") return card;
    if (card && card.color && card.value) return `${card.color} ${card.value}`;
    return "";
}

function parseCard(cardStr) {
    if (!cardStr) return null;
    if (typeof cardStr !== "string") {
        if (cardStr.color && cardStr.value) return cardStr;
        return { color: "black", value: "?" };
    }
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

document.getElementById("start-btn").addEventListener("click", async () => {
    const result = await startGame("rulesbased");
    if (!result.success) return alert(result.error);
    if (!result.data || !result.data.game_id) {
        alert("Erreur: game_id manquant dans la réponse !");
        return;
    }
    gameId = result.data.game_id;
    playerIdx = 0;
    await updateGameState();
    await playBotIfNeeded();
});

document.getElementById("draw-btn").addEventListener("click", async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    const result = await drawCardsAPI(gameId, playerIdx, 1);
    if (!result.success) return alert(result.error);
    await updateGameState();
    await playBotIfNeeded();
});

async function tryPlayCard(cardIdx) {
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);
    const state = stateRes.data.state;
    const hand = state.hands[playerIdx];
    const cardStr = hand[cardIdx];
    const parsed = parseCard(cardStr);

    // Si c'est une Wild, demande la couleur AVANT de jouer
    if (parsed.value.startsWith("Wild")) {
        document.getElementById("color-choice").style.display = 'flex';
        window.pendingWild = { cardIdx };
        return;
    }

    // Joue la carte normale avec playTurnAPI (index dans la main)
    const playRes = await playTurnAPI(gameId, cardIdx);
    if (!playRes.success) return alert(playRes.error);
    await updateGameState();
    await playBotIfNeeded();
}

// Handler couleur Wild
document.querySelectorAll(".color-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
        if (!window.pendingWild) return;
        const { cardIdx } = window.pendingWild;
        const chosenColor = btn.dataset.color.charAt(0).toUpperCase() + btn.dataset.color.slice(1);

        // 1. Joue la carte Wild (playTurnAPI)
        const playRes = await playTurnAPI(gameId, cardIdx);
        if (!playRes.success) return alert(playRes.error);

        // 2. Change la couleur côté backend
        const colorRes = await chooseColorAPI(gameId, chosenColor);
        if (!colorRes.success) return alert(colorRes.error);

        document.getElementById("color-choice").style.display = 'none';
        window.pendingWild = null;
        await updateGameState();
        await playBotIfNeeded();
    });
});

async function updateGameState() {
    if (!gameId) return;
    const result = await getGameState(gameId);
    if (!result.success) return alert(result.error);
    const state = result.data.state;
    currentColor = state.current_color;
    renderHand(state.hands[playerIdx]);
    renderTopCard(state.discard_pile[state.discard_pile.length - 1]);
    renderBotHand(state.hands[1]);
    if (state.winner !== undefined && state.winner !== null) {
        setTimeout(() => {
            alert(state.winner === playerIdx ? "🎉 Vous avez gagné !" : "🤖 Le bot a gagné !");
        }, 100);
    }
}

// Fonction pour faire jouer le bot tant que c'est à lui
async function playBotIfNeeded() {
    let stateRes = await getGameState(gameId);
    while (stateRes.success && stateRes.data.state.current_player !== playerIdx && stateRes.data.state.winner === null) {
        const botRes = await playTurnAPI(gameId, null);
        if (!botRes.success) return alert(botRes.error);
        await updateGameState();
        stateRes = await getGameState(gameId);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    updateGameState();
});