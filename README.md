# AWAP 2022 Game Engine

Game Engine for AWAP 2022 - Wifi Rumble

## How-to:
1. Clone this repo
2. `cd` into this repo
3. `cd` into `src`
4. Run `python3 main.py`
5. Open the viewer on your browser
6. Upload the replay file that appears in `replays`
7. Watch the magic Richard coded happen

## Save and replay maps
1. `cd` into `src`
2. Run `python3 savemaps.py` to save the map of every replay, or `python3 savemaps.py -r YOURSEED` to save the map of the replay file with seed `YOURSEED`.
3. Run `python3 main.py -m YOURSEED` to run a game on a saved map with seed `YOURSEED`.

## Clear maps and replays (ik its extra af)
1. Go to `src` and give the cleaning files `rm_replays.sh` and `rm_maps.sh` permissions with `chmod +x [filename here]`.
2. Clear the `../maps` and `../replays` folders, respectively, by running `./rm_maps.sh` and `./rm_replays.sh`.