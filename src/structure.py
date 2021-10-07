from enum import Enum
from team import *

class StructureInfo:
    def __init__(self, id, name, cost, can_build):
        self.id = id
        self.name = name
        self.cost = cost
        self.can_build = can_build

class StructureType(Enum):
    GENERATOR = StructureInfo(
            id=0,
            name="Generator",
            cost=1000,
            can_build=False
        )
    ROAD = StructureInfo(
            id=1,
            name="Road",
            cost=10,
            can_build=True
        )
    TRANSFORMER = StructureInfo(
            id=2,
            name="Transformer",
            cost=50,
            can_build=True
        )
    TOWER = StructureInfo(
            id=3,
            name="Tower",
            cost=250,
            can_build=True
        )
    PRESERVE = StructureInfo(
            id=4,
            name="Preserve",
            cost=0,
            can_build=False
        )

    def get_cost(self):
        return self.value.cost

    def get_can_build(self):
        return self.value.can_build


class Structure:
    def __init__(self, struct_type, x, y, team, powered=False):
        self.x = x
        self.y = y
        self.team = team
        self.type = struct_type

    def __str__(self):
        return f"[{self.type.name} {str(self.team)} {(self.x, self.y)}, P:{self.powered}]"

    def _copy(self):
        return Structure(self.x, self.y, self.team, self.type)

    def _equal(self, s):
        return self.x == s.x and self.y == s.y and self.team == s.team and self.type == s.type

#
#
# class Generator(Structure):
#     def __init__(self, x, y, team):
#         super().__init__(StructureType.GENERATOR, x, y, team)
#
#
# class Road(Structure):
#     def __init__(self, x, y, team):
#         super().__init__(StructureType.ROAD, x, y, team)
#
#
# class Transformer(Structure):
#     def __init__(self, x, y, team):
#         super().__init__(StructureType.TRANSFORMER, x, y, team)
#
#
# class Tower(Structure):
#     def __init__(self, x, y, team):
#         super().__init__(StructureType.TOWER, x, y, team)
#
#
# class Preserve(Structure):
#     def __init__(self, x, y, team):
#         super().__init__(StructureType.PRESERVE, x, y, team)
