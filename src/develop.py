from src.GameManager import *
from src.Player import *

def tempFunc(input_vector):
    return 5


player_1 = Player(tempFunc)
player_2 = Player(tempFunc)
player_3 = Player(tempFunc)
player_4 = Player(tempFunc)

game_manager = GameManager([player_1, player_2, player_3, player_4])


print(game_manager.player_turn)