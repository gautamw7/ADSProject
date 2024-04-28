import pygame
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 50
QUEUE_SIZE = 5

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Queue Sorting Game")

# Font
font = pygame.font.SysFont(None, 24)

def get_points(elapsed_time):
    if elapsed_time <=5:
        return 100
    elif elapsed_time <= 10:
        return 75
    elif elapsed_time <= 15:
        return 25
    else:
        return 0

star_images = {
    '3': pygame.image.load('photos/star3.png'),
    '2': pygame.image.load('photos/star2.png'),
    '1': pygame.image.load('photos/star1.png'),
    '0': pygame.image.load('photos/star0.png')
}

def show_completion_screen(moves):
    screen.fill(BLACK)
    message = "You have completed the maze!"
    text = font.render(message, True, GREEN)

    # Determine the number of stars
    if moves <= 10:
        stars = '3'
    elif moves <= 15:
        stars = '2'
    elif moves <= 20:
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

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def isEmpty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.isEmpty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.isEmpty():
            print("Queue is empty.")
            pygame.quit()
            sys.exit()
        temp = self.front
        data = temp.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return data

def draw_moves_counter(moves):
    moves_text = font.render(f"Moves: {moves}", True, WHITE)
    moves_rect = moves_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(moves_text, moves_rect)

def draw_instruction_panel():
    instruction_text1 = font.render("Use '1' to move 2 elements position at the start.", True, WHITE)
    instruction_text2 = font.render("Use '2' keys to push the first element to the last.",True,WHITE)
    instruction_rect1 = instruction_text1.get_rect(bottomleft=(10, SCREEN_HEIGHT - 25))
    instruction_rect2 = instruction_text2.get_rect(bottomleft=(10, SCREEN_HEIGHT - 10))
    screen.blit(instruction_text1, instruction_rect1)
    screen.blit(instruction_text2, instruction_rect2)

def draw_queue(queue, moves):
    total_width = QUEUE_SIZE * BLOCK_SIZE
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - BLOCK_SIZE) // 2

    draw_moves_counter(moves)
    draw_instruction_panel()

    current = queue.front
    for i in range(QUEUE_SIZE):
        if current:
            pygame.draw.rect(screen, WHITE, (start_x + i * BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE))
            text = font.render(str(current.data), True, BLACK)
            text_rect = text.get_rect(center=(start_x + i * BLOCK_SIZE + BLOCK_SIZE // 2, start_y + BLOCK_SIZE // 2))
            screen.blit(text, text_rect)
            current = current.next
        else:
            pygame.draw.rect(screen, WHITE, (start_x + i * BLOCK_SIZE, start_y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, RED, (start_x + i * BLOCK_SIZE + 10, start_y + 10,
                                           BLOCK_SIZE - 20, BLOCK_SIZE - 20))

def move1(queue):
    if queue.isEmpty() or queue.front.next is None:
        print("Not enough elements to perform move 1.")
        return
    temp = queue.front.data
    queue.front.data = queue.front.next.data
    queue.front.next.data = temp

# Function to perform move 2
def move2(queue):
    if queue.isEmpty() or queue.front == queue.rear:
        print("Not enough elements to perform move 2.")
        return
    data = queue.dequeue()
    queue.enqueue(data)

def isSorted(queue):
    if queue.isEmpty() or queue.front == queue.rear:
        return True
    current = queue.front
    while current.next:
        if current.data > current.next.data:
            return False
        current = current.next
    return True


def play_game(queue):
    moves = 0
    while not isSorted(queue):
        draw_queue(queue, moves)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    move1(queue)
                    moves += 1
                elif event.key == pygame.K_2:
                    move2(queue)
                    moves += 1

        screen.fill(BLACK)
        draw_queue(queue, moves)
        pygame.display.flip()

    show_completion_screen(moves)


def main():
    queue = Queue()

    for _ in range(QUEUE_SIZE):
        data = random.randint(0, 99)
        queue.enqueue(data)

    play_game(queue)

if __name__ == "__main__":
    main()
