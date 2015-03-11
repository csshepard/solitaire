import random
from card import Card


class Deck(object):
    def __init__(self, source=None, amount=0):
        # Creates a list of cards
        # if source is given, Deck is created from cards in source
        # if no source is given, a standard 52 card deck is created
        # amount is number of cards used when source is given
        self.deck = []
        if source is None:
            suits = ['Spade', 'Heart', 'Club', 'Diamond']
            for suit in suits:
                for value in range(1, 14):
                    self.deck.append(Card(value, suit))
        else:
            if len(source) < amount <= 0:        # ensure amount is valid
                raise ValueError('Invalid card amount')
            for num in range(amount):
                self.deck.append(source.deal())  # Cards removed from source

    def __repr__(self):
        deckstr = ''
        for acard in self.deck:
            deckstr = deckstr + acard + '\n'
        return repr(deckstr)

    def __str__(self):
        deckstr = ''
        for acard in self.deck:
            deckstr = deckstr + acard + '\n'
        return deckstr

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, item):
        return self.deck[item]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
