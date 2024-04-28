import pygame
import sys
import math
import random

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

FONT = pygame.font.SysFont('comicsans', 90)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_XO(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), LINE_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), LINE_WIDTH)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), int(SQUARE_SIZE / 2 - 20), LINE_WIDTH)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True

def check_winner(board, player):
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True

    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True

    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or \
            all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True

    return False

def get_available_moves(board):
    moves = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == EMPTY:
                moves.append((row, col))
    return moves

def simulate_game(board, player):
    while True:
        available_moves = get_available_moves(board)
        if not available_moves or check_winner(board, PLAYER_X) or check_winner(board, PLAYER_O):
            break
        row, col = random.choice(available_moves)
        board[row][col] = player
        player = PLAYER_X if player == PLAYER_O else PLAYER_O

class Node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = None

    def expand(self, board):
        self.untried_moves = get_available_moves(board)
        random.shuffle(self.untried_moves)
        for move in self.untried_moves:
            self.children.append(Node(move, self))

    def select_child(self):
        selected_child = max(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))
        return selected_child


def mcts(board, player, simulations=1000):
    root = Node()
    for _ in range(simulations):
        node = root
        temp_board = [row[:] for row in board]
        while not node.untried_moves and node.children:
            node = node.select_child()
            row, col = node.move
            temp_board[row][col] = player
            player = PLAYER_X if player == PLAYER_O else PLAYER_O

        if node.untried_moves:
            move = random.choice(node.untried_moves)
            row, col = move
            temp_board[row][col] = player
            player = PLAYER_X if player == PLAYER_O else PLAYER_O
            node.expand(temp_board)
            node = node.children[-1]

        simulate_game(temp_board, player)

        while node:
            node.visits += 1
            if check_winner(temp_board, PLAYER_X):
                node.wins += 1
            node = node.parent

    if root.children:
        best_child = max(root.children, key=lambda c: c.wins / c.visits)
        return best_child.move
    else:
        return random.choice(get_available_moves(board))


def main():
    # Initialize scores
    player_score = 0
    computer_score = 0

    board = [[EMPTY for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    current_player = PLAYER_X

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_player == PLAYER_X:
                    row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    if board[row][col] == EMPTY:
                        board[row][col] = PLAYER_X
                        if check_winner(board, PLAYER_X):
                            game_over = True
                        elif is_board_full(board):
                            game_over = True
                        current_player = PLAYER_O
                else:
                    row, col = mcts(board, PLAYER_O)
                    if board[row][col] == EMPTY:
                        board[row][col] = PLAYER_O
                        if check_winner(board, PLAYER_O):
                            game_over = True
                        elif is_board_full(board):
                            game_over = True
                        current_player = PLAYER_X
                # Draw scores


        screen.fill(WHITE)
        draw_grid()
        draw_XO(board)

        if game_over:
            if check_winner(board, PLAYER_X):
                player_score += 1  # Increment player score if they win
                label = FONT.render("Player wins!", True, RED)
            elif check_winner(board, PLAYER_O):
                computer_score += 1  # Increment computer score if they win
                label = FONT.render("Computer wins!", True, BLUE)
            else:
                label = FONT.render("It's a tie!", True, BLACK)

            screen.blit(label, (WIDTH / 2 - label.get_width() / 2, HEIGHT / 2 - label.get_height() / 2))

            # Display scores
            score_font = pygame.font.SysFont('comicsans', 40)
            player_score_text = score_font.render(f"Player: {player_score}", True, BLACK)
            computer_score_text = score_font.render(f"Computer: {computer_score}", True, BLACK)
            screen.blit(player_score_text, (10, 10))
            screen.blit(computer_score_text, (WIDTH - computer_score_text.get_width() - 10, 10))

            pygame.display.update()
            pygame.time.delay(2000)

            board = [[EMPTY for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            game_over = False
            current_player = PLAYER_X

        pygame.display.update()

if __name__ == "__main__":
    main()
