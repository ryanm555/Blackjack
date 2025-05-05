import random
from settings import *
class Blackjack:
    def __init__(self, balance):

        one_deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', "J", 'Q', 'K', 'A'] * 4
        self.deck = one_deck * NUM_DECKS
        #Shuffle Deck
        random.shuffle(self.deck)
        #Players Card Initialized
        self.players = PLAYERS
        #Reset Cards    
        for player in self.players:
            self.players[player] = []
        
        self.game_over = False
        self.user_balance = balance

        #Give every player two cards to start
        for player in self.players:
            self.players[player].append(self.draw_card())
            self.players[player].append(self.draw_card())

    def draw_card(self):
        #Return a card while removing it from the deck
        return self.deck.pop()
    
    def get_card_value(self, card, ace_value=11):
        if card in ["K", "Q", "J"]:
            return 10
        elif card == "A":
            return ace_value
        else:
            return int(card)
        
    def get_player_hand_value(self, player):
        #Get value of the hand
        hand = self.players.get(player)
        value = sum(self.get_card_value(card) for card in hand)
        aces = hand.count('A')

        #If over and have an ace, ace automatically = 1
        while value > 21 and aces > 0:
                value -= 10
                aces -= 1

        return value
    
    def player_hit(self, player, ace_value=11):
        if not self.game_over:
            self.players[player].append(self.draw_card())

            if self.get_player_hand_value(player) > 21:
                return True #Player Bustet Return True
            
            return False #No bust contiues Game
            
    def dealer_play(self):
        #Dealer can not draw any more cards if hand_value > 17
        while self.get_player_hand_value('dealer') < 17:
            self.players['dealer'].append(self.draw_card())
    
    def reset_game(self):
        self.__init__(self.user_balance)

    def check_winner(self):
        dealer_value = self.get_player_hand_value('dealer')
        winning_players = []

        # If dealer busts, all non-busted players win
        if dealer_value > 21:
            return [player for player in self.players if player != 'dealer' and self.get_player_hand_value(player) <= 21]

        # Otherwise, find the highest valid player score
        highest_score = -1
        for player in PLAYERS:

            player_value = self.get_player_hand_value(player)
            if player_value > 21:
                continue  # Skip players who bust

            #Check if the player is currently >= to current highest_score
            if player_value >= highest_score:
                if player_value > highest_score: #New Highest Score Found
                    highest_score = player_value
                    winning_players.clear()
                    winning_players.append(player)
                    Standoff = False
                else: #equals old High score so add on
                    winning_players.append(player)
                    Standoff = True
        
        if Standoff:
            return ("Standoff", winning_players)

        return winning_players
    
    def place_bet(self):
        # Prompt for bet from the user
        print(f"\nYour balance: {self.user_balance}")
        bet = 0
        while bet < MIN_BET or bet > MAX_BET or bet > self.user_balance:
            try:
                bet = int(input(f"Place your bet (between {MIN_BET} and {MAX_BET}): "))
                if bet < MIN_BET or bet > MAX_BET:
                    print(f"Bet must be between {MIN_BET} and {MAX_BET}.")
                elif bet > self.user_balance:
                    print("You don't have enough balance to place this bet.")
            except ValueError:
                print("Please enter a valid number.")

        self.user_balance -= bet
        return bet
    
    def has_blackjack(self, player):
        return self.get_player_hand_value(player) == 21 and len(self.players[player]) == 2

    def adjust_balance(self, bet, winning_result):
        if isinstance(winning_result, tuple):
            standoff_players = winning_result[1]
            if 'user' in standoff_players:
                self.user_balance += bet
        elif isinstance(winning_result, list):
            if 'user' in winning_result:
                #You get what you bet back * 2 to replace your bet and add your winnnings
                self.user_balance += bet * 2
        elif winning_result == "Dealer Wins!":
            pass

def main(balance):
    game = Blackjack(balance)
    print("Welcome to Blackjack!\n")

    bet = game.place_bet()
    
    # Print initial hands of all players and the dealer
    print("Initial hands:")
    for player in game.players:
        if player == 'dealer':
            print(f"Dealer's hand: ['{game.players['dealer'][0]}', 'Hidden']")
        else:
            print(f"{player.capitalize()}'s hand: {game.players[player]}, Value: {game.get_player_hand_value(game.players[player])}")
    
    # Players take turns (automated for all except user)
    for player in ['user', 'player1', 'player2', 'player3', 'player4', 'player5', 'player6']: 
        if player == 'user':  # User's turn (interactive)
            print(f"\n{player.capitalize()}'s Turn:")
            while True and game.get_player_hand_value(game.players['user']) <= 21:
                print(f"Your hand: {game.players[player]}, Value: {game.get_player_hand_value(game.players[player])}")

                action = input("Do you want to hit or stand? (h/s): ").lower()
                if action == 'h':
                    is_busted = game.player_hit(player)
                    print(f"You Drew {game.players[player][-1]}")
                    if is_busted:
                        print(f"{player.capitalize()} Busts! Moving to next player.")
                        continue
                else:
                    break  # Player stands

        else:  # Automated players
            print(f"\n{player.capitalize()}'s Turn:")
            #Players do not hit when over 17 like Dealer
            if OTHER_PLAYERS_HIT_LIMIT <= game.get_player_hand_value(game.players[player]) <= 21:
                print(f"{player.capitalize()} Stands")
            while game.get_player_hand_value(game.players[player]) < 17:
                game.player_hit(player)
                print(f"{player.capitalize()} Drew {game.players[player][-1]}")
                print(f"{player.capitalize()}'s hand: {game.players[player]}, Value: {game.get_player_hand_value(game.players[player])}")
    
    # Dealer's turn
    print("\nDealer's turn...")
    game.dealer_play()
    print(f"Dealer Drew: {game.players['dealer'][-1]}")
    print(f"Dealer's hand: {game.players['dealer']}, Value: {game.get_player_hand_value(game.players['dealer'])}")

    # Determine winners
    winning_result = game.check_winner()
    if not winning_result:
        print("Dealer Wins!")
    else:
        #If type is string it is either Dealer Wins or Standoff
        #If type is list it is a list of the winning players
        if isinstance(winning_result, list):
            print(f"\nWinner(s): {', '.join(winning_result)}")
        elif isinstance(winning_result, tuple):
            print(f"\nWinner(s): {winning_result[1]}")

        game.adjust_balance(bet, winning_result)
        print(f"Your Updated Balance: {game.user_balance}")

    if (game.user_balance) == 0:
        print("You are broke and can no longer play!")
    else:
        if input("\nDo you want to play again? (y/n): ").lower() == 'y':
            main(game.user_balance)

if __name__ == "__main__":
    main(STARTING_BALANCE)



# Useful information
# Player goes first
# Followed by all six other players then Dealer
# Currently there is no splitting
# Aces are assumed to be 11 unless over 21 then it turns into a 1
# There is currently no betting system
