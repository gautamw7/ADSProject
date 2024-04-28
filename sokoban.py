import pygame
import sys
from collections import deque
import heapq

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)

CELL_SIZE = 30
MARGIN = 3

game_map = [
    "######################",
    "#              #     #",
    "#             #   .  #",
    "#   ####      #      #",
    "#             #      #",
    "#             ####   #",
    "#             #      #",
    "#.                  .#",
    "#             #      #",
    "#             #      #",
    "#   ####      #      #",
    "#             #      #",
    "#             ####   #",
    "#                    #",
    "######################"
]

player_pos = (2, 13)

target_spots = [(14, 1), (14, 13), (2, 5), (5, 2), (10, 10)]

box_positions = [(5, 5), (9, 9), (11,12), (3, 4), (7, 5)]

WINDOW_WIDTH = len(game_map[0]) * (CELL_SIZE + MARGIN) + MARGIN
WINDOW_HEIGHT = len(game_map) * (CELL_SIZE + MARGIN) + MARGIN

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Sokoban")

clock = pygame.time.Clock()


def draw_map():
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            color = WHITE
            if game_map[row][col] == "#":
                color = BLACK
            pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * col + MARGIN,
                                              (MARGIN + CELL_SIZE) * row + MARGIN,
                                              CELL_SIZE,
                                              CELL_SIZE])


def draw_player():
    pygame.draw.circle(screen, RED, ((MARGIN + CELL_SIZE) * player_pos[0] + MARGIN + CELL_SIZE // 2,
                                     (MARGIN + CELL_SIZE) * player_pos[1] + MARGIN + CELL_SIZE // 2),
                       min(CELL_SIZE, CELL_SIZE) // 2)


def draw_boxes():
    for pos in box_positions:
        pygame.draw.rect(screen, GREEN, ((MARGIN + CELL_SIZE) * pos[0] + MARGIN,
                                         (MARGIN + CELL_SIZE) * pos[1] + MARGIN,
                                         CELL_SIZE, CELL_SIZE))


def draw_targets():
    for pos in target_spots:
        pygame.draw.rect(screen, LIGHT_BLUE, ((MARGIN + CELL_SIZE) * pos[0] + MARGIN,
                                               (MARGIN + CELL_SIZE) * pos[1] + MARGIN,
                                               CELL_SIZE, CELL_SIZE))


def move_player(dx, dy):
    global player_pos
    x = player_pos[0] + dx
    y = player_pos[1] + dy

    if (x, y) not in box_positions and game_map[y][x] != "#":
        player_pos = (x, y)
    elif (x, y) in box_positions:
        new_x = x + dx
        new_y = y + dy
        if game_map[new_y][new_x] != "#" and (new_x, new_y) not in box_positions:
            box_positions.remove((x, y))
            box_positions.append((new_x, new_y))
            player_pos = (x, y)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_player(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)

    screen.fill(WHITE)

    draw_map()

    draw_targets()

    draw_boxes()

    draw_player()

    win = all(box_pos in target_spots for box_pos in box_positions)
    if win:
        print("You win!")
        pygame.quit()
        sys.exit()

    clock.tick(60)

    pygame.display.flip()