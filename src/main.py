import json

from structure import *
from game import *
from custom_json import *

# you have to be in src
bot_folder = "../bots"
bot_path = f"{bot_folder}/bot.py"
save_path = "../replays"

# Exact format of maps:
# .json file with "info" and "generators" entries
# info is a 2d array of (passability, population) tuples for each tile location
# generators is a 1d array of (x,y) coordinates if there exist a generator at (x,y)

map_settings = MapInfo(1078, 48, 48, MapUtil.x_sym, num_generators=3, num_cities=50)

game = Game(bot_path, bot_path, map_settings)

# for x in range(game.width):
#     for y in range(game.height):
#         if len(game.map[x][y].structures) > 0:
#             print(x, y)

game.play_game()
# game.play_turn(0)

id = game.save_replay(save_path)


# TEMPORARY: being used to make a sample map in the correct format
# to test the code used for reading custom maps

def save_map():

    #load simple map entry from replay json file
    replay_file = f"{save_path}/replay-{id}.awap22"
    replay_data = json.load(open(replay_file))

    simple_map = replay_data["map"]

    rows, cols = len(simple_map[0]), len(simple_map)
    info = [[0]*cols]*rows
    generators = []

    # iterate through simple map to get info
    for i in range(rows):
        for j in range(cols):
            passability, population, structure = simple_map[i][j]
            info[i][j] = (passability, population)

            # ref structure.py: code for generator type is 0
            if structure and structure[3] == 0:
                generators += [(i,j)]
        
    # save into map json file
    with open("sample_map.awap22", "w") as f:
        obj = {
            "info": info,
            "generators": generators,
        }
        json.dump(obj, f)

save_map()


# print(CustomEncoder().encode(game.map[0][51].structures))
