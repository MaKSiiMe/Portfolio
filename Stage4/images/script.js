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

let selectedCardIndex = null;

function playSelectedCard() {
    if (selectedCardIndex === null) {
        alert("Sélectionne une carte d'abord !");
        return;
    }
    const card = document.querySelectorAll(".card")[selectedCardIndex];
    alert(`Tu joues : ${card.textContent}`);
    // TODO: envoyer au backend
    selectedCardIndex = null;
    card.style.border = "2px solid white"; // désélection
}

function drawCard() {
    alert("Tu as pioché une carte !");
    // TODO: appeler l’API pour piocher et mettre à jour la main
}

function passTurn() {
    alert("Tu passes ton tour.");
    // TODO: appeler l’API
}

function renderHand(cards) {
    const handDiv = document.getElementById("hand");
    handDiv.innerHTML = '';
    cards.forEach((card, index) => {
        const div = document.createElement("div");
        div.className = `card ${card.color}`;
        div.textContent = card.value;
        div.onclick = () => {
            document.querySelectorAll(".card").forEach(c => c.style.border = "2px solid white");
            div.style.border = "2px solid gold";
            selectedCardIndex = index;
        };
        handDiv.appendChild(div);
    });
}

