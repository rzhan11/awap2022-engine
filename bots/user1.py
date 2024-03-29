import sys

import random
import time

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return



    def find_path(self, starts, dests, blocked_tiles):
        prev = {s: None for s in starts}
        q = list(starts)
        index = 0
        while index < len(q):
            state = q[index]
            if state in dests:
                path = [state]
                cur = state
                while cur not in starts:
                    cur = prev[cur]
                    path += [cur]

                path = path[::-1]
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = state[0] + dx, state[1] + dy
                # in bounds and not already visited
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in prev:
                    continue
                if (nx, ny) in blocked_tiles:
                    continue

                prev[(nx, ny)] = state
                q += [(nx, ny)]


            index += 1

        return None


    def play_turn(self, turn_num, map, player_info):
        print("turn", turn_num, player_info)
        # Test Timer: if turn_num % 5 == 0: time.sleep(5)
        self.us = player_info.team
        self.width = len(map)
        self.height = len(map[0])

        self.set_bid(turn_num % 3)

        gens = []
        pops = []
        for x in range(self.width):
            for y in range(self.height):
                if map[x][y].population > 0 and map[x][y].structure is None:
                    pops += [(x, y)]

                st = map[x][y].structure
                if st is not None:
                    if st.team == self.us and st.type == StructureType.GENERATOR:
                        gens += [(x, y)]

        my_tiles = set()
        blocked_tiles = set()
        for x in range(self.width):
            for y in range(self.height):
                st = map[x][y].structure
                if st is not None:
                    if st.team == self.us:
                        my_tiles.add((x, y))
                    else:
                        blocked_tiles.add((x, y))


        path = self.find_path(my_tiles, pops, blocked_tiles)
        if path is not None:
            for x, y in path:
                if map[x][y].population > 0:
                    t = StructureType.TOWER
                else:
                    t = StructureType.ROAD
                self.build(t, x, y)
                # print(self._to_build[0])

        return
