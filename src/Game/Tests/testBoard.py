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

        # Place settlement on node 31 and city on 32
        board.nodes[31].settlement = [1, 0, 0, 0]
        board.nodes[32].city = [0, 1, 0, 0]

        # Test node 31 is not empty
        self.assertEqual(board.nodes[31].isEmpty(), False)

        # Test node 32 is not empty
        self.assertEqual(board.nodes[32].isEmpty(), False)

        # Test node 40 is empty
        self.assertEqual(board.nodes[40].isEmpty(), True)

    def testConnectedNodesBuiltOn(self):
        """
        Test function to check connected nodes not built on
        """
        # Initialise board
        board = Board(4)

        # Place settlement on node 31
        board.nodes[31].settlement = [1, 0, 0, 0]

        # Test node 32 returns false as it is connected to 31
        self.assertEqual(board.connectedNodesBuiltOn(32), False)

        # Test node 33 returns True as it isn't connected to 31
        self.assertEqual(board.connectedNodesBuiltOn(33), True)

class TestEdge(unittest.TestCase):
    def testIsEmpty(self):
        """
        Test edge isEmpty function
        """
        # Initialise board
        board = Board(4)

        # Place road on edge 20
        board.edges[20].road = [1, 0, 0, 0]

        # Test edge 20 is not empty
        self.assertEqual(board.edges[20].isEmpty(), False)

        # Test node 32 is empty
        self.assertEqual(board.nodes[32].isEmpty(), True)

    def testEdgeHasRoadOrSettlement(self):
        """
        Test edgeHasRoadOrSettlement function of board
        """
        # Initialise board
        board = Board(4)

        # Test unconnected edge
        self.assertEqual(board.edgeHasRoadOrSettlement(24, 2), False)

        """
        Test by road connectivity:
        
        Edge 20 connects nodes 11 and 21
        - node 11: connected to edges: 13, 14, 20
        - node 21: connected to edges: 20, 27, 28
        """
        # Place road on edge 20
        board.edges[20].road = [1, 0, 0, 0]

        # Test edge 13 (connected to node 11) for player 0
        self.assertEqual(board.edgeHasRoadOrSettlement(13, 0), True)

        # Test edge 13 (connected to node 11) for player 2
        self.assertEqual(board.edgeHasRoadOrSettlement(13, 2), False)

        """
        Test by settlement and city connectivity:
        
        Edge 48 connects nodes 36 and 37
        """
        # Place settlement on node 36
        board.nodes[36].settlement = [1, 0, 0, 0]

        # Test edge 48 for player 0
        self.assertEqual(board.edgeHasRoadOrSettlement(48, 0), True)

        # Test edge 48 for player 2
        self.assertEqual(board.edgeHasRoadOrSettlement(48, 2), False)

        # Remove settlement and build city
        board.nodes[36].settlement = [0, 0, 0, 0]
        board.nodes[36].city = [1, 0, 0, 0]

        # Test edge 48 for player 0
        self.assertEqual(board.edgeHasRoadOrSettlement(48, 0), True)

        # Test edge 48 for player 2
        self.assertEqual(board.edgeHasRoadOrSettlement(48, 2), False)


class NodeEdgeConnectivity(unittest.TestCase):
    def testNodeHasRoad(self):
        """
        Test Board nodeHasRoad function
        """
        # Initialise board
        board = Board(4)

        # Test node 30 with no connected edges built on
        self.assertEqual(board.nodeHasRoad(30, 2), False)

        # Test node 30 with one connected built on but wrong player
        board.nodes[30].connected_edges[0].road = [1, 0, 0, 0]
        self.assertEqual(board.nodeHasRoad(30, 2), False)

        # Test node 30 with one connected built on but correct player
        board.nodes[30].connected_edges[0].road = [1, 0, 0, 0]
        self.assertEqual(board.nodeHasRoad(30, 0), True)


if __name__ == '__main__':
    unittest.main()

