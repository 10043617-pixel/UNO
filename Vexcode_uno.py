# ---------------------------------------------------------------------------- #
#                                                                              #
#   Project:       VEX EXP UNO Game Setup                                      #
#   Module:        main.py                                                     #
#   Author:        VEXcode EXP                                                 #
#   Created:       2026                                                        #
#   Description:   Complete UNO Deck setup and starting hand display           #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import urandom

brain = Brain()

# --- Custom Random Generator ---
def shuffle_list(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = urandom.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

# --- UNO Deck Definition ---
COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']
WILD_CARDS = ['Wild', 'Wild +4']

def create_deck():
    deck = []
    
    # Add colored cards (25 cards per color: Red, Yellow, Green, Blue)
    for color in COLORS:
        deck.append("%s 0" % color)
        for val in VALUES[1:]:
            deck.append("%s %s" % (color, val))
            deck.append("%s %s" % (color, val))
            
    # Add wild cards (4 Wild, 4 Wild +4)
    for wild in WILD_CARDS:
        for _ in range(4):
            deck.append(wild)
            
    return deck

# --- Drawing Functions ---
def draw_card(deck):
    """Draws 1 card from the top of the deck."""
    if len(deck) > 0:
        return deck.pop(0)
    return None

def start_game(deck, hand_size=7):
    """Draws starting hand of 7 cards."""
    hand = []
    for _ in range(hand_size):
        card = draw_card(deck)
        if card:
            hand.append(card)
    return hand

# --- Screen Display Helper (Strict 5 Rows x 16 Columns) ---
def shorten_card_name(card_str):
    """Abbreviates card names to fit side-by-side in 16 total screen columns."""
    res = card_str.replace("Yellow", "Yel")
    res = res.replace("Green", "Grn")
    res = res.replace("Blue", "Blu")
    res = res.replace("Reverse", "Rev")
    return res

def display_hand_on_screen(hand):
    brain.screen.clear_screen()
    
    # Row 1: Header (16 chars max)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("HAND (%d CARDS)" % len(hand))
    
    # Rows 2 to 5: Display 2 cards per line (Left col: 1-4, Right col: 5-7)
    for i in range(4):
        row = i + 2
        brain.screen.set_cursor(row, 1)
        
        # Left column card (Cards 1 to 4)
        card_left = shorten_card_name(hand[i]) if i < len(hand) else ""
        c1_str = "%d:%s" % (i + 1, card_left)
        c1_str = c1_str[:7]
        
        # Right column card (Cards 5 to 7)
        c2_str = ""
        if (i + 4) < len(hand):
            card_right = shorten_card_name(hand[i + 4])
            c2_str = "%d:%s" % (i + 5, card_right)
            c2_str = c2_str[:8]
            
        # Format line under 16 total character columns
        line_output = "%-8s %-7s" % (c1_str, c2_str)
        brain.screen.print(line_output[:16])

def main():
    # 1. Create and shuffle full 108-card deck
    uno_deck = create_deck()
    shuffle_list(uno_deck)

    # 2. Draw 7-card starting hand
    player_hand = start_game(uno_deck, 7)

    # 3. Print hand to Console / Terminal output
    print("=== STARTING HAND (7 Cards) ===")
    count = 1
    for card in player_hand:
        print("Card %d: %s" % (count, card))
        count += 1
        
    print("")
    print("Remaining cards in deck: %d" % len(uno_deck))

    # 4. Render hand onto 5x16 VEX EXP LCD Screen
    display_hand_on_screen(player_hand)

# Run program
main()
