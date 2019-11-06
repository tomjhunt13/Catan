import time

from src.GameManager import *
from src.Player import *

player_1 = Player(randomAction)
player_2 = Player(randomAction)
player_3 = Player(randomAction)
player_4 = Player(randomAction)

game_manager = GameManager([player_1, player_2, player_3, player_4])

start_time = time.time()
game_manager.startGame()
end_time = time.time()

print(end_time - start_time)