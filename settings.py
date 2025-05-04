#Bet Settings
MIN_BET = 10
MAX_BET = 100

CONSTANT_BET = 25

#Number of Decks
NUM_DECKS = 4

#USER STARTING_BALANCE
STARTING_BALANCE = 100

#Card
OTHER_PLAYERS_HIT_LIMIT = 17

#Note: The order of play is determined by the order in this dictionary
PLAYERS = {
            'player1': [],    # Player 1's hand
            'player2': [],    # Player 2's hand
            'player3': [],    # Player 3's hand
            #'player4': [],    # Player 4's hand
            #'player5': [],    # Player 5's hand
            #'player6': [],    # Player 6's hand
            'user': [],       # User's hand
            'dealer': []      # Dealer's hand (KEEP THIS AT THE BOTTOM, DEALER PLAYS LAST)
        }

THREAD_COUNT = 10