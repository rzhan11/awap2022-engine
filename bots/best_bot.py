# Hi there, and welcome to AWAP 2022 - Wifi Rumble!
# Here's the Player class file where you'll do all your coding.
# Submit this file, which will contain the implementation details of your bot,
# to the AWAP website to run it against other bots.

import sys

import random

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    # Initialize any variables, etc you might want to keep
    # track of throughout the game.
    def __init__(self):
        print("Init")

    # Play your turn by building structures, spending your money, and
    # maximizing population reached!
    def play_turn(self, turn_num, map, player_info):
        # perusing the map
        height, width = len(map), len(map[0])
        a_tile = map[0][0]
        print(a_tile.x, a_tile.y, a_tile.passability, a_tile.population)
        structure = a_tile.structure
        print(structure.x, structure.y, structure.team, structure.type)

        # checking player stats
        print(player_info.team, player_info.money)
        print(f'Served {player_info.utility} last round')

        # building a (currently illegal) structure
        x, y = 0, 0
        self.build(StructureType.ROAD, x, y)

        # bidding 0 dollars to build first on every turn
        self.set_bid(0)
