import deck


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
        adeck = deck.Deck()
        adeck.shuffle()
        self.pile1 = CardPile(adeck, 1)   # Tableau Piles
        self.pile1.update()
        self.pile2 = CardPile(adeck, 2)
        self.pile2.update()
        self.pile3 = CardPile(adeck, 3)
        self.pile3.update()
        self.pile4 = CardPile(adeck, 4)
        self.pile4.update()
        self.pile5 = CardPile(adeck, 5)
        self.pile5.update()
        self.pile6 = CardPile(adeck, 6)
        self.pile6.update()
        self.pile7 = CardPile(adeck, 7)
        self.pile7.update()
        self.home1 = CardPile()          # Foundation Piles
        self.home2 = CardPile()
        self.home3 = CardPile()
        self.home4 = CardPile()
        self.pile0 = CardPile(adeck)     # Combination of Deck and Waste Piles

    def __str__(self):
        boardlst = []
        # Draw Pile
        if self.pile0.flip > 0:
            boardlst.append('***  ')
        else:
            boardlst.append('---  ')
        # Waste Pile
        if self.pile0.flip < len(self.pile0):
            boardlst.extend([str(self.pile0.pile[self.pile0.flip]), ' '])
        else:
            boardlst.append('---  ')
        boardlst.append('     ')
        # Foundation Piles
        if len(self.home1.pile):
            boardlst.extend([str(self.home1.pile[-1]), ' '])
        else:
            boardlst.append('---  ')
        if len(self.home2.pile):
            boardlst.extend([str(self.home2.pile[-1]), ' '])
        else:
            boardlst.append('---  ')
        if len(self.home3.pile):
            boardlst.extend([str(self.home3.pile[-1]), ' '])
        else:
            boardlst.append('---  ')
        if len(self.home4.pile):
            boardlst.extend([str(self.home4.pile[-1]), '\n\n'])
        else:
            boardlst.append('---\n\n')
        for x in range(max([len(pile) for pile in
                            [self.pile1, self.pile2, self.pile3,
                             self.pile4, self.pile5, self.pile6,
                             self.pile7]])):
            if self.pile1.flip > x:
                boardlst.append('***  ')
            elif len(self.pile1) > x:
                boardlst.extend([str(self.pile1[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile2.flip > x:
                boardlst.append('***  ')
            elif len(self.pile2) > x:
                boardlst.extend([str(self.pile2[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile3.flip > x:
                boardlst.append('***  ')
            elif len(self.pile3) > x:
                boardlst.extend([str(self.pile3[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile4.flip > x:
                boardlst.append('***  ')
            elif len(self.pile4) > x:
                boardlst.extend([str(self.pile4[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile5.flip > x:
                boardlst.append('***  ')
            elif len(self.pile5) > x:
                boardlst.extend([str(self.pile5[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile6.flip > x:
                boardlst.append('***  ')
            elif len(self.pile6) > x:
                boardlst.extend([str(self.pile6[x]), ' '])
            else:
                boardlst.append('---  ')
            if self.pile7.flip > x:
                boardlst.append('***\n')
            elif len(self.pile7) > x:
                boardlst.extend([str(self.pile7[x]), '\n'])
            else:
                boardlst.append('---\n')
        return ''.join(boardlst)

    def deal(self, amount=3):
        if self.pile0.flip == 0:        # All cards have been dealt
            self.pile0.flip = len(self.pile0)
        else:
            self.pile0.flip -= amount   # Deal, at most, amount cards
            if self.pile0.flip < 0:
                self.pile0.flip = 0

    def movepile(self, source_pile, dest_pile):
        if source_pile.flip == len(source_pile):
            return False
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if len(dest_pile.pile) > 0:    # Check for empty pile
            dest_card = dest_pile[-1]  # Set top card
            if source_pile is self.pile0:
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
                        return True
        # Source card is King and dest is empty
        elif source_pile[source_pile.flip].value == 13:
            if source_pile is self.pile0:
                dest_pile.pile.append(source_pile.pop(source_pile.flip))
            else:
                dest_pile.pile.extend(source_pile[source_pile.flip:])
                del source_pile.pile[source_pile.flip:]
            return True
        return False

    def movehome(self, source_pile):
        # Card is top on pile
        if len(source_pile) == 0 or source_pile.flip == len(source_pile):
            return False
        source_index = -1
        # Card is face up card on waste pile
        if source_pile is self.pile0:
            source_index = source_pile.flip
        source_card = source_pile[source_index]
        homes = {'Spade': self.home1,
                 'Heart': self.home2,
                 'Club': self.home3,
                 'Diamond': self.home4}
        dest_pile = homes[source_card.suit]
        # Foundation has cards
        if len(dest_pile) > 0:
            if source_card.value == dest_pile[-1].value + 1:
                dest_pile.pile.append(source_pile.pop(source_index))
                return True
        # Foundation is empty and card is Ace
        elif source_pile[source_index].value == 1:
            dest_pile.pile.append(source_pile.pop(source_index))
            return True
        return False

    def checkwin(self):
        if (len(self.home1) == 13 and len(self.home2) == 13 and
                len(self.home3) == 13 and len(self.home4) == 13):
            return True
