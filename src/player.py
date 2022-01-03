from structure import *
from game_constants import GameConstants as GC

from enum import Enum
from abc import ABC, abstractmethod


class Team(Enum):
    NEUTRAL = -1
    RED = 0
    BLUE = 1


class PlayerInfo:

    def __init__(self, team, active=True, money=GC.PLAYER_STARTING_MONEY, utility=0.0):
        self.team = team
        self.active = active # In the game (time limit exceeded = not active)
        self.money = money
        self.utility = utility
        self.time_bank = GC.TIME_BANK
        self.bid = 0

    def __str__(self):
        return f"[T: {self.team}, M: {self.money}, U: {self.utility}, A: {self.active}]"

    def _copy(self):
        return PlayerInfo(self.team, self.active, self.money, self.utility)


class Player:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def play_turn(self, turn_num, map, my_info):
        pass

    def set_bid(self, bid):
        self._bid = bid

    def build(self, struct_type, x, y):
        self._to_build += [(struct_type, x, y)]
