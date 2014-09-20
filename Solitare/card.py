
class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

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
        return '{0} {1} '.format(values[self.value], self.suit[0])
