import pygame, sys, math
import time
from pygame.locals import *

#
VERTICAL = 0
HORIZONTAL = 1
RIGHTDOWN = 2
RIGHTUP = 3

# Game Setting
TARGET_FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
STONE_SIZE = 31
LEFT = 1
TURN = 1
gameBoard = []

BLACK = "black"
WHITE = "white"
BLANK = "*"

# Game Init
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Four Go')
fps_clock = pygame.time.Clock()
gameOver = False
winner = ""

# Load Images
bStone = pygame.image.load("black.png")
wStone = pygame.image.load("white.png")
board = pygame.image.load("board.png")

board = pygame.transform.scale(board, (600, 600))
bStone = pygame.transform.scale(bStone, (STONE_SIZE, STONE_SIZE))
wStone = pygame.transform.scale(wStone, (STONE_SIZE, STONE_SIZE))


def isFour(color, x, y):
    flag = False  # flag for panjung
    length = 0

    # =========================================================
    #
    # Check if the stones are four_same_colored
    # return True if there are four_same_colored_aligned stones
    # return False if there not.
    # implement codes here.
    #
    # =========================================================


def setGame(gameBoard):
    for i in range(19):
        oneRow = []
        for j in range(19):
            oneRow.append(BLANK)
        gameBoard.append(oneRow)


def canDraw(x, y):
    if gameBoard[y][x] == BLANK:
        return True
    else:
        return False


def drawStone(color, x, y):
    global gameBoard
    global TURN

    print(str(x) + ", " + str(y))

    px = 20 + STONE_SIZE * x
    py = 20 + STONE_SIZE * y

    px -= STONE_SIZE / 2
    py -= STONE_SIZE / 2

    if canDraw(x, y):
        if color == 'black':
            screen.blit(bStone, (px, py))
            gameBoard[y][x] = BLACK
        else:
            screen.blit(wStone, (px, py))
            gameBoard[y][x] = BLACK
        TURN = TURN+1


def roundingOff(n):
    float_n = n - int(n)

    if float_n >= 0.5:
        n = int(n) + 1
    else:
        n = int(n)

    return n


def pixelToCord(x, y):
    x = (x - 20) / STONE_SIZE
    y = (y - 20) / STONE_SIZE

    x = roundingOff(x)
    y = roundingOff(y)

    return (x, y)


# Draw Board

screen.blit(board, (0, 0))

setGame(gameBoard)
# Main Loop
while True:
    for event in pygame.event.get():
        if not gameOver:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    x, y = pixelToCord(event.pos[0], event.pos[1])
                    if TURN % 2 == 1:
                        drawStone("black", x, y)
                        if isFour(BLACK, x, y):
                            gameOver = True
                            winner = BLACK
                    else:
                        drawStone("white", x, y)
                        if isFour(WHITE, x, y):
                            gameOver = True
                            winner = WHITE
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

    fps_clock.tick(TARGET_FPS)
