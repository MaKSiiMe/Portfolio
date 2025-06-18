const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { chargerCarte } = require('./carte'); // Assurez-vous que le chemin est correct

chargerCarte((cartes) => {
    console.log('Cartes chargées depuis la base de donné db :', cartes);
});

const app = express();
const server = http.createServer(app);
const io = new Server(server);

let gameState = {
    iaCount: 5,
    ia: new Array(5).fill({}),
    joueur: [
        { couleur: 'Rouge', valeur: '5' },
        { couleur: 'Bleu', valeur: '+2' },
        { couleur: 'Vert', valeur: '3' },
    ],
    pile: [{ couleur: 'Jaune', valeur: '7' }],
    tour: 'joueur',
    uno: false,
};

app.use(express.static(__dirname));

io.on('connection', (socket) => {
    console.log('Un joueur connecté');
    socket.emit('maj', gameState);

    socket.on('jouerCarte', (index) => {
        // Logique pour jouer une carte
        console.log(`Carte jouée à l'index: ${index}`);
    });

    socket.on('piocher', () => {
        console.log('Carte piochée');
    });

    socket.on('nouvelle partie', () => {
        console.log('Nouvelle partie');
    });

    socket.on('initialiser', () => {
        socket.emit('maj', gameState);
    });
});

server.listen(3000, () => {
    console.log('Serveur démarré sur http://localhost:3000');
});