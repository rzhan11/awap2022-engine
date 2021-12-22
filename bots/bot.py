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



    def find_path(self, start, dest):
        prev = {start: None}
        q = [start]
        index = 0
        while index < len(q):
            state = q[index]
            if state == dest:
                path = [state]
                cur = state
                while cur != start:
                    cur = prev[cur]
                    path += [cur]

                path = path[::-1]
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = state[0] + dx, state[1] + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in prev:
                    continue
                prev[(nx, ny)] = state
                q += [(nx, ny)]


            index += 1

        return None


    def play_turn(self, turn_num, map, my_info):
        print("turn", turn_num, my_info)

        us = my_info.team
        self.width = len(map)
        self.height = len(map[0])

        gens = []
        pops = []
        for x in range(self.width):
            for y in range(self.height):
                if map[x][y].population > 0 and map[x][y].structure is None:
                    pops += [(x, y)]

                st = map[x][y].structure
                if st is not None:
                    if st.team == us and st.type == StructureType.GENERATOR:
                        gens += [(x, y)]

        if len(pops) > 0:
            dest = pops[0]
            path = self.find_path(gens[0], dest)
            for loc in path:
                if loc == dest:
                    t = StructureType.TOWER
                else:
                    t = StructureType.ROAD
                self.build(t, loc[0], loc[1])
                # print(self._to_build[0])


        return
