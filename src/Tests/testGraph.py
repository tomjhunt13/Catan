import unittest

from src.Graph import *


class TestGraph(unittest.TestCase):

    def test_constructNodeConnectivityMatrix(self):
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
        expected_matrix = [[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0]]
        self.assertEqual(constructNodeConnectivityMatrix(edges), expected_matrix)


    def test_longestContinousPath(self):
        """
        Tests for path length functionality
        """

        # Initialise graph
        graph = Graph()

        """ Test no edges """
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 0)

        """ Test one edge """
        # Add two nodes
        n_0 = graph.appendNodeToGraph()
        n_1 = graph.appendNodeToGraph()

        # Add edge
        graph.appendEdgeToGraph([n_0, n_1])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 1)

        """ Test two edges """
        # Add one nodes
        n_2 = graph.appendNodeToGraph()

        # Add edge
        graph.appendEdgeToGraph([n_1, n_2])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 2)

        """ Test branch with one branch with two edges, one with one edge """
        # Add nodes and edges for longer branch
        n_3 = graph.appendNodeToGraph()
        n_4 = graph.appendNodeToGraph()
        graph.appendEdgeToGraph([n_2, n_3])
        graph.appendEdgeToGraph([n_3, n_4])

        # Add node and edge for shorter branch
        n_5 = graph.appendNodeToGraph()
        graph.appendEdgeToGraph([n_2, n_5])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 4)

        """ Add edge connecting branches to add loop """
        graph.appendEdgeToGraph([n_4, n_5])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 6)

        """ Add edge to complete second loop """
        graph.appendEdgeToGraph([n_0, n_5])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 7)

        """ Add node and edge branching off loops """
        n_6 = graph.appendNodeToGraph()
        graph.appendEdgeToGraph([n_1, n_6])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 7)

        """ Add edge to complete third loop """
        graph.appendEdgeToGraph([n_3, n_6])
        length, path = graph.longestContinousPath()
        self.assertEqual(length, 8)

        del(graph)

        """ Larger test case """
        # Initialise graph
        graph_1 = Graph(nodes=[], edges=[])

        # Add nodes
        graph_nodes = [None] * 14
        for i in range(14):
            graph_nodes[i] = graph_1.appendNodeToGraph()

        # Add edges
        edge_pairs = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 8],
            [8, 9],
            [5, 9],
            [9, 10],
            [10, 11],
            [11, 12],
            [12, 8],
            [11, 13]]

        for edge in edge_pairs:
            graph_1.appendEdgeToGraph([graph_nodes[edge[0]], graph_nodes[edge[1]]])

        length, path = graph_1.longestContinousPath()
        self.assertEqual(length, 13)


if __name__ == '__main__':
    unittest.main()

