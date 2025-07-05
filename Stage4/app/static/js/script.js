document.addEventListener('DOMContentLoaded', () => {
    // Boutons
    const startBtn = document.getElementById('startBtn');
    const stateBtn = document.getElementById('stateBtn');
    const playTurnBtn = document.getElementById('playTurnBtn');
    const drawBtn = document.getElementById('drawBtn');
    const chooseColorBtn = document.getElementById('chooseColorBtn');
    const scoresBtn = document.getElementById('scoresBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const isPlayableBtn = document.getElementById('isPlayableBtn');
    const debugBtn = document.getElementById('debugBtn');
    const gameStateEl = document.getElementById('gameState');

    let gameId = null;
    let debugMode = false;
    let lastAPIData = null;

    // Helper pour afficher/masquer le JSON
    function showDebug(json) {
        gameStateEl.textContent = JSON.stringify(json, null, 2);
    }

    function showStateSimple(state) {
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

    function enableAll(disable=false) {
        // Active ou désactive tous les boutons sauf debug
        [stateBtn, playTurnBtn, drawBtn, chooseColorBtn, scoresBtn, deleteBtn, isPlayableBtn]
            .forEach(btn => btn.disabled = disable);
    }

    // ---- Endpoint Actions ----

    // START GAME
    startBtn.addEventListener('click', async () => {
        let numPlayers = parseInt(prompt("Nombre de joueurs (2-10) ?", 2));
        if (isNaN(numPlayers)) numPlayers = 2;
        let agentType = prompt("Type d'agent ('rulesbased', 'random', 'ppo') ?", "rulesbased");
        if (!["rulesbased", "random", "ppo"].includes(agentType)) agentType = "rulesbased";
        startBtn.disabled = true;
        gameStateEl.textContent = "Starting game...";
        try {
            const res = await fetch('/api/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_players: numPlayers, agent_type: agentType })
            });
            const data = await res.json();
            lastAPIData = data;
            if (data.success && data.data && data.data.game_id) {
                gameId = data.data.game_id;
                enableAll(false);
                stateBtn.disabled = false;
                playTurnBtn.disabled = false;
                drawBtn.disabled = false;
                chooseColorBtn.disabled = false;
                scoresBtn.disabled = false;
                deleteBtn.disabled = false;
                isPlayableBtn.disabled = false;
                await showGameState();
            } else {
                gameStateEl.textContent = "Erreur création partie : " + (data.error || "");
                startBtn.disabled = false;
            }
        } catch (e) {
            gameStateEl.textContent = "Error starting game.";
            startBtn.disabled = false;
        }
    });

    // GAME STATE
    async function showGameState() {
        if (!gameId) return;
        try {
            const res = await fetch(`/api/game_state/${gameId}`);
            const data = await res.json();
            lastAPIData = data;
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "Unknown error");
                return;
            }
            if (debugMode) showDebug(data);
            else showStateSimple(data.data.state);
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
    }
    stateBtn.addEventListener('click', showGameState);

    // PLAY TURN
    playTurnBtn.addEventListener('click', async () => {
        if (!gameId) return;
        let input = prompt("Index de la carte à jouer (optionnel, vide pour IA/bot)", "");
        let body = { game_id: gameId };
        if (input !== "" && input !== null) {
            let idx = parseInt(input);
            if (!isNaN(idx)) body.human_input = idx;
        }
        playTurnBtn.disabled = true;
        try {
            const res = await fetch('/api/play_turn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            lastAPIData = data;
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "");
                playTurnBtn.disabled = false;
                return;
            }
            await showGameState();
            // Disable play if victoire
            const winner = data.data && data.data.winner;
            if (winner !== null && winner !== undefined) playTurnBtn.disabled = true;
            else playTurnBtn.disabled = false;
        } catch (e) {
            gameStateEl.textContent = "Error playing turn.";
            playTurnBtn.disabled = false;
        }
    });

    // DRAW CARDS
    drawBtn.addEventListener('click', async () => {
        if (!gameId) return;
        let idx = prompt("Index joueur (0 ou 1)", "0");
        let count = prompt("Nb cartes à piocher", "1");
        drawBtn.disabled = true;
        try {
            const res = await fetch('/api/draw_cards', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    game_id: gameId,
                    player_idx: parseInt(idx),
                    count: parseInt(count)
                })
            });
            const data = await res.json();
            lastAPIData = data;
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "");
            } else {
                await showGameState();
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
        drawBtn.disabled = false;
    });

    // CHOOSE COLOR
    chooseColorBtn.addEventListener('click', async () => {
        if (!gameId) return;
        let color = prompt("Nouvelle couleur ('Red', 'Yellow', 'Blue', 'Green')", "Red");
        if (!color) return;
        chooseColorBtn.disabled = true;
        try {
            const res = await fetch('/api/choose_color', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game_id: gameId, color: color })
            });
            const data = await res.json();
            lastAPIData = data;
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "");
            } else {
                await showGameState();
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
        chooseColorBtn.disabled = false;
    });

    // GET SCORES
    scoresBtn.addEventListener('click', async () => {
        if (!gameId) return;
        try {
            const res = await fetch(`/api/get_scores/${gameId}`);
            const data = await res.json();
            lastAPIData = data;
            if (!data.success) {
                gameStateEl.textContent = "Erreur API : " + (data.error || "");
            } else {
                gameStateEl.textContent = "Scores : " + data.data.scores.join(" / ");
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
    });

    // DELETE GAME
    deleteBtn.addEventListener('click', async () => {
        if (!gameId) return;
        if (!confirm("Supprimer la partie ?")) return;
        try {
            const res = await fetch(`/api/delete_game/${gameId}`, { method: 'DELETE' });
            const data = await res.json();
            lastAPIData = data;
            if (data.success) {
                gameStateEl.textContent = data.data.message;
                gameId = null;
                enableAll(true);
                startBtn.disabled = false;
            } else {
                gameStateEl.textContent = "Erreur suppression : " + (data.error || "");
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
    });

    // IS PLAYABLE
    isPlayableBtn.addEventListener('click', async () => {
        let card = prompt("Carte à tester (ex: 'Red 5')", "Red 5");
        let topCard = prompt("Carte sur la pile (ex: 'Yellow +2')", "Yellow +2");
        let currentColor = prompt("Couleur courante ('Red', 'Blue', 'Yellow', 'Green')", "Red");
        try {
            const res = await fetch('/api/is_playable', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    card,
                    top_card: topCard,
                    current_color: currentColor
                })
            });
            const data = await res.json();
            lastAPIData = data;
            if (data.success) {
                gameStateEl.textContent = `Playable: ${data.data.playable}`;
            } else {
                gameStateEl.textContent = "Erreur API : " + (data.error || "");
            }
        } catch (e) {
            gameStateEl.textContent = "Erreur réseau.";
        }
    });

    // DEBUG BUTTON
    debugBtn.addEventListener('click', () => {
        debugMode = !debugMode;
        debugBtn.textContent = debugMode ? "Masquer JSON" : "Afficher JSON (debug)";
        if (debugMode && lastAPIData) {
            gameStateEl.textContent = JSON.stringify(lastAPIData, null, 2);
        } else {
            showGameState();
        }
    });

    // Initial state
    enableAll(true);
    gameStateEl.textContent = "Aucune partie en cours.";
    debugBtn.textContent = "Afficher JSON (debug)";
});
