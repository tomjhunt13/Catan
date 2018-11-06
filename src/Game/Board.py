from random import shuffle
from src.Game.Graph import *


class BoardNode:
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
        - self.resource_dice_rolls is a list of which rolls get each resource
        """
        self.resource_probabilities = [0] * 5
        self.resource_dice_rolls = [[], [], [], [], []]

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

        # Edges which are connected to this node
        self.connected_edges = []

    def isEmpty(self):
        """
        Checks if node has not been built on
        :return: Bool - True if node is empty
        """
        for i in range(len(self.city)):
            if (self.settlement[i] == 1) or (self.city[i] == 1):
                return False

        return True


class BoardEdge:
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
        self.nodes = [node_1, node_2]

        """
        Roads:
        - self.road is a boolean list stating if edge has road on it
        - The index of the value refers to the player ID (player 1 is user)
        """
        self.road = [0] * number_of_players

    def isEmpty(self):
        """
        Checks if edge has not been built on
        :return: Bool - True if edge is empty
        """
        for i in range(len(self.road)):
            if self.road[i] == 1:
                return False

        return True


class Board:
    """
    Class used to represent board
    """

    def __init__(self, number_of_players):
        """
        Initialises representation of the board
        :param number_of_players: number of players in game
        """

        # Initialise nodes
        number_of_nodes = 54
        self.nodes = [None] * number_of_nodes
        for node_id in range(number_of_nodes):
            self.nodes[node_id] = BoardNode(node_id, number_of_players)

        # Initialise edges
        edge_pairs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
                       [0, 8], [2, 10], [4, 12], [6, 14],
                       [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15],
                       [7, 17], [9, 19], [11, 21], [13, 23], [15, 25],
                       [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26],
                       [16, 27], [18, 29], [20, 31], [22, 33], [24, 35], [26, 37],
                       [27, 28], [28, 29], [29, 30], [30, 31], [31, 32], [32, 33], [33, 34], [34, 35], [35, 36], [36, 37],
                       [28, 38], [30, 40], [32, 42], [34, 44], [36, 46],
                       [38, 39], [39, 40], [40, 41], [41, 42], [42, 43], [43, 44], [44, 45], [45, 46],
                       [39, 47], [41, 49], [43, 51], [45, 53],
                       [47, 48], [48, 49], [49, 50], [50, 51], [51, 52], [52, 53]]

        self.node_connectivity_matrix = constructNodeConnectivityMatrix(edge_pairs)

        self.edges = [None] * len(edge_pairs)
        for edge_id in range(len(edge_pairs)):
            self.edges[edge_id] = BoardEdge(edge_id, edge_pairs[edge_id][0], edge_pairs[edge_id][1], number_of_players)

            # Add edges to list of connected edges on each node
            self.nodes[edge_pairs[edge_id][0]].connected_edges.append(self.edges[edge_id])
            self.nodes[edge_pairs[edge_id][1]].connected_edges.append(self.edges[edge_id])

        # Define connectivity between nodes and hexes
        # Each element is one hex and is a list of nodes that are connected to it
        self.hex_node_connectivity = [[0, 1, 2, 8, 9, 10],
                                      [2, 3, 4, 10, 11, 12],
                                      [4, 5, 6, 12, 13, 14],
                                      [7, 8, 9, 17, 18, 19],
                                      [9, 10, 11, 19, 20, 21],
                                      [11, 12, 13, 21, 22, 23],
                                      [13, 14, 15, 23, 24, 25],
                                      [16, 17, 18, 27, 28, 29],
                                      [18, 19, 20, 29, 30, 31],
                                      [20, 21, 22, 31, 32, 33],
                                      [22, 23, 24, 33, 34, 35],
                                      [24, 25, 26, 35, 36, 37],
                                      [28, 29, 30, 38, 39, 40],
                                      [30, 31, 32, 40, 41, 42],
                                      [32, 33, 34, 42, 43, 44],
                                      [34, 35, 36, 44, 45, 46],
                                      [39, 40, 41, 47, 48, 49],
                                      [41, 42, 43, 49, 50, 51],
                                      [43, 44, 45, 51, 52, 53]]

        # Create all hexes - resource order is [ Wheat, Stone, Brick, Sheep, Wood ]
        number_of_resource = [4, 3, 3, 4, 4]
        self.hexes = []
        for resource_type in range(len(number_of_resource)):
            for i in range(number_of_resource[resource_type]):
                self.hexes.append(Hex(0, resource_type))
        self.hexes.append(Hex(0, -1))

        # Shuffle list
        shuffle(self.hexes)

        # Choose dice roles !!!Currently chosen at random but should implement proper order
        number_markers = [2, 5, 4, 6, 3, 9, 8, 11, 11, 10, 6, 3, 8, 4, 8, 10, 11, 12]
        self.hex_dice_roll_list = [None] * 13
        shuffle(number_markers)
        hex_index = 0
        for hexagon in self.hexes:
            hexagon.ID = hex_index
            if hexagon.resource_index != -1:
                hexagon.dice_roll = number_markers[hex_index]
                hexagon.probability = probabilityOfRoll(number_markers[hex_index])

                if not self.hex_dice_roll_list[number_markers[hex_index]]:
                    self.hex_dice_roll_list[number_markers[hex_index]] = [hexagon]
                else:
                    self.hex_dice_roll_list[number_markers[hex_index]].append(hexagon)

                # Update connected nodes
                for node in self.hex_node_connectivity[hex_index]:
                    self.nodes[node].resource_dice_rolls[hexagon.resource_index].append(hexagon.dice_roll)
                    if hexagon.dice_roll not in self.nodes[node].resource_dice_rolls[hexagon.resource_index]:
                        self.nodes[node].resource_probabilities[hexagon.resource_index] += hexagon.probability
                hex_index += 1

    def getInputValues(self):
        """
        Assemble board parameters
        :return: Board parameters
        """
        # Node inputs
        resource_probabilities = []
        settlements = []
        cities = []
        ports = []

        for node in self.nodes:
            resource_probabilities += node.resource_probabilities
            settlements += node.settlement
            cities += node.city
            ports += node.ports

        # Edge inputs
        roads = []
        for edge in self.edges:
            roads += edge.road

        return resource_probabilities + settlements + cities + ports + roads

    def connectedNodesBuiltOn(self, node_index):
        """
        Check if any nodes connected to node node_index are built on
        :param node_index: Index of node to check
        :return: Bool - True if connected nodes are empty
        """
        node_connectivity = self.node_connectivity_matrix[node_index]
        for i, node in enumerate(node_connectivity):
            # If connected
            if node != 0:
                # If connected node is built on return False
                if not self.nodes[i].isEmpty():
                    return False

        return True

    def nodeHasRoad(self, node_index, player_index):
        """
        Checks a node is connected to an edge with a road built by player player_index
        :param node_index: Index of node to check
        :param player_index: Index of player to check road of
        :return: Bool - True if any connected edges have a road built by player player_index on them
        """
        # For each connected edge check road
        for edge in self.nodes[node_index].connected_edges:
            if edge.road[player_index] == 1:
                return True

        return False

    def edgeHasRoadOrSettlement(self, edge_index, player_index):
        """
        Checks an edge is connected at either end to another road, settlement or city belonging to player player_index
        :param edge_index: Index of edge to check
        :param player_index: Index of player to check connections of
        :return: Bool - True if either connected node is connected
        """
        # Check if player has settlement or city on either node or if player has a road connected to either node
        for node_index in range(2):
            if self.nodes[self.edges[edge_index].nodes[node_index]].settlement[player_index] == 1 or self.nodes[self.edges[edge_index].nodes[node_index]].city[player_index] == 1:
                return True

            if self.nodeHasRoad(self.edges[edge_index].nodes[node_index], player_index):
                return True

        return False

    def getLengthOfRoad(self, edge_index, player_index):
        """
        Gets length of continuous road connected to edge edge_index
        :param edge_index: Index of edge to calculate road length of
        :return:
        """

        # First search out from edge

        self._recursiveRoadLength(edge_index, self.edges[edge_index].nodes[0], player_index)



    def _recursiveRoadLength(self, edge_index, node_index, player_index):

        # Check player player_index has roads connected to node node_index that isn't edge edge_index
        for edge in self.nodes[node_index].connected_edges:

            print(edge)

class Hex:
    def __init__(self, ID, resource_index):
        self.ID = ID
        self.resource_index = resource_index
        self.dice_roll = 0
        self.probability = 0


def probabilityOfRoll(number):
    a = [0, 0, 1.0/36.0, 2.0/36.0, 3.0/36.0, 4.0/36.0, 5.0/36.0, 6.0/36.0, 5.0/36.0, 4.0/36.0, 3.0/36.0, 2.0/36.0, 1.0/36.0]
    return a[number]