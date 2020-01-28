#Drawing cards
def draw_card(target_player):
    if len(target_player.deck) > 0:
        temp = target_player.deck.pop(0)
        target_player.hand.append(temp)

def firepunch(target_player, target_enemy):
    target_enemy.hp -= int(target_player.attack * 1 + 4)

def use_skill(command, target_player, target_enemy_list):
    if len(command) > 1:
        if int(command[1]) <= len(target_player.skill):
            if target_player.energy >= target_player.skill[int(command[1])][0] and target_player.skill[int(command[1])][3] == 0:
                if target_player.skill[int(command[1])][2] == 'draw':
                    target_player.energy -= target_player.skill[int(command[1])][0]
                    draw_card(target_player)
                    target_player.skill[int(command[1])][3] = target_player.skill[int(command[1])][4]
                if target_player.skill[int(command[1])][2] == 'firepunch':
                    if len(command) > 2:
                        if int(command[2]) <= len(target_enemy_list):
                            target_player.energy -= target_player.skill[int(command[1])][0]
                            firepunch(target_player, target_enemy_list[int(command[2])])
                            target_player.skill[int(command[1])][3] = target_player.skill[int(command[1])][4]