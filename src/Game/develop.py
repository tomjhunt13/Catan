from src.Game.GameManager import *
from src.Game.Player import *

player_1 = Player(randomAction)
player_2 = Player(randomAction)
player_3 = Player(randomAction)
player_4 = Player(randomAction)

game_manager = GameManager([player_1, player_2, player_3, player_4])
game_manager.startGame()


print(game_manager.player_turn)