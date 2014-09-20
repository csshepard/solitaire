import os
from copy import deepcopy
from deck import *


class CardPile(object):
    def __init__(self, deck=None, amount=0):
        #Creates a pile of cards which is divided into face up and face down sections
        #Initially all but one card is face down
        #If deck is None, creates an empty pile, else deals from deck
        #Amount determines number of cards to deal, 0 deals all cards from deck

        self.pile = []    # List of cards
        self.flip = -1    # Index where cards flip from face down to face up
        if deck is not None:
            if amount == 0:
                amount = len(deck)
            self.flip = amount - 1
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
        self.pile2 = CardPile(deck, 2)
        self.pile3 = CardPile(deck, 3)
        self.pile4 = CardPile(deck, 4)
        self.pile5 = CardPile(deck, 5)
        self.pile6 = CardPile(deck, 6)
        self.pile7 = CardPile(deck, 7)
        self.home1 = CardPile()           # Foundation Piles
        self.home2 = CardPile()
        self.home3 = CardPile()
        self.home4 = CardPile()
        self.discard = CardPile(deck)     # Combination of Deck and Waste Piles
        self.discard.flip += 1            # Flip the face up card on the waste back down
    
    def deal3(self):
        if self.discard.flip == 0:        # All cards have been dealt
            self.discard.flip = len(self.discard)
        else:
            self.discard.flip -= 3       #Deal, at most, 3 cards
            if self.discard.flip < 0:
                self.discard.flip = 0

    def movepile(self, source_pile, dest_pile, card_amount):
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if card_amount < 1:              #Move all face up cards
            card_amount = len(source_pile[source_pile.flip:])
        elif card_amount > len(source_pile[source_pile.flip:]):
            return False
        if source_pile is self.discard:
            source_card = source_pile[source_pile.flip]
        else:
            source_card = source_pile[-card_amount]
        if len(dest_pile.pile) > 0:
            dest_card = dest_pile[-1]
            if source_card.value == dest_card.value - 1:
                if dest_card.suit in cross_color[source_card.suit]:
                    if source_pile is self.discard:
                        dest_pile.pile.append(source_pile[source_pile.flip])
                        del source_pile.pile[source_pile.flip]
                    else:
                        dest_pile.pile.extend(source_pile[-card_amount:])
                        del source_pile.pile[-card_amount:]
                    return True
        elif source_card.value == 13:
            if source_pile is self.discard:
                dest_pile.pile.append(source_pile[source_pile.flip])
                del source_pile.pile[source_pile.flip]
            else:
                dest_pile.pile.extend(source_pile[-card_amount:])
                del source_pile.pile[-card_amount:]
            return True
        return False

    def movehome(self, source_pile, dest_pile):
        source_index = -1
        if source_pile is self.discard:
            source_index = source_pile.flip
        if len(dest_pile) > 0:
            if source_pile[source_index].value == dest_pile[-1].value + 1 and \
               source_pile[source_index].suit == dest_pile[-1].suit:
                dest_pile.pile.append(source_pile.pile.pop(source_index))
                return True
        elif source_pile[source_index].value == 1:
            dest_pile.pile.append(source_pile.pile.pop(source_index))
            return True
        return False

    def checkwin(self):
        if len(self.home1) == 13 and len(self.home2) == 13 and len(self.home3) == 13 and len(self.home4) == 13:
            return True

    def printboard2(self):
        if self.discard.flip > 0:
            print('*** ', end=' ')
        else:
            print('--- ', end=' ')
        if self.discard.flip < len(self.discard):
            print(self.discard.pile[self.discard.flip], end=' ')
        else:
            print('--- ', end=' ')
        print('    ', end=' ')
        if len(self.home1.pile):
            print(self.home1.pile[-1], end=' ')
        else:
            print('--- ', end=' ')
        if len(self.home2.pile):
            print(self.home2.pile[-1], end=' ')
        else:
            print('--- ', end=' ')
        if len(self.home3.pile):
            print(self.home3.pile[-1], end=' ')
        else:
            print('--- ', end=' ')
        if len(self.home4.pile):
            print(self.home4.pile[-1])
        else:
            print('--- ')
        print('')
        for x in range(20):
            fall_through = 0
            if self.pile1.flip > x:
                print('*** ', end=' ')
            elif len(self.pile1) > x:
                print(self.pile1.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile2.flip > x:
                print('*** ', end=' ')
            elif len(self.pile2) > x:
                print(self.pile2.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile3.flip > x:
                print('*** ', end=' ')
            elif len(self.pile3) > x:
                print(self.pile3.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile4.flip > x:
                print('*** ', end=' ')
            elif len(self.pile4) > x:
                print(self.pile4.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile5.flip > x:
                print('*** ', end=' ')
            elif len(self.pile5) > x:
                print(self.pile5.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile6.flip > x:
                print('*** ', end=' ')
            elif len(self.pile6) > x:
                print(self.pile6.pile[x], end=' ')
            else:
                print('--- ', end=' ')
                fall_through += 1
            if self.pile7.flip > x:
                print('*** ')
            elif len(self.pile7) > x:
                print(self.pile7.pile[x])
            else:
                print('--- ')
                fall_through += 1
            if fall_through == 7:
                break

game = Solitare()
move_stack = []
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
while True:
    os.system('clear')
    game.printboard2()
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
                print('Moved')
                if source != '0':
                    input_dict[source].update()
            else:
                print('Invalid')
        else:
            if game.movehome(input_dict[source], input_dict[dest]):
                print('Moved')
                if source !='0':
                    input_dict[source].update()
            else:
                print('Invalid')
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