import random
from settings import *
from blackjack import Blackjack

def simulate_blackjack(trials, starting_balance):
    total_bet = 0
    total_winnings = 0
    
    for _ in range(trials):
        game = Blackjack(starting_balance)
        bet = random.randint(MIN_BET, min(MAX_BET, game.user_balance))  # Random valid bet
        total_bet += bet
        
        # Simulate player's game (automated hitting strategy: hit below 17)
        while game.get_hand_value(game.players['user']) < 17:
            game.player_hit('user')
        
        game.dealer_play()
        winning_result = game.check_winner()
        game.adjust_balance(bet, winning_result)
        
        total_winnings += game.user_balance - starting_balance
    
    ev = total_winnings / total_bet if total_bet > 0 else 0
    return ev


trials = 1000000  # Number of simulations
starting_balance = 1000  # Arbitrary starting balance
ev = simulate_blackjack(trials, starting_balance)
print(f"Estimated EV per $ bet: {ev:.4f}")
