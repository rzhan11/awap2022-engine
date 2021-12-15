from structure import *
from game_constants import GameConstants as GC

from enum import Enum
from abc import ABC, abstractmethod


class Team(Enum):
    NEUTRAL = -1
    RED = 0
    BLUE = 1


class PlayerInfo:

    def __init__(self, team, money=GC.PLAYER_STARTING_MONEY, utility=0.0):
        self.team = team
        self.money = money
        self.utility = utility

    def __str__(self):
        return f"[T: {self.team}, M: {self.money}, U: {self.utility}]"

    def _copy(self):
        return PlayerInfo(self.team, self.money, self.utility)


class Player:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def play_turn(self, turn_num, map, my_info):
        pass

    def build(self, struct_type, x, y):
        self._to_build += [(struct_type, x, y)]
