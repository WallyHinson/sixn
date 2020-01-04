"""An implementation of the 6 nimmt! card game using pygame."""


import os, pygame, random


# Define the pygame display size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the card size -- these dimensions allow 12 cards (with spacing)
# across the screen, and 7 cards (with spacing) down the screen.
CARD_WIDTH = 64
CARD_HEIGHT = 80

# Define the needed colors as RGB tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (21, 142, 15)
BLUE = (180, 200, 255)
YELLOW = (255, 242, 0)
RED = (255, 0, 0)
PURPLE = (64, 32, 64)

# Define the maximum framerate
FRAMERATE = 30

# Define constants for the different elements of a card
CARD_NUMBER = 0
CARD_STARS = 1
CARD_IMAGE = 2
CARD_X = 3
CARD_Y = 4
CARD_MOVING = 5
CARD_DX = 6
CARD_DY = 7


# The deck will be a list of [number, stars, image, x, y, moving, dx, dy]
# lists
deck = []


def main():
    init()
    game_loop()


def init():
    """Initial setup before the game starts."""
    global deck

    pygame.init()

    # For now, create each card near the middle of the screen, with random
    # motion
    for i in range(1, 105):
        deck.append([i, stars(i), card_image(i),
                     random.randrange(SCREEN_WIDTH // 3, SCREEN_WIDTH // 3 * 2),
                     random.randrange(SCREEN_HEIGHT // 3, SCREEN_HEIGHT //3 * 2),
                     True,
                     random.randrange(-5, 6),
                     random.randrange(-5, 6)])


def stars(n):
    """Return the number of stars associated with card number n."""
    if n == 55:
        return 7
    elif n % 11 == 0:
        return 5
    elif n % 10 == 0:
        return 3
    elif n % 5 == 0:
        return 2
    else:
        return 1

    
def card_image(n):
    """Return the image for card number n."""
    # The number of stars on the card determines the base image used,
    # as well as the foreground / background colors used later.
    s = stars(n)
    filename = os.path.join("images", "card_" + str(s) + ".png")
    image = pygame.image.load(filename)

    # Set foreground and background colors based on card type (# of stars)
    if s == 7:
        fg, bg = RED, PURPLE
    elif s == 5:
        fg, bg = YELLOW, RED
    elif s == 3:
        fg, bg = BLACK, YELLOW
    elif s == 2:
        fg, bg = BLACK, BLUE
    else:
        fg, bg = BLACK, WHITE
        
    # Render the card number using the selected colors
    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 24)
    text = font.render(str(n), True, fg, bg)

    # Add the card number to the base card image
    x = (CARD_WIDTH - text.get_width()) / 2
    y = 31
    image.blit(text, (x, y))
    
    return image


def game_loop():
    """The main game loop -- almost everything happens here."""
    # Create and set up the display surface
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("sixn")

    # Create a clock to regulate the frame rate
    clock = pygame.time.Clock()

    cards = []
    
    running = True
    while running:
        # Restore the background before drawing any cards
        screen.fill(GREEN)
    
        for card in cards:
            if card[CARD_MOVING] == True:
                # Update the card's position
                card[CARD_X] += card[CARD_DX]
                card[CARD_Y] += card[CARD_DY]

                # Stop its motion if it's hit any screen edge
                if card[CARD_X] < 0:
                    card[CARD_X] = 0
                    card[CARD_MOVING] = False
                elif card[CARD_X] > SCREEN_WIDTH - CARD_WIDTH:
                    card[CARD_X] = SCREEN_WIDTH - CARD_WIDTH
                    card[CARD_MOVING] = False
                if card[CARD_Y] < 0:
                    card[CARD_Y] = 0
                    card[CARD_MOVING] = False
                elif card[CARD_Y] > SCREEN_HEIGHT - CARD_HEIGHT:
                    card[CARD_Y] = SCREEN_HEIGHT - CARD_HEIGHT
                    card[CARD_MOVING] = False

                # Clear the moving flag if dx and dy are both zero
                if card[CARD_DX] == 0 and card[CARD_DY] == 0:
                    card[CARD_MOVING] = False

            # Blit card to screen in its new location
            screen.blit(card[CARD_IMAGE], (card[CARD_X], card[CARD_Y]))

        # Show the udpated screen   
        pygame.display.update()
        
        # Get and process events -- exit on QUIT; spawn a new card on a
        # MOUSEBUTTONUP or exit if the deck is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if len(deck):
                    cards.append(deck.pop())
                else:
                    running = False

        # Run no faster than FRAMERATE frames per second
        clock.tick(FRAMERATE)

    pygame.quit()
    exit()
    

if __name__ == "__main__":
    main()
