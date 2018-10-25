import random

from src.Game.GameManager import *
from src.Game.Player import *

def tempFunc(input_vector):
    return 5

def randomAction(inputVector):
    """
    Sample wrapper function for network
    :param inputVector: vector containing all player knowledge of the game state
    :return: dictionary made up of vectors containing the choices made by the network broken up by category for convenience
    """

    # Generate random values for choices of settlement placement
    settlements = [0] * 54
    cities = [0] * 54
    for i in range(54):
        settlements[i] = random.uniform(0, 1)
        cities[i] = random.uniform(0, 1)

    # Generate random values for choices of settlement placement
    roads = [0] * 72
    for i in range(72):
        roads[i] = random.uniform(0, 1)

    # Trading
    trade = [0] * 20
    for i in range(72):
        roads[i] = random.uniform(0, 1)

    # Ending turn
    end_turn = [random.uniform(0, 1)]

    output_dictionary = {'Settlements': settlements, 'Cities': cities, 'Roads': roads, 'EndTurn': end_turn, 'Trade': trade}
    output_vector = settlements + cities + roads + trade + end_turn

    return output_dictionary, output_vector


player_1 = Player(randomAction)
player_2 = Player(randomAction)
player_3 = Player(randomAction)
player_4 = Player(randomAction)

game_manager = GameManager([player_1, player_2, player_3, player_4])


print(game_manager.player_turn)