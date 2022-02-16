import sys

import random
import math
from heapq import heapify, heappop, heappush

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

        return

    def check_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

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

    def get_surround_tiles(self, x, y):
        L = [(x + dx, y + dy) for dx, dy in self.dlocs]
        return [(nx, ny) for nx, ny in L if self.check_bounds(nx, ny)]

    def check_service(self, x, y):
        for dx, dy in self.dlocs:
            (nx, ny) = (x + dx, y + dy)
            if self.check_bounds(nx, ny):
                st = self.map[nx][ny].structure
                if st is not None and st.team == self.us:
                    return True
        return False

    # tower will provide service to new tower
    def should_build_tower(self, x, y):
        for dx, dy in self.dlocs:
            (nx, ny) = (x + dx, y + dy)
            if self.check_bounds(nx, ny) and self.map[nx][ny].population > 0:
                if not self.check_service(nx, ny):
                    return True
        return False


    def play_turn(self, turn_num, map, player_info):
        print("turn", turn_num, player_info)

        self.dlocs = []
        for i in range(-GC.TOWER_RADIUS, GC.TOWER_RADIUS + 1):
            for j in range(-GC.TOWER_RADIUS, GC.TOWER_RADIUS + 1):
                if i * i + j * j <= GC.TOWER_RADIUS * GC.TOWER_RADIUS:
                    self.dlocs += [(i, j)]
        # print(self.dlocs)

        self.set_bid(turn_num % 2)

        self.us = player_info.team
        self.width = len(map)
        self.height = len(map[0])
        self.map = map

        pops = self.get_target_pops()

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
                if self.should_build_tower(x, y):
                    t = StructureType.TOWER
                else:
                    t = StructureType.ROAD
                self.build(t, x, y)
        else:
            pops = self.get_target_pops(allow_served=True)
            path = self.find_path(my_tiles, pops, map)
            if path is not None:
                for x, y in path:
                    if self.should_build_tower(x, y):
                        t = StructureType.TOWER
                    else:
                        t = StructureType.ROAD
                    self.build(t, x, y)
                # print(self._to_build[0])
        # else:
        #     self.try_random_build(my_tiles, player_info)

        return

    def get_target_pops(self, allow_served=False):
        pops = set()
        for x in range(self.width):
            for y in range(self.height):
                if self.map[x][y].population > 0:
                    if (not self.check_service(x, y)) or allow_served:
                        nearby_tiles = self.get_surround_tiles(x, y)
                        pops.update(nearby_tiles)

        if allow_served:
            print(len(pops), list(pops)[:5])

        return pops

    #
    # def defend(self, my_structs, player_info):
    #     vals = []
    #     valid_tiles = self.get_valid_tiles(my_structs)
    #     for tx, ty in valid_tiles:
    #
    #     # find closest my_struct
    #
    #     for tx, ty, cost in valid_tiles:
    #         if player_info.money >= cost:
    #             print("hi", tx, ty)
    #             self.build(build_type, tx, ty)
    #             player_info.money -= cost
    #             print(self._to_build)
    #



    ''' Helper method for trying to build a random structure'''
    def try_random_build(self, my_structs, player_info):
        # choose a type of structure to build
        build_type = StructureType.ROAD

        # identify the set of tiles that we can build on
        valid_tiles = []

        # look for a empty tile that is adjacent to one of our structs
        for x in range(self.width):
            for y in range(self.height):
                # check this tile contains one of our structures
                st = self.map[x][y].structure
                if st is None or st.team != player_info.team:
                    continue
                # check if any of the adjacent tiles are open
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    (nx, ny) = (st.x + dx, st.y + dy)
                    # check if adjacent tile is valid (on the map and empty)
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.map[nx][ny].structure is None:
                            cost = build_type.get_base_cost() * self.map[nx][ny].passability
                            # check if my team can afford this structure
                            if player_info.money >= cost:
                                # attempt to build
                                valid_tiles.append((nx, ny, cost))

        for tx, ty, cost in valid_tiles:
            if player_info.money >= cost:
                print("hi", tx, ty)
                self.build(build_type, tx, ty)
                player_info.money -= cost
        print(self._to_build)
