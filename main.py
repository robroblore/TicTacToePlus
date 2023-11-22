import os.path
import sys

import pygame

# Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_WIDTH = 12

# Other variables

current_player = 1
theme = 0


# Functions


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# get_path() Imported from link above, needed in order to use images for the standalone .exe
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


# Draw the grid
def DrawGrid():
    screen.fill(background)
    for x in range(1, 3):
        pygame.draw.line(screen, draw_color, (x * SCREEN_WIDTH / 3, 0), (x * SCREEN_WIDTH / 3, SCREEN_HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, draw_color, (0, x * SCREEN_HEIGHT / 3), (SCREEN_WIDTH, x * SCREEN_HEIGHT / 3),
                         LINE_WIDTH)


# Draw the players' moves (j'ai passe bcp trop de temps a faire les calcules j'en ai marre)
def DrawPlayers(board):
    x_pos = 0
    for x in board:
        y_pos = 0

        for y in x:
            if y == 1:
                pygame.draw.line(screen, draw_color, ((x_pos*2+1) * (SCREEN_WIDTH / 6), y_pos * (SCREEN_HEIGHT / 3)),
                                 ((x_pos*2+1) * (SCREEN_WIDTH / 6), (y_pos+1) * (SCREEN_HEIGHT / 3)), LINE_WIDTH)
            elif y == -1:
                pygame.draw.line(screen, draw_color, (x_pos * (SCREEN_WIDTH / 3), (y_pos*2+1) * (SCREEN_HEIGHT / 6)),
                                 ((x_pos+1) * (SCREEN_WIDTH/3), (y_pos*2+1) * (SCREEN_HEIGHT / 6)), LINE_WIDTH)
            elif y == 2:
                pygame.draw.line(screen, draw_color, ((x_pos*2+1) * (SCREEN_WIDTH / 6), y_pos * (SCREEN_HEIGHT / 3)),
                                 ((x_pos*2+1) * (SCREEN_WIDTH / 6), (y_pos + 1) * (SCREEN_HEIGHT / 3)), LINE_WIDTH)
                pygame.draw.line(screen, draw_color, (x_pos * (SCREEN_WIDTH / 3), (y_pos*2+1) * (SCREEN_HEIGHT / 6)),
                                 ((x_pos+1) * (SCREEN_WIDTH / 3), (y_pos*2+1) * (SCREEN_HEIGHT / 6)), LINE_WIDTH)
            y_pos += 1

        x_pos += 1


# Handles the mouse click (checks position, checks board and updates the board)
# TODO: Don't allow the player to play + twice
# TODO: If player can't play anything, skip turn
def HandleMouseClick(pos, board, player):
    cell_x = pos[0]
    cell_y = pos[1]
    if board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] == 0:
        board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] = player

    elif (board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] != player
          and board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] != 2):
        board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] = 2

    else:
        return 1

    print(game_board)
    return -1


def CheckWin(board, player):
    return


# Get the user's desired theme
# theme = input("Enter theme (light/dark): ").lower()
# while theme != "light" and theme != "dark" and theme != "l" and theme != "d":
#     theme = input("Theme doesn't exist, please enter light(l) or dark(d): ").lower()
#
# if theme == "light" or theme == "l":
#     theme = 1
# else:
#     theme = 0

# Set the background and draw color according to the theme
background = (255 * theme, 255 * theme, 255 * theme)
draw_color = (255 * (1 - theme), 255 * (1 - theme), 255 * (1 - theme))

# Initialize pygame
pygame.init()
# Create the screen (window)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set the title of the window
pygame.display.set_caption("TicTacToe +")
pygame.display.set_icon(pygame.image.load(get_path("icon.png")))

game_board = \
    [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

print(game_board)

# Game loop
run = True
while run:

    DrawGrid()
    DrawPlayers(game_board)
    CheckWin(game_board, current_player*-1)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_player *= HandleMouseClick(pygame.mouse.get_pos(), game_board, current_player)

    # Update game state
    pygame.display.update()

pygame.quit()
quit()
