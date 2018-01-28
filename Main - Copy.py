import time
import math
import pygame
import sys
from Ai import *
from pygame.locals import *

#
VERTICAL = 0
HORIZONTAL = 1
RIGHTDOWN = 2
RIGHTUP = 3

# Game Setting
TARGET_FPS = 60
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
STONE_SIZE = 19
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
board = pygame.image.load("board2.png")

board = pygame.transform.scale(board, (500, 500))
bStone = pygame.transform.scale(bStone, (STONE_SIZE, STONE_SIZE))
wStone = pygame.transform.scale(wStone, (STONE_SIZE, STONE_SIZE))


def isFour(color, x, y):
    if ai.checkOneLine(color, x, y, RIGHTUP, 4, gameBoard):
        return True
    elif ai.checkOneLine(color, x, y, RIGHTDOWN, 4, gameBoard):
        return True
    elif ai.checkOneLine(color, x, y, HORIZONTAL, 4, gameBoard):
        return True
    elif ai.checkOneLine(color, x, y, VERTICAL, 4, gameBoard):
        return True
    else:
        return False

def setGame(gameBoard):
    for i in range(5):
        oneRow = []
        for j in range(5):
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
        elif color == 'white':
            screen.blit(wStone, (px, py))
            gameBoard[y][x] = WHITE
        TURN += 1


def roundingOff(n):
    float_n = n - int(n)

    if float_n >= 0.5:
        n = int(n) + 1
    else:
        n = int(n)

    return n


def pixelToCord(x, y):
    x = x / STONE_SIZE
    y = y / STONE_SIZE

    x = roundingOff(x)
    y = roundingOff(y)

    return (x, y)


# Draw Board

screen.blit(board, (0, 0))

setGame(gameBoard)
ai = Ai(gameBoard)
oldX = 0
oldY = 0
# Main Loop
while True:
    for event in pygame.event.get():
        if not gameOver and event.type == MOUSEBUTTONDOWN and event.button == LEFT:
            x, y = pixelToCord(event.pos[0], event.pos[1])
            if TURN % 2 == 1:
                oldX = x
                oldY = y
                drawStone("black", x, y)
                ai.update(gameBoard)
                if isFour(BLACK, x, y):
                    gameOver = True
                    winner = BLACK
                print(gameBoard)
            else:
                aiPosition = []
                aiPosition = ai.calculateTree(x, y)
                drawStone("white", aiPosition[0], aiPosition[1])
                ai.update(gameBoard)
                if isFour(WHITE, x, y):
                    gameOver = True
                    winner = WHITE
                print(gameBoard)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
        if gameOver:
            print("gg")

    fps_clock.tick(TARGET_FPS)
