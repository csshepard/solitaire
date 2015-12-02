"""Driver script for text based solitaire game
- The following inputs are valid:
  - 1 or <blank>: Draws a card from the deck
  - 2: Moves card(s) from one pile to another
  - 3: Automatically moves all valid cards to the foundation piles
  - 4: Undo the last move
  - 5: Start a new game
  - 0: Quit current game
- When moving a card the following inputs are used to specify a pile
  - 0: Draw Pile
  - 1-7: The Tableau Piles from left to right
  - H: The Foundation Piles (used when moving to foundation piles)
  - H1-H4: The Foundation Piles from left to right (used when moving from the foundation piles)

The four foundation piles always hold the same suit.  From left to right they are Spade, Heart, Club, Diamond.
"""
from __future__ import print_function
from Solitaire.solitaire import Solitaire
from copy import deepcopy
from time import sleep


def create_complete_game():
    """Used for debug, creates a game where the first 4 tableau piles are
    filed with the cards King through 2 of all 4 suits, and the draw pile
    has the 4 Aces
    """
    from Solitaire.playing_cards import Card
    from Solitaire.solitaire import CardPile
    test_game = Solitaire()
    test_game.deck.pile = [Card(1, 'Spade'), Card(1, 'Heart'),
                           Card(1, 'Club'), Card(1, 'Diamond')]
    test_game.deck.flip = 4
    test_game.piles[0].pile = [Card(13, 'Spade'), Card(12, 'Heart'),
                               Card(11, 'Spade'), Card(10, 'Heart'),
                               Card(9, 'Spade'), Card(8, 'Heart'),
                               Card(7, 'Spade'), Card(6, 'Heart'),
                               Card(5, 'Spade'), Card(4, 'Heart'),
                               Card(3, 'Spade'), Card(2, 'Heart')]
    test_game.piles[0].flip = 0
    test_game.piles[1].pile = [Card(13, 'Heart'), Card(12, 'Spade'),
                               Card(11, 'Heart'), Card(10, 'Spade'),
                               Card(9, 'Heart'), Card(8, 'Spade'),
                               Card(7, 'Heart'), Card(6, 'Spade'),
                               Card(5, 'Heart'), Card(4, 'Spade'),
                               Card(3, 'Heart'), Card(2, 'Spade')]
    test_game.piles[1].flip = 0
    test_game.piles[2].pile = [Card(13, 'Club'), Card(12, 'Diamond'),
                               Card(11, 'Club'), Card(10, 'Diamond'),
                               Card(9, 'Club'), Card(8, 'Diamond'),
                               Card(7, 'Club'), Card(6, 'Diamond'),
                               Card(5, 'Club'), Card(4, 'Diamond'),
                               Card(3, 'Club'), Card(2, 'Diamond')]
    test_game.piles[2].flip = 0
    test_game.piles[3].pile = [Card(13, 'Diamond'), Card(12, 'Club'),
                               Card(11, 'Diamond'), Card(10, 'Club'),
                               Card(9, 'Diamond'), Card(8, 'Club'),
                               Card(7, 'Diamond'), Card(6, 'Club'),
                               Card(5, 'Diamond'), Card(4, 'Club'),
                               Card(3, 'Diamond'), Card(2, 'Club')]
    test_game.piles[3].flip = 0
    test_game.piles[4] = CardPile()
    test_game.piles[5] = CardPile()
    test_game.piles[6] = CardPile()
    return test_game


def set_input_dict(game):
    """Sets the input dictionary to point to the attributes of game.
    Needed because Undo changes the game object
    """
    input_dict = {'0': game.deck,
                  '1': game.piles[0],
                  '2': game.piles[1],
                  '3': game.piles[2],
                  '4': game.piles[3],
                  '5': game.piles[4],
                  '6': game.piles[5],
                  '7': game.piles[6],
                  'h1': game.homes[0],
                  'h2': game.homes[1],
                  'h3': game.homes[2],
                  'h4': game.homes[3],
                  'H1': game.homes[0],
                  'H2': game.homes[1],
                  'H3': game.homes[2],
                  'H4': game.homes[3]}
    return input_dict


def move(game, selection=None):
    """Initiates a move, either pile to pile or card to foundation
    Returns True if move was successful

    Args:
        game (Solitaire): The game where the move will be made
        selection (optional, list of str): The input queue.
            It should contain two more inputs, a source pile and a
            destination pile.  Default is None (user will be prompted)
    """
    input_dict = set_input_dict(game)
    source = destination = ''
    if selection:
        source = selection.pop(0)
    while True:
        if source in input_dict:
            break
        source = input('Source Card\n|0: Available Card'
                       '|''1-7: Piles|H1-H4: Home Piles|\n: ')
    if selection:
        destination = selection.pop(0)
    while True:
        if (destination != '0' and (destination in input_dict or
                                    destination.lower() == 'h')):
            break
        destination = input('Destination Pile\n|1-7: Piles|H1-H4: Home Piles|\n: ')
    if destination in input_dict:
        if game.move_pile(input_dict[source], input_dict[destination]):
            return True
    else:
        if game.move_home(input_dict[source]):
            return True
    return False


def weight_move(game, move):
    """Takes a move and weights it according to how productive the move will be, lower weight holds higher precedence
    Weights:
    0: move card to foundation
    1: move card from waste to tableau
    2: move whole pile from tableau to tableau
    3: move partial pile from tableau to tableau
    4: move card from foundation to tableau
    5: deal cards from deck to waste
    99: lowest precedence to prevent pile switching loop
    Returns (int): precedence

    Args:
        game (Solitaire): The game currently being played
        move (tuple): (from pile, destination pile)
    """
    # move home
    if move[1] in game.homes:
        return 0
    # move from home
    elif move[0] in game.homes:
        return 5
    # deal from deck
    elif move[1] is game.deck:
        return 4
    # move from waste
    elif move[0] is game.deck:
        return 1
    # top king to empty pile
    elif len(move[1]) == 0 and move[0].flip == 0:
        return 99
    # full pile
    elif len(move[1]) == 0 or move[1][-1].value - 1 == move[0][move[0].flip].value:
        return 2
    # partial pile
    else:
        return 3


class AutoMove(object):
    def __init__(self):
        self.moves = {}
        self.best_move = None
        self.first_cycle = None

    def __call__(self, game):
        """Makes one valid move
        Return True if a move was performed

        Args:
            game (Solitaire): The game where the cards will be moved
        """
        if (self.best_move is not None and self.best_move[0] is not game.deck and
                game.move_pile(self.best_move[1], self.best_move[0], move=False)):
            self.moves[(self.best_move[1], self.best_move[0])] = 99
        for move in list(self.moves.keys()):
            if not game.move_pile(move[0], move[1], move=False):
                del self.moves[move]
        if (game.deck, game.deck) not in self.moves and len(game.deck) > 0:
            self.moves[(game.deck, game.deck)] = weight_move(game, (game.deck, game.deck))
        for source_pile in [game.deck] + game.piles + game.homes:
            for destination_pile in game.homes + game.piles:
                if source_pile in game.homes and destination_pile in game.homes:
                    continue
                if ((source_pile, destination_pile) not in self.moves and
                        game.move_pile(source_pile, destination_pile, move=False)):
                    self.moves[(source_pile, destination_pile)] = weight_move(game, (source_pile, destination_pile))
        self.best_move = min(self.moves, key=self.moves.get)
        del self.moves[self.best_move]
        if self.best_move[1] is game.deck:
            return game.deal()
        else:
            return game.move_pile(*self.best_move)


def run_game():
    """The games main loop."""
    game = Solitaire()  # Create new game
    move_stack = []
    auto_move = AutoMove()
    print('\n', game, sep='')
    while True:  # Main Loop
        move_stack.append(deepcopy(game))
        selection = input('|1: Deal|2: Move Card'
                          '|3: Move Cards Home|4: Undo|5:New Game\n: ').split()
        if len(selection) == 0 or selection[0] == '1':
            game.deal()
            print('\n', game, sep='')
        elif selection[0] == '2':
            selection.pop(0)
            if move(game, selection):
                print('\n', game, sep='')
            else:
                move_stack.pop()

        elif selection[0] == '3':
            while any(game.move_home(pile) for pile in game.piles + [game.deck]):
                sleep(0.2)
                print('\n', game, sep='')
                move_stack.append(deepcopy(game))
            move_stack.pop()
        elif selection[0] == '4':
            move_stack.pop()
            if len(move_stack) > 0:
                game = move_stack.pop()
                print('\n', game, sep='')
        elif selection[0] == '0':
            break
        elif selection[0] == 'DEBUG':
            game = create_complete_game()
            print('\n', game, sep='')
        elif selection[0] == '5':
            game = Solitaire()
            move_stack = []
            print('\n', game, sep='')
        elif selection[0] == 'a':
            if auto_move(game):
                print('\n', game, sep='')
            else:
                move_stack.pop()
        if game.check_win():
            print('YOU WIN!!!!')
            break


if __name__ == '__main__':
    try:
        input = raw_input
    except NameError:
        pass
    run_game()
