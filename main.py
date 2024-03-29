import pygame


# Constant variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_WIDTH = 12


# Other variables
current_player = 1
theme = 0
played_plus_last_round = [False, False, False]


# Functions
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
                pygame.draw.line(screen, draw_color,
                                 ((x_pos * 2 + 1) * (SCREEN_WIDTH / 6), (y_pos * (SCREEN_HEIGHT / 3)) + SCREEN_HEIGHT / 18),
                                 ((x_pos * 2 + 1) * (SCREEN_WIDTH / 6), ((y_pos + 1) * (SCREEN_HEIGHT / 3)) - SCREEN_HEIGHT / 18), LINE_WIDTH)
            elif y == -1:
                pygame.draw.line(screen, draw_color,
                                 ((x_pos * (SCREEN_WIDTH / 3) + SCREEN_WIDTH / 18), (y_pos * 2 + 1) * (SCREEN_HEIGHT / 6)),
                                 (((x_pos + 1) * (SCREEN_WIDTH / 3) - SCREEN_WIDTH / 18), (y_pos * 2 + 1) * (SCREEN_HEIGHT / 6)), LINE_WIDTH)
            elif y == 2:
                pygame.draw.line(screen, draw_color,
                                 ((x_pos * 2 + 1) * (SCREEN_WIDTH / 6), (y_pos * (SCREEN_HEIGHT / 3)) + SCREEN_HEIGHT / 18),
                                 ((x_pos * 2 + 1) * (SCREEN_WIDTH / 6), ((y_pos + 1) * (SCREEN_HEIGHT / 3)) - SCREEN_HEIGHT / 18), LINE_WIDTH)
                pygame.draw.line(screen, draw_color,
                                 ((x_pos * (SCREEN_WIDTH / 3) + SCREEN_WIDTH / 18), (y_pos * 2 + 1) * (SCREEN_HEIGHT / 6)),
                                 (((x_pos + 1) * (SCREEN_WIDTH / 3) - SCREEN_WIDTH / 18), (y_pos * 2 + 1) * (SCREEN_HEIGHT / 6)), LINE_WIDTH)
            y_pos += 1

        x_pos += 1


# Handles the mouse click (checks position, checks board and updates the board)
def HandleMouseClick(pos, board, player, played_plus):
    cell_x = pos[0]
    cell_y = pos[1]

    # The // 3 is used to get the cell's position in the board (divides the screen into 3x3 cells)
    if board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] == 0:
        board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] = player
        played_plus[player + 1] = False

    # elif for the "plus" mechanic
    elif (board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] != player
          and board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] != 2
          and (not played_plus[player + 1] or 0 not in board)):  # This line checks if player has already played a plus
                                                                 # last round but if no other places available skip his
                                                                 # turn (in reality just lets him play whatever he wants
                                                                 # instead of skipping 2 turns)
        board[cell_x // (SCREEN_WIDTH // 3)][cell_y // (SCREEN_HEIGHT // 3)] = 2
        played_plus[player + 1] = True

    else:
        return 1

    CheckWin(board, player)
    return -1


def CheckWin(board, player):
    global run
    if (
            board[0][0] == board[0][1] == board[0][2] != 0 or
            board[1][0] == board[1][1] == board[1][2] != 0 or
            board[2][0] == board[2][1] == board[2][2] != 0 or
            board[0][0] == board[1][0] == board[2][0] != 0 or
            board[0][1] == board[1][1] == board[2][1] != 0 or
            board[0][2] == board[1][2] == board[2][2] != 0 or
            board[0][0] == board[1][1] == board[2][2] != 0 or
            board[0][2] == board[1][1] == board[2][0] != 0
    ):
        if player == -1:
            player = 2
        print(f"Player {player} won!")
        run = False


# Get the user's desired theme
theme = input("Enter theme (light/dark): ").lower()
while theme not in ["light", "dark", "l", "d"]:
    theme = input("Theme doesn't exist, please enter light(l) or dark(d): ").lower()

if theme == "light" or theme == "l":
    theme = 1
else:
    theme = 0

# Set the background and draw color according to the theme
background = (255 * theme, 255 * theme, 255 * theme)
draw_color = (255 * (1 - theme), 255 * (1 - theme), 255 * (1 - theme))

# Initialize pygame
pygame.init()
# Create the screen (window)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set the title of the window
pygame.display.set_caption("TicTacToe +")
pygame.display.set_icon(pygame.image.load("icon.png"))

game_board = \
    [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

# Game loop
run = True
while run:
    # Draw the grid and the players' moves
    DrawGrid()
    DrawPlayers(game_board)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_player *= HandleMouseClick(pygame.mouse.get_pos(), game_board, current_player,
                                               played_plus_last_round)

    # Update game state
    pygame.display.update()

pygame.quit()
