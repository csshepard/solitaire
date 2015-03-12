import nose.tools as nose

class Card(object):
    def __init__(self, value=1, suit='Spade'):
        # Creates a card object that has a numeric value and a string suit
        # If no args are passed, the Ace of Spades is created
        if 0 < value < 14:
            self.value = value
        else:
            raise ValueError('{} not a valid card value'.format(value))
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        if suit in suits:
            self.suit = suit
        else:
            raise ValueError('{} not a valid card suit'.format(suit))

    def __repr__(self):
        return repr('Value = {0}, Suit = {1}'.format(self.value, self.suit))

    def __str__(self):
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
        return '{0} {1}'.format(values[self.value], self.suit[0])

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

# Tests

def test_default_card_creation():
    test_card = Card()
    ace_spades = Card(1, 'Spade')
    nose.assert_equal(test_card, ace_spades)

def test_card_repr_all_52():
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
    nose.assert_raises(ValueError, Card, 0, 'Spade')
    nose.assert_raises(ValueError, Card, 1, 'Spades')
    nose.assert_raises(ValueError, Card, 14, 'SPADE')