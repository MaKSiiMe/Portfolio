# Règles de Combat Pokémon TCG Pocket

Ce document décrit les principes fondamentaux du jeu et des combats dans Pokémon TCG Pocket.

---

## Table des Matières
1. [À propos des Decks](#à-propos-des-decks)
2. [Zones de Combat](#zones-de-combat)
3. [Préparation d'un Combat](#préparation-dun-combat)
4. [Déroulement d'un Tour](#déroulement-dun-tour)
5. [Mettre un Pokémon K.O. et Issue d'un Combat](#mettre-un-pokémon-ko-et-issue-dun-combat)
6. [Contrôle Pokémon et États Spéciaux](#contrôle-pokémon-et-états-spéciaux)
7. [Nombre Maximum de Tours et Temps Imparti](#nombre-maximum-de-tours-et-temps-imparti)
8. [Tableau des Règles et Fonctions](#tableau-des-règles-et-fonctions)

---

## À propos des Decks

### Règles de Construction
- Le deck doit contenir **20 cartes**.
- Il doit inclure **au moins un Pokémon de base**.
- Il ne doit pas contenir **plus de deux cartes du même nom**.

### Sélection des Énergies
- Choisissez **jusqu'à trois types d'Énergies** pour un deck.
- Ces Énergies seront **générées pendant les combats**.

---

## Zones de Combat

- **Deck** : Cartes posées face cachée.
- **Poste Actif** : Zone où les Pokémon utilisent leurs attaques.
- **Banc** : Trois emplacements pour les Pokémon de Banc.
- **Pile de défausse** : Cartes défaussées visibles par les deux joueurs.
- **Main** : Cartes utilisables durant le combat (limite de 10 cartes).

---

## Préparation d'un Combat

1. Une pièce est lancée pour déterminer qui commence.
2. Les cartes sont piochées automatiquement.
3. Les joueurs placent un Pokémon de base sur le Poste Actif et éventuellement sur le Banc.
4. Les joueurs touchent « Commencer » pour démarrer le combat.

---

## Déroulement d'un Tour

### Début du Tour
- Piochez une carte.
- De l'Énergie est générée (sauf au premier tour du joueur qui commence).

### Actions Possibles
- **Placer un Pokémon sur le Banc** : Tant qu'il y a des emplacements vides.
- **Attacher de l'Énergie** : À un Pokémon Actif ou de Banc.
- **Jouer des cartes Dresseur** : Une seule carte Supporter par tour.
- **Faire évoluer un Pokémon** : Impossible au premier tour ou si le Pokémon vient d'être mis en jeu.
- **Utiliser les talents des Pokémon** : Certains talents nécessitent des conditions spécifiques.
- **Battre en retraite** : Défaussez une Énergie par symbole d'Énergie Incolore dans le coût de retraite.
- **Utiliser une attaque** : Terminez votre tour après l'attaque.

---

## Mettre un Pokémon K.O. et Issue d'un Combat

### Mettre un Pokémon K.O.
- Gagnez **1 point** (ou plus pour certains Pokémon spéciaux).
- Défaussez le Pokémon K.O. et ses cartes attachées.
- Remplacez le Pokémon Actif par un Pokémon de Banc.

### Issue d'un Combat
- Un joueur gagne s'il atteint le nombre de points requis.
- Un joueur perd s'il n'a plus de Pokémon en jeu.
- Déclarer forfait entraîne une défaite.

---

## Contrôle Pokémon et États Spéciaux

### Contrôle Pokémon
- Se produit après chaque tour.
- Applique les effets des talents et des cartes Dresseur.
- Les Pokémon sans PV restants sont mis K.O.

### États Spéciaux
- **Empoisonné** : 10 dégâts par Contrôle Pokémon.
- **Brûlé** : 20 dégâts par Contrôle Pokémon (lancez une pièce pour guérir).
- **Endormi / Paralysé** : Empêche d'attaquer ou de battre en retraite.
- **Confus** : Lancer une pièce pour attaquer (pile = échec).

### Guérir des États Spéciaux
- Placez le Pokémon sur le Banc.
- Faites évoluer le Pokémon.
- Utilisez une carte ou un talent spécifique.

---

## Nombre Maximum de Tours et Temps Imparti

- **Nombre de tours** : Limité, entraîne une égalité si atteint.
- **Temps imparti** :
  - Chaque joueur dispose d'un temps total pour le combat.
  - Chaque tour est limité en temps.
  - Une décision aléatoire est prise si le temps est écoulé.

---

## Tableau des Règles et Fonctions

Ce tableau associe chaque règle du jeu à une fonction Python correspondante dans le moteur de jeu.

| **Règle**                                                                 | **Fonction Python**  |
|---------------------------------------------------------------------------|----------------------|
| Le deck doit contenir **20 cartes**.                                      |                      |
| Le deck doit inclure **au moins un Pokémon de base**.                     |                      |
| Le deck ne doit pas contenir **plus de deux cartes du même nom**.         |                      |
| Choisissez **jusqu'à trois types d'Énergies** pour un deck.               |                      |
| Les Énergies seront **générées pendant les combats**.                     |                      |
| **Deck** : Cartes posées face cachée.                                     |                      |
| **Poste Actif** : Zone où les Pokémon utilisent leurs attaques.           |                      |
| **Banc** : Trois emplacements pour les Pokémon de Banc.                   |                      |
| **Pile de défausse** : Cartes défaussées visibles par les deux joueurs.   |                      |
| **Main** : Cartes utilisables durant le combat (limite de 10 cartes).     |                      |
| Une pièce est lancée pour déterminer qui commence.                        |                      |
| Les cartes sont piochées automatiquement.                                 |                      |
| Les joueurs placent un Pokémon de base sur le Poste Actif.                |                      |
| Les joueurs peuvent placer des Pokémon sur le Banc.                       |                      |
| Piochez une carte au début de chaque tour.                                |                      |
| De l'Énergie est générée (sauf au premier tour du joueur qui commence).   |                      |
| Placer un Pokémon sur le Banc tant qu'il y a des emplacements vides.      |                      |
| Attacher de l'Énergie à un Pokémon Actif ou de Banc.                      |                      |
| Jouer une seule carte Supporter par tour.                                 |                      |
| Faire évoluer un Pokémon (impossible au premier tour ou si mis en jeu).   |                      |
| Utiliser les talents des Pokémon (sous conditions spécifiques).           |                      |
| Battre en retraite en défaussant une Énergie par symbole Incolore.        |                      |
| Utiliser une attaque et terminer le tour.                                 |                      |
| Gagnez **1 point** (ou plus pour certains Pokémon spéciaux) en K.O.       |                      |
| Défaussez le Pokémon K.O. et ses cartes attachées.                        |                      |
| Remplacez le Pokémon Actif par un Pokémon de Banc.                        |                      |
| Un joueur gagne s'il atteint le nombre de points requis.                  |                      |
| Un joueur perd s'il n'a plus de Pokémon en jeu.                           |                      |
| Déclarer forfait entraîne une défaite.                                    |                      |
| Contrôle Pokémon après chaque tour.                                       |                      |
| Les Pokémon sans PV restants sont mis K.O.                                |                      |
| **Empoisonné** : 10 dégâts par Contrôle Pokémon.                          |                      |
| **Brûlé** : 20 dégâts par Contrôle Pokémon (lancez une pièce pour guérir).|                      |
| **Endormi / Paralysé** : Empêche d'attaquer ou de battre en retraite.     |                      |
| **Confus** : Lancer une pièce pour attaquer (pile = échec).               |                      |
| Placez le Pokémon sur le Banc pour guérir des États Spéciaux.             |                      |
| Faites évoluer le Pokémon pour guérir des États Spéciaux.                 |                      |
| Utilisez une carte ou un talent spécifique pour guérir des États Spéciaux.|                      |
| Nombre de tours limité, entraîne une égalité si atteint.                  |                      |
| Chaque joueur dispose d'un temps total pour le combat.                    |                      |
| Chaque tour est limité en temps.                                          |                      |
| Une décision aléatoire est prise si le temps est écoulé.                  |                      |
