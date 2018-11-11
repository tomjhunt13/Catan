import unittest

from src.Game.RoadNetwork import *
from src.Game.Board import *


class TestRoadNetwork(unittest.TestCase):

    def test_breakRoadAtNode(self):
        """
        Test that breakRoadAtNode is correct
        """
        # Initialise RoadNetwork
        game_board = Board(4)
        road_network = RoadNetwork(game_board, 0)

        # Add two roads to network -> Edges: 14 (connecting nodes 11 and 12) and 8 (connecting nodes 12 and 4)
        road_network.addRoad(14)
        road_network.addRoad(8)

        # Break network at board node 12
        road_network.breakRoadAtNode(12)

        # Test longest path is 1
        length, path = road_network.longestContinousPath()
        self.assertEqual(length, 1)

        # Add road to broken node -> Edge 3 (connecting nodes 4 and 3)
        road_network.addRoad(3)

        # Test length
        length, path = road_network.longestContinousPath()
        self.assertEqual(length, 2)

        # Add road to end -> Edge 2 (connecting nodes 3 and 2)
        road_network.addRoad(2)

        # Test length
        length, path = road_network.longestContinousPath()
        self.assertEqual(length, 3)

        # Break node 3
        road_network.breakRoadAtNode(3)

        # Test length
        length, path = road_network.longestContinousPath()
        self.assertEqual(length, 2)










        print('3')

if __name__ == '__main__':
    unittest.main()

