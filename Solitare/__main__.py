from solitare import Solitare
from copy import deepcopy
from time import sleep


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
    while True:  # Main Loop
        source = dest = ''
        print('\n', game, sep='')
        selection = input('|1: Deal|2: Move Card|3: Undo|\n: ').split()
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
        if game.check_win():
            while max([len(pile) for pile in game.piles]) > 0:
                map(game.move_home, game.piles)
                print('\n', game, sep='')
                sleep(1)
            print('YOU WIN!!!!')
            break
