import { startGame, playCardAPI, drawCardAPI, getGameState } from './api.js';

let gameId = null;
let playerIdx = 0;
let playerHand = [];
let topCard = null;

window.onload = () => {
    const fullDeck = generateFullDeck();
    renderHand(fullDeck);
};

document.getElementById("start-btn").addEventListener("click", async () => {
    const data = await startGame();
    gameId = data.game_id;
    playerIdx = 0; // joueur humain
    const state = await getGameState(gameId);
    playerHand = state.hands[playerIdx];
    topCard = state.discard_pile[state.discard_pile.length - 1];
    renderHand(playerHand);
    renderTopCard();
});

document.getElementById("draw-btn").addEventListener("click", async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    const result = await drawCardAPI(gameId, playerIdx);
    playerHand = result.state.hands[playerIdx];
    topCard = result.state.discard_pile.at(-1);
    renderHand(playerHand);
    renderTopCard();
});

function generateFullDeck() {
    const colors = ['red', 'green', 'blue', 'yellow'];
    const deck = [];

    // Cartes colorées : 0 (1x), 1-9, +2, ↺, ⏩ (2x)
    colors.forEach(color => {
        deck.push({ value: '0', color });

        for (let i = 1; i <= 9; i++) {
            deck.push({ value: String(i), color });
            deck.push({ value: String(i), color });
        }

        ['+2', '↺', '⏩'].forEach(symbol => {
            deck.push({ value: symbol, color });
            deck.push({ value: symbol, color });
        });
    });

    // Cartes spéciales noires
    for (let i = 0; i < 4; i++) {
        deck.push({ value: '+4', color: 'black' });
        deck.push({ value: '🎨', color: 'black' });
    }

    return deck;
}

function renderHand(cards) {
    const handDiv = document.getElementById("hand");
    handDiv.innerHTML = '';

    const hiddenCard = document.createElement("div");
    hiddenCard.className = "card-back";
    hiddenCard.textContent = "🂠";
    handDiv.appendChild(hiddenCard);

    cards.forEach(card => {
        const div = document.createElement("div");
        div.className = `card ${card.color}`;
        div.textContent = card.value;
        div.onclick = async () => {
            if (!gameId) return;
            const result = await playCardAPI(gameId, playerIdx, card);
            if (result.error) return alert(result.error);
            playerHand = result.state.hands[playerIdx];
            topCard = result.state.discard_pile.at(-1);
            renderHand(playerHand);
            renderTopCard();
        };
        handDiv.appendChild(div);
    });
}

function renderTopCard() {
    const zone = document.getElementById("top-card");
    if (topCard) {
        zone.textContent = `${topCard.color} ${topCard.value}`;
    }
}

window.renderAllUnoCards = function() {
    const fullDeck = generateFullDeck();
    renderHand(fullDeck);
};