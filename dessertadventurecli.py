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

#Drawing cards
def draw_card(target_player):
    if len(target_player.deck) > 0:
        temp = target_player.deck.pop(0)
        target_player.hand.append(temp)

#Printing player status
def print_status(target_player):
    hp_percent = int(target_player.hp / target_player.max_hp * 100)
    energy_percent = int(target_player.energy / target_player.max_energy * 100)
    window.addstr(1, 41, 'HP ' + str(target_player.hp) + '/' + str(target_player.max_hp))
    window.addstr(2, 41, '(')
    window.addstr(2, 53, ')')
    if hp_percent != 0:
        for i in range(hp_percent // 10 + 1):
            if hp_percent > 30:
                window.addstr(2, 42 + i, '=', curses.color_pair(4))
            else:
                window.addstr(2, 42 + i, '=', curses.color_pair(2))

    window.addstr(3, 41, 'Energy ' + str(target_player.energy) + '/' + str(target_player.max_energy))
    window.addstr(4, 41, '(')
    window.addstr(4, 53, ')')
    if energy_percent != 0:
        for i in range(energy_percent // 10 + 1):
            window.addstr(4, 42 + i, '=', curses.color_pair(5))

#Printing battle scene
def print_battle(target_player, target_enemy_list):
    hp_percent = int(target_player.hp / target_player.max_hp * 100)
    energy_percent = int(target_player.energy / target_player.max_energy * 100)

    window.addstr(0, 0, '#')
    window.addstr(0, 59, '#')
    window.addstr(10, 0, '#')
    window.addstr(10, 59, '#')
    for i in range(1, 59):
        window.addstr(0, i, '=')
        window.addstr(10, i, '=')
    for i in range(1, 10):
        window.addstr(i, 0, '|')
        window.addstr(i, 59, '|')
    window.addstr(11, 0, '>')

    window.addstr(3, 2, 'PPP')

    #Printing enemies
    for i in range(len(target_enemy_list)):
        if i < 3:
            window.addstr(1 + 3 * i, 25, str(i) + '. EEE')
            window.addstr(2 + 3 * i, 25, str(target_enemy_list[i].hp) + '/' + str(target_enemy_list[i].max_hp))
        if i >= 3:
            window.addstr(1 + 3 * (i - 3), 40, str(i) + '. EEE')
            window.addstr(2 + 3 * (i - 3), 40, str(target_enemy_list[i].hp) + '/' + str(target_enemy_list[i].max_hp))

    #Printing hand
    for i in range(0, 60):
        window.addstr(12, i, '=')
    for i in range(len(target_player.hand)):
        if i < 4:
            window.addstr(13, 15 * i + 1, str(target_player.hand[i][0]))
            window.addstr(14, 15 * i + 1, str(target_player.hand[i][1]))
        else:
            window.addstr(15, 15 * (i - 4) + 1, str(target_player.hand[i][0]))
            window.addstr(16, 15 * (i - 4) + 1, str(target_player.hand[i][1]))

    for i in range(0, 60):
        window.addstr(17, i, '=')

    #Printing hp, energy bars
    window.addstr(18, 1, 'HP : ' + str(target_player.hp) + '/' + str(target_player.max_hp))
    window.addstr(18, 31, 'Energy : ' + str(target_player.energy) + '/' + str(target_player.max_energy))
    if hp_percent != 0:
        for i in range(hp_percent // 5 + 1):
            if hp_percent > 30:
                window.addstr(19, 2 + i, '=', curses.color_pair(4))
            else:
                window.addstr(19, 2 + i, '=', curses.color_pair(2))

    if energy_percent != 0:
        for i in range(energy_percent // 5 + 1):
            window.addstr(19, 32 + i, '=', curses.color_pair(5))

    window.addstr(19, 1, '(')
    window.addstr(19, 23, ')')
    window.addstr(19, 31, '(')
    window.addstr(19, 53, ')')

#Printing win window
def print_win(target_gold, target_exp):
    window.addstr(2, 10, '#')
    window.addstr(2, 49, '#')
    window.addstr(8, 10, '#')
    window.addstr(8, 49, '#')
    for i in range(11, 49):
        window.addstr(2, i, '=')
        window.addstr(8, i, '=')
    for i in range(3, 8):
        window.addstr(i, 10, '|')
        window.addstr(i, 49, '|')
    for i in range(3, 8):
        for j in range(11, 49):
            window.addstr(i, j, ' ')
    window.addstr(3, 12, 'You win!')
    window.addstr(4, 12, 'You got ' + str(target_gold) + ' gold.')
    window.addstr(5, 12, 'You got ' + str(target_exp) + ' exp.')
    window.addstr(6, 12, 'Press any key to continue.')

try:
    #Setting curses
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    window.keypad(True)

    #Setting color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    #Declaring player class
    player = playerclass.Player()
    
    #Setting global flags
    battle_mode = False
    battle_initiated = False

    #Declaring enemy list
    enemy_list = []

    #Setting player's hand and deck
    player.hand = []
    player.deck = [[6, 'firestorm'], [2, 'fireball'], [2, 'fireball'], [1, 'firebolt'], [1, 'firebolt'], [1, 'firebolt']]

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
            curses.curs_set(0)
            window.erase()
            print_map(map_board)
            print_status(player)
            window.addstr(player.pos[0], player.pos[1] * 4 + 1, 'PPP', curses.color_pair(4))
            window.refresh()
            move = window.getch()
            
            #If player is trying to move upward
            if move == 96 + 23 and player.pos[0] > 0:
                if map_board[player.pos[0] - 1][player.pos[1]] != 'WWW':
                    player.pos[0] -= 1

            #If player is trying to move downward
            if move == 96 + 19 and player.pos[0] < len(map_board) - 1:
                if map_board[player.pos[0] + 1][player.pos[1]] != 'WWW':
                    player.pos[0] += 1

            #If player is trying to move left
            if move == 96 + 1 and player.pos[1] > 0:
                if map_board[player.pos[0]][player.pos[1] - 1] != 'WWW':
                    player.pos[1] -= 1

            #If player is trying to move right
            if move == 96 + 4 and player.pos[1] < len(map_board[0]) - 1:
                if map_board[player.pos[0]][player.pos[1] + 1] != 'WWW':
                    player.pos[1] += 1

            #If player is trying to exit
            if move == 27:
                break

            if map_board[player.pos[0]][player.pos[1]] == 'EEE':
                battle_mode = True
                battle_initiated = False

        #While player is in battle
        if battle_mode == True:
            if battle_initiated == False:
                enemy0 = enemyclass.Enemy(3, 12)
                enemy1 = enemyclass.Enemy(3, 12)
                enemy2 = enemyclass.Enemy(3, 12)
                enemy3 = enemyclass.Enemy(4, 10)
                enemy4 = enemyclass.Enemy(4, 10)
                enemy_list = [enemy0, enemy1, enemy2, enemy3, enemy4]
                random.shuffle(player.deck)
                for i in range(3):
                    draw_card(player)
                battle_initiated = True

            i = 0
            while i < len(enemy_list):
                if enemy_list[i].hp <= 0:
                    enemy_list.pop(i)
                else:
                    i = i + 1

            if len(enemy_list) == 0:
                window.erase()
                print_battle(player, enemy_list)
                print_win(10, 10)
                window.refresh()

                curses.cbreak()
                curses.curs_set(0)
                a = window.getch()
                battle_mode = False
                map_board[player.pos[0]][player.pos[1]] = '   '
                for i in range(len(player.hand)):
                    temp = player.hand.pop(0)
                    player.deck.append(temp)
                continue
                
            #Printing lines
            curses.nocbreak()
            curses.echo()
            curses.curs_set(1)
            window.erase()
            print_battle(player, enemy_list)
            window.move(11, 2)
            window.refresh()

            #Getting command
            command = list(map(str, window.getstr().decode(encoding = 'utf-8').split()))
            if len(command) > 0:
                if command[0] == 'attack':
                    if len(command) > 1:
                        if command[1] == '0' and len(enemy_list) > 0:
                            enemy_list[0].hp -= player.attack
                        if command[1] == '1' and len(enemy_list) > 1:
                            enemy_list[1].hp -= player.attack
                        if command[1] == '2' and len(enemy_list) > 2:
                            enemy_list[2].hp -= player.attack
                        if command[1] == '3' and len(enemy_list) > 3:
                            enemy_list[3].hp -= player.attack
                        if command[1] == '4' and len(enemy_list) > 4:
                            enemy_list[4].hp -= player.attack

                if command[0] == 'draw':
                    draw_card(player)

                if command[0] == 'exit':
                    break

                if command[0] == 'usecard':
                    carddata.use_card(command, player, enemy_list)

    curses.endwin()
    sys.exit()

#When things get wrong...
except:
    curses.endwin()
    traceback.print_exc()
    sys.exit()
