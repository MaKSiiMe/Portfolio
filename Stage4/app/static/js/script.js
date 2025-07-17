import { startGame, getGameState, playTurnAPI } from './api.js';

// ----- CONFIGURATION -----
const BOT_DELAY_MS = 2500; // Temps d'attente entre chaque action du bot (ms)

let gameId = null;            // Identifiant unique de la partie en cours
let playerIdx = 0;            // Index du joueur humain (ici joueur 0)
let currentColor = null;      // Couleur en cours dans la partie
let botPlaying = false;       // Flag : vrai quand le bot est en train de jouer
let lastPlayerHandSize = null; // Mémorise le nb de cartes dans la main du joueur avant chaque tour du bot

// ----- OUTILS DE CARTE -----

// Décompose une chaîne de carte en un objet {color, value}
// Par exemple "Red +2" => { color: "Red", value: "+2" }
function parseCard(cardStr) {
    if (!cardStr) return null;
    const parts = cardStr.split(' ');
    if (parts.length === 2) return { color: parts[0], value: parts[1] };
    if (parts.length === 3) return { color: parts[0], value: parts[1] + ' ' + parts[2] };
    return { color: 'black', value: cardStr };
}

// Renvoie vrai si la carte est un joker Wild
function isWild(card) {
    return card.value.toLowerCase().includes('wild');
}

// ----- RENDERING (affichage/main/cartes) -----

// Affiche la main du joueur humain (en retirant les Wild si besoin)
function renderHand(cards) {
    const handDiv = document.getElementById('hand');
    handDiv.innerHTML = '';
    cards.forEach((cardStr, idx) => {
        const card = parseCard(cardStr);
        if (isWild(card)) return; // On masque les Wild
        const div = document.createElement('div');
        div.className = `card ${card.color.toLowerCase()}`;
        const valueSpan = document.createElement('span');
        valueSpan.className = 'card-value';
        valueSpan.innerText = card.value;
        div.appendChild(valueSpan);
        // Clic pour jouer cette carte
        div.onclick = () => tryPlayCard(idx);
        // Animation de pioche quand nouvelle carte (rapide)
        div.classList.add('drawn');
        setTimeout(() => div.classList.remove('drawn'), 500);
        handDiv.appendChild(div);
    });
}

// Affiche la carte du dessus de la pile
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

// Affiche la main du bot sous forme de dos de cartes
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

// ----- EVENEMENTS : Lancement et boutons -----

// Lancer une nouvelle partie
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

// Pioche manuelle du joueur humain
document.getElementById('draw-btn').addEventListener('click', async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    animateDrawCard(document.getElementById('hand')); // Anime la pioche
    const result = await playTurnAPI(gameId, null);
    if (!result.success) return alert(result.error);
    await updateGameState();
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);
    if (shouldBotPlay(stateRes.data.state)) {
        await playBotIfNeeded();
    }
});

// ----- Action : jouer une carte -----

// Quand le joueur clique une carte de sa main
async function tryPlayCard(cardIdx) {
    const stateRes = await getGameState(gameId);
    if (!stateRes.success) return alert(stateRes.error);
    const state = stateRes.data.state;
    const hand = state.hands[playerIdx];
    const cardStr = hand[cardIdx];
    const parsed = parseCard(cardStr);

    // On empêche les Wild dans cette variante
    if (isWild(parsed)) {
        alert('Les cartes Wild ne sont pas autorisées dans cette partie.');
        return;
    }

    // Lance la requête pour jouer la carte (backend)
    const playRes = await playTurnAPI(gameId, cardIdx);
    if (!playRes.success) {
        if (playRes.error && playRes.error.includes('not playable')) {
            showTemporaryPopup('❌ Cette carte n\'est pas jouable !');
            return;
        }
        return alert(playRes.error);
    }

    // Si c'est un +2 ou +4 qu'on pose, anime la pioche du bot !
    if (parsed.value === '+2' || parsed.value === '+4') {
        animateDrawCardBot(document.getElementById('bot-hand'));
    }

    await updateGameState();
    showEffectMessageIfNeeded(cardStr);
    await handleCardEffectIfNeeded(cardStr);

    // Si c'est au bot : lance la boucle bot
    const stateRes2 = await getGameState(gameId);
    if (!stateRes2.success) return alert(stateRes2.error);
    if (shouldBotPlay(stateRes2.data.state)) {
        await playBotIfNeeded();
    }
}

// Vérifie si c'est au bot de jouer
function shouldBotPlay(state) {
    return state.current_player !== playerIdx && state.winner === null;
}

// ----- BOUCLE BOT avec animation pioche quand on subit un +2/+4 -----

async function playBotIfNeeded() {
    if (botPlaying) return; // Évite de lancer deux boucles bot en parallèle
    botPlaying = true;
    try {
        while (true) {
            // 1. Etat courant avant le tour du bot
            const stateRes = await getGameState(gameId);
            if (!stateRes.success) {
                alert(stateRes.error);
                break;
            }
            const state = stateRes.data.state;
            if (!shouldBotPlay(state)) break;
            // Mémorise la taille de ta main avant le coup du bot
            const preHandSize = (lastPlayerHandSize !== null ? lastPlayerHandSize : state.hands[playerIdx]?.length || 0);

            // 2. Le bot joue son tour (joue carte/pioche/etc.)
            const botRes = await playTurnAPI(gameId, null);
            if (!botRes.success) {
                alert(botRes.error);
                break;
            }

            // 3. Etat après le coup du bot : regarde si tu as pioché
            const postStateRes = await getGameState(gameId);
            const postHandSize = postStateRes.data.state.hands[playerIdx]?.length || 0;
            const diff = postHandSize - preHandSize;

            // 4. Si tu as pioché (subi un +2/+4), on ANIME la pioche
            if (diff > 0) {
                for (let i = 0; i < diff; i++) {
                    animateDrawCard(document.getElementById('hand'));
                }
                // Pause pour bien voir la pioche arriver
                await new Promise(res => setTimeout(res, 850));
            }
            lastPlayerHandSize = postHandSize;

            await updateGameState(); // Rafraîchit affichages
            await new Promise(res => setTimeout(res, BOT_DELAY_MS)); // Pause avant prochain coup du bot
        }
    } finally {
        botPlaying = false;
    }
}

// ----- MAJ affichage / mémorisation taille main joueur -----

async function updateGameState() {
    if (!gameId) return;
    const result = await getGameState(gameId);
    if (!result.success) return alert(result.error);
    const state = result.data.state;
    currentColor = state.current_color;

    // Affiche ou masque le bouton pioche selon le tour
    const drawBtn = document.getElementById('draw-btn');
    drawBtn.style.display = (state.current_player === playerIdx) ? 'inline-block' : 'none';

    // Rafraîchit l'affichage du jeu
    renderHand(state.hands[playerIdx]);
    renderTopCard(state.discard_pile.at(-1));
    renderBotHand(state.hands);
    renderDrawPile(state.draw_pile_count ?? 10);

    // Si victoire, popup + bloque pioche
    if (state.winner !== undefined && state.winner !== null) {
        setTimeout(() => {
            alert(state.winner === playerIdx ? '🎉 Vous avez gagné !' : '🤖 Le bot a gagné !');
        }, 100);
        drawBtn.style.display = 'none';
        return;
    }

    // Mémorise taille actuelle de ta main (pour la prochaine boucle playBotIfNeeded)
    if (state.hands && state.hands[playerIdx]) {
        lastPlayerHandSize = state.hands[playerIdx].length;
    }

    // Relance bot si besoin
    if (shouldBotPlay(state)) {
        await playBotIfNeeded();
    }
}

// ----- ANIMATIONS + OUTILS -----

// Affiche plusieurs dos de cartes comme pile à piocher
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
    // Clique sur la pile pour piocher (pour UX)
    pileDiv.title = 'Cliquez pour piocher';
    pileDiv.onclick = () => {
        if (document.getElementById('draw-btn').style.display !== 'none') {
            animateDrawCard(document.getElementById('hand'));
            document.getElementById('draw-btn').click();
        }
    };
}

// Animation carte qui va de la pioche vers la main du joueur humain
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

// Animation carte qui va de la pioche vers la main du bot
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

// Affiche un message spécial lors de l'effet (optionnel)
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

// Popup temporaire contextuel
function showTemporaryPopup(text) {
    const popup = document.createElement('div');
    popup.className = 'popup-message';
    popup.textContent = text;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 2000);
}

// Placeholder pour d'autres effets si besoin
async function handleCardEffectIfNeeded(cardStr) {
    return;
}

// Cache le bouton pioche au démarrage de la page tant que la partie n’est pas lancée
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('draw-btn').style.display = 'none';
});