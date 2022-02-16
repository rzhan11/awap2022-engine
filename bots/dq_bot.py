## Bot which takes the place of a DQ'ed player

import sys

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init DQ Bot")
        self.turn = 0
        return


    def play_turn(self, turn_num, map, player_info):
        print(f"[DQ Bot] {player_info.team} DQ'ed")
        return
