import { startGame, getGameState, playTurnAPI } from './api.js';

const BOT_DELAY_MS = 2000; // ralentit le bot

let gameId = null;
let playerIdx = 0;
let currentColor = null;
let botPlaying = false;
let lastPlayerHandSize = null;

function parseCard(cardStr) {
    if (!cardStr) return null;
    const parts = cardStr.split(' ');
    if (parts.length === 2) return { color: parts[0], value: parts[1] };
    if (parts.length === 3) return { color: parts[0], value: parts[1] + ' ' + parts[2] };
    return { color: 'black', value: cardStr };
}

function isWild(card) {
    return card.value.toLowerCase().includes('wild');
}

function renderHand(cards) {
    const handDiv = document.getElementById('hand');
    handDiv.innerHTML = '';
    cards.forEach((cardStr, idx) => {
        const card = parseCard(cardStr);
        if (isWild(card)) return;
        const div = document.createElement('div');
        div.className = `card ${card.color.toLowerCase()}`;
        const valueSpan = document.createElement('span');
        valueSpan.className = 'card-value';
        valueSpan.innerText = card.value;
        div.appendChild(valueSpan);
        div.onclick = () => tryPlayCard(idx);
        div.classList.add('drawn');
        setTimeout(() => div.classList.remove('drawn'), 500);
        handDiv.appendChild(div);
    });
}

function renderTopCard(cardStr) {
    const zone = document.getElementById('top-card');
    zone.innerHTML = '';
    if (!cardStr) return;
    const card = parseCard(cardStr);
    if (isWild(card)) return;
    const div = document.createElement('div');
    div.className = `card ${card.color.toLowerCase()}`;
    const valueSpan = document.createElement('span');
    valueSpan.className = 'card-value';
    valueSpan.innerText = card.value;
    div.appendChild(valueSpan);
    zone.appendChild(div);
    div.classList.add('fadeIn');
}

function renderBotHand(hands) {
    const botDiv = document.getElementById('bot-hand');
    botDiv.innerHTML = '';
    if (hands && hands.length > 1) {
        hands[1].forEach(() => {
            const div = document.createElement('div');
            div.className = 'card-back';
            div.textContent = '🂠';
            botDiv.appendChild(div);
        });
    }
}

document.getElementById('start-btn').addEventListener('click', async () => {
    const result = await startGame('rulesbased');
    if (!result.success) return alert(result.error);
    if (!result.data?.game_id) return alert('Erreur: game_id manquant dans la réponse !');
    gameId = result.data.game_id;
    playerIdx = 0;
    document.getElementById('draw-btn').style.display = 'inline-block';
    lastPlayerHandSize = null;
    await updateGameState();
    await playBotIfNeeded();
});

document.getElementById('draw-btn').addEventListener('click', async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    animateDrawCard(document.getElementById('hand'));
    const result = await playTurnAPI(gameId, null);
    if (!result.success) return alert(result.error);
    await updateGameState();
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);
    if (shouldBotPlay(stateRes.data.state)) {
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

    if (isWild(parsed)) {
        alert('Les cartes Wild ne sont pas autorisées dans cette partie.');
        return;
    }

    const playRes = await playTurnAPI(gameId, cardIdx);
    if (!playRes.success) {
        if (playRes.error && playRes.error.includes('not playable')) {
            showTemporaryPopup('❌ Cette carte n\'est pas jouable !');
            return;
        }
        return alert(playRes.error);
    }

    if (parsed.value === '+2' || parsed.value === '+4') {
        animateDrawCardBot(document.getElementById('bot-hand'));
    }

    await updateGameState();
    showEffectMessageIfNeeded(cardStr);
    await handleCardEffectIfNeeded(cardStr);

    const stateRes2 = await getGameState(gameId);
    if (!stateRes2.success) return alert(stateRes2.error);

    if (shouldBotPlay(stateRes2.data.state)) {
        await playBotIfNeeded();
    }
}

function shouldBotPlay(state) {
    return state.current_player !== playerIdx && state.winner === null;
}

// Boucle du bot + animation de pioche quand tu te prends un +2/+4
async function playBotIfNeeded() {
    if (botPlaying) return;
    botPlaying = true;
    try {
        while (true) {
            const stateRes = await getGameState(gameId);
            if (!stateRes.success) {
                alert(stateRes.error);
                break;
            }
            const state = stateRes.data.state;
            if (!shouldBotPlay(state)) break;

            // Taille AVANT le tour du bot
            const preHandSize = (lastPlayerHandSize !== null ? lastPlayerHandSize : state.hands[playerIdx]?.length || 0);

            const botRes = await playTurnAPI(gameId, null);
            if (!botRes.success) {
                alert(botRes.error);
                break;
            }

            const postStateRes = await getGameState(gameId);
            const postHandSize = postStateRes.data.state.hands[playerIdx]?.length || 0;

            // Animation si le bot t'a fait piocher (ex: +2, +4)
            const diff = postHandSize - preHandSize;
            if (diff > 0) {
                for (let i = 0; i < diff; i++) {
                    animateDrawCard(document.getElementById('hand'));
                }
                // Petite pause pour voir clairement l'animation
                await new Promise(res => setTimeout(res, 850));
            }
            lastPlayerHandSize = postHandSize;

            await updateGameState();
            await new Promise(res => setTimeout(res, BOT_DELAY_MS));
        }
    } finally {
        botPlaying = false;
    }
}

async function updateGameState() {
    if (!gameId) return;
    const result = await getGameState(gameId);
    if (!result.success) return alert(result.error);

    const state = result.data.state;
    currentColor = state.current_color;

    const drawBtn = document.getElementById('draw-btn');
    drawBtn.style.display = (state.current_player === playerIdx) ? 'inline-block' : 'none';

    renderHand(state.hands[playerIdx]);
    renderTopCard(state.discard_pile.at(-1));
    renderBotHand(state.hands);
    renderDrawPile(state.draw_pile_count ?? 10);

    if (state.winner !== undefined && state.winner !== null) {
        setTimeout(() => {
            alert(state.winner === playerIdx ? '🎉 Vous avez gagné !' : '🤖 Le bot a gagné !');
        }, 100);
        drawBtn.style.display = 'none';
        return;
    }

    // MAJ pour l'animation du prochain tour bot
    if (state.hands && state.hands[playerIdx]) {
        lastPlayerHandSize = state.hands[playerIdx].length;
    }

    if (shouldBotPlay(state)) {
        await playBotIfNeeded();
    }
}

function renderDrawPile(remainingCards = 10) {
    const pileDiv = document.getElementById('draw-pile-stack');
    pileDiv.innerHTML = '';
    const maxVisible = Math.min(remainingCards, 5);
    for (let i = 0; i < maxVisible; i++) {
        const back = document.createElement('div');
        back.className = 'card-back stacked';
        back.style.top = `-${i * 3}px`;
        back.style.left = `-${i * 3}px`;
        back.style.zIndex = i;
        pileDiv.appendChild(back);
    }
    pileDiv.title = 'Cliquez pour piocher';
    pileDiv.onclick = () => {
        if (document.getElementById('draw-btn').style.display !== 'none') {
            animateDrawCard(document.getElementById('hand'));
            document.getElementById('draw-btn').click();
        }
    };
}

function animateDrawCard(targetElement) {
    const drawPile = document.getElementById('draw-pile-stack');
    const pileCards = drawPile.querySelectorAll('.card-back.stacked');
    if (pileCards.length === 0) return;
    const lastPileCard = pileCards[pileCards.length - 1];
    const card = lastPileCard.cloneNode(true);
    lastPileCard.remove();
    card.classList.add('draw-animation');
    card.style.zIndex = 1000;
    const pileRect = drawPile.getBoundingClientRect();
    const handRect = targetElement.getBoundingClientRect();

    const tx = handRect.left - pileRect.left;
    const ty = handRect.top - pileRect.top;

    card.style.left = pileRect.left + 'px';
    card.style.top = pileRect.top + 'px';
    card.style.position = 'fixed';
    card.style.setProperty('--tx', `${tx}px`);
    card.style.setProperty('--ty', `${ty}px`);
    document.body.appendChild(card);

    setTimeout(() => card.remove(), 700);
}

function animateDrawCardBot(targetElement) {
    const drawPile = document.getElementById('draw-pile-stack');
    const pileCards = drawPile.querySelectorAll('.card-back.stacked');
    if (pileCards.length === 0) return;
    const lastPileCard = pileCards[pileCards.length - 1];
    const card = lastPileCard.cloneNode(true);
    lastPileCard.remove();
    card.className = 'card-back draw-animation';

    const pileRect = drawPile.getBoundingClientRect();
    const handRect = targetElement.getBoundingClientRect();

    const tx = handRect.left - pileRect.left;
    const ty = handRect.top - pileRect.top;

    card.style.left = pileRect.left + 'px';
    card.style.top = pileRect.top + 'px';
    card.style.setProperty('--tx', `${tx}px`);
    card.style.setProperty('--ty', `${ty}px`);
    document.body.appendChild(card);
    setTimeout(() => card.remove(), 700);
}

function showEffectMessageIfNeeded(cardStr) {
    const card = parseCard(cardStr);
    if (!card || isWild(card)) return;

    let message = '';
    if (card.value === '+2') message = '🤖 Le bot va piocher 2 cartes !';
    else if (card.value === '+4') message = '🤖 Le bot va piocher 4 cartes !';
    else if (card.value.toLowerCase() === 'skip') message = '⏭️ Tour du bot sauté !';
    else if (card.value.toLowerCase() === 'reverse') message = '🔄 Sens du jeu inversé !';

    if (message) showTemporaryPopup(message);
}

function showTemporaryPopup(text) {
    const popup = document.createElement('div');
    popup.className = 'popup-message';
    popup.textContent = text;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 2000);
}

async function handleCardEffectIfNeeded(cardStr) {
    return;
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('draw-btn').style.display = 'none';
});