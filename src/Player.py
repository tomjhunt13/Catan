import random
import math


class Player:
    def __init__(self, move_function):
        """
        Class to handle player
        :param move_function: Reference to function which determines which move to make next
        """

        self.player_index = 0
        self.game_manager = None
        self.move_function = move_function

        # Information known about other players (ignore element corresponding to self)
        self.number_of_resource_cards = [0, 0, 0, 0]
        self.number_of_development_cards = [0, 0, 0, 0]

        """
        Power Cards:

        - self.development_cards is a list of number of each type of card
         - List order is: [Knight, Take 2 Resources, Construct 2 Roads, Monopoly, Victory Point]]
        """
        self.development_cards = [0] * 5

        """
        Resources:

        - self.resource_cards is a list of number of each type of class
        - list order is: [Wheat, Stone, Brick, Sheep, Wood]
        - self.resource_dice_rolls is a list of which rolls get each resource
        """
        self.resource_cards = [0] * 5

        """
        Initialise road, settlement and city pieces:

         - self.building_pieces is list of quantities of each type of piece 
         - List is in order: [Road, Settlement, City] 
        """
        self.building_pieces = [15, 5, 4]


        # List of best trade deals via ports / 4:1 for each resource
        self.best_trade_type = [4, 4, 4, 4, 4]

    def setup(self):
        """
        Defines player logic for set-up phase of game (Turn 0)
        :return: node_index of settlement, edge_index of road
        """
        print('\nPlayer ' + str(self.player_index) + ':')
        print('Placing settlement')
        # Evaluate network to get output vector and dictionary
        network_output, vector_output = self.evaluateNetwork(self.assembleInputVector())
        settlements_vector = network_output['Settlements']

        # Whilst settlement hasn't been placed, find maximum node in settlements_vector and try and build there. If can't, choose next best
        settlement_built = False
        nodes_tested = 0
        while not settlement_built:
            nodes_tested += 1
            desired_node = settlements_vector.index(max(settlements_vector))
            if self.game_manager.buildSettlement(self, desired_node):
                settlement_built = True
            else:
                settlements_vector[desired_node] = 0

            if nodes_tested == 53:
                break

        print('Placing road')
        # Evaluate network to get output vector and dictionary
        network_output, vector_output = self.evaluateNetwork(self.assembleInputVector())
        roads_vector = network_output['Roads']

        # Get list of connected edges which player has built settlement on
        available_edges = self.game_manager.game_board.nodes[desired_node].connected_edges

        # Find edge from available edges with highest value of roads vector
        road_location = available_edges[0].ID
        max_output = roads_vector[road_location]
        for edge in available_edges:
            if roads_vector[edge.ID] > max_output:
                road_location = edge.ID
                max_output = roads_vector[edge.ID]

        self.game_manager.buildRoad(self, road_location)

        return desired_node, road_location

    def action(self):
        """
        Wrapper around controller for player. Continuously makes decisions until pass decision made
        """

        # Evaluate network and return decision
        network_output, vector_output = self.evaluateNetwork(self.assembleInputVector())

        # Go through output from decision corresponding to highest output to lowest until valid move found
        while True:

            # Find highest decision
            key, element = getHighestAcrossDictionaries(network_output)

            # Check for ending turn
            if key == 'EndTurn':
                return
            else:
                # If not ending turn, attempt action or set corresponding element to 0 if not possible
                self.game_manager.action_functions[key](self, element)
                network_output[key][element] = 0

        # If not returned, call action again to make next decision
        self.action()

    def endGame(self, points):
        pass

    def updateOtherPlayers(self):
        pass

    def assembleInputVector(self):
        """
        Assembles input vector for network based on current state of board
        :return: input vector
        """
        # Assemble all input values
        board_vector = self.game_manager.game_board.getInputValues()
        return board_vector + self.number_of_resource_cards + self.number_of_development_cards + self.development_cards + self.resource_cards

    def evaluateNetwork(self, input_vector):
        return self.move_function(input_vector)

    def hasResources(self, resources):
        """
        Checks player has resources
        :param resources: Vector of quantity of resources required in order [Wheat, Stone, Brick, Sheep, Wood]
        :return: Bool - True if player has enough resources
        """
        if (self.resource_cards[0] >= resources[0]) and (self.resource_cards[1] >= resources[1]) and (
                self.resource_cards[2] >= resources[2]) and (self.resource_cards[3] >= resources[3]) and (
                self.resource_cards[4] >= resources[4]):
            return True

        return False

    def discardHalfCards(self):
        """
        Currently discards random choice of cards
        """

        # Get number of cards to discard
        total_cards_in_hand = sum(self.resource_cards)
        number_to_discard = math.ceil(total_cards_in_hand / 2.0)

        # Discard cards
        while number_to_discard != 0:
            index_to_discard = random.randint(0, 4)
            if self.resource_cards[index_to_discard] != 0:
                self.resource_cards[index_to_discard] -= 1
                number_to_discard -= 1

    def moveRobber(self):
        """
        Moves robber and takes card from player
        """

        # Now random!
        self.game_manager.robber_location = random.randint(0, 17)

    def choosePlayerToStealFrom(self, list_of_players):
        """
        Choose which player to steal from when player must choose to steal resource card from another player (ie robber)
        """

        # Currently random
        random.shuffle(list_of_players)
        return list_of_players[0]






def getHighestAcrossDictionaries(output_dictionary):
    """
    Given a dictionary of lists, find the dictionary key and element index of the highest valued element in the dictionary
    :param output_dictionary: Dictionary to search
    :return: key - Key of dictionary with highest valued element, index - index of highest valued element in key
    """
    max_key = None
    element_index = None
    current_max = 0

    # Check through each key in dictionary
    for key in output_dictionary.keys():

        # Return index of max value in key
        max_value_in_key = max(output_dictionary[key])
        index_of_max_value_in_key = output_dictionary[key].index(max_value_in_key)

        # If larger than existing largest, update max_key and element_index
        if max_value_in_key > current_max:
            max_key = key
            element_index = index_of_max_value_in_key
            current_max = max_value_in_key

    return max_key, element_index


def randomAction(inputVector):
    """
    Sample wrapper function for network
    :param inputVector: vector containing all player knowledge of the game state
    :return: dictionary made up of vectors containing the choices made by the network broken up by category for convenience
    """

    # Generate random values for choices of settlement placement
    settlements = [0] * 54
    cities = [0] * 54
    for i in range(54):
        settlements[i] = random.uniform(0, 1)
        cities[i] = random.uniform(0, 1)

    # Generate random values for choices of settlement placement
    roads = [0] * 72
    for i in range(72):
        roads[i] = random.uniform(0, 1)

    # Trading
    trade_with_game = [0] * 20
    for i in range(20):
        trade_with_game[i] = random.uniform(0, 1)

    # Ending turn
    end_turn = [random.uniform(0, 1)]

    # Purchasing development card
    buy_development_card = [random.uniform(0, 1)]

    # Use development card
    knight = [random.uniform(0, 1)]

    output_dictionary = {'Settlements': settlements, 'Cities': cities, 'Roads': roads,
                         'EndTurn': end_turn, 'TradeWithGame': trade_with_game,
                         'BuyDevelopmentCard': buy_development_card,
                         'Knight': knight}
    output_vector = settlements + cities + roads + end_turn + trade_with_game + buy_development_card + knight

    return output_dictionary, output_vector