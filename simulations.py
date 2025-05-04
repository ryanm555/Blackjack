import random
from settings import *
from blackjack import Blackjack
from solutionTable import solution_table
from multiprocessing import Pool
import time

import numpy as np
from math import floor, sqrt

def simulatateThread(params):
    trials = params[0]
    starting_balance = params[1]
    id = params[2]
    
    nightly_results = []
    
    for i in range(trials):

        #Each iteration of this for loop represents 1 "night out"
        #In this case, there is a max amount of money to spend in one trip.

        if i % 20000 == 0 and id == 0:
            print(id, "Trial Number:", i) 
        
        # Start Game
        game = Blackjack(starting_balance)

        #Intialize night_bet and game.user_balance
        night_bet = 0
        
        #Each iteration of this while loop is one game
        #Also, betting rules can be tweaked... See below.
        
        game.user_balance = starting_balance

        while night_bet + CONSTANT_BET < starting_balance:
            
            bet = CONSTANT_BET

            game.user_balance -= bet

            night_bet += bet
            
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
        
        #This needs to be inside the for loop..
        #How much money are you leaving with after betting "starting_balance"
        nightly_ev = game.user_balance / starting_balance #Techically, this is wrong. It assumes that all money is used, but w/ $25 bet consistently it actually is.
        nightly_results.append(nightly_ev)
    
    return nightly_results

def simulations(trials, starting_balance):
    trials_assigned = []
    trials_left = trials
    all_nightly_results = []
    params = []
    
    
    for i in range(THREAD_COUNT):
        trials_to_do = floor(trials/THREAD_COUNT)
        trials_left -= trials_to_do
        if(trials_left < floor(trials/THREAD_COUNT)):
            trials_to_do += trials_left
            trials_left = 0

        trials_assigned.append(trials_to_do)
        params.append([trials_to_do, starting_balance, i])
    
    with Pool(THREAD_COUNT) as p:
        for thread_results in p.map(simulatateThread, params):
            all_nightly_results.extend(thread_results)
    
    # Calculate overall EV and standard deviation from all results
    overall_ev = np.mean(all_nightly_results)
    overall_std_dev = np.std(all_nightly_results)

    return overall_ev, overall_std_dev

if __name__ == '__main__':
    trials = 100000 # Number of simulations
    start_time = time.time()
    ev, std_dev = simulations(trials, STARTING_BALANCE)
    print(f"Estimated EV per $ bet: {ev:.4f}")
    print(f"Standard Deviation of nightly EV: {std_dev:.4f}")
    print(f"Calculated in {time.time() - start_time:.2f}")
