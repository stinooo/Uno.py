import pygame
import random
import os
from button import Button

# Initialize Pygame
pygame.init()

# Get screen size from system
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Set up display
screen = pygame.display.set_mode((screen_width - 100, screen_height - 100), pygame.RESIZABLE)
pygame.display.set_caption("Uno Game")

# Load images
background_image = pygame.image.load('./files/background.jpg')

# Create Resizer class to handle dynamic resizing
class Resizer:
    def __init__(self, original_width, original_height):
        self.original_width = original_width
        self.original_height = original_height

    # Dynamically resize image based on current window size
    def scale_image(self, image, window_width, window_height):
        scale_x = window_width / self.original_width
        scale_y = window_height / self.original_height
        new_size = (int(image.get_width() * scale_x), int(image.get_height() * scale_y))
        return pygame.transform.scale(image, new_size)

    # Dynamically scale position based on current window size
    def scale_position(self, original_x, original_y, window_width, window_height):
        scaled_x = int((original_x / self.original_width) * window_width)
        scaled_y = int((original_y / self.original_height) * window_height)
        return scaled_x, scaled_y

# Initialize resizer with the original screen dimensions
resizer = Resizer(screen.get_width(), screen.get_height())

def get_font(size):  # Returns the default font in the desired size
    return pygame.font.Font(None, size)

# Define Card class
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

    def get_image(self):
        return card_images[f"{self.color}_{self.value}"]

# Define colors and values for the cards
colors = ['Red', 'Yellow', 'Green', 'Blue']
values = list(range(0, 10)) + ['Skip', 'Reverse', 'Draw']

# Load card images
card_images = {}
for color in colors:
    for value in values:
        card_name = f"{color}_{value}"
        card_images[card_name] = pygame.image.load(f"./files/{card_name}.png")
card_images["Wild_Draw"] = pygame.image.load(f"./files/Wild_Draw.png")
card_images["Wild"] = pygame.image.load(f"./files/Wild.png")

def play():
    global screen
    # Initialize game variables
    deck = [Card(color, value) for color in colors for value in values] * 2
    random.shuffle(deck)
    player_hand = [deck.pop() for _ in range(7)]
    computer_hand = [deck.pop() for _ in range(7)]
    discard_pile = [deck.pop()]
    current_card = discard_pile[-1]
    current_color = current_card.color
    current_value = current_card.value
    player_turn = True
    game_over = False

    # Game loop
    while not game_over:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    for i, card in enumerate(player_hand):
                        if card.get_image().get_rect(center=(100 + i * 100, screen_height - 200)).collidepoint(event.pos):
                            if card.color == current_color or card.value == current_value:
                                current_card = card
                                current_color = card.color
                                current_value = card.value
                                player_hand.pop(i)
                                discard_pile.append(card)
                                player_turn = False
                                break
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Draw everything
        screen.fill((0, 128, 0))
        screen.blit(background_image, (0, 0))
        for i, card in enumerate(player_hand):
            screen.blit(card.get_image(), (100 + i * 100, screen_height - 200))
        for i, card in enumerate(computer_hand):
            screen.blit(card_images['Blue_0'], (100 + i * 100, 100))
        screen.blit(current_card.get_image(), (screen_width // 2, screen_height // 2))
        pygame.display.flip()

def options():
    global screen
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                    return
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame.display.update()

def main_menu():
    global screen
    while True:
        screen.blit(pygame.transform.scale(background_image, screen.get_size()), (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    return
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                    return
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    return
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame.display.update()

main_menu()
