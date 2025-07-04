import { startGame, getGameState, playTurnAPI, drawCardsAPI, chooseColorAPI } from './api.js';

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
        div.classList.add("drawn");
        setTimeout(() => div.classList.remove("drawn"), 500);
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
    div.classList.add("fadeIn");
}

function renderBotHand(cards) {
    const botDiv = document.getElementById("bot-hand");
    botDiv.innerHTML = '';
    if (cards && cards.length > 1) {
        cards[1].forEach(() => {
            const div = document.createElement("div");
            div.className = "card-back";
            div.textContent = "🂠";
            botDiv.appendChild(div);
        });
    }
}

document.getElementById("start-btn").addEventListener("click", async () => {
    const result = await startGame("rulesbased");
    if (!result.success) return alert(result.error);
    if (!result.data?.game_id) return alert("Erreur: game_id manquant dans la réponse !");
    gameId = result.data.game_id;
    playerIdx = 0;
    document.getElementById("draw-btn").style.display = "inline-block";
    await updateGameState();
    await playBotIfNeeded();
});

document.getElementById("draw-btn").addEventListener("click", async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    const result = await drawCardsAPI(gameId, playerIdx, 1);
    if (!result.success) return alert(result.error);

    if (result.data.cards && result.data.cards.length > 0) {
        const newCardStr = result.data.cards[0];
        const pileDiv = document.getElementById("draw-pile-stack");
        const tempCard = document.createElement("div");
        const parsed = parseCard(newCardStr);
        tempCard.className = `card ${parsed.color.toLowerCase()} fly-to-hand`;
        tempCard.textContent = parsed.value;

        const rectFrom = pileDiv.getBoundingClientRect();
        tempCard.style.left = `${rectFrom.left}px`;
        tempCard.style.top = `${rectFrom.top}px`;
        document.body.appendChild(tempCard);

        const handDiv = document.getElementById("hand");
        const rectTo = handDiv.getBoundingClientRect();

        requestAnimationFrame(() => {
            tempCard.style.transform = `translate(${rectTo.left - rectFrom.left}px, ${rectTo.top - rectFrom.top}px) scale(0.6)`;
            tempCard.style.opacity = "0";
        });

        setTimeout(() => {
            tempCard.remove();
            updateGameState();
            playBotIfNeeded();
        }, 650);
    } else {
        await updateGameState();
        await playBotIfNeeded();
    }
});

async function tryPlayCard(cardIdx) {
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);
    const state = stateRes.data.state;
    const hand = state.hands[playerIdx];
    const cardStr = hand[cardIdx];
    const parsed = parseCard(cardStr);

    if (parsed.value.startsWith("Wild")) {
        document.getElementById("color-choice").style.display = 'flex';
        window.pendingWild = { cardIdx };
        return;
    }

    const playRes = await playTurnAPI(gameId, cardIdx);
    if (!playRes.success) return alert(playRes.error);

    await updateGameState();
    showEffectMessageIfNeeded(cardStr);
    await handleCardEffectIfNeeded(cardStr);

    // Après coup, on vérifie à qui c'est le tour selon backend
    const stateRes2 = await getGameState(gameId);
    if (!stateRes2.success) return alert(stateRes2.error);
    const currentPlayer = stateRes2.data.state.current_player;

    if (currentPlayer !== playerIdx) {
        // C'est au bot de jouer (potentiellement saut de tour pour humain)
        await playBotIfNeeded();
    }
    // Sinon c'est encore à toi, on attend que tu joues
}

document.querySelectorAll(".color-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
        if (!window.pendingWild) return;
        const { cardIdx } = window.pendingWild;
        const chosenColor = btn.dataset.color.charAt(0).toUpperCase() + btn.dataset.color.slice(1);

        const playRes = await playTurnAPI(gameId, cardIdx);
        if (!playRes.success) return alert(playRes.error);

        const colorRes = await chooseColorAPI(gameId, chosenColor);
        if (!colorRes.success) return alert(colorRes.error);

        document.getElementById("color-choice").style.display = 'none';
        window.pendingWild = null;

        const stateRes = await getGameState(gameId);
        const state = stateRes.data.state;
        const playedCard = state.discard_pile.at(-1);

        await updateGameState();
        showEffectMessageIfNeeded(playedCard);
        await handleCardEffectIfNeeded(playedCard);

        const currentPlayer = state.current_player;
        if (currentPlayer !== playerIdx) {
            await playBotIfNeeded();
        }
    });
});

async function updateGameState() {
    if (!gameId) return;
    const result = await getGameState(gameId);
    if (!result.success) return alert(result.error);
    const state = result.data.state;
    currentColor = state.current_color;

    const drawBtn = document.getElementById("draw-btn");
    drawBtn.style.display = (state.current_player === playerIdx) ? "inline-block" : "none";

    renderHand(state.hands[playerIdx]);
    renderTopCard(state.discard_pile.at(-1));
    renderBotHand(state.hands);
    renderDrawPile(state.draw_pile_count ?? 10);

    if (state.winner !== undefined && state.winner !== null) {
        setTimeout(() => {
            alert(state.winner === playerIdx ? "🎉 Vous avez gagné !" : "🤖 Le bot a gagné !");
        }, 100);
        drawBtn.style.display = "none";
    }
}

async function playBotIfNeeded() {
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);

    const state = stateRes.data.state;
    if (state.current_player !== playerIdx && state.winner === null) {
        // Tour du bot - on joue UNE seule fois
        const oldTopCard = state.discard_pile.at(-1);
        const botRes = await playTurnAPI(gameId, null);
        if (!botRes.success) return alert(botRes.error);

        await updateGameState();

        const newState = await getGameState(gameId);
        const newTopCard = newState?.data?.state?.discard_pile?.at(-1);
        if (newTopCard && newTopCard !== oldTopCard) {
            showEffectMessageIfNeeded(newTopCard);
            await handleCardEffectIfNeeded(newTopCard);
        }
    }
}

function renderDrawPile(remainingCards = 10) {
    const pileDiv = document.getElementById("draw-pile-stack");
    pileDiv.innerHTML = '';

    for (let i = 0; i < remainingCards; i++) {
        const back = document.createElement("div");
        back.className = "card-back stacked";
        back.style.top = `-${i * 2}px`;
        back.style.left = `-${i * 2}px`;
        pileDiv.appendChild(back);
    }

    pileDiv.title = "Cliquez pour piocher";
    pileDiv.onclick = () => {
        if (document.getElementById("draw-btn").style.display !== "none") {
            document.getElementById("draw-btn").click();
        }
    };
}

function showEffectMessageIfNeeded(cardStr) {
    const card = parseCard(cardStr);
    if (!card) return;

    let message = '';

    if (card.value === '+2') message = "🤖 Le bot va piocher 2 cartes !";
    else if (card.value === '+4') message = "🤖 Le bot va piocher 4 cartes !";
    else if (card.value.toLowerCase() === 'skip') message = "⏭️ Tour du bot sauté !";
    else if (card.value.toLowerCase() === 'reverse') message = "🔄 Sens du jeu inversé !";
    else if (card.value.toLowerCase().includes('wild')) message = "🎨 Changement de couleur !";

    if (message) {
        showTemporaryPopup(message);
    }
}

function showTemporaryPopup(text) {
    const popup = document.createElement('div');
    popup.className = 'popup-message';
    popup.textContent = text;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 2000);
}

async function handleCardEffectIfNeeded(cardStr) {
    const card = parseCard(cardStr);
    if (!card) return;

    let cardsToDraw = 0;

    if (card.value === '+2') cardsToDraw = 2;
    else if (card.value === '+4') cardsToDraw = 4;

    if (cardsToDraw > 0) {
        const stateRes = await getGameState(gameId);
        if (!stateRes.success) return;
        const state = stateRes.data.state;

        const targetPlayer = state.current_player;

        const drawRes = await drawCardsAPI(gameId, targetPlayer, cardsToDraw);
        if (!drawRes.success) return alert(drawRes.error);

        await updateGameState();
    }
}

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("draw-btn").style.display = "none";
});