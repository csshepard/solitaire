from deck import Deck


class CardPile(object):
    def __init__(self, deck=None, amount=0):
        # Creates a pile of cards divided into face up and face down sections
        # Initially all cards are face down
        # If deck is None, creates an empty pile, else deals from deck
        # Amount determines number of cards to deal, <=0 deals all from deck

        self.pile = []    # List of cards
        self.flip = 0    # Index where cards flip from face down to face up
        if deck is not None:
            if len(deck) < amount or amount <= 0:
                amount = len(deck)
            self.flip = amount
            for _ in range(amount):
                self.pile.append(deck.deal())

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

    def pop(self, start_index=-1):
        return self.pile.pop(start_index)


class Solitare(object):
    def __init__(self):
        deck = Deck()
        deck.shuffle()
        self.piles = [CardPile(deck, 1), CardPile(deck, 2),
                      CardPile(deck, 3), CardPile(deck, 4),
                      CardPile(deck, 5), CardPile(deck, 6),
                      CardPile(deck, 7)]
        self._update()
        self.homes = [CardPile(), CardPile(), CardPile(), CardPile()]
        self.deck = CardPile(deck)     # Combination of Deck and Waste Piles

    def __str__(self):
        board_lst = []
        # Draw Pile
        if self.deck.flip > 0:
            board_lst.append('***  ')
        else:
            board_lst.append('---  ')
        # Waste Pile
        if self.deck.flip < len(self.deck):
            board_lst.extend([str(self.deck.pile[self.deck.flip]), '  '])
        else:
            board_lst.append('---  ')
        board_lst.append('     ')
        # Foundation Piles
        for index in range(4):
            if len(self.homes[index].pile):
                board_lst.extend([str(self.homes[index].pile[-1]), '  '])
            else:
                board_lst.append('---  ')
        board_lst.append('\n\n')
        for row in range(max([len(pile) for pile in self.piles])):
            for column in range(7):
                if self.piles[column].flip > row:
                    board_lst.append('***  ')
                elif len(self.piles[column]) > row:
                    board_lst.extend([str(self.piles[column][row]), '  '])
                else:
                    board_lst.append('---  ')
            board_lst.append('\n')
        return ''.join(board_lst)

    def deal(self, amount=3):
        if self.deck.flip == 0:        # All cards have been dealt
            self.deck.flip = len(self.deck)
        else:
            self.deck.flip -= amount   # Deal, at most, amount cards
            if self.deck.flip < 0:
                self.deck.flip = 0

    def move_pile(self, source_pile, destination_pile):
        if source_pile.flip == len(source_pile):
            return False
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if len(destination_pile.pile) > 0:    # Check for empty pile
            destination_card = destination_pile[-1]  # Set top card
            if source_pile is self.deck:
                source_card = source_pile[source_pile.flip]
                if (source_card.value == destination_card.value - 1 and
                        destination_card.suit in
                        cross_color[source_card.suit]):
                    destination_pile.pile.append(source_pile.pop(
                        source_pile.flip))
                    return True
            else:
                for card in source_pile[source_pile.flip:]:
                    if (card.value == destination_card.value - 1 and
                            destination_card.suit in cross_color[card.suit]):
                        destination_pile.pile.extend(
                            source_pile[source_pile.pile.index(card):])
                        del source_pile.pile[source_pile.pile.index(card):]
                        self._update()
                        return True
        # Source card is King and destination is empty
        elif source_pile[source_pile.flip].value == 13:
            if source_pile is self.deck:
                destination_pile.pile.append(source_pile.pop(source_pile.flip))
            else:
                destination_pile.pile.extend(source_pile[source_pile.flip:])
                del source_pile.pile[source_pile.flip:]
                self._update()
            return True
        return False

    def move_home(self, source_pile):
        # Card is top on pile
        if source_pile.flip == len(source_pile):
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
                self._update()
                return True
        # Foundation is empty and card is Ace
        elif source_card.value == 1:
            dest_pile.pile.append(source_pile.pop(source_index))
            self._update()
            return True
        return False

    def check_win(self):
        # return [len(self.homes[x]) for x in range(4)] == [13]*4
        return all(map(lambda x: len(self.homes[x]) == 13, range(4)))

    def _update(self):
        for pile in self.piles:
            pile.update()