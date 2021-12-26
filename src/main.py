import json
import argparse
import os

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
parser.add_argument("-m","--custom_map_seed", help="Run with custom map (../maps/map-CUSTOM_MAP_SEED.awap22).", default=None)
args = parser.parse_args()

if args.custom_map_seed:
    custom_map = f'../maps/map-{args.custom_map_seed}.awap22'
    if os.path.isfile(custom_map):
        map_settings = MapInfo(custom_map_path=custom_map)
    else:
        print(f"Map {custom_map} could not be found. Run python3 main.py -h for help. Exiting")
        exit(0)
else:
    map_settings = MapInfo(1078, 48, 48, MapUtil.x_sym, num_generators=3, num_cities=50)

game = Game(bot1_path, bot2_path, map_settings)

game.play_game()

game.save_replay(save_path)
