import unittest

from src.Game.Board import *

class Connectivity(unittest.TestCase):

    def testConstructNodeConnectivityMatrix(self):
        """
        Test that connectivity matrix is correct
        """
        # Triangular graph
        edges = [[0, 1], [1, 2], [0, 2]]
        expected_matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(constructNodeConnectivityMatrix(edges), expected_matrix)

        # Triangular graph with one edge missing
        edges = [[0, 1], [1, 2]]
        expected_matrix = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        self.assertEqual(constructNodeConnectivityMatrix(edges), expected_matrix)

        # 1 node to 4 others
        edges = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]
        expected_matrix = [[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]]
        self.assertEqual(constructNodeConnectivityMatrix(edges), expected_matrix)


class EmptyNodes(unittest.TestCase):
    def testIsEmpty(self):
        """
        Test Node isEmpty function
        """
        # Initialise board
        board = Board(4)
        board.generateBoard()

        # Place settlement on node 31 and city on 32
        board.nodes[31].settlement = [1, 0, 0, 0]
        board.nodes[32].city = [0, 1, 0, 0]

        # Test node 31 is not empty
        self.assertEqual(board.nodes[31].isEmpty(), False)

        # Test node 32 is not empty
        self.assertEqual(board.nodes[32].isEmpty(), False)

        # Test node 40 is not empty
        self.assertEqual(board.nodes[40].isEmpty(), True)


    def testConnectedNodesBuiltOn(self):
        """
        Test function to check connected nodes not built on
        """
        # Initialise board
        board = Board(4)
        board.generateBoard()

        # Place settlement on node 31
        board.nodes[31].settlement = [1, 0, 0, 0]

        # Test node 32 returns false as it is connected to 31
        self.assertEqual(board.connectedNodesBuiltOn(32), False)

        # Test node 33 returns True as it isn't connected to 31
        self.assertEqual(board.connectedNodesBuiltOn(33), True)

if __name__ == '__main__':
    unittest.main()

