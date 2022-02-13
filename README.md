# AWAP 2022 Game Engine

This is the AWAP 2022 game engine.

Sample bots can be found in the `bots/` folder. Competitors should also develop their bots in this folder.

### Requirements
* [Python 3](https://www.python.org/downloads/) (Developed/tested in **3.8.9**, other versions probably work)

## Project Structure
* `README.md` - This file
* `run_game.py` - Runs a game between two players on a map
* `game_settings.json` - Contains game settings used in `run_game.py` (specifies players and map)
* `bots/` - Contains player source code
* `maps/` - Contains maps (download your custom maps to here)
* `replays/` - Contains match replays
* `src/` - Contains the engine source code


## How-to:

### Download
* `git clone https://github.com/rzhan11/cell-towers.git` - Downloads the repo

### Run a match
* `cd` into this repo
* `python3 run_game.py` - Runs the game
    * Specify players/maps by modifying `game_settings.json`
    * Games can also be run with CLI arguments (`python3 run_game.py -h` for details)

### View match replay
* Open the viewer ([from website - NOT UP YET](VIEWER_URL) or [install locally](https://github.com/rzhan11/cell-towers-viewer))
* Upload a replay file (match replays are saved in the `replays/` folder)
