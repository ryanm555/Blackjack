import pygame
import sys
from blackjack import Blackjack
from settings import *
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    game = Blackjack(STARTING_BALANCE)  # ✅ Fixed: Pass starting balance
    balance = STARTING_BALANCE
    bet = 0
    user_turn = True  # Track if it's the user's turn
    betting_phase = True  # Player must place a bet before starting

    # Buttons
    bet_10_button = pygame.Rect(100, 500, 100, 50)
    bet_50_button = pygame.Rect(250, 500, 100, 50)
    bet_100_button = pygame.Rect(400, 500, 100, 50)
    
    hit_button = pygame.Rect(100, 600, 150, 50)
    stand_button = pygame.Rect(300, 600, 150, 50)
    play_again_button = pygame.Rect(500, 600, 150, 50)

    clock = pygame.time.Clock()

    while True:
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if betting_phase:
                    if bet_10_button.collidepoint(event.pos) and balance >= 10:
                        bet = 10
                        balance -= 10
                        betting_phase = False
                    elif bet_50_button.collidepoint(event.pos) and balance >= 50:
                        bet = 50
                        balance -= 50
                        betting_phase = False
                    elif bet_100_button.collidepoint(event.pos) and balance >= 100:
                        bet = 100
                        balance -= 100
                        betting_phase = False

                elif not game.game_over:
                    if hit_button.collidepoint(event.pos) and user_turn:
                        is_busted = game.player_hit("user")
                        if is_busted:
                            user_turn = False  # User busts, move to AI & dealer

                    elif stand_button.collidepoint(event.pos) and user_turn:
                        user_turn = False  # Move to AI players and dealer

                elif game.game_over and play_again_button.collidepoint(event.pos):
                    game.reset_game()
                    user_turn = True
                    betting_phase = True  # Restart betting phase

        # Display balance
        draw_text(f"Balance: ${balance}", font, WHITE, screen, 650, 50)

        if betting_phase:
            if balance == 0:
                #Display Broke Message
                draw_text("You are Broke!", font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                sys.exit()

            draw_text("Place Your Bet:", font, WHITE, screen, 100, 450)
            pygame.draw.rect(screen, WHITE, bet_10_button)
            draw_text("$" + str(MIN_BET), small_font, BLACK, screen, 130, 515)

            pygame.draw.rect(screen, WHITE, bet_50_button)
            draw_text("$" + str(MAX_BET // 2), small_font, BLACK, screen, 280, 515)

            pygame.draw.rect(screen, WHITE, bet_100_button)
            draw_text("$" + str(MAX_BET), small_font, BLACK, screen, 430, 515)

        else:
            # Display hands
            y_offset = 50
            for player, hand in game.players.items():
                if player == "dealer":
                    if not game.game_over:
                        draw_text(f"{player.capitalize()}'s hand: {hand[0]}, ?", font, WHITE, screen, 100, y_offset)
                    else:
                        draw_text(f"{player.capitalize()}'s hand: {hand}, Value: {game.get_hand_value(hand)}", font, WHITE, screen, 100, y_offset)
                else:
                    draw_text(f"{player.capitalize()}'s hand: {hand}, Value: {game.get_hand_value(hand)}", font, WHITE, screen, 100, y_offset)
                y_offset += 50

            # If user is done, let AI & dealer play
            if not user_turn and not game.game_over:
                for ai_player in ["player1", "player2", "player3", "player4", "player5", "player6"]:
                    while game.get_hand_value(game.players[ai_player]) < 17:
                        game.player_hit(ai_player)

                game.dealer_play()  # Dealer plays after AI players
                
                # Determine the winner
                winning_result = game.check_winner()
                game.game_over = True  # Mark game as finished

                # Adjust balance based on winner
                if isinstance(winning_result, list) and "user" in winning_result:
                    balance += bet * 2  # Win -> Double the bet
                elif winning_result == "Standoff":
                    balance += bet  # Standoff -> Refund bet

            if game.game_over:
                screen.fill(GREEN)
                draw_text(f"Balance: ${balance}", font, WHITE, screen, 650, 50)

                # Show final hands
                y_offset = 50
                for player, hand in game.players.items():
                    draw_text(f"{player.capitalize()}'s hand: {hand}, Value: {game.get_hand_value(hand)}", font, WHITE, screen, 100, y_offset)
                    y_offset += 50

                # Display winner(s)
                if isinstance(winning_result, list):
                    draw_text(f"Winner(s): {', '.join(winning_result)}", font, WHITE, screen, 100, 500)
                    if 'user' in winning_result:
                        draw_text(f"You Made ${2*bet}", font, WHITE, screen, 100, 550)
                elif winning_result == "Standoff":
                    draw_text("Standoff! You get your bet back.", font, WHITE, screen, 100, 500)
                elif winning_result == "Dealer Wins":
                    draw_text("Dealer Wins!", font, WHITE, screen, 100, 500)
                else:
                    draw_text("Error", font, WHITE, screen, 100, 500)

                # Play Again Button
                pygame.draw.rect(screen, WHITE, play_again_button)
                draw_text("Play Again", small_font, BLACK, screen, 510, 615)

            else:
                # Hit & Stand buttons
                pygame.draw.rect(screen, WHITE, hit_button)
                draw_text("Hit", small_font, BLACK, screen, 130, 615)

                pygame.draw.rect(screen, WHITE, stand_button)
                draw_text("Stand", small_font, BLACK, screen, 330, 615)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
