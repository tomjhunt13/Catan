from src.Game.Graph import *

class RoadNetwork(Graph):
    def __init__(self, game_board):
        """
        Class to represent a players road network
        :param game_board: Instance of Board class for current game
        """
        self.game_board = game_board
        super(RoadNetwork, self).__init__()


    def addRoad(self, edge_index):
        """
        Add a road to the road network
        :param edge_index: Index of edge to build on (referring to the board graph)
        """

        # First add nodes to network !!! Make sure add connectivity
        board_node_indices = self.game_board.edges[edge_index].nodes

        node_0_dict = {'board_index': board_node_indices[0]}
        node_1_dict = {'board_index': board_node_indices[1]}

        index_0 = self.appendNodeToGraph(node_0_dict)
        index_1 = self.appendNodeToGraph(node_1_dict)

        # Add edge between nodes
        self.appendEdgeToGraph([index_0, index_1], {'edge_index': edge_index})

    def breakRoadAtNode(self, node_index):
        """
        Handle event where this players road is broken by another players settlment
        :param node_index: Index of node which settlement was built on
        """
        pass
        # If another player builds a settlement at node node_index which breaks the road network, add another node to graph to represent disconnect



if __name__ == "__main__":
    a = RoadNetwork()

    print(dir(a))