"""A simple solitaire game

Classes:
    CardPile: a list of cards with a divider
    Solitaire: The solitaire game
"""
from .playing_cards import Deck


class CardPile(object):
    """a list of cards that have a divider separating them into 2 parts.
    They are either face down or face up.  The face down cards are at the
    start of the list.  The face up cards start at [flip] and go to the end
    of the list.  When cards are added to an existing pile, they are added
    face up.

    Attributes:
        pile (list of Cards): the list of cards in the pile
        flip (int): the index where the cards flip from face down to face up

    Public Methods:
        update(): flips the top card face up if it was face down
        get_face_up(): iterates through the list of face up cards
        move_card(source_pile, index): moves single card to end of pile
        move_cards(source_pile, index): moves multiple cards to end of pile

    """
    def __init__(self, deck=None, amount=0):
        """Creates a pile of face down cards

        Args:
            deck(optional, Deck): a deck of cards that will be used to create
                the CardPile, default is None
            amount (optional, int): the number of cards to deal,
                <=0 deals all from deck
        """

        self.pile = []
        self.flip = 0
        if deck is not None:
            if amount <= 0:
                amount = len(deck)
            self.flip = amount
            for _ in range(amount):
                try:
                    self.pile.append(deck.deal())
                except IndexError:
                    print("Attempted to deal from empty deck")
                    break

    def __len__(self):
        return len(self.pile)

    def __getitem__(self, item):
        return self.pile[item]

    def __repr__(self):
        return repr('A pile of {0} cards, {1} are face up'.format(
            len(self.pile), len(self.pile)-self.flip))

    def index(self, item):
        return self.pile.index(item)

    def update(self):
        """Flips over top card if face down"""
        if self.pile and self.flip > len(self.pile) - 1:
            self.flip -= 1

    def get_face_up(self):
        """creates an iterator that returns tuples containing
        the face up cards and their index in the pile
        """
        index = self.flip
        while index < len(self.pile):
            yield (self.pile[index], index)
            index += 1

    def move_card(self, source_pile, index):
        """Move a single card from source_pile to the end of the pile

        Args:
            source_pile (CardPile): the pile that the cards will be moved from
            index (int): the index of the card in source_pile that will be
                moved
        """
        self.pile.append(source_pile.pile.pop(index))

    def move_cards(self, source_pile, index):
        """Move multiple cards from source_pile.  This will move all cards
        from index to the end of the source_pile.

        Args:
            source_pile (CardPile): the pile that the cards will be moved from
            index (int): the index of the first card in source_pile that will
                be moved
        """
        self.pile.extend(source_pile[index:])
        del source_pile.pile[index:]


class Solitaire(object):
    """A simple text based solitaire game

    Attributes:
        piles (list of CardPiles): a list of 7 CardPiles that represent
            the tableau piles of a solitaire game
        homes (list of CardPiles): a list of 4 CardPiles that represent
            the foundation piles of a solitaire game
        deck (CardPile): a CardPile that doubles as the draw pile and
            the waste pile

    Public Methods:
        deal(amount):  moves cards from draw pile to waste pile, default 3
        move_pile(source_pile, destination_pile): move cards between piles
        move_home(source_pile): move card to foundation piles
        check_win(): returns True if game has been completed
    """
    def __init__(self):
        """Initiates a solitaire game.  Deals out the 7 tableau piles and
        flips over the top card.  Creates the 4 CardPiles that will be the
        foundation piles.  Deals the remaining cards to the draw pile
        """
        deck = Deck()
        deck.shuffle()
        self.piles = [CardPile(deck, 1), CardPile(deck, 2),
                      CardPile(deck, 3), CardPile(deck, 4),
                      CardPile(deck, 5), CardPile(deck, 6),
                      CardPile(deck, 7)]
        self._update()
        self.homes = [CardPile(), CardPile(), CardPile(), CardPile()]
        self.deck = CardPile(deck)

    def __str__(self):
        board_lst = []
        # Draw Pile
        if self.deck.flip > 0:
            board_lst.append('***  ')
        else:
            board_lst.append('---  ')
        # Waste Pile
        if self.deck.flip < len(self.deck):
            board_lst.extend(
                [str(next(self.deck.get_face_up())[0]), '  '])
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
        """Deals cards from the draw pile to the waste pile.  If all cards
        will be dealt, only deals to the end of the pile.  If all cards have
        been dealt, all cards are moved from waste to draw pile

        Args:
            amount (optional, int): amount of cards to be moved from draw
                to waste, default is 3 cards
        """
        if self.deck.flip == 0:        # All cards have been dealt
            self.deck.flip = len(self.deck)
        else:
            self.deck.flip -= amount   # Deal, at most, amount cards
            if self.deck.flip < 0:
                self.deck.flip = 0
        return True

    def move_pile(self, source_pile, destination_pile, move=True):
        """Move cards from waste pile or tableau pile to another tableau pile.
        If source pile is waste pile, only top card will be moved.  If source
        pile is a tableau pile, face up cards will be searched for a possible
        move.  Returns True if move is successful, False if move was illegal

        Args:
            source_pile (CardPile): the CardPile where the cards will be moved
                from
            destination_pile (CardPile): the CardPile where the cards will be
                moved to
            move (Bool) : If True, then move is completed, otherwise only
                move validity is returned
        """
        if source_pile.flip == len(source_pile):
            return False
        cross_color = {'Spade': ['Heart', 'Diamond'],
                       'Heart': ['Spade', 'Club'],
                       'Club': ['Heart', 'Diamond'],
                       'Diamond': ['Spade', 'Club']}
        if len(destination_pile.pile) > 0:    # Check for empty pile
            destination_card = destination_pile[-1]  # Set top card
            if source_pile is self.deck or destination_pile in self.homes:
                source_card = source_pile[-1]
                if source_pile is self.deck:
                    source_card = source_pile[source_pile.flip]
                if ((destination_pile in self.homes and
                        source_card.suit == destination_card.suit and
                        source_card.value == destination_card.value + 1) or
                    (destination_pile not in self.homes and
                        source_card.value == destination_card.value - 1 and
                        destination_card.suit in
                        cross_color[source_card.suit])):
                    if move:
                        destination_pile.move_card(source_pile, source_pile.index(source_card))
                        self._update()
                    return True
            else:
                for card in source_pile.get_face_up():
                    if (card[0].value == destination_card.value - 1 and
                            destination_card.suit in
                            cross_color[card[0].suit]):
                        if move:
                            destination_pile.move_cards(source_pile, card[1])
                            self._update()
                        return True
        # Source card is King or Ace and destination is empty
        else:
            if destination_pile in self.homes:
                source_card = (source_pile[-1], -1)
                if source_pile is self.deck:
                    source_card = next(source_pile.get_face_up())
            else:
                source_card = next(source_pile.get_face_up())
            if ((destination_pile in self.piles and source_card[0].value == 13) or
                    (destination_pile in self.homes and source_card[0].value == 1)):
                if move:
                    if source_pile is self.deck or destination_pile in self.homes:
                        destination_pile.move_card(source_pile, source_card[1])
                    else:
                        destination_pile.move_cards(source_pile, source_card[1])
                    self._update()
                return True
            return False

    def move_home(self, source_pile, move=True):
        """Move card from source_pile to a foundation pile. Foundation pile
        is determined by suit of top card on source pile.  The order is
        Spade, Heart, Club, Diamond.  Returns True if move was successful,
        False if move was illegal

        Args:
            source_pile (CardPile): the CardPile where the card will be
                moved from
            move (Bool) : If True, then move is completed, otherwise only
                move validity is returned
        """
        # Card is top on pile
        if source_pile.flip == len(source_pile):
            return False
        source_index = -1
        # Card is face up card on waste pile
        if source_pile is self.deck:
            source_index = source_pile.flip
        source_card = source_pile[source_index]
        destination_pile = None
        for pile in self.homes:
            if len(pile) > 0 and pile[0].suit == source_card.suit:
                destination_pile = pile
                break
        if destination_pile is None:
            for pile in self.homes:
                if len(pile) == 0:
                    destination_pile = pile
                    break
        if ((len(destination_pile) == 0 and source_card.value == 1) or
                (len(destination_pile) > 0 and
                 source_card.value == destination_pile[-1].value + 1)):
            if move:
                destination_pile.move_card(source_pile, source_index)
                self._update()
            return True
        return False

    def check_win(self):
        """Checks if game has been completed.  Returns True if all
        foundation piles have 13 cards in them
        """
        return all([len(self.homes[x]) == 13 for x in range(4)])

    def _update(self):
        """Flips top card face up on all tableau piles"""
        for pile in self.piles:
            pile.update()
