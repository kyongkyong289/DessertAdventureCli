class Player:
    #Player stats
    hp = 25
    max_hp = 0
    energy = 8
    max_energy = 8
    attack = 3
    magic_attack = 3
    armor = 0
    magic_armor = 0
    gold = 0
    level = 1
    exp = 0
    max_exp = 50
    max_hp_level = [0, 25, 27, 29, 32, 35]
    max_exp_level = [0, 50, 60, 70, 80, 1000000]
    pos = [0, 0]
    location = 'Village'
    skill = []
    hand = []
    deck = []
    deck_original = []
    item = []

    def __init__(self):
        self.max_exp = self.max_exp_level[1]
        self.max_hp = self.max_hp_level[1]

    def level_up(self):
        if self.level < 5:
            while self.exp >= self.max_exp_level[self.level] and self.level < 5:
                self.exp -= self.max_exp_level[self.level]
                self.level += 1
                self.max_exp = self.max_exp_level[self.level]