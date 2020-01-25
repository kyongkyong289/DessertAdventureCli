def fireball(target_player, target_enemy):
    target_enemy.hp -= int(target_player.magic_attack * 1.5 + 5)

def firebolt(target_player, target_enemy):
    target_enemy.hp -= int(target_player.magic_attack * 1 + 3)

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
                        target_player.energy -= target_player.hand[int(command[1])][0]
                        fireball(target_player, target_enemies[int(command[2])])
                        target_player.hand.pop(int(command[1]))
        
