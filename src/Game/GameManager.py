import random

from src.Game.Board import *
from src.Game.RoadNetwork import *

"""
GameManager class to store and manage rules of game
"""

class GameManager:
    def __init__(self, players):
        # Initialise Board
        number_of_players = 4
        self.game_board = Board(number_of_players)

        """
        Initialise power cards:
        
        - self.number_of_power_cards is list of quantities of each type of power card 
        - List is in order: [Knight, Take 2 Resources, Construct 2 Roads, Monopoly, Victory Point] 
        """
        self.number_of_power_cards = [20, 3, 3, 3, 5]

        # Initialise player states
        self.players = players
        self.player_turn = 0
        self.starting_player = 0
        self.points = [0, 0, 0, 0]
        self.road_network = [None] * 4
        self.road_lengths = [0, 0, 0, 0]
        for index, player in enumerate(self.players):
            player.player_index = index
            player.game_manager = self

            # Initialise player road network
            self.road_network[index] = RoadNetwork(self.game_board, index)

        # self.action_functions is a dictionary storing references to the functions to perform actions
        self.action_functions = {'Settlements': self.buildSettlement,
                                 'Cities': self.buildCity,
                                 'Roads': self.buildRoad}

    def startGame(self):
        """
        Start game
        """
        print("Starting Game")
        self.turn_counter = 0
        self.setupPlayers()

    def setupPlayers(self):
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

        # Iterate over ordered list and get each player to place a settlement and a road
        settlement_node = [None] * 4
        for player_index in setup_order:
            node_chosen, edge_chosen = self.players[player_index].setup()
            settlement_node[player_index] = node_chosen

        # Give each player one resource from second settlement placement
        for player_index in range(4):
            for resource_index in range(5):
                self.players[player_index].resource_cards[resource_index] = len(self.game_board.nodes[settlement_node[player_index]].resource_dice_rolls[resource_index])

        self.player_turn = int(self.starting_player)
        self.turn_counter = 1
        self.turnManager()

    def turnManager(self):
        """
        Outer loop for turn function
        """
        game_ended = False

        while not game_ended:

            # Take turn
            self.turn()

            # Check game has ended
            if self.turn_counter == 50:
                game_ended = True

            # Increment turn counter
            self.player_turn = loopingIterator(self.player_turn)
            if self.player_turn == self.starting_player:
                self.turn_counter += 1

    def turn(self):
        """
        Defines logic for what happens on a new turn.

        1) Roll die and update all players with resources OR go into robber state
        2) Until player passes, do action
        3) Check no players have reached the score limit
        4) If game hasn't ended increment player counter
        """

        print('\nRound: ' + str(self.turn_counter) + ', Player: ' + str(self.player_turn))

        # Step 1: Roll die and give out resources
        dice_roll = rollDice(2)
        print('Player has rolled a ' + str(dice_roll))

        # Check roll isn't 7
        if dice_roll != 7:
            # Get corresponding hexes on board
            for hex in self.game_board.hex_dice_roll_list[dice_roll]:

                # Get all nodes connected to this hex
                for node_index in self.game_board.hex_node_connectivity[hex.ID]:

                    # For each player check if node built on
                    for player_index in range(4):

                        # Check player has built on node
                        node_resource_contribution = 0
                        if self.game_board.nodes[node_index].settlement[player_index] == 1:
                            node_resource_contribution = 1
                        elif self.game_board.nodes[node_index].city[player_index] == 1:
                            node_resource_contribution = 2

                        self.players[player_index].resource_cards[hex.resource_index] += node_resource_contribution
                        if node_resource_contribution != 0:
                            print('Player ' + str(player_index) + ' has received ' + str(node_resource_contribution) + ' of resource type ' + str(hex.resource_index) + ' from node ' + str(node_index))

                            # Update all other players that player player_index has received resources
                            for i in range(4):
                                if i != player_index:
                                    self.players[i].number_of_resource_cards[player_index] += node_resource_contribution
        else:
            # 7 has been rolled, go into robber state
            print('Robber')

        # Step 2: Make current player perform actions until they pass go
        self.players[self.player_turn].action()

    def count_points(self, player):
        """
        Counts number of points player has
        :param player: Player to count points of
        :return: Number of points player has
        """

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
        Checks whether player can build a settlement at given node index and does so if can
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
        5) Node is connected to a relevant road OR game is in setup phase
        6) Don't allow building by port on turn 1!!!!
        """

        # Check 1
        if not self.game_board.nodes[node_index].isEmpty():
            return False

        # Check 2
        if self.turn_counter != 0:
            if not player.hasResources([1, 0, 1, 1, 1]):
                return False

        # Check 3
        if player.building_pieces[1] == 0:
            return False

        # Check 4 - From node connectivity matrix, check if any node connected to desired build node is built on
        if not self.game_board.connectedNodesBuiltOn(node_index):
            return False

        # Check 5
        if self.turn_counter != 0:
            if not self.game_board.nodeHasRoad(node_index, player.player_index):
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

        # Update settlement pieces
        player.building_pieces[1] -= 1

        # Check settlement hasn't broken chain of roads

        print('Player ' + str(player.player_index) + ' built settlement on node ' + str(node_index))
        return True

    def buildRoad(self, player, edge_index):
        """
        Checks whether player can build a road on a given edge and does so if can
        :param player: Player class instance
        :param edge_index: Index of edge which player wants to build on
        :return: Bool - can player build at desired location
        """

        """
        Checks to perform:

        1) Edge isn't occupied
        2) Player has resources OR game is in setup phase
        3) Player has enough road pieces to place
        4) Either end of edge is connected to settlement, city or road built by player
        """

        # Check 1
        if not self.game_board.edges[edge_index].isEmpty():
            return False

        # Check 2
        if self.turn_counter != 0:
            if not player.hasResources([0, 0, 1, 0, 1]):
                return False

        # Check 3
        if player.building_pieces[0] == 0:
            return False

        # Check 4
        if not self.game_board.edgeHasRoadOrSettlement(edge_index, player.player_index):
            return False

        # If gotten this far, road passes all checks:
        # Update board
        self.game_board.edges[edge_index].road[player.player_index] = 1

        # Update resources in players hand
        if self.turn_counter != 0:
            player.resource_cards[2] -= 1
            player.resource_cards[4] -= 1

        # Update road pieces
        player.building_pieces[0] -= 1

        # Update player RoadNetwork
        self.road_network[player.player_index].addRoad(edge_index)

        # Check if new road is longest road
        player_road_length, path = self.road_network[player.player_index].longestContinousPath()
        self.road_lengths[player.player_index] = player_road_length

        print('Player ' + str(player.player_index) + ' built road on edge ' + str(edge_index) +
              ', connecting nodes ' + str(self.game_board.edges[edge_index].nodes[0]) +
              ' and ' + str(self.game_board.edges[edge_index].nodes[1]) +
              '. Players longest road: ' + str(player_road_length))

        return True

    def buildCity(self, player, node_index):
        """
        Checks whether player can build a city on a given node and does so if can
        :param player: Player class instance
        :param node_index: Index of node which player wants to build city on
        :return: Bool - can player build city at desired location
        """

        """
        Checks to perform:

        1) Player has settlement at node
        2) Player has resources to build city
        3) Player has enough city pieces to place
        """

        # Check 1
        if self.game_board.nodes[node_index].city[player.player_index] == 0:
            return False

        # Check 2
        if not player.hasResources([2, 3, 0, 0, 0]):
            return False

        # Check 3
        if player.building_pieces[2] == 0:
            return False

        # If gotten this far, city passes all checks:
        # Update board
        self.game_board.nodes[node_index].city[player.player_index] == 1

        # Update resources in players hand
        player.resource_cards[0] -= 2
        player.resource_cards[1] -= 3

        # Update city pieces
        player.building_pieces[2] -= 1

        print('Player ' + str(player.player_index) + ' built a city on node ' + str(node_index))
        return True

    def useKnightCard(self):
        pass

    def useTwoRoadsCard(self):
        pass

    def useMonopolyCard(self):
        pass

    def useVictoryPointCard(self):
        pass

    def useTakeTwoResourcesCard(self):
        pass

    def buyPowerCard(self):
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

def rollDice(number_of_die):
    """
    Simulates rolling of number_of_die die and returns result
    :param number_of_die: Number of die to simulate
    :return: Result of roll
    """
    total_value = 0
    for die in range(number_of_die):
        total_value += random.randrange(1, 7)

    return total_value
