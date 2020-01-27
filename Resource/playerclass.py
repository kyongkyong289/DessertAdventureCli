class Player:
    #Player stats
    hp = 25
    max_hp = 25
    energy = 8
    max_energy = 8
    attack = 3
    magic_attack = 3
    armor = 0
    magic_armor = 0
    gold = 0
    level = 1
    exp = 0
    max_exp_level = [0, 50, 60, 70, 80, 100]
    max_exp = 25
    pos = [0, 0]
    skill = [[0, 'draw', 0, 1], [2, 'firepunch', 0, 2]]
    hand = []
    deck = []
    deck_original = []
    item = []

    def __init__(self):
        self.max_exp = self.max_exp_level[1]