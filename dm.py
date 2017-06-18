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
Should you be allowed to block an empty deck with a club?
possible stuck if player plays a heart and all decks are blocked
bug: play spade after trying to play a heart when both decks are blocked allows you to look at a deck as well. basically turns aren't ending properly
restructure the turn system
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
  
def action_draw_onecard(player, deck):
  if not cannot_draw_from_deck(deck):
    HANDS[player].append(DECKS[deck].pop())
    return 0
  return 1
    
def action_discard_diamond(player, card):
  deck = player 
  if not cannot_draw_from_deck(deck):
    HANDS[player].remove(card)
    add_to_center(card) #add the card to the center
    action_draw_onecard(player, deck)
    return 0
  return 1
  
#when a club is discarded the player chooses the deck to place it on top of.
#if the deck# is already being blocked, then move both cards to centerpile.
#if the deck# is not being blocked, update blocks[] with the new card and deck info. 
def action_discard_club(player, card, deck):
  if deck in BLOCKS:
    remove_block(deck) 
    add_to_center(card)
  else:
    add_block(card, deck)
  HANDS[player].remove(card)
  return 0

    
#if the chosen deck is not currently being blocked then discard heart to center pile and reveal the top card of that deck.
#then, allow the player to choose card from any unblocked deck (but not center pile)

def action_discard_heart(player, card, deck):
  if not cannot_draw_from_deck(deck):
    HANDS[player].remove(card)
    add_to_center(card)
    return DECKS[deck][len(DECKS[deck])-1] #consider returning the print statement 
  return 1

#if the deck is not currently blocked then discard spade to center pile and draw from that deck
def action_discard_spade(player, card, deck):
  if not cannot_draw_from_deck(deck):
    HANDS[player].remove(card)
    add_to_center(card)
    action_draw_onecard(player, deck)
    return 0
  return 1

#check if deck is blocked or empty
def cannot_draw_from_deck(deck):
  if type(deck) != type(1):
    if show_output:
      print "Deck is not an integer"
    return 1
  if deck > nplayers-1:
    if show_output:
      print "Invalid deck selection"
    return 1
  if deck in BLOCKS:
    if show_output:
      print "INVALID MOVE: You cannot draw from a blocked deck"
    return 1
  if len(DECKS[deck]) < 1:
    if show_output:
      print "INVALID MOVE: You cannot draw from an empty deck"
    return 1
  return 0
  
#return 0 if you can draw from a deck
#return 1 if there are no available decks to draw from
def cannot_draw_from_any_deck():
  for i in range(len(DECKS)):
    if not cannot_draw_from_deck(i):
      print "You can draw from deck ", i
      return 0
  print "You cannot draw from any deck"
  return 1
    

#if the centerpile is not empty then take the top card of the center pile and add it to the player's hand
def action_draw_from_center(player):
  if len(CENTER) > 0:
    HANDS[player].append(CENTER.pop())
    return 0
  else:
    if show_output:
      print "You cannot draw from an empty center pile"
  return 1

def action_player_discard(player, card):
  suit = card[1] 
  print "Attempting to discard suit: ", suit
  
  #DISCARD DIAMOND
  if suit == 'd':
    return action_discard_diamond(player,card)
  
  #DISCARD CLUB
  elif suit == 'c':
    if show_output:
      print "which deck would you like to block or unblock? "
    deck = int(raw_input())
    return action_discard_club(player, card,deck)
    
  #DISCARD HEART  
  elif suit == 'h':
    if cannot_draw_from_any_deck():
      if show_output:
        print "All decks are blocked or empty so you cannot play a heart"
      return 1
    if show_output:
      print "which deck would you like to look at? "
    deck = int(raw_input())
    peek_at_card = action_discard_heart(player,card,deck)
    if peek_at_card != 1:
      if show_output:
        print "You see a ",peek_at_card
      player_draw_card = 0 #force player to draw a card from a deck at this point
      while not player_draw_card:
        if show_output:
          print "which deck would you like to take from? "
        deck = int(raw_input())
        if not action_draw_onecard(player, deck):
          player_draw_card = 1
          return 0
    else:
      if show_output:
        print "Action failed (This deck might be blocked)"
      return 1
  #DISCARD SPADE
  elif suit == 's':
    if show_output:
      print "which deck would you like to take from? "
    deck = int(raw_input())
    return action_discard_spade(player, card, deck)
  else:
    return 1
    
def add_to_center(card):
  if len(card) == 2:
    print "Putting ", card, " in center pile"
    CENTER.append(card)
  else:
    print "CARD ERROR"
  
  
#update blocked deck array 
def add_block(card, decknumber):
  BLOCKS.append(card)
  BLOCKS.append(decknumber)

def remove_block(deck):
  if deck in BLOCKS:
    i = BLOCKS.index(deck) #store the index of the card in the block list
    add_to_center(BLOCKS[i-1])
    BLOCKS.remove(deck) #get rid of the card
    
  
def output_information(player):
  string = ''
  print "****************************************"
  print "Player #", player, "'s turn with cards: "
  if len(HANDS[player]) > 0:
      print HANDS[player]
  else:
    string += "no cards in hand"
  if len(CENTER) > 0:
    string += "Center card ("+str(len(CENTER))+"): "+ str(CENTER[len(CENTER)-1])
  for i in range(len(BLOCKS)):
    if type(BLOCKS[i]) == type(1):
      print "Deck ",BLOCKS[i]," is blocked by ",BLOCKS[i-1]
  print string
  
def evaluate_input(player, action):
  #DRAW FROM CENTER
  if action == 'd':
    return action_draw_from_center(player)
  #PASS TURN
  elif action == 'p':
    return 0
  #DISCARD (card)
  elif action in HANDS[player]:
    return action_player_discard(player, action)
  else:
    if show_output: 
      print "Did not understand that action"
    return 1
  
  
  
def get_input(player):
  if show_output:
    print "(d)raw card from center, type the card to discard, or (p)ass"
  action = raw_input()
  if evaluate_input(player, action):
    get_input(player) #turn is not over
  else:
    return 0
    
def add_up_scores():
  scores = []
  for i in range(len(HANDS)):
    scores.append(0)
    for j in range(len(HANDS[i])):
      if HANDS[i][j][1] == 'd':
        rank = HANDS[i][j][0]
        value = 0
        if rank == 'J' or rank == 'Q' or rank == 'K':
          value = 10
        elif rank == 'A':
          value = 11
        else:
          value = int(rank)
        scores[i] += value
  return scores
        
show_output = 1
nplayers = 2
DECKS = deal_decks(nplayers)
HANDS = draw_starting_hand(nplayers, DECKS)
CENTER = []
#BLOCKS = ['0h',0,'0h',1] #[card, deck#, card, deck#, ...]
BLOCKS = []
#print HANDS[0]
#print CENTER
#print action_discard_diamond(0, '2d')
#print HANDS[0]
#print CENTER8s

playerturn = 0
emptyDeckCounter = 0

while emptyDeckCounter < nplayers-1:
  #output information
  #get player input
  #evaluate player input based on current status
  #next player
  
  output_information(playerturn)
  if(get_input(playerturn)==0): #next turn 
    if show_output:
      print "________________________________________"
    if playerturn < nplayers-1:
      playerturn += 1
    else:
      playerturn = 0
    
  #check endgame condition
  emptyDeckCounter = 0
  for i in range(len(DECKS)):
    if len(DECKS[i]) == 0:
      emptyDeckCounter+=1
      
print "game over, scores:"
print add_up_scores()
    
#print test
#pdb.set_trace()
  
    
    
  

