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

#Printing map
def print_map(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
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

    player = playerclass.Player()
    battle_mode = False

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
            window.erase()
            print_map(map_board)
            window.addstr(player.pos[0], player.pos[1] * 4 + 1, 'PPP')
            window.refresh()
            move = window.getch()
            
            #If player is trying to move upward
            if move == 96 + 23 and player.pos[0] > 0:
                if map_board[player.pos[0] - 1][player.pos[1]] == '   ':
                    player.pos[0] -= 1
                elif map_board[player.pos[0] - 1][player.pos[1]] == 'EEE':
                    player.pos[0] -= 1
                    battle_mode = True

            #If player is trying to move downward
            if move == 96 + 19 and player.pos[0] < len(map_board) - 1:
                if map_board[player.pos[0] + 1][player.pos[1]] == '   ':
                    player.pos[0] += 1
                elif map_board[player.pos[0] + 1][player.pos[1]] == 'EEE':
                    player.pos[0] += 1
                    battle_mode = True

            #If player is trying to move left
            if move == 96 + 1 and player.pos[1] > 0:
                if map_board[player.pos[0]][player.pos[1] - 1] == '   ':
                    player.pos[1] -= 1
                elif map_board[player.pos[0]][player.pos[1] - 1] == 'EEE':
                    player.pos[1] -= 1
                    battle_mode = True

            #If player is trying to move right
            if move == 96 + 4 and player.pos[1] < len(map_board[0]) - 1:
                if map_board[player.pos[0]][player.pos[1] + 1] == '   ':
                    player.pos[1] += 1
                elif map_board[player.pos[0]][player.pos[1] + 1] == 'EEE':
                    player.pos[1] += 1
                    battle_mode = True

            if move == 27:
                break

        #While player is in battle
        if battle_mode == True:
            window.erase()
            window.addstr(0, 0, 'Battle Mode!')
            window.refresh()

            move = window.getch()
            break

    curses.endwin()
    sys.exit()

#When things get wrong...
except:
    curses.endwin()
    traceback.print_exc()
    sys.exit()