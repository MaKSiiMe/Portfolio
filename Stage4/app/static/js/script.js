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
