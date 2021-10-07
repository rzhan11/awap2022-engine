import sys
sys.path.insert(1, "../src")

from player import *
from constants import *

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return

    def play_turn(self, turn_num, map, my_info):
        print("turn", self.turn, my_info)
        self.build(StructureType.GENERATOR, 1, 1)
        self.turn += 1
        return
