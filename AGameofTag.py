import time
import sys
import pygame
import random
from collections import deque

CELL_SIZE = 40
GRID_WIDTH = 10
GRID_HEIGHT = 10
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
class CellType:
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    BOT = 3

class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Cell:
    def __init__(self, row, col, cell_type):
        self.row = row
        self.col = col
        self.cell_type = cell_type

star_images = {
    '3': pygame.transform.scale(pygame.image.load('photos/star3.png'), (100, 100)),
    '2': pygame.transform.scale(pygame.image.load('photos/star2.png'), (100, 100)),
    '1': pygame.transform.scale(pygame.image.load('photos/star1.png'), (100, 100)),
    '0': pygame.transform.scale(pygame.image.load('photos/star0.png'), (100, 100))
}

def game_over(stars):
    global screen, steps
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Define the screen
    screen.fill(WHITE)

    star_image = star_images[str(stars)]  # Convert stars to a string before accessing the dictionary
    star_rect = star_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Center the star image
    screen.blit(star_image, star_rect)

    font = pygame.font.SysFont(None, 36)
    reload_text = font.render("Press 'R' to reload", True, BLACK)
    reload_rect = reload_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(reload_text, reload_rect)

    # Display "You Lost" message
    lost_text = font.render("You Lost", True, BLACK)
    lost_rect = lost_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(lost_text, lost_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Add a delay of 2 seconds (2000 milliseconds)
                    pygame.time.delay(1000)
                    main()

        pygame.time.Clock().tick(10)  # Limit the loop to 10 frames per second


class Game:
    def __init__(self):
        self.grid = [[Cell(row, col, CellType.EMPTY) for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]
        self.player_position = (0, 0)
        self.bot_positions = [(0, 0)]
        self.generate_level()
        self.last_bot_move_time = pygame.time.get_ticks()


    def generate_level(self):
        walls = [
            (0,7),
            (1,1), (1,2), (1,6), (1,9),
            (2,2), (2,5),
            (3,0), (3,7),
            (4,2), (4,3), (4,4), (4,7), (4,9),
            (5,1), (5,2), (5,4),
            (6,4), (6,8),
            (7,4), (7,8),
            (8,1), (8,8)
        ]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if (row, col) in walls:
                    self.grid[row][col].cell_type = CellType.WALL

        self.player_position = self.get_random_empty_position()
        self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.PLAYER

        self.bot_positions = []
        for _ in range(2):
            bot_position = self.get_random_empty_position()
            while self.calculate_distance(self.player_position, bot_position) < 5:
                bot_position = self.get_random_empty_position()
            self.bot_positions.append(bot_position)
            self.grid[bot_position[1]][bot_position[0]].cell_type = CellType.BOT

    def calculate_distance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


    def get_random_empty_position(self):
        while True:
            row = random.randint(0, len(self.grid) - 1)
            col = random.randint(0, len(self.grid[0]) - 1)
            if self.grid[row][col].cell_type == CellType.EMPTY:
                return (col, row)

    def is_valid_position(self, position):
        col, row = position
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def is_empty_position(self, position):
        col, row = position
        return self.is_valid_position(position) and self.grid[row][col].cell_type == CellType.EMPTY

    def move_player(self, direction):
        new_position = (self.player_position[0] + direction[0], self.player_position[1] + direction[1])
        if self.is_empty_position(new_position):
            self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.EMPTY
            self.player_position = new_position
            self.grid[self.player_position[1]][self.player_position[0]].cell_type = CellType.PLAYER

    def move_bots(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bot_move_time >= 250:
            for i, bot_position in enumerate(self.bot_positions):
                bot_direction = self.get_bot_direction(bot_position)
                new_position = (bot_position[0] + bot_direction[0], bot_position[1] + bot_direction[1])
                if self.is_empty_position(new_position):
                    self.grid[bot_position[1]][bot_position[0]].cell_type = CellType.EMPTY
                    self.bot_positions[i] = new_position
                    self.grid[new_position[1]][new_position[0]].cell_type = CellType.BOT
            self.last_bot_move_time = current_time

            for bot_position in self.bot_positions:
                if bot_position == self.player_position:
                    print("Game Over - Player caught by a bot!")
                    return True

        return False

    def get_bot_direction(self, bot_position):
        if self.calculate_distance(bot_position, self.player_position) == 1:
            print("Player is adjacent to bot. Moving towards player.")
            return self.get_direction_towards_bot(bot_position, self.player_position)
        else:
            for bot_pos in self.bot_positions:
                if self.calculate_distance(bot_pos, self.player_position) == 1:
                    print("Player is adjacent to another bot. Waiting.")
                    return (0, 0)

            print("Player is not adjacent to bot. Using BFS.")
            visited = {}
            queue = deque([(bot_position, 0, None)])
            while queue:
                current_position, distance, previous_position = queue.popleft()
                if current_position == self.player_position:
                    while previous_position != bot_position:
                        current_position = previous_position
                        previous_position = visited[current_position][1]
                    return self.get_direction_towards_bot(bot_position, current_position)
                visited[current_position] = (distance, previous_position)
                for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    new_position = (current_position[0] + direction[0], current_position[1] + direction[1])
                    if self.is_valid_position(new_position) and new_position not in visited and self.grid[new_position[1]][new_position[0]].cell_type != CellType.WALL:
                        queue.append((new_position, distance + 1, current_position))
            return (0, 0)

    def get_direction_towards_bot(self, bot_position, player_position):
        dx = player_position[0] - bot_position[0]
        dy = player_position[1] - bot_position[1]
        if abs(dx) > abs(dy):
            return (1 if dx > 0 else -1, 0)
        else:
            return (0, 1 if dy > 0 else -1)

    def draw(self, screen, time_elapsed):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                cell = self.grid[row][col]
                if cell.cell_type == CellType.WALL:
                    pygame.draw.rect(screen, (100, 100, 100), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell.cell_type == CellType.PLAYER:
                    pygame.draw.rect(screen, (0, 255, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell.cell_type == CellType.BOT:
                    pygame.draw.rect(screen, (255, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        time_text = f"Time: {time_elapsed:.2f} sec"
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(time_text, True, BLACK)
        screen.blit(text_surface, (10, 10))  # Position the timer text on the left side
        pygame.display.flip()
        pygame.display.flip()

def instruction_screen(screen):
    font = pygame.font.SysFont(None, 30)
    instructions = [
        "Welcome to the Pac-Man Game!",
        "Use UP DOWN LEFT RIGHT keys to move Pac-Man.",
        "Avoid the red bots!",
        "Survive for as long as you can to earn stars.",
        "Press any key to start the game."
    ]
    y = 100
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH + 200, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Pursuit Square")
    for instruction in instructions:
        text_surface = font.render(instruction, True, WHITE)
        text_rect = text_surface.get_rect(center=((SCREEN_WIDTH + 200) // 2, y))
        screen.blit(text_surface, text_rect)
        y += 40
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                waiting = False

def main():
    pygame.init()
    pygame.display.set_caption("Pygame Pursuit Square")
    clock = pygame.time.Clock()

    game = Game()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    instruction_screen(screen)  # Corrected function call

    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.move_player(Direction.UP)
        elif keys[pygame.K_DOWN]:
            game.move_player(Direction.DOWN)
        elif keys[pygame.K_LEFT]:
            game.move_player(Direction.LEFT)
        elif keys[pygame.K_RIGHT]:
            game.move_player(Direction.RIGHT)

        game.move_bots()

        for bot_position in game.bot_positions:
            if game.calculate_distance(bot_position, game.player_position) == 1:
                print("Game Over - Player caught by a bot!")
                running = False
                break

        screen.fill((255, 255, 255))
        time_elapsed = time.time() - start_time
        game.draw(screen, time_elapsed)  # Pass elapsed time to the draw method

        clock.tick(FPS)

    # Calculate star rating based on survival time
    if time_elapsed >= 30:
        stars = 3
    elif time_elapsed >= 20:
        stars = 2
    elif time_elapsed >= 10:
        stars = 1
    else:
        stars = 0

    print(f"Survival Time: {time_elapsed:.2f} sec")
    print(f"Stars Earned: {stars}")
    # Add a delay of 2 seconds (2000 milliseconds)
    pygame.time.delay(500)
    game_over(stars)  # Ensure the game_over() function is defined

    pygame.quit()


if __name__ == "__main__":
    main()
