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
    card_width = 200
    card_height = 300
    for i, card in enumerate(hand):
        # Load and scale card images only for the cards in hand
        if card not in card_images:
            card_image = pygame.image.load(f"./files/{card}.png")
            card_images[card] = pygame.transform.scale(card_image, (card_width, card_height))
        card_x = x + i * (card_width + 10) + scroll_offset
        card_y = y
        if card_x <= mouse_x <= card_x + card_width and card_y <= mouse_y <= card_y + card_height:
            card_y -= 10  # Move the card up when hovered
        screen.blit(card_images[card], (card_x, card_y))

def can_play(card, top_card):
    if "Wild" in card:
        return True
    card_color, card_value = card.split('_')
    top_color, top_value = top_card.split('_')
    return (
        card_color == top_color or
        card_value == top_value or
        "Wild" in card
    )

def play_turn(player_hand, top_card):
    playable_cards = [card for card in player_hand if can_play(card, top_card)]
    if playable_cards:
        chosen_card = playable_cards[0]  # For simplicity, play the first playable card
        player_hand.remove(chosen_card)
        discard_pile.append(chosen_card)
        return chosen_card
    else:
        # No playable cards, draw a card
        new_card = draw_card(deck)
        player_hand.append(new_card)
        return f"draw {new_card}"

def process_special_card(card, turn_order, player_hands, current_player_index):
    card_type = card.split('_')[1] if "Wild" not in card else card
    if card_type == "Skip":
        return (current_player_index + 2) % len(player_hands)  # Skip next player
    elif card_type == "Reverse":
        turn_order.reverse()
        return (current_player_index + 1) % len(player_hands)  # Reverse changes direction but doesn't skip a turn
    elif card_type == "Draw":
        next_player_index = (current_player_index + 1) % len(player_hands)
        player_hands[next_player_index].extend([draw_card(deck) for _ in range(2)])
        return (current_player_index + 1) % len(player_hands)
    elif card_type == "Wild_Draw":
        next_player_index = (current_player_index + 1) % len(player_hands)
        player_hands[next_player_index].extend([draw_card(deck) for _ in range(4)])
        return (current_player_index + 1) % len(player_hands)
    else:
        return (current_player_index + 1) % len(player_hands)