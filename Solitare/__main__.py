import Solitare
from copy import deepcopy
if __name__ == '__main__':
    game = Solitare.Solitare()  # Create new game
    move_stack = [deepcopy(game)]    # Create stack for undo
    input_dict = {'0': game.pile0,
                  '1': game.pile1,
                  '2': game.pile2,
                  '3': game.pile3,
                  '4': game.pile4,
                  '5': game.pile5,
                  '6': game.pile6,
                  '7': game.pile7,
                  'H1': game.home1,
                  'H2': game.home2,
                  'H3': game.home3,
                  'H4': game.home4}
    while True:  # Main Loop
        source = dest = ''
        print('\n', game, sep='')
        selection = input('|1: Deal|2: Move Card|3: Undo|\n: ').split()
        if len(selection) == 0 or selection[0] == '1':
            game.deal()
            move_stack.append(deepcopy(game))
        elif selection[0] == '2':
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
                index = 1
                if game.movepile(input_dict[source], input_dict[dest], index):
                    if source != '0':
                        input_dict[source].update()
                    move_stack.append(deepcopy(game))
            else:
                if game.movehome(input_dict[source]):
                    if source != '0':
                        input_dict[source].update()
                    move_stack.append(deepcopy(game))
        elif selection[0] == '0':
            break
        elif selection[0] == '3':
            if move_stack:
                game = move_stack.pop()
                input_dict = {'0': game.pile0,
                              '1': game.pile1,
                              '2': game.pile2,
                              '3': game.pile3,
                              '4': game.pile4,
                              '5': game.pile5,
                              '6': game.pile6,
                              '7': game.pile7,
                              'H1': game.home1,
                              'H2': game.home2,
                              'H3': game.home3,
                              'H4': game.home4}
        if game.checkwin():
            print('YOU WIN!!!!')
            break
