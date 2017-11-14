# dm
diamond mines 
A simple card game implemented in python.

GAME RULES
start with player 0, then 1, etc. min 2 max 6 players
end game when all decks are empty
On a player's turn, they may:

DRAW from center pile and place in their hand

DISCARD: toss card from their hand onto the center pile

DIAMOND DISCARD: draw from own deck if deck is not blocked (END TURN)
CLUB 
ACTION: Place on any deck to prevent drawing from that deck (END TURN)
DISCARD: Draw from own deck (END TURN)
HEART DISCARD: view top card of any deck that is not blocked, then draw from any deck that is not blocked (END TURN)
SPAD EDISCARD: Draw from any deck that is not blocked (END TURN)
END GAME: count diamonds in each hand to determine winner (blackjack style points)

TO DO:
Test all actions
Add a runtime loop for player actions (while len(DECKS) > 0...)
Win and end conditions
