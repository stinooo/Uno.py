import pygame

pygame.init()
def display_menu():
    running = True
    font = pygame.font.Font(None, 74)
    title = font.render("UNO Game", True, BLACK)

    # Laad de achtergrondafbeelding
    background = pygame.image.load("files/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    button_font = pygame.font.Font(None, 50)
    ready_button = button_font.render("Ready", True, WHITE)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

    while running:
        # Teken de achtergrond
        screen.blit(background, (0, 0))

        # Teken menu-onderdelen
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        pygame.draw.rect(screen, RED, button_rect)
        screen.blit(ready_button, (button_rect.x + 25, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False  # Verlaat het menu als op "Ready" wordt geklikt

        pygame.display.flip()
