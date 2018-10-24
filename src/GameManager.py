from src.Board import *
from src.Player import *


"""
GameManager class to store and manage rules of game
"""

class GameManager:
    def __init__(self, players):
        # Initialise Board
        number_of_players = 4
        self.game_board = Board(number_of_players)
        self.game_board.generateBoard()

        # Initialise player states
        self.players = players
        self.player_turn = 0
        self.points = [0, 0, 0, 0]

        # Start game
        print("Starting Game")
        self.turn_counter = 0
        self.turn()

    def turn(self):
        """
        Call take turn function in player class and check if turn wins game
        """

        print(self.turn_counter)

        # Take turn
        self.players[self.player_turn].takeTurn(self)
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

    def isMoveValid(self):
        pass

    def updateBoard(self):
        pass


