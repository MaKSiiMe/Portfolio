const db = require('./db');

function chargerCarte(callback) {
    db.query('SELECT * FROM cartes', (err, results) => {
        if (err) {
            console.error('Erreur lors du chargement des cartes:', err);
            callback([]); // Renvoie un tableau vide si erreur
            return;
        }
        callback(results);
    });
}

module.exports = {
    chargerCarte
};