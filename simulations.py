import random
from settings import *
from blackjack import Blackjack
from solutionTable import solution_table
from multiprocessing import Pool
import time

from math import floor

def simulatateThread(params):
    trials = params[0]
    starting_balance = params[1]
    id = params[2]
    
    total_winnings = 0
    
    for i in range(trials):

        if i % 10 == 0:
            print(id, "Trial Number:", i) 
        
        # Start Game
        game = Blackjack(starting_balance)

        #Intialize night_bet and game.user_balance
        night_bet = 0
        
        # Each time this while loop runs represents 1 "night out"...
        # In this case, there is a max amount of money to spend in one trip.
        # Also, betting rules can be tweaked... See below.
        
        game.user_balance = starting_balance

        while night_bet < starting_balance:
            
            # Rule for betting
            if game.user_balance < MIN_BET:
                break
            bet = random.randint(MIN_BET, min(game.user_balance, MAX_BET))  # Random valid bet
            game.user_balance -= bet

            #Note about ABOVE: We should probably add a minimum betting option in the Blackjack script.. - Amanuel

            night_bet += bet
        
            # Simulate player's game (automated hitting strategy: hit below 17)
            # while game.get_hand_value("user") < 17:
            #     game.player_hit('user')
            
            dealer_hand_value = game.get_card_value(game.players['dealer'][0])
            player_hand_value = 0
            decision = ''

            for player in game.players:                
                if player == 'user':
                    while game.get_player_hand_value('user') < 21 and decision != 'S':
                        player_hand_value = game.get_player_hand_value('user')
                        decision = solution_table[player_hand_value - 4][dealer_hand_value - 2]

                        if decision == "D":
                            game.player_hit('user')
                else:
                    while game.get_player_hand_value(player) < 21:
                        if game.get_player_hand_value(player) < 17:
                            game.player_hit(player)
                        else:
                            break
                            
            winning_result = game.check_winner()
            game.adjust_balance(bet, winning_result)
            game.reset_game()
        
        total_winnings += game.user_balance


            
    total_bet = trials * starting_balance
    ev = total_winnings / total_bet
    return ev

def simulations(trials, starting_balance):
    trials_assigned = []
    trials_left = trials
    ev = 0
    params = []
    for i in range(THREAD_COUNT):
        trials_to_do = floor(trials/THREAD_COUNT)
        trials_left -= trials_to_do
        if(trials_left < floor(trials/THREAD_COUNT)):
            trials_to_do += trials_left
            trials_left = 0

        trials_assigned.append(trials_to_do)
        params.append([trials_to_do, starting_balance, i])
    
    i = 0
    with Pool(THREAD_COUNT) as p:
        for x in p.map(simulatateThread, params):
            ev += x * (trials_assigned[i]/trials)
            i+=1
        return ev

if __name__ == '__main__':
    trials = 1000 # Number of simulations
    start_time = time.time()
    ev = simulations(trials, STARTING_BALANCE)
    print(f"Estimated EV per $ bet: {ev:.4f}")
    print(f"Calculated in {time.time() - start_time:.2f}")
