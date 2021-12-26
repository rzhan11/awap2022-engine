import sys
sys.path.insert(1, "../src")

import random
from heapq import heapify, heappop, heappush

from player import *
from structure import *
from game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return


    def find_path(self, starts, dests, map):
        prev = {s: None for s in starts}
        best_dist = {s: 0 for s in starts}
        q = [(0, s) for s in starts]
        while len(q) > 0:
            cur_dist, cur_loc = heappop(q)
            if cur_loc in dests:
                path = [cur_loc]
                cur = cur_loc
                while cur not in starts:
                    cur = prev[cur]
                    path += [cur]

                path = path[::-1]
                return path

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = cur_loc[0] + dx, cur_loc[1] + dy
                # in bounds and not blocked
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if map[nx][ny].structure is not None:
                    continue
                # is better distance
                new_dist = cur_dist + map[nx][ny].passability
                if (nx, ny) in best_dist and new_dist >= best_dist[(nx, ny)]:
                    continue

                prev[(nx, ny)] = cur_loc
                best_dist[(nx, ny)] = new_dist
                heappush(q, (new_dist, (nx, ny)))



        return None


    def play_turn(self, turn_num, map, my_info):
        print("turn", turn_num, my_info)

        self.us = my_info.team
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
                    if st.team == self.us and st.type == StructureType.GENERATOR:
                        gens += [(x, y)]

        # find starting tiles
        my_tiles = set()
        for x in range(self.width):
            for y in range(self.height):
                st = map[x][y].structure
                if st is not None:
                    if st.team == self.us:
                        my_tiles.add((x, y))


        path = self.find_path(my_tiles, pops, map)
        if path is not None:
            for x, y in path:
                if map[x][y].population > 0:
                    t = StructureType.TOWER
                else:
                    t = StructureType.ROAD
                self.build(t, x, y)
                # print(self._to_build[0])

        return
