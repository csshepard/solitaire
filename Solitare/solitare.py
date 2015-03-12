from deck import Deck


class CardPile(object):
    def __init__(self, adeck=None, amount=0):
        # Creates a pile of cards divided into face up and face down sections
        # Initially all cards are face down
        # If deck is None, creates an empty pile, else deals from deck
        # Amount determines number of cards to deal, <=0 deals all from deck

        self.pile = []    # List of cards
        self.flip = -1    # Index where cards flip from face down to face up
        if adeck is not None:
            if len(adeck) < amount or amount <= 0:
                amount = len(adeck)
            self.flip = amount
            for x in range(amount):
                self.pile.append(adeck.deal())

    def __len__(self):
        return len(self.pile)

    def __getitem__(self, item):
        return self.pile[item]

    def __repr__(self):
        return repr('A pile of {0} cards, {1} are face up'.format(
                    len(self.pile), len(self.pile)-self.flip))

    def update(self):
        # Flips over top card if face down
        if self.pile and self.flip > len(self.pile) - 1:
            self.flip -= 1

    def pop(self, index=-1):
        return self.pile.pop(index)


class Solitare(object):
    def __init__(self):
        adeck = Deck()
        adeck.shuffle()
        self.piles = [CardPile(adeck, 1), CardPile(adeck, 2),
                      CardPile(adeck, 3), CardPile(adeck, 4),
                      CardPile(adeck, 5), CardPile(adeck, 6),
                      CardPile(adeck, 7)]
        for pile in self.piles:
            pile.update()
        self.homes = [CardPile(), CardPile(), CardPile(), CardPile()]
        self.deck = CardPile(adeck)     # Combination of Deck and Waste Piles

    def __str__(self):
        boardlst = []
        # Draw Pile
        if self.deck.flip > 0:
            boardlst.append('***  ')
        else:
            boardlst.append('---  ')
        # Waste Pile
        if self.deck.flip < len(self.deck):
            boardlst.extend([str(self.deck.pile[self.deck.flip]), '  '])
        else:
            boardlst.append('---  ')
        boardlst.append('     ')
        # Foundation Piles
        if len(self.homes[0].pile):
            boardlst.extend([str(self.homes[0].pile[-1]), '  '])
        else:
            boardlst.append('---  ')
        if len(self.homes[1].pile):
            boardlst.extend([str(self.homes[1].pile[-1]), '  '])
        else:
            boardlst.append('---  ')
        if len(self.homes[2].pile):
            boardlst.extend([str(self.homes[2].pile[-1]), '  '])
        else:
            boardlst.append('---  ')
        if len(self.homes[3].pile):
            boardlst.extend([str(self.homes[3].pile[-1]), '\n\n'])
        else:
            boardlst.append('---\n\n')
        for x in range(max([len(pile) for pile in
                            [self.piles[0], self.piles[1], self.piles[2],
                             self.piles[3], self.piles[4], self.piles[5],
                             self.piles[6]]])):
            if self.piles[0].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[0]) > x:
                boardlst.extend([str(self.piles[0][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[1].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[1]) > x:
                boardlst.extend([str(self.piles[1][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[2].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[2]) > x:
                boardlst.extend([str(self.piles[2][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[3].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[3]) > x:
                boardlst.extend([str(self.piles[3][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[4].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[4]) > x:
                boardlst.extend([str(self.piles[4][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[5].flip > x:
                boardlst.append('***  ')
            elif len(self.piles[5]) > x:
                boardlst.extend([str(self.piles[5][x]), '  '])
            else:
                boardlst.append('---  ')
            if self.piles[6].flip > x:
                boardlst.append('***\n')
            elif len(self.piles[6]) > x:
                boardlst.extend([str(self.piles[6][x]), '\n'])
            else:
                boardlst.append('---\n')
        return ''.join(boardlst)

    def deal(self, amount=3):
        if self.deck.flip == 0:        # All cards have been dealt
            self.deck.flip = len(self.deck)
        else:
            self.deck.flip -= amount   # Deal, at most, amount cards
            if self.deck.flip < 0:
                self.deck.flip = 0

    def movepile(self, source_pile, dest_pile):
        if source_pile.flip == len(source_pile):
            return False
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if len(dest_pile.pile) > 0:    # Check for empty pile
            dest_card = dest_pile[-1]  # Set top card
            if source_pile is self.deck:
                if (source_pile[source_pile.flip].value ==
                        dest_card.value - 1 and dest_card.suit in
                        cross_color[source_pile[source_pile.flip].suit]):
                    dest_pile.pile.append(source_pile.pop(
                        source_pile.flip))
                    return True
            else:
                for card in source_pile[source_pile.flip:]:
                    if (card.value == dest_card.value - 1 and
                            dest_card.suit in cross_color[card.suit]):
                        dest_pile.pile.extend(
                            source_pile[source_pile.pile.index(card):])
                        del source_pile.pile[source_pile.pile.index(card):]
                        source_pile.update()
                        return True
        # Source card is King and dest is empty
        elif source_pile[source_pile.flip].value == 13:
            if source_pile is self.deck:
                dest_pile.pile.append(source_pile.pop(source_pile.flip))
            else:
                dest_pile.pile.extend(source_pile[source_pile.flip:])
                del source_pile.pile[source_pile.flip:]
                source_pile.update()
            return True
        return False

    def movehome(self, source_pile):
        # Card is top on pile
        if len(source_pile) == 0 or source_pile.flip == len(source_pile):
            return False
        source_index = -1
        # Card is face up card on waste pile
        if source_pile is self.deck:
            source_index = source_pile.flip
        source_card = source_pile[source_index]
        homes = {'Spade': self.homes[0],
                 'Heart': self.homes[1],
                 'Club': self.homes[2],
                 'Diamond': self.homes[3]}
        dest_pile = homes[source_card.suit]
        # Foundation has cards
        if len(dest_pile) > 0:
            if source_card.value == dest_pile[-1].value + 1:
                dest_pile.pile.append(source_pile.pop(source_index))
                source_pile.update()
                return True
        # Foundation is empty and card is Ace
        elif source_pile[source_index].value == 1:
            dest_pile.pile.append(source_pile.pop(source_index))
            source_pile.update()
            return True
        return False

    def checkwin(self):
        if (len(self.homes[0]) == 13 and len(self.homes[1]) == 13 and
                len(self.homes[2]) == 13 and len(self.homes[3]) == 13):
            return True
