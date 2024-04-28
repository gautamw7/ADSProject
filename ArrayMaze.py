import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900

ROWS = 21
COLS = 20

start_ticks = pygame.time.get_ticks()

def get_points(elapsed_time):
    if elapsed_time <=5:
        return 100
    elif elapsed_time <= 10:
        return 75
    elif elapsed_time <= 15:
        return 25
    else:
        return 0

# Assuming you have images named star3.png, star2.png, star1.png, star0.png
star_images = {
    '3': pygame.image.load('photos/star3.png'),
    '2': pygame.image.load('photos/star2.png'),
    '1': pygame.image.load('photos/star1.png'),
    '0': pygame.image.load('photos/star0.png')
}

def show_completion_screen(elapsed_time):
    screen.fill(BLACK)
    message = "You have completed the maze!"
    text = font.render(message, True, GREEN)

    # Determine the number of stars
    if elapsed_time <= 13:
        stars = '3'
    elif elapsed_time <= 17:
        stars = '2'
    elif elapsed_time <= 23:
        stars = '1'
    else:
        stars = '0'

    star_image = star_images[stars]
    star_rect = star_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)
    screen.blit(star_image, star_rect)

    pygame.display.flip()
    pygame.time.wait(5000)


maze = [
    ['S', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', '#', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'E', '#'],
    ['#', '#', '#', ' ', '#', '#', '#', '#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#', '#', '#', '#'],
    ['#', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

player_row, player_col = 0, 0
for i in range(ROWS):
    for j in range(COLS):
        if maze[i][j] == 'S':
            player_row = i
            player_col = j

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")

font = pygame.font.Font(None, 36)

def draw_maze():
    for i in range(ROWS):
        for j in range(COLS):
            cell = maze[i][j]
            if cell == '#':
                pygame.draw.rect(screen, WHITE, (j * 40, i * 40, 40, 40))
            elif cell == 'S':
                pygame.draw.rect(screen, GREEN, (j * 40, i * 40, 40, 40))
            elif cell == 'E':
                pygame.draw.rect(screen, RED, (j * 40, i * 40, 40, 40))
            else:
                pass

def move_player(new_row, new_col):
    global player_row, player_col
    if 0 <= new_row < ROWS and 0 <= new_col < COLS and maze[new_row][new_col] != '#':
        player_row = new_row
        player_col = new_col

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move_player(player_row - 1, player_col)
        elif keys[pygame.K_LEFT]:
            move_player(player_row, player_col - 1)
        elif keys[pygame.K_DOWN]:
            move_player(player_row + 1, player_col)
        elif keys[pygame.K_RIGHT]:
            move_player(player_row, player_col + 1)

        if maze[player_row][player_col] == 'E':
            end_ticks = pygame.time.get_ticks()
            game_over = True
            elapsed_time = (end_ticks - start_ticks) / 1000
            show_completion_screen(elapsed_time)
            pygame.time.wait(5000)
            running = False

        screen.fill(BLACK)
        draw_maze()
        pygame.draw.rect(screen, BLUE, (player_col * 40, player_row * 40, 40, 40))
        pygame.display.flip()

        pygame.time.delay(100)
    else:
        pygame.time.wait(100)  # Just wait around if the game is over

pygame.quit()
sys.exit()
