import pygame
import sys
from uno_game import is_reverse_or_skip_card, start_game, render_hand, draw_card, can_play

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Networked UNO Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Button dimensions
button_width = 200
button_height = 50

# Input box dimensions
input_box_width = 200
input_box_height = 50

# Card dimensions
card_width = 200
card_height = 300

def draw_button(screen, color, x, y, width, height, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def draw_input_box(screen, color, x, y, width, height, text):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + 10, y + 10))

def draw_label(screen, text, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def draw_color_indicator(screen, color, x, y, size=50):
    color_map = {
        "red": RED,
        "blue": BLUE,
        "green": GREEN,
        "yellow": YELLOW
    }
    if color not in color_map:
        # Handle invalid or unspecified colors (like 'Wild')
        pygame.draw.rect(screen, WHITE, (x, y, size, size))  # Default to white background
        pygame.draw.rect(screen, BLACK, (x, y, size, size), 2)  # Border
    else:
        pygame.draw.rect(screen, color_map[color], (x, y, size, size))
        pygame.draw.rect(screen, BLACK, (x, y, size, size), 2)  # Border

def choose_color():
    choosing_color = True
    chosen_color = None
    while choosing_color:
        screen.fill(WHITE)
        draw_button(screen, RED, WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height, "Red")
        draw_button(screen, YELLOW, WIDTH // 2 - button_width // 2, HEIGHT // 2 - 40, button_width, button_height, "Yellow")
        draw_button(screen, GREEN, WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height, "Green")
        draw_button(screen, BLUE, WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height, "Blue")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2:
                    if HEIGHT // 2 - 100 <= mouse_y <= HEIGHT // 2 - 100 + button_height:
                        chosen_color = "red"
                        choosing_color = False
                    elif HEIGHT // 2 - 40 <= mouse_y <= HEIGHT // 2 - 40 + button_height:
                        chosen_color = "yellow"
                        choosing_color = False
                    elif HEIGHT // 2 + 20 <= mouse_y <= HEIGHT // 2 + 20 + button_height:
                        chosen_color = "green"
                        choosing_color = False
                    elif HEIGHT // 2 + 80 <= mouse_y <= HEIGHT // 2 + 80 + button_height:
                        chosen_color = "blue"
                        choosing_color = False

        pygame.display.flip()
        clock.tick(30)

    return chosen_color

def show_win_screen(screen, winner_name):
    running = True
    while running:
        screen.fill(WHITE)
        
        # Draw winner text
        font = pygame.font.Font(None, 74)
        text = font.render(f"{winner_name} Wins!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        
        # Draw exit button
        draw_button(screen, RED, WIDTH // 2 - button_width // 2, 
                   HEIGHT // 2 + 50, button_width, button_height, "Exit")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if exit button clicked
                if (WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2 and
                    HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 50 + button_height):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(30)

def main():
    running = True
    player1_name = ""
    player2_name = ""
    active_input = None

    while running:
        screen.fill(WHITE)
        
        # Draw labels
        draw_label(screen, "Player 1 Name:", WIDTH // 2 - input_box_width // 2 - 200, HEIGHT // 2 - 100)
        draw_label(screen, "Player 2 Name:", WIDTH // 2 - input_box_width // 2 - 200, HEIGHT // 2)

        # Draw input boxes and buttons
        draw_input_box(screen, BLACK, WIDTH // 2 - input_box_width // 2, HEIGHT // 2 - 100, input_box_width, input_box_height, player1_name)
        draw_input_box(screen, BLACK, WIDTH // 2 - input_box_width // 2, HEIGHT // 2, input_box_width, input_box_height, player2_name)
        draw_button(screen, GREEN, WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height, "Start Game")
        draw_button(screen, RED, WIDTH // 2 - button_width // 2, HEIGHT // 2 + 160, button_width, button_height, "Exit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2:
                    if HEIGHT // 2 + 100 <= mouse_y <= HEIGHT // 2 + 100 + button_height:
                        if player1_name and player2_name:
                            running = False
                    elif HEIGHT // 2 + 160 <= mouse_y <= HEIGHT // 2 + 160 + button_height:
                        pygame.quit()
                        sys.exit()
                if WIDTH // 2 - input_box_width // 2 <= mouse_x <= WIDTH // 2 + input_box_width // 2:
                    if HEIGHT // 2 - 100 <= mouse_y <= HEIGHT // 2 - 100 + input_box_height:
                        active_input = "player1"
                    elif HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + input_box_height:
                        active_input = "player2"

            elif event.type == pygame.KEYDOWN:
                if active_input == "player1":
                    if event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                elif active_input == "player2":
                    if event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode

        pygame.display.flip()
        clock.tick(30)

    # Start game
    deck, discard_pile, player1_hand, player2_hand = start_game()
    turn_order = [player1_hand, player2_hand]
    current_index = 0
    running = True
    show_player1_hand = True
    played_card = None
    card_played_this_turn = False

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_player1_hand:
                    hand = player1_hand
                else:
                    hand = player2_hand

                if not card_played_this_turn:
                    for i, card in enumerate(hand):
                        card_x = WIDTH // 2 - (len(hand) * (card_width + 10)) // 2 + i * (card_width + 10)
                        card_y = HEIGHT - card_height - 20 if show_player1_hand else 20
                        if card_x <= mouse_x <= card_x + card_width and card_y <= mouse_y <= card_y + card_height:
                            if can_play(card, discard_pile[-1]):
                                played_card = card
                                hand.remove(played_card)
                                discard_pile.append(played_card)
                                ## to see card play in console
                                print(f"Player {current_index + 1} played: {played_card}")
                                card_played_this_turn = True
                                if "Wild_Draw" in played_card:
                                    chosen_color = choose_color()
                                    discard_pile[-1] = f"{chosen_color}_Wild_Draw"
                                    # Add 4 cards to other player's hand
                                    next_player_hand = player2_hand if show_player1_hand else player1_hand
                                    for _ in range(4):
                                        new_card = draw_card(deck)
                                        next_player_hand.append(new_card)
                                    # Skip their turn by playing another turn
                                    card_played_this_turn = True
                                    show_player1_hand = not show_player1_hand
                                    current_index = (current_index + 1) % len(turn_order)
                                    played_card = None
                                elif "Wild" in played_card:
                                    chosen_color = choose_color()
                                    discard_pile[-1] = f"{chosen_color}_Wild"
                                    card_played_this_turn = True
                                elif "red_Draw" in played_card: 
                                    next_player_hand = player2_hand if show_player1_hand else player1_hand
                                    for _ in range(2):
                                        new_card = draw_card(deck)
                                        next_player_hand.append(new_card)
                                    # Sla de beurt over
                                    show_player1_hand = not show_player1_hand
                                    current_index = (current_index + 1) % len(turn_order)
                                    played_card = None
                                elif "blue_Draw" in played_card: 
                                    next_player_hand = player2_hand if show_player1_hand else player1_hand
                                    for _ in range(2):
                                        new_card = draw_card(deck)
                                        next_player_hand.append(new_card)
                                    # Sla de beurt over
                                    show_player1_hand = not show_player1_hand
                                    current_index = (current_index + 1) % len(turn_order)
                                    played_card = None
                                elif "yellow_Draw" in played_card: 
                                    next_player_hand = player2_hand if show_player1_hand else player1_hand
                                    for _ in range(2):
                                        new_card = draw_card(deck)
                                        next_player_hand.append(new_card)
                                    # Sla de beurt over
                                    show_player1_hand = not show_player1_hand
                                    current_index = (current_index + 1) % len(turn_order)
                                    played_card = None
                                elif "green_Draw" in played_card: 
                                    next_player_hand = player2_hand if show_player1_hand else player1_hand
                                    for _ in range(2):
                                        new_card = draw_card(deck)
                                        next_player_hand.append(new_card)
                                    # Sla de beurt over
                                    show_player1_hand = not show_player1_hand
                                    current_index = (current_index + 1) % len(turn_order)
                                    played_card = None

                                if is_reverse_or_skip_card(played_card):
                                    card_played_this_turn = False
                                if len(hand) == 0:  # Check if player has won
                                    winner = player1_name if show_player1_hand else player2_name
                                    show_win_screen(screen, winner)
                                break

                # Check if the "Take Card" button is clicked
                if 50 <= mouse_x <= 50 + button_width and HEIGHT // 2 - button_height // 2 <= mouse_y <= HEIGHT // 2 + button_height // 2:
                    if not card_played_this_turn:  # Only allow drawing if no card was played
                        new_card = draw_card(deck)
                        hand.append(new_card)
                        # Automatically end turn after drawing
                        show_player1_hand = not show_player1_hand
                        current_index = (current_index + 1) % len(turn_order)
                        played_card = None
                        card_played_this_turn = False

                # Check if the "Next Turn" button is clicked
                if 50 <= mouse_x <= 50 + button_width and HEIGHT // 2 - button_height // 2 - 60 <= mouse_y <= HEIGHT // 2 - button_height // 2 - 60 + button_height:
                    # Als er geen kaart gespeeld is, trek automatisch een kaart
                    if not card_played_this_turn:
                        new_card = draw_card(deck)
                        hand = player1_hand if show_player1_hand else player2_hand
                        hand.append(new_card)
                        print(f"Player {current_index + 1} drew a card: {new_card}")
                    # Automatically end turn after drawing
                    show_player1_hand = not show_player1_hand
                    current_index = (current_index + 1) % len(turn_order)
                    played_card = None
                    card_played_this_turn = False

        screen.fill(WHITE)

        # Render hands
        if show_player1_hand:
            render_hand(screen, player1_hand, WIDTH // 2 - (len(player1_hand) * (card_width + 10)) // 2, HEIGHT - card_height - 20, mouse_x, mouse_y)
        else:
            render_hand(screen, player2_hand, WIDTH // 2 - (len(player2_hand) * (card_width + 10)) // 2, 20, mouse_x, mouse_y)

        # Render top card of discard pile
        top_card = discard_pile[-1]
        if "Wild" in top_card:
            top_card_image = pygame.image.load("./files/Wild.png")
        else:
            top_card_image = pygame.image.load(f"./files/{top_card}.png")
        top_card_image = pygame.transform.scale(top_card_image, (card_width, card_height))
        screen.blit(top_card_image, (WIDTH // 2 - card_width // 2, HEIGHT // 2 - card_height // 2))

        # Add color indicator for wild cards
        if "Wild" in top_card:
            color = top_card.split("_")[0]  # Get color from the card name
            if color not in ["red", "blue", "green", "yellow"]:
                color = "white"  # Default for unspecified colors
            draw_color_indicator(screen, color, WIDTH // 2 + card_width // 2 + 20, HEIGHT // 2 - 25)

        # Draw "Take Card" button
        draw_button(screen, BLUE, 50, HEIGHT // 2 - button_height // 2, button_width, button_height, "Take Card")

        # Draw "Next Turn" button
        draw_button(screen, GREEN, 50, HEIGHT // 2 - button_height // 2 - 60, button_width, button_height, "Next Turn")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()