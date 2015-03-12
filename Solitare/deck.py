import random
from card import Card
import nose.tools as nose


class Deck(object):
    def __init__(self):
        # Creates a deck of cards with all 52 standard cards

        self.deck = []
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        for suit in suits:
            for value in range(1, 14):
                self.deck.append(Card(value, suit))

    def __repr__(self):
        deckstr = ''
        for acard in self.deck:
            deckstr = deckstr + repr(acard) + '\n'
        return repr(deckstr)

    def __str__(self):
        deckstr = ''
        for acard in self.deck:
            deckstr = deckstr + str(acard) + '\n'
        return deckstr

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, item):
        return self.deck[item]

    def add_card(self, card):
        self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


# Tests
def test_full_deck_creation():
    deck = Deck()
    full_deck = Deck()
    full_deck.deck = [Card(value, suit) for suit in
                      ['Spade', 'Heart', 'Club', 'Diamond']
                      for value in range(1, 14)]
    nose.assert_equal(deck.deck, full_deck.deck)

def test_deck_shuffle():
    deck = Deck()
    deck_str = str(deck)
    shuffled = str(deck)
    nose.assert_equal(deck_str, shuffled)
    for x in range(10):
        deck.shuffle()
        shuffled = str(deck)
        nose.assert_not_equal(deck_str, shuffled)
        deck_str = shuffled

def test_deck_deal():
    deck = Deck()
    nose.assert_equal(Card(13, 'Diamond'), deck.deal())
    nose.assert_not_equal(Card(13, 'Diamond'), deck.deal())
    nose.assert_equal(Card(11, 'Diamond'), deck.deal())