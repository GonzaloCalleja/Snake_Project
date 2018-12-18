
# All settings to control several game posibilities
# game options
TITLE = "Snake!"
WIDTH = 700
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'
SPRITESHEET = "grass_background.jpg"

# Snake properties
SNAKE_PIXEL_SIZE = 10
SNAKE_SPEED = 5

AI_on = False
if not AI_on:
    WIDTH = 600
    HEIGHT = 600
    SNAKE_PIXEL_SIZE = 30
    SNAKE_SPEED = 3

SNAKE_HEIGHT = SNAKE_PIXEL_SIZE
SNAKE_WIDTH = SNAKE_PIXEL_SIZE
ROWS = HEIGHT // SNAKE_HEIGHT
COLUMNS = WIDTH // SNAKE_WIDTH
INITIAL_POS = ((COLUMNS//2)*SNAKE_WIDTH,(ROWS//2)*SNAKE_HEIGHT)


# If the speed divided by half the length is not 0,
# when going through an edge the speed will not place the snake in a
# correct position by itself

if SNAKE_SPEED == SNAKE_PIXEL_SIZE:
    W_ADJUST = SNAKE_WIDTH //2
    H_ADJUST = SNAKE_HEIGHT //2
else:
    W_ADJUST = (SNAKE_WIDTH /2)%SNAKE_SPEED
    H_ADJUST = (SNAKE_HEIGHT /2)%SNAKE_SPEED

DIE_ON_EDGE = False
# LOOK = ["Joined", "Separated"]
#    0 - Joined  1 - Separated by one pixel
SEP_CHOICE = 0

# apple
APPLE_VALUE = 2
APPLE_HEIGHT = SNAKE_PIXEL_SIZE
APPLE_WIDTH = SNAKE_PIXEL_SIZE

# rock
ROCK_HEIGHT = SNAKE_PIXEL_SIZE
ROCK_WIDTH = SNAKE_PIXEL_SIZE

# block
BLOCK_HEIGHT = SNAKE_PIXEL_SIZE
BLOCK_WIDTH = SNAKE_PIXEL_SIZE

# gate
GATE_HEIGHT = SNAKE_PIXEL_SIZE
GATE_WIDTH = SNAKE_PIXEL_SIZE

ROCK_POSITIONS = [(0,0),(1,0),(2,0),(1,1),(0,1),(0,2),
                  (19, 19), (18, 19), (17, 19), (18, 18), (19, 18), (19, 17),
                  (19, 0), (18, 0), (17, 0), (18, 1), (19, 1), (19, 2),
                  (0, 19), (1, 19), (2, 19), (1, 18), (0, 18), (0, 17),
                  (5,5),(15,15),(5,15),(15,5)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
PURPLE = (75,0,130)
DARK_GREEN = (0,100,0)
BORDER_RED = (61, 26, 26)
BROWN = (139,69,19)
GREY = (192,192,192)
