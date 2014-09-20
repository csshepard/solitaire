import os
from copy import deepcopy
from deck import *


class CardPile(object):
    def __init__(self, deck=None, amount=0):
        #Creates a pile of cards which is divided into face up and face down sections
        #Initially all cards are face down
        #If deck is None, creates an empty pile, else deals from deck
        #Amount determines number of cards to deal, <=0 deals all cards from deck

        self.pile = []    # List of cards
        self.flip = -1    # Index where cards flip from face down to face up
        if deck is not None:
            if len(deck) < amount or amount <= 0:
                amount = len(deck)
            self.flip = amount
            for x in range(amount):
                self.pile.append(deck.deal())

    def __len__(self):
        return len(self.pile)

    def __getitem__(self, item):
        return self.pile[item]

    def __repr__(self):
        return repr('A pile of {0} cards, {1} are face up'.format(len(self.pile), len(self.pile)-self.flip))

    def update(self):
        #Flips over top card if face down
        if self.flip > len(self.pile) - 1:
            self.flip -= 1


class Solitare(object):
    def __init__(self):
        deck = Deck()
        deck.shuffle()
        self.pile1 = CardPile(deck, 1)    # Tableau Piles
        self.pile1.update()
        self.pile2 = CardPile(deck, 2)
        self.pile2.update()
        self.pile3 = CardPile(deck, 3)
        self.pile3.update()
        self.pile4 = CardPile(deck, 4)
        self.pile4.update()
        self.pile5 = CardPile(deck, 5)
        self.pile5.update()
        self.pile6 = CardPile(deck, 6)
        self.pile6.update()
        self.pile7 = CardPile(deck, 7)
        self.pile7.update()
        self.home1 = CardPile()           # Foundation Piles
        self.home2 = CardPile()
        self.home3 = CardPile()
        self.home4 = CardPile()
        self.deck = CardPile(deck)     # Combination of Deck and Waste Piles

    def __str__(self):
        board = ''
        if self.deck.flip > 0:
            board = ''.join([board, '***  '])
        else:
            board = ''.join([board, '---  '])
        if self.deck.flip < len(self.deck):
            board = ''.join([board, str(self.deck.pile[self.deck.flip]), ' '])
        else:
            board = ''.join([board, '---  '])
        board = ''.join([board, '     '])
        if len(self.home1.pile):
            board = ''.join([board, str(self.home1.pile[-1]), ' '])
        else:
            board = ''.join([board, '---  '])
        if len(self.home2.pile):
            board = ''.join([board, str(self.home2.pile[-1]), ' '])
        else:
            board = ''.join([board, '---  '])
        if len(self.home3.pile):
            board = ''.join([board, str(self.home3.pile[-1]), ' '])
        else:
            board = ''.join([board, '---  '])
        if len(self.home4.pile):
            board = ''.join([board, str(self.home4.pile[-1]), '\n\n'])
        else:
            board = ''.join([board, '---\n\n'])
        for x in range(21):
            fall_through = 0
            if self.pile1.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile1) > x:
                board = ''.join([board, str(self.pile1[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile2.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile2) > x:
                board = ''.join([board, str(self.pile2[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile3.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile3) > x:
                board = ''.join([board, str(self.pile3[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile4.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile4) > x:
                board = ''.join([board, str(self.pile4[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile5.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile5) > x:
                board = ''.join([board, str(self.pile5[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile6.flip > x:
                board = ''.join([board, '***  '])
            elif len(self.pile6) > x:
                board = ''.join([board, str(self.pile6[x]), ' '])
            else:
                board = ''.join([board, '---  '])
                fall_through += 1
            if self.pile7.flip > x:
                board = ''.join([board, '***\n'])
            elif len(self.pile7) > x:
                board = ''.join([board, str(self.pile7[x]), '\n'])
            else:
                board = ''.join([board, '---\n'])
                fall_through += 1
            if fall_through == 7:
                return board

    def deal3(self):
        if self.deck.flip == 0:        # All cards have been dealt
            self.deck.flip = len(self.deck)
        else:
            self.deck.flip -= 3       # Deal, at most, 3 cards
            if self.deck.flip < 0:
                self.deck.flip = 0

    def movepile(self, source_pile, dest_pile, card_amount):
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if card_amount < 1:              # Move all face up cards
            card_amount = len(source_pile[source_pile.flip:])
        elif card_amount > len(source_pile[source_pile.flip:]):
            return False
        if source_pile is self.deck:  # Set top face up card
            source_card = source_pile[source_pile.flip]
        else:
            source_card = source_pile[-card_amount]  # Set deepest moving card
        if len(dest_pile.pile) > 0:    # Check for empty pile
            dest_card = dest_pile[-1]  # Set top card
            if source_card.value == dest_card.value - 1:    # check if pile can be moved
                if dest_card.suit in cross_color[source_card.suit]:
                    if source_pile is self.deck:  # if moving from deck, only move face up card
                        dest_pile.pile.append(source_pile.pop(source_pile.flip))
                    else:
                        dest_pile.pile.extend(source_pile[-card_amount:])
                        del source_pile.pile[-card_amount:]
                    return True
        elif source_card.value == 13:     # Source card is King and dest is empty
            if source_pile is self.deck:
                dest_pile.pile.append(source_pile.pop(source_pile.flip))
            else:
                dest_pile.pile.extend(source_pile[-card_amount:])
                del source_pile.pile[-card_amount:]
            return True
        return False

    def movehome(self, source_pile, dest_pile):
        source_index = -1             # Card is top on pile
        if source_pile is self.deck:
            source_index = source_pile.flip   # Card is face up card on deck
        if len(dest_pile) > 0:  # Foundation has cards
            if source_pile[source_index].value == dest_pile[-1].value + 1 and \
               source_pile[source_index].suit == dest_pile[-1].suit:
                dest_pile.pile.append(source_pile.pile.pop(source_index))
                return True
        elif source_pile[source_index].value == 1:  # Foundation is empty and card is Ace
            dest_pile.pile.append(source_pile.pile.pop(source_index))
            return True
        return False

    def checkwin(self):
        if len(self.home1) == 13 and len(self.home2) == 13 and \
           len(self.home3) == 13 and len(self.home4) == 13:
            return True

if __name__ == '__main__':
    game = Solitare()  # Create new game
    move_stack = []    # Create stack for undo
    input_dict = {'0': game.deck,
                  '1': game.pile1,
                  '2': game.pile2,
                  '3': game.pile3,
                  '4': game.pile4,
                  '5': game.pile5,
                  '6': game.pile6,
                  '7': game.pile7,
                  'H1': game.home1,
                  'H2': game.home2,
                  'H3': game.home3,
                  'H4': game.home4}
    while True:  # Main Loop
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
        print(game)
        selection = input('|1: Deal|2: Move Card|3: Undo|\n: ')
        if selection == '1' or selection == '':
            move_stack.append(deepcopy(game))
            game.deal3()
        elif selection == '2':
            move_stack.append(deepcopy(game))
            while True:
                source = input('Source Card\n|0: Available Card|1-7: Piles|H1-H4: Home Piles|\n: ')
                if source in input_dict:
                    break
            while True:
                dest = input('Destination Pile\n|1-7: Piles|H1-H4: Home Piles|\n: ')
                if dest != '0' and dest in input_dict:
                    break
            if dest < '8':
                index = 1
                if source != '0' and source < '8':
                    if not input_dict[source].flip == len(input_dict[source]) - 1:
                        while True:
                            index_str = input('How Many Cards to move: ')
                            if index_str == '':
                                index = 0
                                break
                            elif index_str.isnumeric():
                                index = int(index_str)
                                break
                if game.movepile(input_dict[source], input_dict[dest], index):
                    if source != '0':
                        input_dict[source].update()
            else:
                if game.movehome(input_dict[source], input_dict[dest]):
                    if source != '0':
                        input_dict[source].update()
        elif selection == '0':
            break
        elif selection == '3':
            if move_stack:
                game = move_stack.pop()
                input_dict = {'0': game.discard,
                              '1': game.pile1,
                              '2': game.pile2,
                              '3': game.pile3,
                              '4': game.pile4,
                              '5': game.pile5,
                              '6': game.pile6,
                              '7': game.pile7,
                              'H1': game.home1,
                              'H2': game.home2,
                              'H3': game.home3,
                              'H4': game.home4}
        if game.checkwin():
            print('YOU WIN!!!!')
            break