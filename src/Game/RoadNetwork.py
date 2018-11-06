from src.Game.Graph import *

class RoadNetwork(Graph):
    def __init__(self, game_board, player_index):
        """
        Class to represent a players road network
        :param game_board: Instance of Board class for current game
        """

        # Initialise board variables
        self.game_board = game_board
        self.board_node_to_road_node = [None] * len(game_board.nodes)
        for i in range(len(self.board_node_to_road_node)):
            self.board_node_to_road_node[i] = []

        self.player_index = player_index
        super(RoadNetwork, self).__init__()


    def addRoad(self, edge_index):
        """
        Add a road to the road network
        :param edge_index: Index of edge to build on (referring to the board graph)
        """

        # For each node connected to board edge, find corresponding node in road network
        road_network_nodes = [None, None]
        for index, node in enumerate(self.game_board.edges[edge_index].nodes):

            # If node is occupied by another players settlement or city - Add new node to RoadNetwork
            if not self.game_board.nodes[node].isEmpty() and self.game_board.nodes[node].settlement[self.player_index] == 0 and self.game_board.nodes[node].city[self.player_index] == 0:
                road_network_nodes[index] = self.appendNodeToGraph({'board_index': self.game_board.edges[edge_index].nodes[index]})
                self.board_node_to_road_node[node].append(road_network_nodes[index])

            # Else find corresponding road network node in self.board_node_to_road_node
            elif len(self.board_node_to_road_node[node]) != 0:
                road_network_nodes[index] = self.board_node_to_road_node[node][0]

            # Else node not in network, so add it
            else:
                road_network_nodes[index] = self.appendNodeToGraph({'board_index': self.game_board.edges[edge_index].nodes[index]})
                self.board_node_to_road_node[node].append(road_network_nodes[index])

        # Add edge between nodes
        self.appendEdgeToGraph(road_network_nodes, {'edge_index': edge_index})

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