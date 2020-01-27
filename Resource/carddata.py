#Using fireball
def fireball(target_player, target_enemy):
    target_enemy.hp -= int(target_player.magic_attack * 1.5 + 5)

#Using firebolt
def firebolt(target_player, target_enemy):
    target_enemy.hp -= int(target_player.magic_attack * 1 + 3)

#Using firestrom
def firestorm(target_player, target_enemy_list):
    for i in range(len(target_enemy_list)):
        target_enemy_list[i].hp -= int(target_player.magic_attack * 5 + 4)

#Command of using card
#usecard a b
#a means ath card of your hand
#b means target enemy

def use_card(command, target_player, target_enemies):
    if len(command) > 1:
        if int(command[1]) <= len(target_player.hand) - 1:
            if target_player.energy >= target_player.hand[int(command[1])][0]:
                if target_player.hand[int(command[1])][1] == 'fireball':
                    if len(command) > 2:
                        if int(command[2]) <= len(target_enemies) - 1:
                            target_player.energy -= target_player.hand[int(command[1])][0]
                            fireball(target_player, target_enemies[int(command[2])])
                            target_player.hand.pop(int(command[1]))
                if target_player.hand[int(command[1])][1] == 'firebolt':
                    if len(command) > 2:
                        if int(command[2]) <= len(target_enemies) - 1:
                            target_player.energy -= target_player.hand[int(command[1])][0]
                            firebolt(target_player, target_enemies[int(command[2])])
                            target_player.hand.pop(int(command[1]))
                if target_player.hand[int(command[1])][1] == 'firestorm':
                    target_player.energy -= target_player.hand[int(command[1])][0]
                    firestorm(target_player, target_enemies)
                    target_player.hand.pop(int(command[1]))