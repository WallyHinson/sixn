"""An implementation of the 6 nimmt! card game using pygame."""


import os
import random

import pygame


# Define the pygame display size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the cell width and height that cards and other game objects
# fit into on the screen
CELL_WIDTH = int(SCREEN_WIDTH / 12)
CELL_HEIGHT = int(SCREEN_HEIGHT / 7)

# Define the card size -- these dimensions allow 12 cards (with spacing)
# across the screen, and 7 cards (with spacing) down the screen at 800x600.
CARD_WIDTH = 64
CARD_HEIGHT = 80

# Define the needed colors as RGB tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
#GREY = (128, 128, 128)
GREEN = (21, 142, 15)
BLUE = (180, 200, 255)
YELLOW = (255, 242, 0)
RED = (255, 0, 0)
PURPLE = (64, 32, 64)
COLORKEY = (0, 255, 0)

# Define the maximum framerate
FRAMERATE = 30


class Card:
    """Class defining the cards used in the game.

    Public attributes:
        number: 1 to 104, inclusive
        stars: number of stars on the card, based on card number
        visible: is the card currently visible?

    Internal attributes:
        _image: visual depiction of the card
        _x: current x position of the card
        _y: current y position of the card
        _frames: number of frames to take moving a card to its destination
        _x_dest: destination x position of a moving card
        _y_dest: destination y position of a moving card
        _remove_on_arrival: should card be removed at end of its animation?

    Public methods:
        __init__(n): create card number n
        place(x, y): place the card at position x, y
        move_to(x, y, frames, remove_on_arrival=False): move card to x, y in
            the given number of frames, optionally removing it from the
            screen once it arrives
        update(): process animation (if any) and redraw the card
    """

    def __init__(self, n):
        """Create card number n."""
        self.number = n
        self.stars = Card.stars(n)
        self.visible = False
        
        self._image = Card.card_image(n)
        self._x = None
        self._y = None
        self._frames = None
        self._dx = None
        self._dy = None
        self._remove_on_arrival = None

    def place(self, x, y):
        """Place the card at position x, y.

        Note: this by itself does not cause the card to be displayed on the
        screen; it must also be added to the list of visible objects, and
        will be displayed once the game loop processes that list and calls
        update() on the card.
        """
        self._x = x
        self._y = y
        self.visible = True

    def move_to(self, x, y, frames, remove_on_arrival=False):
        """Move the card to a new position, optionally removing it afterwards.

        Sets the animation parameters for the card so that it will move
        from its current position to the given x, y position in the given
        number of frames.  If remove_on_arrival is True, the card will be
        dropped from the list of visible cards once it reaches its
        destination (for example, each card in a row being picked up by a
        player could move to the player's image and disappear.)
        """
        self._frames = frames
        self._dx = (x - self._x) / frames
        self._dy = (y - self._y) / frames
        self._remove_on_arrival = remove_on_arrival

    def update(self):
        """Process any animation updates and draw the card on the screen."""
        assert self.visible == True
        if self._frames is not None:
            # update position and decrement frame count
            self._x += self._dx
            self._y += self._dy
            self._frames -= 1
            
            if self._frames == 0:
                # card has reached its destination -- reset _frames, _dx,
                # and _dy to indicate no further animation
                self._frames = None
                self._dx = None
                self._dy = None
                
                if self._remove_on_arrival == True:
                    # setting visible to False will cause the game loop to
                    # drop the card from the list of visible objects after
                    # the current frame is displayed
                    self.visible = False
                    
        screen.blit(self._image, (int(self._x), int(self._y)))

    @staticmethod
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

    @staticmethod   
    def card_image(n):
        """Return the image for card number n."""
        # The number of stars on the card determines the base image used,
        # as well as the foreground / background colors used later.
        s = Card.stars(n)
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

        # Set pure green (0, 255, 0) to be transparent, then convert the
        # image to the most appropriate format
        image.set_colorkey(COLORKEY)
        image = image.convert()
        
        return image


class Deck:
    """Class defining the deck of cards to be used in the game.

    Public attributes:
        none

    Internal attributes:
        _deck: list of cards currently in the deck
        
    Public methods:
        __init__(): create a new ordered deck
        shuffle(): shuffle the deck
        draw(): draw and return the top card from the deck
    """

    def __init__(self):
        """Create a new, ordered deck."""
        self._deck = []
        for n in range(1, 105):
            self._deck.append(Card(n))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self._deck)

    def draw(self):
        """Draw the top card from the deck.

        Will raise an IndexError exception if called when the deck is
        empty.  Shouldn't happen, as the full deck will never be used
        in normal gameplay.
        """
        return self._deck.pop()


class Player:
    """Class defining the players in the game.

    Public attributes:
        score: the player's score
        hand: the player's hand (0 - 10 cards)
        visible: is the player visible on the screen?  (Always True)

    Internal attributes:
        _x: x position
        _y: y position
        _image: player image    

    Public methods:
        __init__(n): create player number n
        update(): draw player and score on the screen
    """

    _images = []

    def __init__(self, n):
        self.score = 0
        self.hand = []
        self.name = "Player {}".format(n)
        self.visible = True

        self._x = 9 * CELL_WIDTH
        self._y = n * CELL_HEIGHT - (CELL_HEIGHT // 2)
        if Player._images == []:
            Player.get_player_images()
        self._image = Player._images[n % 3]        

    def update(self):
        screen.blit(self._image, (self._x, self._y))

    @staticmethod
    def get_player_images():
        """Build list of player images."""
        for i in range(3):
            filename = os.path.join("images", "face_" + str(i) + ".png")
            image = pygame.image.load(filename)

            # Set pure green (0, 255, 0) to be transparent, then convert the
            # image to the most appropriate format
            image.set_colorkey(COLORKEY)
            image = image.convert()

            Player._images.append(image)


class Game:
    """Class containing the game state.

    Public attributes:
        deck: the deck of cards
        rows: the four rows where cards are placed (up to 5 each)
        players: the players in the game
        screen_objects: all visible screen objects
        click_function: function to call on mouse click,
            with signature (game, event)

        Public methods:
        __init__(n): create a game with n players
        add_screen_object(obj): add a new object to the list of screen objects
        cleanup_screen_objects(): remove any objects that are no longer visible
    """

    def __init__(self, n):
        """Create a game with n players."""
        assert 2 <= n <= 5
        self.deck = None
        self.rows = [[], [], [], []]
        self.players = []
        self.screen_objects = []
        self.click_function = None
        for i in range(n):
            player = Player(i + 1)
            self.players.append(player)
            self.screen_objects.append(player)

    def add_screen_object(self, obj):
        """Add obj to the list of screen objects."""
        self.screen_objects.append(obj)

    def cleanup_screen_objects(self):
        """Remove any screen objects that are no longer visible."""
        updated_objects = [obj for obj in self.screen_objects
                           if obj.visible == True]
        self.screen_objects = updated_objects
            
        
# Make the screen global for simplicity...may change later?
screen = None


def main():
    init()
    game_loop()


def init():
    """Initial setup before the game starts."""
    global screen

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("sixn")


def game_loop():
    """The main game loop -- almost everything happens here."""
    # Create a clock to regulate the frame rate
    clock = pygame.time.Clock()

    # Create a Game object to hold the game state
    game = Game(3)
    game.deck = Deck()
    game.deck.shuffle()
    game.click_function = spawn_card

    # Place some cards
    for y in range(1, 5):
        for x in range(1, 6):
            card = game.deck.draw()
            card.place(x * CELL_WIDTH, y * CELL_HEIGHT)
            game.add_screen_object(card)
    
    running = True
    while running:
        # Restore the background
        screen.fill(GREEN)
    
        # Draw all visible screen objects
        for obj in game.screen_objects:
            obj.update()
    
        # Show the udpated screen   
        pygame.display.update()

        # Drop any objects that are no longer visible
        game.cleanup_screen_objects()
        
        # Get and process events -- exit on QUIT; spawn a new card on a
        # MOUSEBUTTONUP or exit if the deck is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if game.click_function is not None:
                    game.click_function(game, event)

        # Run no faster than FRAMERATE frames per second
        clock.tick(FRAMERATE)

    pygame.quit()
    exit()
    

def random_xy():
    """Return a random (x, y) position on the screen."""
    x = random.randint(0, SCREEN_WIDTH - CARD_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - CARD_HEIGHT)

    return (x, y)


def spawn_card(game, event):
    """Spawn a card at the current mouse position, moving somewhere else."""
    x, y = event.pos
    card = game.deck.draw()
    card.place(x, y)
    card.move_to(*random_xy(), random.randint(5, 150),
                 random.choice([True, False]))
    game.add_screen_object(card)                 


if __name__ == "__main__":
    main()
