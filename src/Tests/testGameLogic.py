import unittest

from src.GameManager import *
from src.Player import *


class SettlementPlacement(unittest.TestCase):

    def testOccupiedNode(self):
        """
        Test that settlement building function doesn't allow building on already occupied node
        """

        # Create game
        player_1 = Player(randomAction)
        player_2 = Player(randomAction)
        player_3 = Player(randomAction)
        player_4 = Player(randomAction)
        game_manager = GameManager([player_1, player_2, player_3, player_4])
        game_manager.turn_counter = 7

        # Give player 1 enough resources for building settlement
        player_1.resource_cards = [3] * 5

        # 1st test another player with settlement on node 5
        game_manager.game_board.nodes[5].settlement = [0, 1, 0, 0]
        self.assertEqual(game_manager.buildSettlement(player_1, 5), False)

        # 1st test another player with city on node 7
        game_manager.game_board.nodes[7].city = [0, 1, 0, 0]
        self.assertEqual(game_manager.buildSettlement(player_1, 7), False)

    def testCorrectResources(self):
        """
        Test that settlement building function doesn't allow building if player doesn't have enough resources
        """

        # Create game
        player_1 = Player(randomAction)
        player_2 = Player(randomAction)
        player_3 = Player(randomAction)
        player_4 = Player(randomAction)
        game_manager = GameManager([player_1, player_2, player_3, player_4])
        game_manager.turn_counter = 7

        # Give player 1 0 resources
        player_1.resource_cards = [0] * 5
        self.assertEqual(game_manager.buildSettlement(player_1, 5), False)

    def testSettlementPieceAvailable(self):
        """
        Test that settlement building function doesn't allow building if player doesn't have settlement pieces to build with
        """

        # Create game
        player_1 = Player(randomAction)
        player_2 = Player(randomAction)
        player_3 = Player(randomAction)
        player_4 = Player(randomAction)
        game_manager = GameManager([player_1, player_2, player_3, player_4])
        game_manager.turn_counter = 7

        # Give player 1 enough resources
        player_1.resource_cards = [4] * 5

        # Give player_1 0 settlement pieces
        player_1.building_pieces[1] = 0
        self.assertEqual(game_manager.buildSettlement(player_1, 5), False)


if __name__ == '__main__':
    unittest.main()