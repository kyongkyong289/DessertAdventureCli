import random

#Using skill spore
def spore(target_player, target_enemy):
    target_player.hp -= target_enemy.attack // 2
    target_card = random.randint(0, len(target_player.hand) - 1)
    target_player.hand[target_card][0] += 1

class Enemy:
    def __init__(self, enemy_attack, enemy_hp):
        self.attack = enemy_attack
        self.hp = enemy_hp
        self.max_hp = enemy_hp

    skill = ['attack']