import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Uno Game")

# Load background image
background_image = pygame.image.load('./files/background.jpg')

# Load card images
card_images = {}
colors = ['Red', 'Yellow', 'Green', 'Blue']
values = list(range(0, 10)) + ['Skip', 'Reverse', 'Draw']
for color in colors:
    for value in values:
        card_name = f"{color}_{value}"
        card_images[card_name] = pygame.image.load(f"./files/{card_name}.png")
pygame.image.load(f"./files/Wild_Draw.png")
pygame.image.load(f"./files/Wild.png.png")
# Define Card class
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f"{self.color} {self.value}"

    def get_image(self):
        return card_images[f"{self.color}_{self.value}"]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Fill the screen with a color (e.g., white)
    screen.fill((255, 255, 255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()