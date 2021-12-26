import json
import os
import argparse

# TEMPORARY: being used to make a sample map in the correct format
# to test the code used for reading custom maps

replay_path = "../replays"
map_path = "../maps"

def save_map(replay_file, seed):
    replay_data = None
    # load simple map entry from replay json file
    try:
        with open(replay_file) as f:
            replay_data = json.load(f)
    except FileNotFoundError:
        print(f"{replay_file} does not exist")
        return
    
    simple_map = replay_data["map"]

    rows, cols = len(simple_map[0]), len(simple_map)
    info = [[0 for _ in range(cols)] for _ in range(rows)]
    generators1, generators2 = [], []

    # iterate through simple map to get info
    for i in range(cols):
        for j in range(rows):
            passability, population, structure = simple_map[i][j]
            info[i][j] = (passability, population)
            
            # ref structure.py: code for generator type is 0
            if structure and structure[3] == 0:
                if structure[2] == 0:
                    generators1 += [(i,j)]
                elif structure[2] == 1:
                    generators2 += [(i,j)]
    
    # save into map json file
        with open(f"{map_path}/map-{seed}.awap22", "w") as f:
            obj = {
                "info": info,
                "generators1": generators1,
                "generators2": generators2
            }
            json.dump(obj, f)
    print(f'Saved map of {replay_file} into {map_path}/map-{seed}.awap22')


parser = argparse.ArgumentParser()
parser.add_argument("-r","--replay_seed", help="specify a map to save (path = ../replays/replay-REPLAY_SEED.awap22)", default=None)
args = parser.parse_args()

if args.replay_seed:
    save_map(f'{replay_path}/replay-{args.replay_seed}.awap22', args.replay_seed)    
else:
    print(f"No replay file specified (run python3 save_maps.py -h for info) - saving all maps from {replay_path}")
    replays = list(set(os.listdir(replay_path)) - set(['.gitignore']))
    for replay_file in replays:
        seed = replay_file[7:14]
        save_map(f'{replay_path}/{replay_file}', seed)