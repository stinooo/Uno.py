import random
import pygame

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
    return deck, discard_pile, player1_hand, player2_hand

def render_hand(screen, hand, x, y, mouse_x, mouse_y, scroll_offset):
    card_images = {}
    base_card_width = 200  # Original width
    base_card_height = 300  # Original height
    
    # Calculate dynamic card size based on hand size
    if len(hand) > 7:
        scale_factor = 7 / len(hand)  # Reduce size proportionally
        card_width = int(base_card_width * scale_factor)
        card_height = int(base_card_height * scale_factor)
        
    else:
        card_width = base_card_width
        card_height = base_card_height

    for i, card in enumerate(hand):
        # Load and scale card images only for the cards in hand
        if card not in card_images:
            card_image = pygame.image.load(f"./files/{card}.png")
            card_images[card] = pygame.transform.scale(card_image, (card_width, card_height))
        if len(hand) > 7:
            x += (base_card_width - card_width) / 2 
        card_x = 20 + x + i * (card_width + 5)  # Reduced spacing between cards
        card_y = y
        if card_x <= mouse_x <= card_x + card_width and card_y <= mouse_y <= card_y + card_height:
            card_y -= 10  # Move the card up when hovered
        
        screen.blit(card_images[card], (card_x, card_y))

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

def is_reverse_card(card):
    if card is None:
        return False
    if "skip" in card:
        return True
    if "Reverse"in card:
        return True