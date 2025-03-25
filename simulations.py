import random
from settings import *
from blackjack import Blackjack
from solutionTable import solution_table


def simulatation(trials, starting_balance):
    total_winnings = 0
    
    for _ in range(trials):
        
        # Start Game
        game = Blackjack(starting_balance)
        
        balance = starting_balance

        #Intialize game_bet
        game_bet = 0
        
        # Each time this while loop runs represents 1 "night out"...
        # In this case, there is a max amount of money to spend in one trip.
        # Also, betting rules can be tweaked... See below.
        
        while game_bet <= starting_balance:
            # Rule for betting
            bet = random.randint(1, game.user_balance)  # Random valid bet
            balance -= bet

            #Note about ABOVE: We should probably add a minimum betting option in the Blackjack script.. - Amanuel

            game_bet += bet
        
            # Simulate player's game (automated hitting strategy: hit below 17)
            while game.get_hand_value(game.players['user']) < 17:
                game.player_hit('user')
        
            game.dealer_play()
            winning_result = game.check_winner()
            game.adjust_balance(bet, winning_result)
            
        
        total_winnings += game.user_balance - starting_balance

    
    total_bet = trials * starting_balance
    ev = total_winnings / total_bet

    return ev


trials = 10000  # Number of simulations
starting_balance = 1000  # Arbitrary starting balance
ev = simulatation(trials, starting_balance)
print(f"Estimated EV per $ bet: {ev:.4f}")
