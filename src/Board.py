class Node:
    def __init__(self, ID, number_of_players):
        """
        Class to represent node on board graph
        :param ID: ID of node
        :param number_of_players: number of players in game
        """
        self.ID = ID

        """
        Resources:
        - self.resource_probablities is a list stating the probability of getting each resource
        - list order is: [ Wheat, Stone, Brick, Sheep, Wood ]
        """
        self.resource_probabilities = [0] * 5

        """
        Settlements and cities:
        - self.settlement and self.city are boolean lists stating if node has a settlement or city on it
        - The index of the value refers to the player ID (player 1 is user)
        """
        self.settlement = [0] * number_of_players
        self.city = [0] * number_of_players

        """
        Ports:
        - self.ports is a boolean list stating if a port type exists on this node
        - list order is: [ 3:1, 2:1 Wheat, 2:1 Stone, 2:1 Brick, 2:1 Sheep, 2:1 Wood ]
        """
        self.ports = [0] * 6


class Edge:
    def __init__(self, ID, node_1, node_2, number_of_players):
        """
        Class to represent edge on board graph
        :param ID: ID of edge
        :param node_1: ID of first connected node
        :param node_2: ID of second connected node
        :param number_of_players: number of players in game
        """

        # Edge info
        self.ID = ID
        self.node_1 = node_1
        self.node_2 = node_2

        """
        Roads:
        - self.road is a boolean list stating if edge has road on it
        - The index of the value refers to the player ID (player 1 is user)
        """
        self.road = [0] * number_of_players


class Board:
    """
    Class used to represent board
    """

    def __init__(self, number_of_players, expanded_board=False):
        """
        Representation of the board
        :param number_of_players: number of players in game
        :param expanded_board: boolean - game is on expanded board or not
        """

        # Board info
        self.expanded_board = expanded_board

        # Initialise nodes
        number_of_nodes = 54
        if expanded_board:
            number_of_nodes = 54
        self.nodes = [None] * number_of_nodes
        for node_id in range(number_of_nodes):
            self.nodes[node_id] = Node(node_id, number_of_players)

        # Initialise edges
        edge_pairs = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7],
                      [1, 9], [3, 11], [5, 13], [7, 15],
                      [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16],
                      [8, 18], [10, 20], [12, 22], [14, 24], [16, 26],
                      [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26], [26,27],
                      [17, 28], [19, 30], [21, 32], [23, 34], [25, 36], [27, 38],
                      [28, 29], [29, 30], [30, 31], [31, 32], [32, 33], [33, 34], [34, 35], [35, 36], [36, 37], [37,39],
                      [29, 39], [31, 41], [33, 43], [35, 45], [37, 47],
                      [39, 40], [40, 41], [41, 42], [42, 43], [43, 44], [44, 45], [45, 46], [46, 47],
                      [40, 48], [42, 50], [44, 52], [46, 54],
                      [48, 49], [49, 50], [50, 51], [51, 52], [52, 53], [53, 54]]

        self.edges = [None] * len(edge_pairs)
        for edge_id in range(len(edge_pairs)):
            self.edges[edge_id] = Edge(edge_id, edge_pairs[edge_id][0], edge_pairs[edge_id][1], number_of_players)

    def generateBoard(self):
        pass

    def getInputValues(self):
        pass

if __name__ == "__main__":
    a = Board(1)
    print()