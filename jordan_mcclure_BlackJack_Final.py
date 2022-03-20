#Jordan McClure "BlackJack Final"
from datetime import datetime
import random
import db as database
import tkinter as tk
from tkinter import *
from tkinter import ttk
from objects import *
def title():
    print('BLACKJACK!')
    print('Blackjack payout is 3:2')



def banking(userMoney, bet, result):
        
    if result == "win":
        userMoney = userMoney + (bet * 1.5)
    elif result == "lose":
        userMoney = userMoney - bet
    userMoney = round(userMoney, 2)
    print("Money: ", round(userMoney, 2))
    database.writeMoney(userMoney)
    return userMoney


def hit(deck, hand):
    hand.addCard(deck.dealCard())
    hand.adjustAces()

def showStart(player, dealer):
    print("\nPlayer's Hand:", *player.cards)
    print("\nPlayer's Hand =", player.value)
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print("", dealer.cards[1])


def showAll(player, dealer):
    print("\nPlayer's Hand:", *player.cards)
    print("\nPlayer's Hand =", player.value)
    print("\nDealer's Hand:", *dealer.cards)
    print("\nDealer's Hand =", dealer.value)

def main():
    

    #Print start time
    now_start = datetime.now()
    start_time = now_start.strftime("%H:%M:%S")
    print("Start time: ", start_time)

    title()
    choice = 'y'
    bet = 0
    userMoney = 100.00
    while choice == 'y':
        result = ''
        userMoney = float(database.readMoney())
        print("Your money: ", userMoney)
        
        #Betting
        while True:
            try:
                bet = float(input("Place your bet: "))
                while bet < 5 or bet > 1000:
                    print("Please enter a valid bet between 5 and 1000.")
                    bet = float(input("Place your bet: "))
                    notvalid =bet < 5 or bet > 1000
                break
            except ValueError:
                print("Not a valid number. Try agian")

        deck = Deck()   # get shuffled deck
        deck.shuffleDeck()

        player = Hand() # player hand
        player.addCard(deck.dealCard())
        player.addCard(deck.dealCard())

        house = Hand() # house hand
        house.addCard(deck.dealCard())
        house.addCard(deck.dealCard())



        # print hands
        showStart(player, house)

        # while user requests an additional card, house deals it
        answer = input('Hit or stand? (default: hit): ')
        while answer in {'', 'h', 'hit'}:
            
            card = hit(deck, player)
            showStart(player, house)
            if player.value > 21:    # player total is > 21
                print('You went over, you lose.')
                result = 'lose'
                answer = 'stand'
                banking(userMoney, bet, result)
                break            
            answer = input('Hit or stand? (default: hit): ')

        if player.value <= 21:
        # house must play the "house rules"
            while house.value < 17:
           
                card = hit(deck, house)
                showAll(player, house)
                if house.value > 21:     # house total is > 21
                    print('House went over, you win.')
                    result = 'win'
                    banking(userMoney, bet, result)
                    break
        

                result = Hand.compareHands(house, player, userMoney, bet)
                banking(userMoney, bet, result)

            print("To play agian enter y, or anything else to exit.")
            choice = input("Play agian:").lower()


    #Print end time
    now_end = datetime.now()
    end_time = now_end.strftime("%H:%M:%S")
    play_time = now_end.replace(microsecond = 0) - now_start.replace(microsecond = 0)
    print("End time: ", end_time)
    print("Play time: ", play_time)

class BlackJackFrame(ttk.Frame):
    def __init__ (self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        self.usermoney = tk.StringVar()
        self.usermoney.set(database.readMoney())
        self.bet = tk.StringVar()
        self.house = tk.StringVar()
        self.housePoints = tk.StringVar()
        self.player = tk.StringVar()
        self.playerPoints = tk.StringVar()
        self.result = tk.StringVar()

        self.playerHand = Hand()
        self.houseHand = Hand()
        self.deck = Deck()

        self.initComponenents()

    def initComponenents(self):

        self.pack()
        ttk.Label(self, text="Money: ").grid(column=0, row=0, sticky=tk.E)
        ttk.Label(self, text="Bet: ").grid(column=0, row=1, sticky=tk.E)
        ttk.Label(self, text="DEALER").grid(column=0, row=2, sticky=tk.E)
        ttk.Label(self, text="Cards: ").grid(column=0, row=3, sticky=tk.E)
        ttk.Label(self, text="Points: ").grid(column=0, row=4, sticky=tk.E)
        ttk.Label(self, text="YOU").grid(column=0, row=5, sticky=tk.E)
        ttk.Label(self, text="Cards: ").grid(column=0, row=6, sticky=tk.E)
        ttk.Label(self, text="Points: ").grid(column=0, row=7, sticky=tk.E)
        ttk.Label(self, text="RESULTS: ").grid(column=0, row=9, sticky=tk.E)

        ttk.Entry(self, width=30, state='readonly', textvariable=self.usermoney).grid(column=1, row=0)
        ttk.Entry(self, width=30, textvariable=self.bet).grid(column=1, row=1)
        ttk.Entry(self, width=30, state='readonly', textvariable=self.house).grid(column=1, row=3)
        ttk.Entry(self, width=30, state='readonly', textvariable=self.housePoints).grid(column=1, row=4)
        ttk.Entry(self, width=30, state='readonly', textvariable=self.player).grid(column=1, row=6)
        ttk.Entry(self, width=30, state='readonly', textvariable=self.playerPoints).grid(column=1, row=7)
        ttk.Entry(self, width=30, state='readonly', textvariable=self.result).grid(column=1, row=9)

        self.makeButtons()
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def makeButtons(self):
        buttonFrameHit = ttk.Frame(self)
        buttonFrameAgain = ttk.Frame(self)

        buttonFrameHit.grid(column = 1, row=8, columnspan = 2, sticky=tk.E)
        buttonFrameAgain.grid(column = 1, row=10, columnspan = 2, sticky=tk.E)

        ttk.Button(buttonFrameHit, text="Hit", command=self.hit).grid(column=0, row=0, padx=5)
        ttk.Button(buttonFrameHit, text="Stand", command=self.stand).grid(column=1, row=0)

        playbutton = ttk.Button(buttonFrameAgain, text="Play", command=self.play).grid(column=0, row=0, padx=5)
        ttk.Button(buttonFrameAgain, text="Exit", command=exit).grid(column=1, row=0)

    def play(self):

        self.bet.set(5)
        if self.bet.get() == "":
            self.result.set("Must bet between 5 and 1000")
            self.bet.set(5)
        else:
            
            self.house.set("")
            self.player.set("")

            self.houseHand.addCard(self.deck.dealCard())
            self.houseHand.addCard(self.deck.dealCard())
            self.house.set((str(self.houseHand.cards[1].ranks)))

            self.playerHand.addCard(self.deck.dealCard())
            self.playerHand.addCard(self.deck.dealCard())
            self.player.set(str(self.playerHand.cards[0].ranks)+ " " +(str(self.playerHand.cards[1].ranks)))

            self.playerPoints.set(self.playerHand.value)

            

    def hit(self):
        bet = self.bet.get()
        usermoney = self.usermoney.get()

        self.playerHand.addCard(self.deck.dealCard())
        self.player.insert(str(self.playerHand.cards.ranks))

        if self.playerHand.value > 21:
            self.player.set("")
            self.result.set("You BUSTED! Dealer wins.")
            usermoney = usermoney - bet
            database.writeMoney(usermoney)
    def stand(self):

        bet = self.bet.get()
        usermoney = self.usermoney.get()
        self.housePoints.set(self.houseHand.value)

        while self.houseHand.value < 17:
            self.houseHand.addCard(self.deck.dealCard())
            self.house.set(str(self.houseHand.cards.ranks))
        if self.houseHand.value > self.playerHand.value:
            self.result.set("You lose")
            result = 'lose'
            usermoney = usermoney - bet
            database.writeMoney(usermoney)
        elif self.houseHand.value < self.playerHand.value:
            self.result.set("You win")
            result = 'win'
            usermoney = usermoney - bet
            database.writeMoney(usermoney)
        elif self.houseHand.value == 21 and 2 == len(self.houseHand.cards) < len(self.playerHand.cards):
            self.result.set("You lose")
            result = 'lose'
            usermoney = usermoney - bet
            database.writeMoney(usermoney)
        elif self.playerHand.value == 21 and 2 == len(self.playerHand.cards) < len(self.houseHand.cards):
            self.result.set("You win")
            result = 'win'
            usermoney = usermoney - bet
            database.writeMoney(usermoney)
        else:
            self.result.set("It's a tie")

    def exit():
        bet = self.bet.get()
        usermoney = self.usermoney.get()
        usermoney = usermoney - bet
        database.writeMoney(usermoney)
        r.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Black Jack Game")
    BlackJackFrame(root)
    root.mainloop()
