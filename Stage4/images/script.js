window.onload = () => {
    const fullDeck = generateFullDeck();
    renderHand(fullDeck);
};

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

    // Exemple : ajouter une carte cachée au début
    const hiddenCard = document.createElement("div");
    hiddenCard.className = "card-back";
    hiddenCard.textContent = "🂠";
    handDiv.appendChild(hiddenCard);

    // Puis toutes les vraies cartes
    cards.forEach(card => {
        const div = document.createElement("div");
        div.className = `card ${card.color}`;
        div.textContent = card.value;
        handDiv.appendChild(div);
    });
}

function updateHand(hand) {
    const handDiv = document.getElementById('player-hand');
    handDiv.innerHTML = '';
    hand.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = `card ${card.color}`;
        cardDiv.innerText = card.value;
        cardDiv.addEventListener('click', () => playCard(card));
        handDiv.appendChild(cardDiv);
    });
}

function updateTopCard(card) {
    const pileDiv = document.getElementById('pile');
    pileDiv.innerHTML = '';
    const cardDiv = document.createElement('div');
    cardDiv.className = `card ${card.color}`;
    cardDiv.innerText = card.value;
    pileDiv.appendChild(cardDiv);
}

async function drawCard() {
    const response = await fetch('/api/draw_card', { method: 'POST' });
    const data = await response.json();

    if (data.card) {
        console.log(`Carte piochée : ${data.card.color} ${data.card.value}`);
    }

    updateHand(data.hand);
    updateTopCard(data.top_card);
}