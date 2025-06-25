const API_BASE = "http://localhost:5000";

// DECK 

function create_deck (seed) {
fetch("http://localhost:5000/api/create_deck", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ seed: 42 }) // ou {} si pas de seed
})
.then(response => response.json())
.then(data => console.log(data.deck))
.catch(error => console.error(error));

}
function reshuffle_discard_pile(deck, discardPile) {
    fetch("http://localhost:5000/api/reshuffle_discard_pile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ deck, discard_pile: discardPile })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Deck après reshuffle:", data.deck);
        console.log("Discard pile maintenant:", data.discard_pile);
    })
    .catch(error => console.error("Erreur lors du reshuffle:", error));
}

// displayDeck(deck) {

function print_board(turn, currentPlayer, topCard, deckSize = null) {
    const bodyData = {
        turn: turn,
        current_player: currentPlayer,
        top_card: topCard
    };

    if (deckSize !== null) {
        bodyData.deck_size = deckSize;
    }

    fetch("http://localhost:5000/api/print_board", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Board state reçu depuis le backend:", data);
        // ici tu peux mettre à jour ton interface utilisateur
    })
    .catch(error => console.error("Erreur lors de la récupération du board state:", error));
}

// game 

function createGame(numPlayers = 2, seed = null) {
    fetch("http://localhost:5000/api/create_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_players: numPlayers, seed: seed })
    })
    .then(res => res.json())
    .then(data => console.log("Game created:", data))
    .catch(err => console.error("Error creating game:", err));
}

function start(self) {
    fetch("http://localhost:5000/api/start", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => console.log("Game started:", data))
    .catch(err => console.error("Error starting game:", err));
}

function handle_first_card(self){
    fetch("http://localhost:5000/api/handle_first_card")
    .then(res => res.json())
    .then(data => console.log("Game state:", data))
    .catch(err => console.error("Error fetching state:", err));
}

function get_state(self) {
    fetch("http://localhost:5000/api/get_state")
    .then(res => res.json())
    .then(data => {
        console.log("Game state:", data);
        // ici tu peux mettre à jour ton interface utilisateur avec l'état du jeu
    })
    .catch(err => console.error("Error fetching state:", err));
}

function draw_card(self, player_idx) {
    fetch("http://localhost:5000/api/draw_card")
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            console.error("Erreur:", data.error);
        } else {
            console.log("Carte piochée. État:", data.state);
        }
    })
    .catch(err => console.error("Erreur lors de la pioche de carte:", err));
}

function play_turn(self, human_input) {
    fetch("http://localhost:5000/api/play_turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ card_index: cardIndex })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            console.error("Erreur:", data.error);
        } else {
            console.log("Tour joué. État:", data.state);
            if (data.winner !== null) {
                console.log(`Le joueur ${data.winner} a gagné !`);
            }
        }
    })
    .catch(err => console.error("Erreur au tour de jeu:", err));
}

function advence_turn(self) {
    fetch("http://localhost:5000/api/advance_turn")
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            console.error("Erreur:", data.error);
        } else {
            console.log("Tour avancé. État:", data.state);
            if (data.winner !== null) {
                console.log(`Le joueur ${data.winner} a gagné !`);
            }
        }
    })
    .catch(err => console.error("Erreur lors de l'avancement du tour:", err));
}

function calculate_score(self) {
    fetch("http://localhost:5000/api/calculate_score")
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            console.error("Erreur:", data.error);
        } else {
            console.log("Score calculé. État:", data.state);
            if (data.winner !== null) {
                console.log(`Le joueur ${data.winner} a gagné !`);
            }
        }
    })
    .catch(err => console.error("Erreur lors du calcul du score:", err));
}

// partie rules.py

async function is_playable(card, topCard, currentColor) {
  const response = await fetch('http://localhost:8000/is_playable', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      card: card,
      top_card: topCard,
      current_color: currentColor
    })
  });

  const data = await response.json();
  return data.playable;
}

async function calculate_card_points(hands, winnerIdx) {
  const response = await fetch('http://localhost:8000/calculate_card_point', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      hands: hands,
      winner_idx: winnerIdx
    })
  });

  const data = await response.json();
  return data.score;
}

async function calculate_score(hands, winnerIdx) {
  const response = await fetch('http://localhost:8000/calculate_score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      hands: hands,
      winner_idx: winnerIdx
    })
  });

  const data = await response.json();
  return data.score;
}

// utils 

async function encode_card(card) {
  const response = await fetch("http://localhost:8000/encode_card", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card })
  });
  const data = await response.json();
  return data.card_id;
}

async function decode_card(card_id) {
  const response = await fetch("http://localhost:8000/decode_card", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_id })
  });
  const data = await response.json();
  return data.card;
}

async function encode_hand(hand, maxSize = 20) {
  const response = await fetch("http://localhost:8000/encode_hand", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ hand, max_size: maxSize })
  });
  const data = await response.json();
  return data.encoded_hand;
}

async function decode_hand(encodedHand) {
  const response = await fetch("http://localhost:8000/decode_hand", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ encoded_hand: encodedHand })
  });
  const data = await response.json();
  return data.hand;
}

// constants

async function fetchConstants() {
  const response = await fetch("http://localhost:8000/constants");
  const data = await response.json();
  return data;
}

// enconding

async function getAllCards() {
  const response = await fetch("http://localhost:8000/all_cards");
  const data = await response.json();
  return data.all_cards;
}

async function cardToIndex(card) {
  const response = await fetch("http://localhost:8000/card_to_index", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card })
  });
  const data = await response.json();
  if (data.error) throw new Error(data.error);
  return data.index;
}

async function indexToCard(index) {
  const response = await fetch("http://localhost:8000/index_to_card", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index })
  });
  const data = await response.json();
  if (data.error) throw new Error(data.error);
  return data.card;
}


