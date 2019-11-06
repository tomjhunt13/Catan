import unittest

from src.Player import *

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

class MaxValue(unittest.TestCase):
    def testGetHighestAcrossDictionaries(self):
        """
        Test getHighestAcrossDictionaries function
        """

        # Initialise dictionary
        test_dict = {'key_1': [1, 2, 1.4, 1.2, 0],
                     'key_2': [0.1, 0.12, 0.3],
                     'key_3': [2.1, 2.05, 1],
                     'key_4': [3]}

        # Perform test
        key, element = getHighestAcrossDictionaries(test_dict)
        self.assertEqual(key, 'key_4')
        self.assertEqual(element, 0)

        # Change value of 'key_4' to not be max and perform test
        test_dict['key_4'][0] = 0
        key, element = getHighestAcrossDictionaries(test_dict)
        self.assertEqual(key, 'key_3')
        self.assertEqual(element, 0)


if __name__ == '__main__':
    unittest.main()