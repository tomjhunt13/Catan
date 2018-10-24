class Player:
    def __init__(self, move_function):
        """
        Class to handle player
        :param move_function: Reference to function which determines which move to make next
        """

        self.move_function = move_function

        # Information known about other players
        self.number_of_resource_cards = [0, 0, 0]
        self.number_of_power_cards = [0, 0, 0]


        """
        Power Cards:
        - self.power_cards is a list of number of each type of card
         - List order is: [ 1 Point, Monopoly, Knight, 2 Roads, 2 Resources]
        """
        self.power_cards = [0] * 5

        """
        Resources:
        - self.resource_cards is a list of number of each type of class
        - list order is: [ Wheat, Stone, Brick, Sheep, Wood ]
        - self.resource_dice_rolls is a list of which rolls get each resource
        """
        self.resource_cards = [0] * 5

    def takeTurn(self, game_manager):
        # Assemble all input values
        board_vector = game_manager.game_board.getInputValues()
        network_input = board_vector + self.number_of_resource_cards + self.number_of_power_cards + self.power_cards + self.resource_cards
        network_output = self.evaluateNetwork(network_input)

    def endGame(self, points):
        pass

    def updateOtherPlayers(self):
        pass

    def evaluateNetwork(self, input_vector):
        return self.move_function(input_vector)


