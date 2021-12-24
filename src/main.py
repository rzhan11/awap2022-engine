import json

from structure import *
from game import *
from custom_json import *

# you have to be in src to run main.py successfully

bot_folder = "../bots"
bot_path = f"{bot_folder}/bot.py"
save_path = "../replays"

# Exact format of a custom map file:
# .json file with "info", "generators1", and "generators2" entries
# info is a 2d array of (passability, population) tuples for each tile location
# generators1 is a 1d array of (x,y) coordinates if there exist a generator for team 1 at (x,y)
# generators2 is a 1d array of (x,y) coordinates if there exist a generator for team 2 at (x,y)

map_path = "../maps/map-9034983.awap22"

# Using custom map
map_settings = MapInfo(custom_map_path=map_path)

# No custom map (Random map)
# map_settings = MapInfo(1078, 48, 48, MapUtil.x_sym, num_generators=3, num_cities=50)

game = Game(bot_path, bot_path, map_settings)

# for x in range(game.width):
#     for y in range(game.height):
#         if len(game.map[x][y].structures) > 0:
#             print(x, y)

game.play_game()
# game.play_turn(0)

game.save_replay(save_path)

# print(CustomEncoder().encode(game.map[0][51].structures))
