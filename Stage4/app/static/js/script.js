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
