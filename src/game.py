'''
Game

'''

import random
import string
import math
from structure import *
from player import *
from constants import Constants
import json
from custom_json import CustomEncoder

class Tile:
    def __init__(self, x, y, population, structures):
        self.x = x
        self.y = y
        self.population = population
        self.structures = []
        self.has_preserve = False
        for s in structures:
            self._build(s)

    def _copy(self):
        return Tile(self.x, self.y, self.population, [s._copy() for s in self.structures])

    def _build(self, s):
        self.structures += [s]
        if s.type == StructureType.PRESERVE:
            self.has_preserve = True

    def _has_same_team_building(self, s):
        for s2 in self.structures:
            if s.team == s2.team:
                return True
        return False


class MapUtil:

    @classmethod
    def x_sym(self, x, y, width, height):
        return (width - 1 - x, y)

    @classmethod
    def y_sym(self, x, y, width, height):
        return (x, height - 1 - y)

    @classmethod
    def rot_sym(self, x, y, width, height):
        return (width - 1 - x, height - 1 - y)

    def get_diffs(rad2):
        max_rad = int(math.sqrt(rad2))
        diffs = []
        for di in range(-max_rad, max_rad + 1):
            for dj in range(-max_rad, max_rad + 1):
                if di * di + dj * dj <= rad2:
                    diffs += [(di, dj)]
        return diffs

    def dist(x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        return dx * dx + dy * dy


class MapInfo():
    def __init__(self, seed, width, height, sym=MapUtil.x_sym, num_cities=10, num_preserves=10):
        self.seed = seed
        self.width = width
        self.height = height
        self.sym = sym
        self.num_cities = num_cities
        self.num_preserves = num_preserves


import importlib
def import_file(module_name, file_path):
    print(module_name, file_path)
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


'''
maps are 32x32 to 64x64
Ensures that maps are symmetric (vertical/horizontal/rotational)
Currently just does horizontal symmetry
'''

class Game:

    def __init__(self, p1_path, p2_path, map_info):
        self.init_map(map_info)
        self.map_neighbors = self.init_neighbors()
        self.populated_tiles = {loc: [] for loc in self.get_populated_tiles()}
        self.tower_diffs = MapUtil.get_diffs(Constants.TOWER_RADIUS)

        self.MyPlayer1 = import_file("Player1", p1_path).MyPlayer
        self.MyPlayer2 = import_file("Player2", p2_path).MyPlayer

        self.p1 = self.MyPlayer1()
        self.p2 = self.MyPlayer2()
        self.p1_state = PlayerInfo(Team.RED)
        self.p2_state = PlayerInfo(Team.BLUE)

        self.frame_changes = []
        self.money_history = []
        self.utility_history = []

    def init_map(self, map_info):
        random.seed(map_info.seed)

        self.width = map_info.width
        self.height = map_info.height

        assert(Constants.MIN_WIDTH <= self.width <= Constants.MAX_WIDTH)
        assert(Constants.MIN_HEIGHT <= self.height <= Constants.MAX_HEIGHT)

        self.map = [[Tile(i, j, 0, []) for j in range(self.height)] for i in range(self.width)]

        for i in range(map_info.num_cities):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            x2, y2 = map_info.sym(x, y, self.width, self.height)
            pop = random.randrange(Constants.CITY_MIN_POP, Constants.CITY_MAX_POP)
            # todo: add neutral structures here
            self.map[x][y].population = pop
            self.map[x2][y2].population = pop

        for i in range(map_info.num_preserves):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            x2, y2 = map_info.sym(x, y, self.width, self.height)
            # todo: add neutral structures here
            self.map[x][y]._build(Structure(StructureType.PRESERVE, x, y, Team.NEUTRAL))
            self.map[x2][y2]._build(Structure(StructureType.PRESERVE, x2, y2, Team.NEUTRAL))

        self.simple_map = [[[tile.population, tile.structures] for tile in col] for col in self.map]



    def in_bounds(self, i, j):
        return 0 <= i < self.width and 0 <= j < self.height

    def init_neighbors(self):
        neighbors = [[[] for j in range(self.height)] for i in range(self.width)]

        for i in range(self.width):
            for j in range(self.height):
                for di, dj in Constants.MOVE_DIRS:
                    ni, nj = i + di, j + dj
                    if self.in_bounds(ni, nj):
                        neighbors[i][j] += [(ni, nj)]

        return neighbors

    def map_copy(self):
        return [[self.map[i][j]._copy() for j in range(self.height)] for i in range(self.width)]

    def get_populated_tiles(self):
        tiles = []
        for i in range(self.width):
            for j in range(self.height):
                if self.map[i][j].population > 0:
                    tiles += [(i, j)]
        return tiles

    def play_game(self):
        for turn_num in range(Constants.NUM_ROUNDS):
            self.play_turn(turn_num)

    def play_turn(self, turn_num):
        # update money, utility
        self.update_resources()

        # reset builds
        self.p1._to_build = []
        self.p2._to_build = []

        # get player turns
        self.p1.play_turn(turn_num, self.map_copy(), self.p1_state)
        self.p2.play_turn(turn_num, self.map_copy(), self.p2_state)

        # update game state based on player actions
        p1_changes = self.try_builds(self.p1._to_build, self.p1_state, Team.RED)
        p2_changes = self.try_builds(self.p2._to_build, self.p2_state, Team.BLUE)

        self.frame_changes += [p1_changes + p2_changes]
        self.money_history += [(self.p1_state.money, self.p2_state.money)]
        self.utility_history += [(self.p1_state.utility, self.p2_state.utility)]

    def update_resources(self):
        self.p1_state.money += Constants.PLAYER_BASE_INCOME
        self.p2_state.money += Constants.PLAYER_BASE_INCOME

        for (x, y), towers in self.populated_tiles.items():
            tile = self.map[x][y]
            for tow in towers:
                score = tile.population / len(tow)
                if tow.team == Team.RED:
                    self.p1_state.money += score
                    self.p1_state.utility += score
                elif tow.team == Team.BLUE:
                    self.p1_state.money += score
                    self.p2_state.utility += score

    def try_builds(self, builds, p_state, team):
        new_builds = []
        structures = [Structure(struct_type, x, y, team) for (struct_type, x, y) in builds]
        for s in structures:
            # check if can build
            if self.can_build(s) and p_state.money >= s.type.get_cost():
                p_state.money -= s.type.get_cost()
                self.map[s.x][s.y]._build(s)
                new_builds += [builds]
                # add towers to populated tiles (for our updates on our side)
                if s.type == StructureType.TOWER:
                    for (dx, dy) in self.tower_diffs:
                        nx, ny = x + dx, y + dy
                        if (nx, ny) in self.populated_tiles:
                            self.populated_tiles[(nx, ny)] += [s]
        return new_builds


    # check if is blocked by preserve, position in bounds, blocked by other buildings
    # potential todo: distance requirement from other towers
    def can_build(self, s):
        # not in bounds or not buildable
        if not self.in_bounds(s.x, s.y) or not s.type.get_can_build():
            return False
        # not blocked by preserve
        t = self.map[s.x][s.y]
        if t.has_preserve:
            return False
        # not blocked by other buildings
        if t._has_same_team_building(s):
            return False
        return True


    def save_replay(self, save_dir):
        random.seed()
        id = random.randint(1e6, 1e7 - 1)
        with open(f"{save_dir}/replay-{id}.awap22", "w") as f:
            obj = {
                "map": self.simple_map,
                "frame_changes": self.frame_changes,
                "money_history": self.money_history,
                "utility_history": self.utility_history
            }
            json.dump(obj, f, cls=CustomEncoder)
