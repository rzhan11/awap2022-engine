import json
import os

# TEMPORARY: being used to make a sample map in the correct format
# to test the code used for reading custom maps

replay_path = "../replays"

def save_map(replay_file, id):
    print(replay_file)

    replay_data = None
    # load simple map entry from replay json file
    with open(replay_file) as f:
        replay_data = json.load(f)

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

    print(info)
    print(generators1)
    print(generators2)
        
    # save into map json file
    with open(f"../maps/map-{id}.awap22", "w") as f:
        obj = {
            "info": info,
            "generators1": generators1,
            "generators2": generators2
        }
        json.dump(obj, f)

replays = list(set(os.listdir(replay_path)) - set(['.gitignore']))
for replay_file in replays:
    id = replay_file[7:14]
    save_map(f'{replay_path}/{replay_file}', id)