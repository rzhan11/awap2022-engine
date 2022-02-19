## Testing timeouts

import sys
import random
import time

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init Loopbot")
        self.turn = 0
        # time.sleep(11)
        return


    def play_turn(self, turn_num, map, player_info):
        print("turn", turn_num, player_info, player_info.time_bank)
        # if turn_num % 13 == 0:
        # time.sleep(5)
        # infinite loop
        # if turn_num % 29 == 0:
        #     x = 0
        #     while(True):
        #         x += 1
        print("Loop bot runs :D")
        return
