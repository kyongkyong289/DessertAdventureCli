#Importing modules
import os
import sys
import curses
import traceback
import random
import time

#Importing game data
from Resource import carddata
from Resource import playerclass
from Resource import enemyclass

#Printing map
def print_map(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'EEE':
                window.addstr(i, j * 4 + 1, board[i][j], curses.color_pair(2))
            else:
                window.addstr(i, j * 4 + 1, board[i][j])
            window.addstr(i, j * 4, "|")
        window.addstr(i, len(board[0]) * 4, "|")

try:
    #Setting curses
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    window.keypad(True)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    player = playerclass.Player()
    battle_mode = False
    battle_initiated = False

    map_board = [['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', 'EEE', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', 'EEE', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', 'EEE', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']]

    #On screen
    while 1:
        if battle_mode == False:
            curses.cbreak()
            curses.noecho()
            window.erase()
            print_map(map_board)
            window.addstr(player.pos[0], player.pos[1] * 4 + 1, 'PPP', curses.color_pair(4))
            window.refresh()
            move = window.getch()
            
            #If player is trying to move upward
            if move == 96 + 23 and player.pos[0] > 0:
                if map_board[player.pos[0] - 1][player.pos[1]] == '   ':
                    player.pos[0] -= 1
                elif map_board[player.pos[0] - 1][player.pos[1]] == 'EEE':
                    player.pos[0] -= 1
                    battle_mode = True
                    battle_initiated = False

            #If player is trying to move downward
            if move == 96 + 19 and player.pos[0] < len(map_board) - 1:
                if map_board[player.pos[0] + 1][player.pos[1]] == '   ':
                    player.pos[0] += 1
                elif map_board[player.pos[0] + 1][player.pos[1]] == 'EEE':
                    player.pos[0] += 1
                    battle_mode = True
                    battle_initiated = False

            #If player is trying to move left
            if move == 96 + 1 and player.pos[1] > 0:
                if map_board[player.pos[0]][player.pos[1] - 1] == '   ':
                    player.pos[1] -= 1
                elif map_board[player.pos[0]][player.pos[1] - 1] == 'EEE':
                    player.pos[1] -= 1
                    battle_mode = True
                    battle_initiated = False

            #If player is trying to move right
            if move == 96 + 4 and player.pos[1] < len(map_board[0]) - 1:
                if map_board[player.pos[0]][player.pos[1] + 1] == '   ':
                    player.pos[1] += 1
                elif map_board[player.pos[0]][player.pos[1] + 1] == 'EEE':
                    player.pos[1] += 1
                    battle_mode = True
                    battle_initiated = False

            if move == 27:
                break

        #While player is in battle
        if battle_mode == True:
            if battle_initiated == False:
                enemy0 = enemyclass.Enemy(3, 12)
                enemy1 = enemyclass.Enemy(3, 12)
                battle_initiated = True

            if enemy0.hp <= 0  and enemy1.hp <= 0:
                battle_mode = False
                map_board[player.pos[0]][player.pos[1]] = '   '
                continue
                
            #Printing lines
            curses.nocbreak()
            curses.echo()
            window.erase()
            window.addstr(2, 2, 'PPP')
            window.addstr(2, 30, 'EEE')
            window.addstr(2, 35, 'EEE')
            window.addstr(1, 0, 'HP : ' + str(player.hp) + '/' + str(player.max_hp))
            window.addstr(1, 28, str(enemy0.hp) + '/' + str(enemy0.max_hp))
            window.addstr(1, 33, str(enemy1.hp) + '/' + str(enemy1.max_hp))
            window.move(4, 1)
            window.refresh()

            #Getting command
            command = list(map(str, window.getstr().decode(encoding = 'utf-8').split()))

            window.addstr(5, 0, str(command))

            if command[0] == 'attack':
                if command[1] == '0':
                    enemy0.hp -= player.attack
                elif command[1] == '1':
                    enemy1.hp -= player.attack

            if command[0] == 'exit':
                break

    curses.endwin()
    sys.exit()

#When things get wrong...
except:
    curses.endwin()
    traceback.print_exc()
    sys.exit()