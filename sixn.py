"""An implementation of the 6 nimmt! card game using pygame."""


import os, pygame, random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CARD_WIDTH = 64
CARD_HEIGHT = 80

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (21, 142, 15)
BLUE = (180, 200, 255)
YELLOW = (255, 242, 0)
RED = (255, 0, 0)
PURPLE = (64, 32, 64)


# The deck will be a list of (number, stars, image) tuples
cards = []


def main():
    init()
    game_loop()


def init():
    """Initial setup before the game starts."""
    global cards

    pygame.init()

    for i in range(1, 105):
        cards.append((i, stars(i), card_image(i)))  


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
    s = stars(n)
    filename = os.path.join("images", "card_" + str(s) + ".png")
    image = pygame.image.load(filename)
    
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
        
    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, 24)
    text = font.render(str(n), True, fg, bg)

    x = (CARD_WIDTH - text.get_width()) / 2
    y = 31
    image.blit(text, (x, y))
    
    return image


def game_loop():
    """The main game loop -- almost everything happens here."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    card = cards.pop()
    
    running = True
    while running:
        screen.fill(GREEN)
        screen.blit(card[2], (64, 64))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if len(cards):
                    card = cards.pop()
                else:
                    running = False

    pygame.quit()
    exit()
    

if __name__ == "__main__":
    main()
