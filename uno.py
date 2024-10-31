import pygame, sys
import random
from button import Button

# Initialize Pygame
pygame.init()

# Get screen size from system
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Set up display
screen = pygame.display.set_mode((screen_width-100, screen_height-100), pygame.RESIZABLE)
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

# Load button images
play_button_image = pygame.image.load("./files/Table_0.png")
options_button_image = pygame.image.load("./files/Table_1.png")
quit_button_image = pygame.image.load("./files/Table_2.png")

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("./files/font.ttf", size)

def play():
    return

def options():
    return

def main_menu():
    global screen
    while True:
        screen_width, screen_height = screen.get_size()

        # Dynamically resize background
        resized_background = pygame.transform.scale(background_image, (screen_width, screen_height))

        # Dynamically resize buttons using Resizer
        resized_play_button = resizer.scale_image(play_button_image, screen_width, screen_height)
        resized_options_button = resizer.scale_image(options_button_image, screen_width, screen_height)
        resized_quit_button = resizer.scale_image(quit_button_image, screen_width, screen_height)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, screen_height // 6))

        # Dynamically position buttons using Resizer
        PLAY_BUTTON = Button(image=resized_play_button,
                             pos=resizer.scale_position(640, 250, screen_width, screen_height),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        OPTIONS_BUTTON = Button(image=resized_options_button,
                                pos=resizer.scale_position(640, 400, screen_width, screen_height),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=resized_quit_button,
                             pos=resizer.scale_position(640, 550, screen_width, screen_height),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Draw background and buttons
        screen.blit(resized_background, (0, 0))
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Update the display
        pygame.display.flip()

# Start the main menu
main_menu()
