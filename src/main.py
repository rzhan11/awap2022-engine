from structure import *
from game import *
from custom_json import *

bot_folder = "../bots"
bot_path = f"{bot_folder}/bot.py"
save_path = f"../replays"

map_settings = MapInfo(1078, 48, 48, MapUtil.x_sym, num_generators=3, num_cities=50)

game = Game(bot_path, bot_path, map_settings)

# for x in range(game.width):
#     for y in range(game.height):
#         if len(game.map[x][y].structures) > 0:
#             print(x, y)

game.play_game()
# game.play_turn(0)


game.save_replay(save_path)

# print(CustomEncoder().encode(game.map[0][51].structures))
