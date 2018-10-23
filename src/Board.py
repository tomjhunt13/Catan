class Node:
    def __init__(self, ID, number_of_players):
        """
        Class to represent node on board graph
        :param ID: ID of node
        :param number_of_players: number of players in game
        """
        self.ID = ID

        # Node state
        self.resource_probabilities = [0] * 5
        self.settlement = [0] * number_of_players
        self.city = [0] * number_of_players

        """
        Ports:
        - self.ports is a boolean list stating if a port type exists on this node
        - list order is: [ 3:1, 2:1 Wheat, 2:1 Stone, 2:1 Brick, 2:1 Sheep, 2:1 Wood ]
        """
        self.ports = [0] * 6


class Edge:
    def __init__(self, node_1, node_2, number_of_players):
        """
        Class to represent edge on board graph
        :param node_1: ID of first connected node
        :param node_2: ID of second connected node
        :param number_of_players: number of players in game
        """

        # Node connectivity
        self.node_1 = node_1
        self.node_2 = node_2

        # Edge state
        self.road = [0] * number_of_players


class Board():
    """
    Class used to represent board
    """

    def __init__(self):
        pass