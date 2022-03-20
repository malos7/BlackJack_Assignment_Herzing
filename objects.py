import random


suits = {'Hearts', 'Diamonds', 'Spades', 'Clubs'}
ranks = {'2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace'}
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
        '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def addCard(self, card):
        self.cards.append(card)
        self.value += values[card.ranks]
        if card.ranks == 'Ace':
            self.aces += 1

    def adjustAces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces  -= 1
    
    def compareHands(house, player, userMoney, bet):

        houseTotal, playerTotal = house.value, player.value
        print("Your have ", playerTotal, " points.")
        print("House has ", houseTotal, " points.")
        if houseTotal > playerTotal:
            print('You lose.')
            result = 'lose'
        elif houseTotal < playerTotal:
            print('You win.')
            result = 'win'
        elif houseTotal == 21 and 2 == len(house) < len(player):
            print('You lose.')
            result = 'lose'
        elif playerTotal == 21 and 2 == len(player) < len(house):
            print('You win.')
            result = 'win'
        else:
            print('A tie.')   
    
        return result


import sqlite3

class Deck:
    def __init__(self):

        self.deck = []     
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+Card.__str__()
        return "the deck has: " + deck_comp
    
    def shuffleDeck(self):
        random.shuffle(self.deck)

    def dealCard(self):
        card = self.deck.pop()
        return card

class Card:
    def __init__ (self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def __str__ (self):
        return self.ranks + " of " + self.suits

