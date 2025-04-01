import random
from settings import *
from blackjack import Blackjack
from solutionTable import solution_table


def simulatation(trials, starting_balance):
    total_winnings = 0
    
    for i in range(trials):

        if i % 50 == 0:
            print("Trial Number:", i) 
        
        # Start Game
        game = Blackjack(starting_balance)
        
        balance = game.user_balance

        #Intialize game_bet
        game_bet = 0
        
        # Each time this while loop runs represents 1 "night out"...
        # In this case, there is a max amount of money to spend in one trip.
        # Also, betting rules can be tweaked... See below.
        
        while game_bet <= starting_balance:
            # Rule for betting
            bet = random.randint(MIN_BET, min(game.user_balance, MAX_BET))  # Random valid bet
            balance -= bet

            #Note about ABOVE: We should probably add a minimum betting option in the Blackjack script.. - Amanuel

            game_bet += bet
        
            # Simulate player's game (automated hitting strategy: hit below 17)
            # while game.get_hand_value(game.players['user']) < 17:
            #     game.player_hit('user')
            
            while True:
                player_hand_value = game.get_player_hand_value('user')
                dealer_hand_value = game.get_card_value(game.players['dealer'][0])

                if player_hand_value < 21:
                    decision = solution_table[player_hand_value - 4][dealer_hand_value - 2]
                else:
                    decision = "S"
                    for player in game.players:
                        if player != "user" and player != "dealer ":
                            if game.get_player_hand_value(player) < 17:
                                game.player_hit(player)

                if decision == "D":
                    game.player_hit('user')
                    for player in game.players:
                        if player != "user" and player != "dealer ":
                            if game.get_player_hand_value(player) < 17:
                                game.player_hit(player)
                else:
                    break

            while True:
                game.player_hit("dealer")
                if game.get_player_hand_value("dealer") > 21:
                    break

            # for player in game.players:
            #     if player != "user":
            #         while game.get_hand_value(game.players[player]) < 17:
            #             game.player_hit(player)
                            
            winning_result = game.check_winner()
            game.adjust_balance(bet, winning_result)

            game.reset_game()
            
        
        total_winnings += game.user_balance - starting_balance
    
    total_bet = trials * starting_balance
    ev = total_winnings / total_bet

    return ev


trials = 100  # Number of simulations
ev = simulatation(trials, STARTING_BALANCE)
print(f"Estimated EV per $ bet: {ev:.4f}")
