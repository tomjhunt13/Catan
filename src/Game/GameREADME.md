# Current Framework:


- _GameManager_ is responsible for all rules and logic of the game as well incrementing the turn
- _Board_ is a representation of the board
- _Player_ contains all the information a single player knows about the game. It makes decisions each turn based on the information it knows
- _develop.py_ is an example script which instantiates all game classes and calls the run function

# Things To Do:
- _Ports:_ Add in ports and port trading. 
    1) Set up port locations in Board \_\__init_\_\_ function
    2) Add function in _GameManager_ to make trades via the ports / using 4:1 without ports
    
- _Win Condition:_ Add points to game and end it when player has won.

- _Player To Player Trading:_ Implement a mechanism to trade with other players and an interface for the AI. Current ideas are: 
    1) Player has function which decides whether or not to accept trade. Try out many combinations on self to find own best offer and offer to others
    
- _Board Setup_: Implement proper ordering of dice roll counters on board in setup

- _Development Cards_: Implement all development cards    