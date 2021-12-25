import json
import argparse

from structure import *
from game import *
from custom_json import *

# you have to be in src to run main.py successfully

bot_folder = "../bots"
bot1_path = f"{bot_folder}/bot.py"
bot2_path = f"{bot_folder}/bot_bfs.py"
save_path = "../replays"

# Exact format of a custom map file:
# .json file with "info", "generators1", and "generators2" entries
# info is a 2d array of (passability, population) tuples for each tile location
# generators1 is a 1d array of (x,y) coordinates if there exist a generator for team 1 at (x,y)
# generators2 is a 1d array of (x,y) coordinates if there exist a generator for team 2 at (x,y)

parser = argparse.ArgumentParser()
parser.add_argument("-m","--custom_map", help="Custom map path [../maps/map-yourmapseed].", default=None)
args = parser.parse_args()

if args.custom_map:
    map_settings = MapInfo(custom_map_path=args.custom_map)
else:
    map_settings = MapInfo(1078, 48, 48, MapUtil.x_sym, num_generators=3, num_cities=50)

game = Game(bot1_path, bot2_path, map_settings)

game.play_game()

game.save_replay(save_path)
