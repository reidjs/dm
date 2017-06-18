#!/usr/bin/env python
'''
GAME RULES
start with player 0, then 1, etc. min 2 max 6 players
end game when all decks are empty

On a player's turn, they may:

DRAW from center pile and place in their hand
DISCARD: toss card from their hand onto the center pile

DIAMOND
DISCARD: draw from own deck if deck is not blocked (END TURN)

CLUB
ACTION: Place on any deck to prevent drawing from that deck (END TURN)
DISCARD: Draw from own deck (END TURN)

HEART
DISCARD: view top card of any deck that is not blocked, then draw from any deck that is not blocked (END TURN)

SPADE
DISCARD: Draw from any deck that is not blocked (END TURN)

END GAME: count diamonds in each hand to determine winner (blackjack style points)

TO DO:
Test all actions
Add a runtime loop for player actions (while len(DECKS) > 0...)
Win and end conditions

'''
import random
import itertools
import pdb
SUITS = 'cdhs'
RANKS = '23456789TJQKA'
DECK = tuple(''.join(card) for card in itertools.product(RANKS, SUITS))
#hand = random.sample(DECK, 5)
#print hand

#n is number of players between 2 and 6
#structure is [[player 1 bottom card, next card,..., top card], [p2 deck], [p3 deck]...]
def deal_decks(n):
  if n < 2 or n > 6:
    return 0
  entireDeck = random.sample(DECK, 52); #shuffle the deck
  decks = []
  for i in range(n):
    decks.append([])
  for i in range(51):
    decks[i%n].append(entireDeck.pop())
  return decks
  
#draw n cards from array d
def draw(n, d):
  x = []
  for i in range(n):
    if len(d) > 0:
      x.append(d.pop())
  return x

#n is number of players, d is all player decks
#returns [[player 1 hand], [player 2 hand], etc]
def draw_starting_hand(n, d):
  hands = []
  for i in range(n):
    hands.append([])
    hands[i] = draw(5, d[i])
  return hands
  

#if player's deck is not being blocked, discard the diamond and draw one card from top of deck
def action_discard_diamond(player, card):
  if player in BLOCKS:
    return "Your deck is currently blocked so you may not draw from it by discarding a diamond"
  else:
    CENTER.append(card) #add the card to the center
    HANDS[player].append(DECKS[player].pop()) #pop card off top of player's deck and put in hand
    return 0
  
#when a club is discarded the player chooses the deck to place it on top of.
#if the deck# is already being blocked, then move both cards to centerpile.
#if the deck# is not being blocked, update blocks[] with the new card and deck info. 
def action_discard_club(card, deck):
  if deck in BLOCKS:
    remove_block(deck) #this automatically places that card in the center pile
    CENTER.append(card)
  else:
    add_block(card, deck)
  return 0

    
#if the chosen deck is not currently being blocked then discard heart to center pile and reveal the top card of that deck.
#then, allow the player to choose card from any unblocked deck (but not center pile)
def action_discard_heart(card, deck):
  if deck in BLOCKS:
    return "You cannot look at a blocked deck"
  else:
    CENTER.append(card)
    print(deck[len(deck)-1])
    return 0 #Notice in this case the player's turn should not end. 

#if the deck is not currently blocked then discard spade to center pile and draw from that deck
def action_discard_spade(player, deck):
  if deck in BLOCKS:
    return "You cannot draw from a blocked deck"
  else:
    CENTER.append(card)
    HANDS[player].append(DECKS[deck].pop())
    return 0

#if the centerpile is not empty then take the top card of the center pile and add it to the player's hand
def action_draw_from_center(player):
  if len(CENTER) > 0:
    HANDS[player.append(CENTER.pop())]
    return 0
  else:
    return "You cannot draw from an empty center pile"


#update blocked deck array 
def add_block(card, decknumber):
  BLOCKS.append(card)
  BLOCKS.append(decknumber)

def remove_block(deck):
  if deck in BLOCKS:
    i = BLOCKS.index(deck) #store the index of the card in the block list
    BLOCKS.remove(deck) #get rid of the card
    CENTER.append(BLOCKS.pop(i-1)) #get rid of the deck storage info and add to top of center pile        

def get_input(player):
  if show_output:
    print "Player #", player, "'s turn with cards: "
    print HANDS[player]
    print "Center card: ", CENTER[len(CENTER)-1]
  action = input('(d)raw card from center or type card to discard')
  #if action == 'd' and action_draw_from_center(player):
    #action = input('(d)raw card from center or type card to discard')
    
    


show_output = 1
nplayers = 4
DECKS = deal_decks(nplayers)
HANDS = draw_starting_hand(nplayers, DECKS)
CENTER = []
BLOCKS = [] #[card, deck#, card, deck#, ...]

print HANDS[0]
print CENTER
print action_discard_diamond(0, '2d')
print HANDS[0]
print CENTER

playerturn = 0
while len(DECKS) > 0:
  get_input(playerturn)
  
  if playerturn < nplayers:
    playerturn += 1
  else:
    playerturn = 0
  DECKS.remove([]) #remove any empty decks
      
    
print test
#pdb.set_trace()
  
    
    
  

