import random

from src.Game.Board import *

"""
GameManager class to store and manage rules of game
"""

class GameManager:
    def __init__(self, players):
        # Initialise Board
        number_of_players = 4
        self.game_board = Board(number_of_players)
        self.game_board.generateBoard()

        # Initialise power cards
        """
        - number_of_power_cards is list of quantities of each type of power card 
        - List is in order: [Knight, Take 2 Resources, Construct 2 Roads, Monopoly, Victory Point] 
        """
        number_of_power_cards = [20, 3, 3, 3, 5]

        # Initialise player states
        self.players = players
        self.player_turn = 0
        self.starting_player = 0
        self.points = [0, 0, 0, 0]
        for index, player in enumerate(self.players):
            player.player_index = index
            player.game_manager = self

        # Start game
        print("Starting Game")
        self.turn_counter = 0
        self.setup_players()

    def setup_players(self):
        """
        Defines game logic used at start of game when players must place settlements.

        1) Choose random player to start
        2) Player chooses where to place settlement
        3) Player chooses where to place road
        4) Repeat steps 2 and 3 for each player incrementing player index
        5) Repeat steps 2 and 3 for each player decrementing player index
        """

        print('Setup Phase:\n')

        # Step 1
        self.starting_player = random.randrange(0, 3)
        print('First player is: Player ' + str(self.starting_player) + '\n')

        # Create ordered list corresponding to order of placing settlements
        setup_order = [self.starting_player] * 8
        for i in range(3):
            setup_order[i + 1] = loopingIterator(setup_order[i])
        setup_order[4] = setup_order[3]
        for i in range(3):
            setup_order[i + 5] = loopingIterator(setup_order[i + 4], increment=False)

        for player_index in setup_order:
            self.players[player_index].setup()

        self.player_turn = int(self.starting_player)
        self.turn()

    def turn(self):
        """
        Defines logic for what happens on a new turn.

        1) Roll die and update all players with resources
        2) Keep re

        Call take turn function in player class and check if turn wins game
        """

        print(self.turn_counter)

        # Take turn
        self.players[self.player_turn].action()
        self.turn_counter += 1

        # Check if player has won
        for index, player in enumerate(self.players):
            self.points[index] = self.count_points(player)
            if self.points[index] == 10:
                print("Player " + str(self.player_turn) + " has won!")
                player.endGame(self.points[index])
                return

        if self.player_turn != 3:
            self.player_turn += 1
        else:
            self.player_turn = 0

        self.turn()

    def count_points(self, player):
        return self.turn_counter


    def endTurn(self):
        """
        Checks whether player can end turn, if so end turn
        :return: Bool - can player pass
        """

        # True apart from whilst setting up game (turn 0)
        if self.turn_counter != 0:
            self.player_turn += 1
            return True
        else:
            return False

    def buildSettlement(self, player, node_index):
        """
        Checks whether player can build a settlement at given node index
        :param player: Player class instance
        :param node_index: Index of node which player wants to build on
        :return: Bool - can player build at desired location
        """

        """
        Checks to perform:
        
        1) Node isn't occupied
        2) Player has resources OR game is in setup phase
        3) Player has enough settlement pieces to place
        4) Node is at least two edges away from another city
        """

        # Check 1
        if not self.game_board.nodes[node_index].isEmpty():
            return False

        # Check 2
        if self.turn_counter != 0:
            if not ((player.resource_cards[0] > 0) and (player.resource_cards[2] > 0) and (player.resource_cards[3] > 0) and (player.resource_cards[4] > 0)):
                return False



        # If gotten this far, settlement passes all checks:
        
        # Update board
        self.game_board.nodes[node_index].settlement[player.player_index] = 1

        # Update resources in players hand
        if self.turn_counter != 0:
            player.resource_cards[0] -= 1
            player.resource_cards[2] -= 1
            player.resource_cards[3] -= 1
            player.resource_cards[4] -= 1

        print('Player ' + str(player.player_index) + ' built settlement on node ' + str(node_index))


    def isMoveValid(self):
        """
        Break down into tests of valid roads settlements etc
        :return:
        """
        pass

    def updateBoard(self):
        pass


def loopingIterator(current_index, increment=True, players=4):
    """
    Get index of next player if incrementing or decrementing index
    :param current_index: current index before increment
    :param increment: boolean value: True means increment index, False means decrement
    :param players: number of players in game
    :return: next index
    """
    if increment:
        next_value = current_index + 1
        if next_value == players:
            return 0
        else:
            return next_value

    else:
        next_value = current_index - 1
        if next_value == -1:
            return players - 1
        else:
            return next_value


if __name__ == "__main__":
    a = 0
    b = 0
    for i in range(10):
        a = loopingIterator(a)
        b = loopingIterator(b, increment=False)

        print(a, b)