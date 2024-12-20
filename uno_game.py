import random
import pygame

WIDTH, HEIGHT = 1600, 900

colors = ["red", "yellow", "green", "blue"]
values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw"]
special_cards = ["Wild", "Wild_Draw"]

special_special = {"Wild", "Draw", "Wild_Draw", "Skip", "Reverse"}


def create_deck():
    deck = []
    for color in colors:
        for value in values:
            deck.append(f"{color}_{value}")
            if value != "0":  # Two of each non-zero value per color
                deck.append(f"{color}_{value}")
    
    # Adding special cards (Wild and Wild Draw Four)
    deck.extend(special_cards * 4)
    
    random.shuffle(deck)
    return deck

def draw_card(deck):
    if not deck:  # If deck is empty, reshuffle discard pile into deck
        reshuffle_deck()
    return deck.pop()

def reshuffle_deck():
    global deck, discard_pile
    last_card = discard_pile[-1]  # Keep the last card as starting discard
    deck = discard_pile[:-1]  # All cards except the last one go back to the deck
    discard_pile = [last_card]  # Start a new discard pile with the last card

    while any(card in last_card for card in special_special):
        random.shuffle(deck)
    
    random.shuffle(deck)


def start_game():
    global deck, discard_pile
    deck = create_deck()
    player1_hand = [draw_card(deck) for _ in range(7)]
    player2_hand = [draw_card(deck) for _ in range(7)]
    discard_pile = [draw_card(deck)]
    while discard_pile[0] in special_cards:
        reshuffle_deck()
    return deck, discard_pile, player1_hand, player2_hand

def render_hand(screen, hand, x, y, mouse_x, mouse_y):
    card_images = {}
    base_card_width = 150  # Original width
    base_card_height = 250  # Original height
    spacing = 5  # space between cards
    max_cards_per_row = 10  # Maximum number of cards per row

    # Calculate dynamic card size based on hand size
    card_width = base_card_width
    card_height = base_card_height

    total_width = min(len(hand), max_cards_per_row) * card_width + (min(len(hand), max_cards_per_row) - 1) * spacing
    start_x = (WIDTH - total_width) // 2

    hitboxes = []  # List to store hitboxes

    for i, card in enumerate(hand):
        # Calculate row and column
        row = i // max_cards_per_row
        col = i % max_cards_per_row

        # Load and scale card images only for the cards in hand
        if card not in card_images:
            card_image = pygame.image.load(f"./files/{card}.png")
            card_images[card] = pygame.transform.scale(card_image, (card_width, card_height))
        
        card_x = start_x + col * (card_width + spacing)
        if row == 0:
            card_y = y + 90  # First row stays at the original y position
        else:
            card_y = y + 90 - (card_height // 2)  # Second row is slightly behind the first row

        # Adjust hitbox to account for overlapping cards
        hitbox_width = card_width if col == len(hand) - 1 else card_width + spacing

        # Add hitbox to the list
        hitboxes.append((card_x, card_y, hitbox_width, card_height))

    # Check hitboxes in reverse order to prioritize topmost cards
    for i in reversed(range(len(hand))):
        card_x, card_y, hitbox_width, card_height = hitboxes[i]
        if card_x <= mouse_x <= card_x + hitbox_width and card_y <= mouse_y <= card_y + card_height:
            card_y -= 10  # Move the card up when hovered

        # Draw the card
        screen.blit(card_images[hand[i]], (card_x, card_y))

    return hitboxes  # Return the list of hitboxes


def can_play(card, top_card):
    # Handle None cases
    if card is None or top_card is None:
        return False
        
    # Wild cards can always be played
    if "Wild" in card:
        return True
        
    # Same cards can always be played
    if card == top_card:
        return True
    
    try:
        # For Wild cards with color, check only the color
        if "Wild" in top_card:
            top_color = top_card.split('_')[0]
            card_color = card.split('_')[0]
            return top_color == card_color
            
        # Split both cards into color and value
        top_color, *top_rest = top_card.split('_')
        card_color, *card_rest = card.split('_')
        
        # For Skip, Draw, and Reverse cards, treat the rest as the value
        top_value = '_'.join(top_rest)
        card_value = '_'.join(card_rest)
        
        # Match either color or value
        return (card_color == top_color or 
                card_value == top_value)
    except:
        return False

def is_reverse_or_skip_card(card):
    if card is None:
        return False
    if "Skip" in card:
        return True
    if "Reverse"in card:
        return True