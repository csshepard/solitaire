
class Card(object):
    def __init__(self, value=1, suit='Spade'):
        #Creates a card object that has a numeric value and a string suit
        #If no args or invalid args are passed, the Ace of Spades is created
        if 0 < value < 14:
            self.value = value
        else:
            self.value = 1
        suits = ['Spade', 'Heart', 'Club', 'Diamond']
        if suit in suits:
            self.suit = suit
        else:
            self.suit = 'Spade'

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
