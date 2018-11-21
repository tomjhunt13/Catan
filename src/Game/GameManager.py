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

        # Start off robber on desert tile
        for index, hex in enumerate(self.game_board.hexes):
            if hex.resource_index == -1:
                self.robber_location = index

        """
        Initialise development cards:
        
        - self.development_cards is deck of development cards 
        - Indices refer to: [Knight, Take 2 Resources, Construct 2 Roads, Monopoly, Victory Point] 
        """
        number_of_development_cards = [20, 3, 3, 3, 5]
        self.development_cards = []
        for development_card_index in range(5):
            for i in range(number_of_development_cards[development_card_index]):
                self.development_cards.append(development_card_index)
        random.shuffle(self.development_cards)

        # Initialise player states
        self.players = players
        self.player_turn = 0
        self.starting_player = 0
        self.points = [0, 0, 0, 0]


        self.road_network = [None] * 4
        self.road_lengths = [0, 0, 0, 0]
        self.longest_road_player_index = 0

        self.settlements = [0, 0, 0, 0]
        self.cities = [0, 0, 0, 0]

        self.knights = [0, 0, 0, 0]
        self.largest_army_index = 0

        for index, player in enumerate(self.players):
            player.player_index = index
            player.game_manager = self

            # Initialise player road network
            self.road_network[index] = RoadNetwork(self.game_board, index)

        # self.action_functions is a dictionary storing references to the functions to perform actions
        self.action_functions = {'Settlements': self.buildSettlement,
                                 'Cities': self.buildCity,
                                 'Roads': self.buildRoad,
                                 'TradeWithGame': self.tradeWithGame,
                                 'BuyDevelopmentCard': self.buyDevelopmentCard,
                                 'Knight': self.useKnightCard}

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

        for i in range(len(self.players)):
            print('Player ' + str(i) + ' finished with ' + str(self.countPoints(i)) + ' points')

    def turnManager(self):
        """
        Outer loop for turn function
        """
        game_ended = False

        while not game_ended:

            # Take turn
            self.turn()

            # Check game has ended
            if self.countPoints(self.player_turn) == 10:
                print('Player ' + str(self.player_turn) + ' has won!')
                game_ended = True
                break

            elif self.turn_counter == 200:
                print('No player won')
                game_ended = True
                break

            print('Player ' + str(self.player_turn) + ' has ' + str(self.countPoints(self.player_turn)) + ' points')

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

                # Check hex isn't blocked by robber
                if hex.ID != self.robber_location:

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
            self.robber()

        # Step 2: Make current player perform actions until they pass go
        self.players[self.player_turn].action()

    def robber(self):
        """
        Manages event where 7 is rolled
        """

        print('Robber')

        # First go through each player and if they have 8 or more cards, tell them to discard half
        for player in self.players:
            if sum(player.resource_cards) > 7:
                player.discardHalfCards()

        # Next current player must move robber
        self.moveRobber(self.player_turn)

    def moveRobber(self, player_index):
        """
        Contains logic for moving robber and stealing resource cards
        :param player_index: Index of player moving robber
        """

        self.players[player_index].moveRobber()
        print('Player ' + str(player_index) + ' moved robber to hex: ' + str(self.robber_location))

        # Get list of all players with connected settlements
        players_to_steal_from = []
        for node in self.game_board.hex_node_connectivity[self.robber_location]:
            for index, player_has_settlement in enumerate(self.game_board.nodes[node].settlement):
                if player_has_settlement == 1 and index != player_index:
                    if index not in players_to_steal_from and sum(self.players[index].resource_cards) > 0:
                        players_to_steal_from.append(index)

        # Steal resource card from a player with a connected settlement to hex
        if len(players_to_steal_from) != 0:
            chosen_player = self.players[player_index].choosePlayerToStealFrom(players_to_steal_from)

            # Get random resource from player
            num_cards = sum(self.players[chosen_player].resource_cards)
            cards_to_take = random.randint(0, num_cards - 1)

            for resource_type in range(5):
                cards_to_take -= self.players[chosen_player].resource_cards[resource_type]
                if cards_to_take < 0:
                    self.players[chosen_player].resource_cards[resource_type] -= 1
                    print('Player ' + str(player_index) + ' stole resource type ' + str(resource_type) + ' from player ' + str(chosen_player))
                    break


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
        6) Don't allow building by port on turn 1
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

        # Break road network for each player apart from player player_index
        for player_i in range(4):
            if player_i != player.player_index:
                self.road_network[player_i].breakRoadAtNode(node_index)

        # Update player best_trade_type if new settlement on port
        if sum(self.game_board.nodes[node_index].ports) != 0:

            # Stop player building by port on setup round
            if self.turn_counter == 0:
                return False

            # Get index of port
            port_index = 0
            for index in range(6):
                if self.game_board.nodes[node_index].ports[index] == 1:
                    port_index = index

            # If 3:1 check that port is better for each resource than existing
            if port_index == 0:
                for resource_index in range(5):
                    if player.best_trade_type[resource_index] > 3:
                        player.best_trade_type[resource_index] = 3
                print('Player ' + str(player.player_index) + ' built a 3:1 port')

            # Else update relevant best_trade_type in Player
            else:
                player.best_trade_type[port_index - 1] = 2
                print('Player ' + str(player.player_index) + ' built a 2:1 port  of resource type ' + str(port_index - 1))

        # Update tally of settlements
        self.settlements[player.player_index] += 1

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

        # Check road is long enough for longest road
        if player_road_length >= 5:

            # Check if new road length is longer than current longest
            max_road_length = max(self.road_lengths)
            number_with_same_length = 0
            for i in range(4):
                if self.road_lengths[i] == max_road_length:
                    number_with_same_length += 1

            if number_with_same_length != 1:
                self.longest_road_player_index = player.player_index
                print('Player ' + str(player.player_index) + ' has longest road')

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
        self.cities[player.player_index] += 1
        self.settlements[player.player_index] -= 1

        print('Player ' + str(player.player_index) + ' built a city on node ' + str(node_index))
        return True

    def tradeWithGame(self, player, trade_index):
        """
        Handles port trading and 4:1 trading
        :param player: Player instance
        :param trade_index: Index of trade to make.
                            0 - 3 is trading Wheat for other
                            4 - 7 is trading Stone for other
                            8 - 11 is trading Brick for other
                            12 - 15 is trading Sheep for other
                            16 - 19 is trading Wood for other

        :return: Bool - can player make the trade
        """

        # Unpack trade_index
        trade_index_to_resource_map = [
            [0, 1],
            [0, 2],
            [0, 3],
            [0, 4],

            [1, 0],
            [1, 2],
            [1, 3],
            [1, 4],

            [2, 0],
            [2, 1],
            [2, 3],
            [2, 4],

            [3, 0],
            [3, 1],
            [3, 2],
            [3, 4],

            [4, 0],
            [4, 1],
            [4, 2],
            [4, 3],
        ]

        resource_index_to_trade = trade_index_to_resource_map[trade_index][0]
        desired_resource = trade_index_to_resource_map[trade_index][1]

        # First find out best trade deal player can make
        required_resources = player.best_trade_type[resource_index_to_trade]

        # Check player has enough cards
        if player.resource_cards[resource_index_to_trade] < required_resources:
            return False

        # Else make trade
        player.resource_cards[resource_index_to_trade] -= required_resources
        player.resource_cards[desired_resource] += 1

        print('Player ' + str(player.player_index) + ' traded ' + str(required_resources) + ' resources of type ' + str(resource_index_to_trade) + ' for 1 resource of type ' + str(desired_resource))


        return True

    def countPoints(self, player_index):
        """
        Counts the total number of points player player_index has
        :param player_index: Index of player to count points of
        :return: Number of points
        """

        total_points = 0

        # Settlements and Cities
        total_points += self.settlements[player_index]
        total_points += 2 * self.cities[player_index]

        # Roads
        if self.road_lengths[self.longest_road_player_index] >= 5:
            if player_index == self.longest_road_player_index:
                total_points += 2

        # Largest army
        if self.knights[self.largest_army_index] >= 3:
            if player_index == self.largest_army_index:
                total_points += 2


        return total_points

    def useKnightCard(self, player, *args):
        """
        Uses knight development card
        :return: Bool - can player use knight development card
        """

        # First check player has Knight development card
        if player.development_cards[0] == 0:
            return False

        print('Player ' + str(player.player_index) + ' has played a knight card')

        # Move robber
        self.moveRobber(player.player_index)

        # Update knights
        self.knights[player.player_index] += 1

        # Check player has enough knights for largest army
        if self.knights[player.player_index] >= 3:

            # Check if new army is larger than current largest
            max_army_size = max(self.knights)
            number_with_same_length = 0
            for i in range(4):
                if self.road_lengths[i] == max_army_size:
                    number_with_same_length += 1

            if number_with_same_length != 1:
                self.largest_army_index = player.player_index
                print('Player ' + str(player.player_index) + ' has largest army')

        return True

    def useTwoRoadsCard(self):
        pass

    def useMonopolyCard(self):
        pass

    def useVictoryPointCard(self):
        pass

    def useTakeTwoResourcesCard(self):
        pass

    def buyDevelopmentCard(self, player, *args):
        """
        Checks whether player can buy a development card and does so if can
        :param player: Player class instance
        :return: Bool - can player buy development card
        """

        # Check player has enough resources
        if not player.hasResources([1, 1, 0, 1, 0]):
            return False

        # Check enough development cards in deck
        if len(self.development_cards) == 0:
            return False

        # Remove development card from deck and give to player
        development_card_index = self.development_cards[0]
        player.development_cards[development_card_index] += 1
        self.development_cards.remove(development_card_index)

        # Remove resources from player
        player.resource_cards[0] -= 1
        player.resource_cards[1] -= 1
        player.resource_cards[3] -= 1

        # Update all other players
        for player_index in range(4):
            if player_index != player.player_index:
                self.players[player_index].number_of_development_cards[player.player_index] += 1

        print('Player ' + str(player.player_index) + ' has purchased a development card.')

        return True


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
