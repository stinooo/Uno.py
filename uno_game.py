import random
import pygame

colors = ["red", "yellow", "green", "blue"]
values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
special_cards = ["Wild", "Wild_Draw"]

def create_deck():
    deck = []
    for color in colors:
        for value in values:
            deck.append(f"{color} {value}")
            if value != "0":  # Two of each non-zero value per color
                deck.append(f"{color} {value}")
    
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
    deck = discard_pile[:-1]  # Keep the last card as starting discard
    discard_pile = discard_pile[-1:]  # Start a new discard pile
    random.shuffle(deck)

def start_game():
    global deck, discard_pile
    deck = create_deck()
    player1_hand = [draw_card(deck) for _ in range(7)]
    player2_hand = [draw_card(deck) for _ in range(7)]
    discard_pile = [draw_card(deck)]
    return deck, discard_pile, player1_hand, player2_hand

def render_hand(screen, hand, x, y):
    card_images = {}
    for i, card in enumerate(hand):
        # Load card images only for the cards in hand
        if card not in card_images:
            card_images[card] = pygame.image.load(f"./files/{card}.png")
        screen.blit(card_images[card], (x, y + i * 30))

def can_play(card, top_card):
    card_color, card_value = card.split() if "Wild" not in card else ("Wild", card)
    top_color, top_value = top_card.split() if "Wild" not in top_card else ("Wild", top_card)
    return (
        card_color == top_color or
        card_value == top_value or
        card_color == "Wild"
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

def process_special_card(card, turn_order):
    card_type = card.split()[1] if "Wild" not in card else card
    if card_type == "Skip":
        return 2  # Skip next player
    elif card_type == "Reverse":
        turn_order.reverse()
        return 1  # Reverse changes direction but doesn't skip a turn
    elif card_type == "Draw Two":
        return "Draw Two"
    elif card_type == "Wild_Draw":
        return "Wild_Draw"

def game_loop():
    deck, discard_pile, player1_hand, player2_hand = start_game()
    turn_order = [player1_hand, player2_hand]
    current_index = 0
    while True:
        current_player = turn_order[current_index]
        top_card = discard_pile[-1]
        print(f"Top card: {top_card}")
        print(f"Player {current_index + 1}'s turn with hand: {current_player}")
        
        played_card = play_turn(current_player, top_card)
        print(f"Player {current_index + 1} played: {played_card}")
        
        # Process card effects if it's a special card
        if "draw" not in played_card:
            top_card = discard_pile[-1]
            effect = process_special_card(top_card, turn_order)
            if effect == 2:  # Skip
                current_index = (current_index + effect) % len(turn_order)
            elif effect == "Draw Two":
                next_player = turn_order[(current_index + 1) % len(turn_order)]
                next_player.extend(draw_card(deck) for _ in range(2))
                current_index = (current_index + 1) % len(turn_order)
            elif effect == "Wild Draw Four":
                next_player = turn_order[(current_index + 1) % len(turn_order)]
                next_player.extend(draw_card(deck) for _ in range(4))
                current_index = (current_index + 1) % len(turn_order)
            else:  # Reverse or normal play
                current_index = (current_index + 1) % len(turn_order)
        else:
            # Draw a card, no special effect processing
            current_index = (current_index + 1) % len(turn_order)
        
        # Check for win
        if not current_player:
            print(f"Player {current_index + 1} wins!")
            break
