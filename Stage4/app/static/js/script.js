import { startGame, playCardAPI, drawCardAPI, getGameState } from './api.js';

let gameId = null;
let playerIdx = 0;
let playerHand = [];
let topCard = null;
let pendingColorChoice = null;

document.getElementById("start-btn").addEventListener("click", async () => {
    const data = await startGame();
    gameId = data.game_id;
    playerIdx = 0;
    const state = await getGameState(gameId);
    playerHand = state.hands[playerIdx];
    topCard = state.discard_pile.at(-1);
    renderHand(playerHand);
    renderTopCard();
});

document.getElementById("draw-btn").addEventListener("click", async () => {
    if (!gameId) return alert("Commencez une partie d'abord !");
    const result = await drawCardAPI(gameId, playerIdx);
    console.log("Résultat drawCardAPI :", result);

    playerHand = result.state.hands[playerIdx];
    topCard = result.state.discard_pile.at(-1);
    renderTopCard();

    const newCard = playerHand.at(-1);
    console.log("Carte piochée :", newCard);

    if (newCard && newCard.color && newCard.value) {
        animateCardFlyingToHand(newCard);

        // ➕ Réduire visuellement la pile
        const pile = document.getElementById("draw-pile-stack");
        if (pile.children.length > 0) {
            pile.removeChild(pile.lastElementChild);
        }

        // Régénérer la pile si elle est vide
        if (pile.children.length === 0) {
            renderDrawPileStack();
        }

    } else {
        console.warn("Carte invalide :", newCard);
        alert("Aucune carte valide n'a été piochée !");
        renderHand(playerHand);
    }
});

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
        div.onclick = () => tryPlayCard(card);
        handDiv.appendChild(div);
    });
}

function renderTopCard() {
    const zone = document.getElementById("top-card");
    zone.innerHTML = '';
    if (!topCard) return;
    const div = document.createElement("div");
    div.className = `card ${topCard.color}`;
    div.textContent = topCard.value;
    zone.appendChild(div);
}

function animateCardDraw(card) {
    const handDiv = document.getElementById("hand");
    const div = document.createElement("div");
    div.className = `card ${card.color} fadeIn`;
    div.textContent = card.value;
    handDiv.appendChild(div);

    // Redessine toute la main après l'animation
    setTimeout(() => renderHand(playerHand), 500);
}

async function tryPlayCard(card) {
    if (!gameId) return;

    if (card.color === 'black') {
        pendingColorChoice = card;
        document.getElementById("color-choice").style.display = 'flex';
        return;
    }

    await sendPlay(card.color, card.value);
}

async function sendPlay(color, value) {
    const cardStr = `${color} ${value}`;
    const result = await playCardAPI(gameId, playerIdx, cardStr);
    if (result.error) return alert(result.error);
    playerHand = result.state.hands[playerIdx];
    topCard = result.state.discard_pile.at(-1);
    renderHand(playerHand);
    renderTopCard();
}

document.querySelectorAll(".color-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
        if (!pendingColorChoice) return;
        const newColor = btn.dataset.color;
        await sendPlay(newColor, pendingColorChoice.value);
        pendingColorChoice = null;
        document.getElementById("color-choice").style.display = 'none';
    });
});

window.renderAllUnoCards = function() {
    const fullDeck = generateFullDeck();
    renderHand(fullDeck);
};

function generateFullDeck() {
    const colors = ['red', 'green', 'blue', 'yellow'];
    const deck = [];
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
    for (let i = 0; i < 4; i++) {
        deck.push({ value: '+4', color: 'black' });
        deck.push({ value: '🎨', color: 'black' });
    }
    return deck;
}

function renderDrawPileStack() {
  const pile = document.getElementById("draw-pile-stack");
  pile.innerHTML = "";

  for (let i = 0; i < 15; i++) {
    const card = document.createElement("div");
    card.className = "card-back stacked";
    const angle = (Math.random() * 6 - 3).toFixed(1);
    const offsetX = Math.random() * 4 - 2;
    const offsetY = i * 1.5;
    card.style.transform = `translate(${offsetX}px, ${offsetY}px) rotate(${angle}deg)`;
    card.style.zIndex = i;
    pile.appendChild(card);
  }
  // Appliquer l'animation de rebond
  pile.classList.remove("pile-reborn"); // reset
  void pile.offsetWidth; // forcer le reflow pour redéclencher l'animation
  pile.classList.add("pile-reborn");
}

function animateCardFlyingToHand(card) {
    const drawPile = document.getElementById("draw-pile-stack");
    const hand = document.getElementById("hand");

    const flyingCard = document.createElement("div");
    flyingCard.className = `card ${card.color}`;
    flyingCard.textContent = card.value;

    // Position absolue initiale (dessus pile)
    const rectStart = drawPile.getBoundingClientRect();
    const rectEnd = hand.getBoundingClientRect();

    flyingCard.style.position = 'absolute';
    flyingCard.style.left = rectStart.left + "px";
    flyingCard.style.top = rectStart.top + "px";
    flyingCard.style.zIndex = 9999;
    flyingCard.style.transition = 'all 0.6s ease-out';
    flyingCard.style.transform = 'scale(1.2)';
    flyingCard.style.pointerEvents = 'none';

    document.body.appendChild(flyingCard);

    setTimeout(() => {
        flyingCard.style.left = rectEnd.left + 60 + "px";
        flyingCard.style.top = rectEnd.top - 20 + "px";
        flyingCard.style.transform = 'scale(0.9)';
        flyingCard.style.opacity = '0.2';
    }, 10);

    setTimeout(() => {
        document.body.removeChild(flyingCard);
        renderHand(playerHand); // met à jour la vraie main après animation
    }, 700);
}




window.addEventListener("DOMContentLoaded", () => {
  renderDrawPileStack();
});
