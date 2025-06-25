import { isPlayable, drawCard } from './api.js';

let hand = ["Red 5", "Green +2", "Wild +4", "Yellow Skip", "Blue 9"];
let topCard = "Red Reverse";
let currentColor = "Red";
let skipNext = false;
let drawPenalty = 0;

function renderHand() {
  const handDiv = document.getElementById("hand");
  handDiv.innerHTML = "";
  hand.forEach((card, index) => {
    const div = document.createElement("div");
    div.className = `card ${getColorClass(card)}`;
    div.innerText = card;
    div.onclick = () => tryPlayCard(card, index, div);
    handDiv.appendChild(div);
  });
}

function renderTopCard() {
  const topDiv = document.getElementById("topCard");
  topDiv.className = `card ${getColorClass(topCard)}`;
  topDiv.innerText = topCard;
}

function getColorClass(card) {
  const color = card.split(" ")[0];
  if (["Red", "Green", "Blue", "Yellow"].includes(color)) return color;
  return "Wild";
}

async function tryPlayCard(card, index, cardElement) {
  const status = document.getElementById("status");
  const { playable } = await isPlayable(card, topCard, currentColor);

  if (!playable) {
    status.innerText = `❌ "${card}" non jouable.`;
    cardElement.style.opacity = 0.5;
    setTimeout(() => cardElement.style.opacity = 1, 500);
    return;
  }

  if (card.includes("+2")) drawPenalty += 2;
  if (card.includes("Wild +4")) drawPenalty += 4;
  if (card.includes("Skip")) skipNext = true;

  topCard = card;
  currentColor = getColorClass(card);
  hand.splice(index, 1);
  status.innerText = `✅ "${card}" joué${drawPenalty ? ` (+${drawPenalty})` : ''}${skipNext ? ' - tour sauté' : ''}.`;

  renderHand();
  renderTopCard();
}

async function handleDrawCard() {
  const { card } = await drawCard();
  hand.push(card);
  document.getElementById("status").innerText = `🃏 Carte piochée : ${card}`;
  renderHand();
}

document.getElementById("drawBtn").addEventListener("click", handleDrawCard);

renderHand();
renderTopCard();

// Simple UNO web demo: start game, play turn, show state

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const playTurnBtn = document.getElementById('playTurnBtn');
    const gameStateEl = document.getElementById('gameState');

    let gameId = null;

    async function updateGameState() {
        if (!gameId) {
            gameStateEl.textContent = "No game in progress.";
            return;
        }
        const res = await fetch(`/api/game_state/${gameId}`);
        if (!res.ok) {
            gameStateEl.textContent = "Game not found or error.";
            playTurnBtn.disabled = true;
            return;
        }
        const data = await res.json();
        gameStateEl.textContent = JSON.stringify(data, null, 2);
    }

    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        playTurnBtn.disabled = true;
        gameStateEl.textContent = "Starting game...";
        try {
            const res = await fetch('/api/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_players: 2 })
            });
            const data = await res.json();
            if (data.game_id) {
                gameId = data.game_id;
                playTurnBtn.disabled = false;
                await updateGameState();
            } else {
                gameStateEl.textContent = "Failed to start game.";
                startBtn.disabled = false;
            }
        } catch (e) {
            gameStateEl.textContent = "Error starting game.";
            startBtn.disabled = false;
        }
    });

    playTurnBtn.addEventListener('click', async () => {
        if (!gameId) return;
        playTurnBtn.disabled = true;
        try {
            const res = await fetch('/api/play_turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game_id: gameId })
            });
            const data = await res.json();
            await updateGameState();
            // If game is over, disable play button
            if (data.winner !== null && data.winner !== undefined) {
                playTurnBtn.disabled = true;
                startBtn.disabled = false;
            } else {
                playTurnBtn.disabled = false;
            }
        } catch (e) {
            gameStateEl.textContent = "Error playing turn.";
            playTurnBtn.disabled = false;
        }
    });

    // Initial state
    playTurnBtn.disabled = true;
    gameStateEl.textContent = "No game in progress.";
});
