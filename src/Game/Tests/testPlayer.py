import unittest

from src.Game.Player import *

class PlayerChecks(unittest.TestCase):

    def testHasResources(self):
        """
        Test hasResources function
        """
        # Initialise player
        player = Player(randomAction)

        # Player with no resources requiring one of each type
        self.assertEqual(player.hasResources([1, 1, 1, 1, 1]), False)

        # Player with no resources requiring 4 resources
        self.assertEqual(player.hasResources([1, 1, 1, 0, 1]), False)

        # Player with enough resources
        player.resource_cards = [2, 2, 2, 2, 2]
        self.assertEqual(player.hasResources([1, 1, 1, 0, 1]), True)

if __name__ == '__main__':
    unittest.main()