"""Playing Cards is used to make representations of playing cards and
playing card decks
Examples:
    Card(5, 'Diamond') : Creates the 5 of Diamonds
    Card(11, 'Heart') : Creates the Jack of Hearts
    Deck() : Creates a deck of cards containing all 52 standard cards
"""

import random
import nose.tools as nose


class Card(object):
    """A Card is a representation of a playing card from a standard deck

    Attributes:
        value (int): a number from 1 to 13 that represents the value of
            card. 1 is Ace, 11 is Jack, 12 is Queen, and 13 is King
        suit (str): a string representing the suit of the card.  It is
            always capitalized and the singular variation
    """
    def __init__(self, value=1, suit='Spade'):
        """Creates a card object that has a numeric value and a string suit

        Attributes:
            value (int, optional): A number from 1 to 14, defaults to 1.
            suit (str, optional): One of the following strings:
                'Spade', 'Heart', 'Club', or 'Diamond', defaults to 'Spade'
        """

        if 0 < value < 14:
            self.value = value
        else:
            raise ValueError('{} not a valid card value'.format(value))
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        if suit in suits or (suit.endswith('s') and suit[:-1] in suits):
            self.suit = suit
        else:
            raise ValueError('{} not a valid card suit'.format(suit))

    def __repr__(self):
        return repr('Value = {0}, Suit = {1}'.format(self.value, self.suit))

    def __str__(self):
        if self.suit == 'Heart' or self.suit == 'Diamond':
            suit = '\033[47;31m'
        else:
            suit = '\033[47;30m'
        values = {1: 'A',
                  2: '2',
                  3: '3',
                  4: '4',
                  5: '5',
                  6: '6',
                  7: '7',
                  8: '8',
                  9: '9',
                  10: 'T',
                  11: 'J',
                  12: 'Q',
                  13: 'K'}
        return suit + '{0} {1}\033[0m'.format(values[self.value], self.suit[0])
        

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value


class Deck(object):
    """A Deck is a list of cards.  A deck can be shuffled, dealt from,
    or have cards added to it.
    """
    def __init__(self, cards=None):
        """Creates a deck of cards.  If cards is None, all 52 cards are
        created.  If cards is supplied, deck is constructed from cards
        Args:
            cards (optional, list of Cards): a list of cards to construct
                a deck from, default is None

        Attributes:
            deck (list of Cards): the list of cards in the deck

        Public Methods:
            add_card(*args): adds cards to end of deck
            shuffle(): randomly arrange cards in deck
            deal(): removes and returns end card in deck
        """
        if cards is None:
            self.deck = []
            suits = ['Spade', 'Heart', 'Club', 'Diamond']
            for suit in suits:
                for value in range(1, 14):
                    self.deck.append(Card(value, suit))
        elif all([card is type(Card) for card in cards]):
            self.deck = cards
        else:
            raise TypeError("List contains non card items")

    def __repr__(self):
        deck_str = ''
        for card in self.deck:
            deck_str += repr(card) + '\n'
        return repr(deck_str)

    def __str__(self):
        deck_str = ''
        for card in self.deck:
            deck_str += str(card) + '\n'
        return deck_str

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, item):
        return self.deck[item]

    def add_card(self, *args):
        """Used to add cards to the deck
        Args:
            args (cards): comma separated cards.
                TypeError is raised in non cards are passed
        """
        for card in args:
            if card is type(Card):
                self.deck.append(card)
            else:
                raise TypeError('{} is not a valid card'.format(card))

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.deck)

    def deal(self):
        """Removes the last card from the deck and returns it"""
        return self.deck.pop()


# Tests
def test_default_card_creation():
    """Tests if card constructor with no arguments creates the Ace of Spades"""
    test_card = Card()
    ace_spades = Card(1, 'Spade')
    nose.assert_equal(test_card, ace_spades)


def test_card_repr_all_52():
    """Tests creation of all 52 cards"""
    spades = [Card(x, 'Spade') for x in range(1, 14)]
    hearts = [Card(x, 'Heart') for x in range(1, 14)]
    clubs = [Card(x, 'Club') for x in range(1, 14)]
    diamonds = [Card(x, 'Diamond') for x in range(1, 14)]
    spades_repr = [repr('Value = 1, Suit = Spade'),
                   repr('Value = 2, Suit = Spade'),
                   repr('Value = 3, Suit = Spade'),
                   repr('Value = 4, Suit = Spade'),
                   repr('Value = 5, Suit = Spade'),
                   repr('Value = 6, Suit = Spade'),
                   repr('Value = 7, Suit = Spade'),
                   repr('Value = 8, Suit = Spade'),
                   repr('Value = 9, Suit = Spade'),
                   repr('Value = 10, Suit = Spade'),
                   repr('Value = 11, Suit = Spade'),
                   repr('Value = 12, Suit = Spade'),
                   repr('Value = 13, Suit = Spade')]
    hearts_repr = [repr('Value = 1, Suit = Heart'),
                   repr('Value = 2, Suit = Heart'),
                   repr('Value = 3, Suit = Heart'),
                   repr('Value = 4, Suit = Heart'),
                   repr('Value = 5, Suit = Heart'),
                   repr('Value = 6, Suit = Heart'),
                   repr('Value = 7, Suit = Heart'),
                   repr('Value = 8, Suit = Heart'),
                   repr('Value = 9, Suit = Heart'),
                   repr('Value = 10, Suit = Heart'),
                   repr('Value = 11, Suit = Heart'),
                   repr('Value = 12, Suit = Heart'),
                   repr('Value = 13, Suit = Heart')]
    clubs_repr = [repr('Value = 1, Suit = Club'),
                  repr('Value = 2, Suit = Club'),
                  repr('Value = 3, Suit = Club'),
                  repr('Value = 4, Suit = Club'),
                  repr('Value = 5, Suit = Club'),
                  repr('Value = 6, Suit = Club'),
                  repr('Value = 7, Suit = Club'),
                  repr('Value = 8, Suit = Club'),
                  repr('Value = 9, Suit = Club'),
                  repr('Value = 10, Suit = Club'),
                  repr('Value = 11, Suit = Club'),
                  repr('Value = 12, Suit = Club'),
                  repr('Value = 13, Suit = Club')]
    diamonds_repr = [repr('Value = 1, Suit = Diamond'),
                     repr('Value = 2, Suit = Diamond'),
                     repr('Value = 3, Suit = Diamond'),
                     repr('Value = 4, Suit = Diamond'),
                     repr('Value = 5, Suit = Diamond'),
                     repr('Value = 6, Suit = Diamond'),
                     repr('Value = 7, Suit = Diamond'),
                     repr('Value = 8, Suit = Diamond'),
                     repr('Value = 9, Suit = Diamond'),
                     repr('Value = 10, Suit = Diamond'),
                     repr('Value = 11, Suit = Diamond'),
                     repr('Value = 12, Suit = Diamond'),
                     repr('Value = 13, Suit = Diamond')]
    nose.assert_equal([repr(x) for x in spades], spades_repr)
    nose.assert_equal([repr(x) for x in hearts], hearts_repr)
    nose.assert_equal([repr(x) for x in clubs], clubs_repr)
    nose.assert_equal([repr(x) for x in diamonds], diamonds_repr)


def test_card_string_all_52():
    """Tests if the string representation of all cards is correct"""
    spades = [Card(x, 'Spade') for x in range(1, 14)]
    hearts = [Card(x, 'Heart') for x in range(1, 14)]
    clubs = [Card(x, 'Club') for x in range(1, 14)]
    diamonds = [Card(x, 'Diamond') for x in range(1, 14)]
    spades_str = ['A S', '2 S', '3 S', '4 S', '5 S', '6 S', '7 S',
                  '8 S', '9 S', 'T S', 'J S', 'Q S', 'K S']
    hearts_str = ['A H', '2 H', '3 H', '4 H', '5 H', '6 H', '7 H',
                  '8 H', '9 H', 'T H', 'J H', 'Q H', 'K H']
    clubs_str = ['A C', '2 C', '3 C', '4 C', '5 C', '6 C', '7 C',
                 '8 C', '9 C', 'T C', 'J C', 'Q C', 'K C']
    diamonds_str = ['A D', '2 D', '3 D', '4 D', '5 D', '6 D', '7 D',
                    '8 D', '9 D', 'T D', 'J D', 'Q D', 'K D']
    nose.assert_equal([str(x) for x in spades], spades_str)
    nose.assert_equal([str(x) for x in hearts], hearts_str)
    nose.assert_equal([str(x) for x in clubs], clubs_str)
    nose.assert_equal([str(x) for x in diamonds], diamonds_str)


def test_invalid_cards():
    """Tests if bad values in card creation will raise an exception"""
    nose.assert_raises(ValueError, Card, 0, 'Spade')
    nose.assert_raises(ValueError, Card, 1, 'Spades')
    nose.assert_raises(ValueError, Card, 14, 'SPADE')


def test_full_deck_creation():
    """Tests that all 52 cards are created in order from the
    default constructor
    """
    deck = Deck()
    full_deck = Deck()
    full_deck.deck = [Card(value, suit) for suit in
                      ['Spade', 'Heart', 'Club', 'Diamond']
                      for value in range(1, 14)]
    nose.assert_equal(deck.deck, full_deck.deck)


def test_deck_shuffle():
    """Tests that the deck is shuffled each time shuffle() is called"""
    deck = Deck()
    deck_str = str(deck)
    shuffled = str(deck)
    nose.assert_equal(deck_str, shuffled)
    for _ in range(10):
        deck.shuffle()
        shuffled = str(deck)
        nose.assert_not_equal(deck_str, shuffled)
        deck_str = shuffled


def test_deck_deal():
    """Tests that cards are dealt from the end of the deck and removed
    when dealt
    """
    deck = Deck()
    nose.assert_equal(Card(13, 'Diamond'), deck.deal())
    nose.assert_not_equal(Card(13, 'Diamond'), deck.deal())
    nose.assert_equal(Card(11, 'Diamond'), deck.deal())


def test_empty_deck():
    """Tests that IndexError is raised when trying to deal from an
    empty deck
    """
    deck = Deck()
    while len(deck) > 0:
        deck.deal()
    nose.assert_raises(IndexError, deck.deal)
