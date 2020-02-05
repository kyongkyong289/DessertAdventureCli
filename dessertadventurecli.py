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
from Resource import skilldata
from Resource import mapdata

#Drawing cards
def draw_card(target_player):
    if len(target_player.deck) > 0:
        temp = target_player.deck.pop(0)
        target_player.hand.append(temp)

#Printing map
def print_map(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'EEE':
                window.addstr(i, j * 4 + 1, board[i][j], curses.color_pair(2))
            elif board[i][j] == '$$$':
                window.addstr(i, j * 4 + 1, board[i][j], curses.color_pair(3))
            elif board[i][j] == '@@@':
                window.addstr(i, j * 4 + 1, board[i][j], curses.color_pair(5))
            else:
                window.addstr(i, j * 4 + 1, board[i][j])
            window.addstr(i, j * 4, "|")

        window.addstr(i, len(board[0]) * 4, "|")

    for i in range(0, 70):
        window.addstr(15, i, '=')

    window.addstr(16, 1, str(player.location))

#Printing player status
def print_status(target_player):
    hp_percent = int(target_player.hp / target_player.max_hp * 100)
    energy_percent = int(target_player.energy / target_player.max_energy * 100)
    exp_percent = int(target_player.exp / target_player.max_exp * 100)

    window.addstr(1, 51, 'HP ' + str(target_player.hp) + '/' + str(target_player.max_hp))
    window.addstr(2, 51, '(')
    window.addstr(2, 63, ')')

    if hp_percent != 0:
        for i in range(hp_percent // 10 + 1):
            if hp_percent > 30:
                window.addstr(2, 52 + i, '=', curses.color_pair(4))
            else:
                window.addstr(2, 52 + i, '=', curses.color_pair(2))

    window.addstr(3, 51, 'Energy ' + str(target_player.energy) + '/' + str(target_player.max_energy))
    window.addstr(4, 51, '(')
    window.addstr(4, 63, ')')

    if energy_percent != 0:
        for i in range(energy_percent // 10 + 1):
            window.addstr(4, 52 + i, '=', curses.color_pair(5))

    window.addstr(7, 51, '(')
    window.addstr(7, 63, ')')
    window.addstr(6, 51, 'Exp ' + str(target_player.exp) + '/' + str(target_player.max_exp) + ' ' + str(exp_percent) + '%')
    window.addstr(5, 51, 'Lv. ' + str(target_player.level))

    if exp_percent != 0:
        for i in range(exp_percent // 10 + 1):
            window.addstr(7, 52 + i, '=', curses.color_pair(3))

    window.addstr(8, 51, 'Gold ')
    window.addstr(8, 56, str(target_player.gold) + 'G', curses.color_pair(3))

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
            window.addstr(14, 15 * i + 1, str(target_player.hand[i][2]))
        else:
            window.addstr(15, 15 * (i - 4) + 1, str(target_player.hand[i][0]))
            window.addstr(16, 15 * (i - 4) + 1, str(target_player.hand[i][2]))

    for i in range(0, 60):
        window.addstr(17, i, '=')

    #Printing skill
    window.addstr(0, 60, 'Skills')

    for i in range(len(target_player.skill)):
        window.addstr(1 + 5 * i, 60, str(player.skill[i][0]))
        window.addstr(2 + 5 * i, 60, str(player.skill[i][2]))
        window.addstr(3 + 5 * i, 60, 'Cooldown')
        window.addstr(4 + 5 * i, 60, str(player.skill[i][3]) + '/' + str(player.skill[i][4]))

    for i in range(60, 80):
        window.addstr(5, i, '=')

    window.addstr(5, 59, '#')

    #Printing items
    for i in range(60, 80):
        window.addstr(10, i, '=')

    window.addstr(11, 60, 'Item')

    for i in range(len(target_player.item)):
        window.addstr(12 + i, 60, str(target_player.item[i]))

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

def print_shop(item_list, scroll):
    window.addstr(1, 2, '#')
    window.addstr(1, 38, '#')
    window.addstr(10, 2, '#')
    window.addstr(10, 38, '#')

    for i in range(2, 10):
        window.addstr(i, 2, '|')
        window.addstr(i, 38, '|')

    for i in range(3, 38):
        window.addstr(1, i, '=')
        window.addstr(10, i, '=')

    for i in range(2, 10):
        for j in range(3, 38):
            window.addstr(i, j, ' ')

    window.addstr(2, 4, 'SHOP')

    for i in range(6):
        if i + scroll < len(item_list):
            window.addstr(3 + i, 4, str(i) + '. ' + str(item_list[i + scroll][1]))
            window.addstr(3 + i, 30, str(item_list[i + scroll][0]) + 'G', curses.color_pair(3))

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

    #Declaring shop
    shop_item_list = [[25, 'strawberry_juice'], [30, 'lemonade'], [45, 'blueberry_juice'], [25, 'strawberry_juice'], [30, 'lemonade'], [45, 'blueberry_juice'], 
                      [35, 'grape_juice'], [30, 'lemonade'], [45, 'blueberry_juice'], [25, 'strawberry_juice'], [30, 'lemonade'], [45, 'blueberry_juice'],
                      [45, 'banana_juice']]
    shop_scroll = 0

    #Setting player's hand and deck
    player.hand = []
    player.deck = [[6, 6, 'firestorm'], [2, 2, 'fireball'], [2, 2, 'fireball'], [1, 1, 'firebolt'], [1, 1, 'firebolt'], [1, 1, 'firebolt']]

    player.gold = 10000
    player.skill = [[0, 0, 'draw', 0, 1], [2, 2, 'firepunch', 0, 2]]

    map_board = [['   ', '   ', '   ', '   ', '@@@', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '$$$', '   ', '   ', '   ', '$$$', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['@@@', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '@@@'],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '$$$', '   ', '   ', '   ', '$$$', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   '],
                 ['   ', '   ', '   ', '   ', '@@@', '   ', '   ', '   ', '   ']]

    temp = []

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

            #If player is trying to enter portal
            if move == 96 + 5 and map_board[player.pos[0]][player.pos[1]] == '@@@':
                if player.location == 'Village':
                    player.location = 'Forest'
                    map_board = []
                    for i in range(len(mapdata.forest_1)):
                        for j in range(len(mapdata.forest_1[0])):
                            temp += [mapdata.forest_1[i][j]]
                        map_board += [temp]
                        temp = []
                    player.pos[0] = 8
                    player.pos[1] = 4
                    continue
                    
                if player.location == 'Forest':
                    player.location = 'Village'
                    map_board = []
                    for i in range(len(mapdata.village)):
                        for j in range(len(mapdata.village[0])):
                            temp += [mapdata.village[i][j]]
                        map_board += [temp]
                        temp = []
                    player.pos[0] = 0
                    player.pos[1] = 4
                    
            #If player is trying to exit
            if move == 27:
                curses.endwin()
                sys.exit()

            if map_board[player.pos[0]][player.pos[1]] == 'EEE':
                battle_mode = True
                battle_initiated = False

            if map_board[player.pos[0]][player.pos[1]] == '$$$':
                #Shop
                while 1:
                    curses.echo()
                    curses.nocbreak()
                    window.erase()
                    print_map(map_board)
                    print_status(player)
                    print_shop(shop_item_list, shop_scroll)
                    window.refresh()
                    window.move(12, 3)

                    command = list(map(str, window.getstr().decode(encoding = 'utf-8').split()))

                    #Checking command
                    if len(command) > 0:
                        if command[0] == 'exit':
                            curses.endwin()
                            sys.exit()

                        if command[0] == 'prev' and shop_scroll > 0:
                            shop_scroll -= 6

                        if command[0] == 'next' and shop_scroll <= len(shop_item_list) - 7:
                            shop_scroll += 6

                        if command[0] == 'buy':
                            if len(command) > 1:
                                if command[1] == '0' and player.gold >= shop_item_list[shop_scroll + 0][0]:
                                    player.gold -= shop_item_list[shop_scroll + 0][0]
                                    player.item += [shop_item_list[shop_scroll + 0][1]]

                                if command[1] == '1' and player.gold >= shop_item_list[shop_scroll + 1][0]:
                                    player.gold -= shop_item_list[shop_scroll + 1][0]
                                    player.item += [shop_item_list[shop_scroll + 1][1]]

                                if command[1] == '2' and player.gold >= shop_item_list[shop_scroll + 2][0]:
                                    player.gold -= shop_item_list[shop_scroll + 2][0]
                                    player.item += [shop_item_list[shop_scroll + 2][1]]

                                if command[1] == '3' and player.gold >= shop_item_list[shop_scroll + 3][0]:
                                    player.gold -= shop_item_list[shop_scroll + 3][0]
                                    player.item += [shop_item_list[shop_scroll + 3][1]]

                                if command[1] == '4' and player.gold >= shop_item_list[shop_scroll + 4][0]:
                                    player.gold -= shop_item_list[shop_scroll + 4][0]
                                    player.item += [shop_item_list[shop_scroll + 4][1]]

                                if command[1] == '5' and player.gold >= shop_item_list[shop_scroll + 5][0]:
                                    player.gold -= shop_item_list[shop_scroll + 5][0]
                                    player.item += [shop_item_list[shop_scroll + 5][1]]

                        if command[0] == 'end':
                            break

        #While player is in battle
        if battle_mode == True:
            #Starting battle
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

                for i in range(len(player.skill)):
                    player.skill[i][3] = 0

                battle_initiated = True

            #Deleting enemies which health is below zero
            i = 0

            while i < len(enemy_list):
                if enemy_list[i].hp <= 0:
                    enemy_list.pop(i)
                else:
                    i = i + 1

            #Ending battle
            if len(enemy_list) == 0:
                window.erase()
                print_battle(player, enemy_list)
                print_win(10, 10)
                window.refresh()
                curses.cbreak()
                curses.curs_set(0)

                player.exp += 10
                player.gold += 10
                a = window.getch()
                battle_mode = False
                map_board[player.pos[0]][player.pos[1]] = '   '

                for i in range(len(player.hand)):
                    temp = player.hand.pop(0)
                    player.deck.append(temp)
                    temp = []
            
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

            #Checking command
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

                if command[0] == 'exit':
                    curses.endwin()
                    sys.exit()

                if command[0] == 'usecard':
                    carddata.use_card(command, player, enemy_list)

                if command[0] == 'useskill':
                    skilldata.use_skill(command, player, enemy_list)
                    
                if command[0] == 'cheat':
                    enemy_list = []

    curses.endwin()
    sys.exit()

#When things get wrong...
except:
    curses.endwin()
    print(map_board)
    traceback.print_exc()
    sys.exit()
