from solitare import Solitare
from copy import deepcopy
from time import sleep


def create_complete_game():
    from card import Card
    from solitare import CardPile
    g = Solitare()
    g.deck.pile = [Card(), Card(1, 'Heart'), Card(1, 'Club'), Card(1, 'Diamond')]
    g.deck.flip = 4
    g.piles[0].pile = [Card(13, 'Spade'), Card(12, 'Heart'), Card(11, 'Spade'),
                       Card(10, 'Heart'), Card(9, 'Spade'), Card(8, 'Heart'),
                       Card(7, 'Spade'), Card(6, 'Heart'), Card(5, 'Spade'),
                       Card(4, 'Heart'), Card(3, 'Spade'), Card(2, 'Heart')]
    g.piles[0].flip = 0
    g.piles[1].pile = [Card(13, 'Heart'), Card(12, 'Spade'), Card(11, 'Heart'),
                       Card(10, 'Spade'), Card(9, 'Heart'), Card(8, 'Spade'),
                       Card(7, 'Heart'), Card(6, 'Spade'), Card(5, 'Heart'),
                       Card(4, 'Spade'), Card(3, 'Heart'), Card(2, 'Spade')]
    g.piles[1].flip = 0
    g.piles[2].pile = [Card(13, 'Club'), Card(12, 'Diamond'), Card(11, 'Club'),
                       Card(10, 'Diamond'), Card(9, 'Club'), Card(8, 'Diamond'),
                       Card(7, 'Club'), Card(6, 'Diamond'), Card(5, 'Club'),
                       Card(4, 'Diamond'), Card(3, 'Club'), Card(2, 'Diamond')]
    g.piles[2].flip = 0
    g.piles[3].pile = [Card(13, 'Diamond'), Card(12, 'Club'), Card(11, 'Diamond'),
                       Card(10, 'Club'), Card(9, 'Diamond'), Card(8, 'Club'),
                       Card(7, 'Diamond'), Card(6, 'Club'), Card(5, 'Diamond'),
                       Card(4, 'Club'), Card(3, 'Diamond'), Card(2, 'Club')]
    g.piles[3].flip = 0
    g.piles[4] = CardPile()
    g.piles[5] = CardPile()
    g.piles[6] = CardPile()
    return g


if __name__ == '__main__':
    game = Solitare()  # Create new game
    move_stack = []
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
    no_loop = True
    while True:  # Main Loop
        if no_loop:
            print('\n', game, sep='')
        no_loop = True
        source = dest = ''
        selection = input('|1: Deal|2: Move Card|3: Move Cards Home|4: Undo|\n: ').split()
        if len(selection) == 0 or selection[0] == '1':
            move_stack.append(deepcopy(game))
            game.deal()
        elif selection[0] == '2':
            move_stack.append(deepcopy(game))
            selection.pop(0)
            if selection:
                source = selection.pop(0)
            while True:
                if source in input_dict:
                    break
                source = input('Source Card\n|0: Available Card|'
                               '1-7: Piles|H1-H4: Home Piles|\n: ')
            if selection:
                dest = selection.pop(0)
            while True:
                if dest != '0' and (dest in input_dict or dest.lower() == 'h'):
                    break
                dest = input('Destination Pile\n'
                             '|1-7: Piles|H: Home Piles|\n: ')
            if dest < '8':
                if not game.move_pile(input_dict[source], input_dict[dest]):
                    move_stack.pop()
            else:
                if not game.move_home(input_dict[source]):
                    move_stack.pop()
        elif selection[0] == '0':
            break
        elif selection[0] == '3':
            move_stack.append(deepcopy(game))
            while (any(map(game.move_home, game.piles)) or
                   game.move_home(game.deck)):
                no_loop = False
                print('\n', game, sep='')
                sleep(0.3)
            if no_loop:
                move_stack.pop()
        elif selection[0] == '4':
            if len(move_stack) > 0:
                game = move_stack.pop()
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
        elif selection[0] == 'DEBUG':
            game = create_complete_game()
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
        if game.check_win():
            print('YOU WIN!!!!')
            break
