// Simple UNO web demo: start game, play turn, show state

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const playTurnBtn = document.getElementById('playTurnBtn');
    const gameStateEl = document.getElementById('gameState');

    // Optionnel : afficher tout le JSON pour debug
    let debugMode = false;
    let lastAPIData = null;

    let gameId = null;

    async function updateGameState() {
        if (!gameId) {
            gameStateEl.textContent = "No game in progress.";
            return;
        }
        try {
            const res = await fetch(`/api/game_state/${gameId}`);
            if (!res.ok) {
                gameStateEl.textContent = "Game not found or error.";
                playTurnBtn.disabled = true;
                return;
            }
            const data = await res.json();
            lastAPIData = data;

            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "Unknown error");
                playTurnBtn.disabled = true;
                startBtn.disabled = false;
                return;
            }

            const state = data.data && data.data.state;
            if (debugMode || !state) {
                gameStateEl.textContent = JSON.stringify(data, null, 2);
            } else {
                // Affichage lisible
                let txt = "";
                txt += `Tour #${state.turn}\n`;
                txt += `Joueur courant : ${state.current_player}\n`;
                txt += `Carte dessus : ${state.discard_pile[state.discard_pile.length-1]}\n`;
                txt += `Main joueur 0 : ${state.hands[0].join(", ")}\n`;
                txt += `Main joueur 1 : ${state.hands[1].join(", ")}\n`;
                txt += `Cartes restantes : ${state.cards_left.join(" / ")}\n`;
                if (state.winner !== null && state.winner !== undefined) {
                    txt += `🎉 Partie terminée ! Gagnant : Joueur ${state.winner} 🎉\n`;
                }
                gameStateEl.textContent = txt;
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
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
            // game_id est dans data.data.game_id
            const gameIdFromAPI = data.data && data.data.game_id;
            if (data.success && gameIdFromAPI) {
                gameId = gameIdFromAPI;
                playTurnBtn.disabled = false;
                await updateGameState();
            } else {
                gameStateEl.textContent = "Failed to start game. " + (data.error || "");
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
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "Unknown error");
                playTurnBtn.disabled = true;
                startBtn.disabled = false;
                return;
            }
            // winner est dans data.data.winner
            const winner = data.data && data.data.winner;
            await updateGameState();
            if (winner !== null && winner !== undefined) {
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

    // (Optionnel) Ajoute un raccourci clavier pour basculer en debug mode
    document.addEventListener('keydown', (e) => {
        if (e.key === 'd' && e.ctrlKey) {
            debugMode = !debugMode;
            if (debugMode && lastAPIData) {
                gameStateEl.textContent = JSON.stringify(lastAPIData, null, 2);
            } else {
                updateGameState();
            }
        }
    });

    // Initial state
    playTurnBtn.disabled = true;
    gameStateEl.textContent = "No game in progress.";
});
