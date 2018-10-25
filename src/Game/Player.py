class Player:
    def __init__(self, move_function):
        """
        Class to handle player
        :param move_function: Reference to function which determines which move to make next
        """

        self.player_index = 0
        self.game_manager = None

        self.move_function = move_function

        # Information known about other players
        self.number_of_resource_cards = [0, 0, 0]
        self.number_of_power_cards = [0, 0, 0]


        """
        Power Cards:
        - self.power_cards is a list of number of each type of card
         - List order is: [Knight, Take 2 Resources, Construct 2 Roads, Monopoly, Victory Point]]
        """
        self.power_cards = [0] * 5

        """
        Resources:
        - self.resource_cards is a list of number of each type of class
        - list order is: [ Wheat, Stone, Brick, Sheep, Wood ]
        - self.resource_dice_rolls is a list of which rolls get each resource
        """
        self.resource_cards = [0] * 5

    def setup(self):
        """
        Defines player logic for set-up phase of game (Turn 0)
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





        #self.game_manager.buildSettlement(self, 3)

        print('Placing road')





    def action(self):
        network_output, vector_output = self.evaluateNetwork(self.assembleInputVector())

        # Search for highest output that is a valid move
        # for key, value in network_output

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
        return board_vector + self.number_of_resource_cards + self.number_of_power_cards + self.power_cards + self.resource_cards


    def evaluateNetwork(self, input_vector):
        return self.move_function(input_vector)


