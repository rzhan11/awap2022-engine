import sys
sys.path.insert(1, "../src")

import random

from player import *
from structure import *
from game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return

    def play_turn(self, turn_num, map, my_info):
        print("turn", turn_num, my_info)

        width = len(map)
        height = len(map[0])

        x, y = random.randrange(0, width), random.randrange(0, height)
        self.build(StructureType.ROAD, x, y)


        return
