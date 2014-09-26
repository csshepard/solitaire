__author__ = 'chris'
import Solitare
import os
from copy import deepcopy
if __name__ == '__main__':
    game = Solitare.Solitare()  # Create new game
    move_stack = []    # Create stack for undo
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
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
        print(game)
        selection = input('|1: Deal|2: Move Card|3: Undo|\n: ')
        if selection == '1' or selection == '':
            move_stack.append(deepcopy(game))
            game.deal3()
        elif selection == '2':
            move_stack.append(deepcopy(game))
            while True:
                source = input('Source Card\n|0: Available Card|1-7: Piles|H1-H4: Home Piles|\n: ')
                if source in input_dict:
                    break
            while True:
                dest = input('Destination Pile\n|1-7: Piles|H: Home Piles|\n: ')
                if dest != '0' and (dest in input_dict or dest == 'H'):
                    break
            if dest < '8':
                index = 1
                if source != '0' and source < '8':
                    if not input_dict[source].flip == len(input_dict[source]) - 1:
                        while True:
                            index_str = input('How Many Cards to move: ')
                            if index_str == '':
                                index = 0
                                break
                            elif index_str.isnumeric():
                                index = int(index_str)
                                break
                if game.movepile(input_dict[source], input_dict[dest], index):
                    if source != '0':
                        input_dict[source].update()
            else:
                if game.movehome(input_dict[source]):
                    if source != '0':
                        input_dict[source].update()
        elif selection == '0':
            break
        elif selection == '3':
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