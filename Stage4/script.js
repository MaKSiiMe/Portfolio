const socket = io();

function renderGame(state) {
    // Affichage Ia
    document.getElementById( 'ia-cards-count').textContent = state.iaCount;
    let IaDIV = document.getElementById('ia-cards');
    IaDIV.innerHTML = '';
    for (let i = 0; i < state.ia.length; i++) {
        let c = document.createElement('div');
        c.className = 'card';
        c.textContent = '?';
        IaDIV.appendChild(c);
    }

    // Affichage Joueur
    let mainDIV = document.getElementById('player-cards');
    mainDIV.innerHTML = '';
    state.joueur.forEach((card, index) => {
        let c = document.createElement('div');
        c.className = 'card' + (card.valeur === 'Joker' || card.valeur === '+4' ? ' joker' : '');
        c.textContent = ( card.couleur ? card.couleur + ' ' : '') + card.valeur;;
        c.style.background = couleurTOCSS(card.couleur, card.valeur);
        c.onclick = () => {
            socket.emit('jouerCarte', index);
        }
        mainDIV.appendChild(c);
    });

    // affichage de pile
    let cp = state.pile[state.pile.length - 1];
    let pileDIV = document.getElementById('pile-card');
    pileDIV.textContent = cp.valeur + (cp.couleur ? ' ' + cp.couleur : '');
    pileDIV.className = 'card' + (cp.valeur === 'Joker' || cp.valeur === '+4' ? ' joker' : '');
    pileDIV.style.background = couleurTOCSS(cp.couleur, cp.valeur);

    // Bouton uno
    
    document.getElementById('uno-button').disabled = !(state.joueur.length === 2 && state.tour === 'joueur') && !state.uno;

    document.getElementById('message').textContent || '';
}

function couleurTOCSS(couleur, valeur) {
    if (valeur === 'Joker' || valeur === '+4') {
        return '#222';
    }
    switch (couleur) {
        case 'Rouge':
            return 'red';
        case 'Bleu':
            return 'blue';
        case 'Vert':
            return 'green';
        case 'Jaune':
            return 'yellow';
        default:
            return '';
    }
}

// gestion des boutons
document.getElementById('draw-button').onclick = () => {
    socket.emit('piocher');
}
document.getElementById('restart-button').onclick = () => {
    socket.emit('nouvelle partie');
}

document.getElementById('draw-card').onclick = () => {
    socket.emit('piocher');
};

document.getElementById('play-card').onclick = () => {
    // Ajoutez la logique pour jouer une carte si nécessaire
    console.log('Jouer une carte (à implémenter)');
};

document.getElementById('end-turn').onclick = () => {
    // Ajoutez la logique pour terminer le tour si nécessaire
    console.log('Terminer le tour (à implémenter)');
};

// Reception des mises à jour du serveur
socket.on('maj', renderGame);

// Demmarage de la partie
socket.emit('initialiser');
