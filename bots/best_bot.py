# Hi there, and welcome to AWAP 2022 - Wifi Rumble!
# Here's the Player class file where you'll do all your coding.
# Submit this file, which will contain the implementation details of your bot,
# to the AWAP website to run it against other bots.

import sys
sys.path.insert(1, "../src")

import random

from player import *
from structure import *
from game_constants import GameConstants as GC

class MyPlayer(Player):

    # Initialize any variables, etc you might want to keep
    # track of throughout the game.
    def __init__(self):
        print("Init")
        self.turn = 0

    # Play your turn by building structures, spending your money, and
    # maximizing population reached!
    def play_turn(self, turn_num, map, my_info):
        height, width = len(map), len(map[0])
        tile = map[0][0]
        print(tile.x, tile.y, tile.passability, tile.population)
        structure = tile.structure
        print(structure.x, structure.y, structure.team, structure.type)
        
        # building a (currently illegal) structure
        x, y = 0, 0
        self.build(StructureType.ROAD, x, y)
