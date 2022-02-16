from .structure import *
from .game_constants import GameConstants as GC

from enum import Enum
from abc import ABC, abstractmethod


class Team(Enum):
    RED = 0
    BLUE = 1


class PlayerInfo:

    def __init__(self, team, money=GC.PLAYER_STARTING_MONEY, utility=0.0,
        time_bank = GC.TURN_TIME_LIMIT * GC.NUM_ROUNDS, paused_at = None, active=True):
        self.team = team
        self.money = money
        self.utility = utility
        self.bid = 0
        self.paused_at = paused_at # Time of last timeout
        self.time_bank = time_bank
        self.active = active # Active if you haven't recently timed out

    def __str__(self):
        return f"[T: {self.team}, M: {self.money}, U: {self.utility}]"

    def _copy(self):
        return PlayerInfo(self.team, self.money, self.utility, self.time_bank, self.paused_at, self.active)


class Player:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def play_turn(self, turn_num, map, player_info):
        pass

    def set_bid(self, bid):
        self._bid = bid

    def build(self, struct_type, x, y):
        self._to_build += [(struct_type, x, y)]
