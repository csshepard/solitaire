import deck


class CardPile(object):
    def __init__(self, adeck=None, amount=0):
        #Creates a pile of cards which is divided into face up and face down sections
        #Initially all cards are face down
        #If deck is None, creates an empty pile, else deals from deck
        #Amount determines number of cards to deal, <=0 deals all cards from deck

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
        return repr('A pile of {0} cards, {1} are face up'.format(len(self.pile), len(self.pile)-self.flip))

    def update(self):
        #Flips over top card if face down
        if self.flip > len(self.pile) - 1:
            self.flip -= 1


class Solitare(object):
    def __init__(self):
        adeck = deck.Deck()
        adeck.shuffle()
        self.pile1 = CardPile(adeck, 1)    # Tableau Piles
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
        self.home1 = CardPile()           # Foundation Piles
        self.home2 = CardPile()
        self.home3 = CardPile()
        self.home4 = CardPile()
        self.pile0 = CardPile(adeck)     # Combination of Deck and Waste Piles

    def __str__(self):
        boardlst = []
        if self.pile0.flip > 0:
            boardlst.append('***  ')
        else:
            boardlst.append('---  ')
        if self.pile0.flip < len(self.pile0):
            boardlst.extend([str(self.pile0.pile[self.pile0.flip]), ' '])
        else:
            boardlst.append('---  ')
        boardlst.append('     ')
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
        for x in range(21):
            fall_through = 0
            if self.pile1.flip > x:
                boardlst.append('***  ')
            elif len(self.pile1) > x:
                boardlst.extend([str(self.pile1[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile2.flip > x:
                boardlst.append('***  ')
            elif len(self.pile2) > x:
                boardlst.extend([str(self.pile2[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile3.flip > x:
                boardlst.append('***  ')
            elif len(self.pile3) > x:
                boardlst.extend([str(self.pile3[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile4.flip > x:
                boardlst.append('***  ')
            elif len(self.pile4) > x:
                boardlst.extend([str(self.pile4[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile5.flip > x:
                boardlst.append('***  ')
            elif len(self.pile5) > x:
                boardlst.extend([str(self.pile5[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile6.flip > x:
                boardlst.append('***  ')
            elif len(self.pile6) > x:
                boardlst.extend([str(self.pile6[x]), ' '])
            else:
                boardlst.append('---  ')
                fall_through += 1
            if self.pile7.flip > x:
                boardlst.append('***\n')
            elif len(self.pile7) > x:
                boardlst.extend([str(self.pile7[x]), '\n'])
            else:
                boardlst.append('---\n')
                fall_through += 1
            if fall_through == 7:
                return ''.join(boardlst)

    def deal3(self):
        if self.pile0.flip == 0:        # All cards have been dealt
            self.pile0.flip = len(self.pile0)
        else:
            self.pile0.flip -= 3       # Deal, at most, 3 cards
            if self.pile0.flip < 0:
                self.pile0.flip = 0

    def movepile(self, source_pile, dest_pile, card_amount):
        if len(source_pile) == 0 or source_pile.flip == len(source_pile):
            return False
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if card_amount < 1:              # Move all face up cards
            card_amount = len(source_pile[source_pile.flip:])
        elif card_amount > len(source_pile[source_pile.flip:]):
            return False
        if source_pile is self.pile0:  # Set top face up card
            source_card = source_pile[source_pile.flip]
        else:
            source_card = source_pile[-card_amount]  # Set deepest moving card
        if len(dest_pile.pile) > 0:    # Check for empty pile
            dest_card = dest_pile[-1]  # Set top card
            if source_card.value == dest_card.value - 1:    # check if pile can be moved
                if dest_card.suit in cross_color[source_card.suit]:
                    if source_pile is self.pile0:  # if moving from deck, only move face up card
                        dest_pile.pile.append(source_pile.pile.pop(source_pile.flip))
                    else:
                        dest_pile.pile.extend(source_pile[-card_amount:])
                        del source_pile.pile[-card_amount:]
                    return True
        elif source_card.value == 13:     # Source card is King and dest is empty
            if source_pile is self.pile0:
                dest_pile.pile.append(source_pile.pile.pop(source_pile.flip))
            else:
                dest_pile.pile.extend(source_pile[-card_amount:])
                del source_pile.pile[-card_amount:]
            return True
        return False

    def movehome(self, source_pile):
        if len(source_pile) == 0 or source_pile.flip == len(source_pile):
            return False
        source_index = -1             # Card is top on pile
        if source_pile is self.pile0:
            source_index = source_pile.flip   # Card is face up card on deck
        suit = source_pile[source_index].suit[0]
        if suit == 'S':
            dest_pile = self.home1
        elif suit == 'H':
            dest_pile = self.home2
        elif suit == 'C':
            dest_pile = self.home3
        else:
            dest_pile = self.home4
        if len(dest_pile) > 0:  # Foundation has cards
            if source_pile[source_index].value == dest_pile[-1].value + 1:
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