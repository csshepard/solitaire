"""Driver script for text based solitaire game"""
from solitaire import Solitaire
from copy import deepcopy
from time import sleep


def create_complete_game():
    """Used for debug, creates a game where the first 4 tableau piles are
    filed with the cards King through 2 of all 4 suits, and the draw pile
    has the 4 Aces
    """
    from playing_cards import Card
    from solitaire import CardPile
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
        destination = input('Destination Pile\n|1-7: Piles|H: Home Piles|\n: ')
    if destination < '8':
        if game.move_pile(input_dict[source], input_dict[destination]):
            return True
    else:
        if game.move_home(input_dict[source]):
            return True
    return False


def auto_move_home(game):
    """Moves cards to foundation piles until no more are possible
    Returns True if a move was performed

    Args:
        game (Solitaire): The game where the cards will be moved
    """
    moved = False
    while any([game.move_home(pile) for pile in game.piles + [game.deck]]):
        moved = True
        print('\n', game, sep='')
        sleep(0.3)
    return moved


def run_game():
    """The games main loop."""
    game = Solitaire()  # Create new game
    move_stack = []
    while True:  # Main Loop
        print('\n', game, sep='')
        move_stack.append(deepcopy(game))
        selection = input('|1: Deal|2: Move Card'
                          '|3: Move Cards Home|4: Undo|5:New Game\n: ').split()
        if len(selection) == 0 or selection[0] == '1':
            game.deal()
        elif selection[0] == '2':
            selection.pop(0)
            if not move(game, selection):
                move_stack.pop()
        elif selection[0] == '3':
            if not auto_move_home(game):
                move_stack.pop()
        elif selection[0] == '4':
            move_stack.pop()
            if len(move_stack) > 0:
                game = move_stack.pop()
        elif selection[0] == '0':
            break
        elif selection[0] == 'DEBUG':
            game = create_complete_game()
        elif selection[0] == '5':
            game = Solitaire()
            move_stack = []
        if game.check_win():
            print('YOU WIN!!!!')
            break


if __name__ == '__main__':
    run_game()
