import pygame
import threading
from serverfile import Server
from client import Client
from uno_game import start_game, draw_card

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Networked UNO Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player1_pos = [WIDTH // 4, HEIGHT // 2]
player2_pos = [3 * WIDTH // 4, HEIGHT // 2]

# Clock
clock = pygame.time.Clock()

def handle_player_movement(keys, player_pos):
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5


def main():
    running = True
    is_server = input("Are you the server? (y/n): ").lower() == 'y'

    # Initialize the UNO game
    deck, discard_pile, player1_hand, player2_hand = start_game()

    if is_server:
        threading.Thread(target=Server).start()
    else:
        threading.Thread(target=Client).start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        handle_player_movement(keys, player1_pos)

        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (*player1_pos, player_size, player_size))
        pygame.draw.rect(screen, BLUE, (*player2_pos, player_size, player_size))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()