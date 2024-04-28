import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (173, 216, 230)
GREEN = (0, 255, 0)

WIDTH = 60
HEIGHT = 60
MARGIN = 5

pygame.init()

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

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    star_image = star_images[stars]
    star_rect = star_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(text, text_rect)
    screen.blit(star_image, star_rect)

    pygame.display.flip()
    pygame.time.wait(7000)



class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def create_linked_list():
    sequence = random.sample(range(1, 6), 5)  # Generate a random sequence of 5 unique numbers
    head = None
    tail = None

    for data in sequence:
        new_node = Node(data)

        if head is None:
            head = tail = new_node
        else:
            tail.next = new_node
            tail = new_node

    return head

def display_linked_list(screen, head, selectedIndex1, selectedIndex2):
    font = pygame.font.SysFont(None, 24)
    current = head
    x = MARGIN + ((600 - (5 * WIDTH + 4 * MARGIN)) / 2)  # Calculate the starting x-coordinate to center the keys
    y = MARGIN
    index = 0
    while current:
        if index == selectedIndex1 or index == selectedIndex2:
            pygame.draw.rect(screen, BLUE, [x, y + 275, WIDTH, HEIGHT])
        else:
                pygame.draw.rect(screen, GRAY, [x, y + 275, WIDTH, HEIGHT])

        text = font.render(str(current.data), True, BLACK)
        text_rect = text.get_rect(center=(x + WIDTH / 2, y + 275 + HEIGHT / 2))  # Center the text within the block
        screen.blit(text, text_rect)
        x += WIDTH + MARGIN

        current = current.next
        index += 1

def is_sorted(head):
    while head and head.next:
        if head.data > head.next.data:
            return False
        head = head.next
    return True

def swap_nodes(head, index1, index2):
    if index1 == index2:
        return head

    currX = head
    for _ in range(index1):
        currX = currX.next

    currY = head
    for _ in range(index2):
        currY = currY.next

    currX.data, currY.data = currY.data, currX.data

    return head

def play_game(screen, head):
        selectedIndex1 = 0
        selectedIndex2 = 1
        printSequence = True
        moves = 0

        font = pygame.font.SysFont(None, 24)
        clock = pygame.time.Clock()

        instructions_font = pygame.font.SysFont(None, 25)
        instructions_text1 = instructions_font.render(
            "Instructions: Use 'A' and 'D' keys to move brackets,", True,
            WHITE)
        instructions_text2 = instructions_font.render(
            "'X' to swap. You can only swap adjacent tiles.", True,
            WHITE)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not is_sorted(head):
                if printSequence:
                    screen.fill(BLACK)
                    display_linked_list(screen, head, selectedIndex1, selectedIndex2)
                    # Adjusting the y-coordinate of instructions_text1 to be 15 pixels above instructions_text2
                    screen.blit(instructions_text1, (screen.get_width() / 2 - instructions_text1.get_width() / 2,
                                                     screen.get_height() - 20 - instructions_text1.get_height() - instructions_text2.get_height()))
                    screen.blit(instructions_text2, (screen.get_width() / 2 - instructions_text2.get_width() / 2,
                                                     screen.get_height() - 10- instructions_text2.get_height()))
                    moves_text = font.render("Moves: {}".format(moves), True, WHITE)
                    screen.blit(moves_text, (10, 10))  # Moves at the top left
                    pygame.display.flip()
                    printSequence = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    if selectedIndex1 is None or selectedIndex1 > 0:
                        selectedIndex2 = selectedIndex1
                        selectedIndex1 = selectedIndex1 - 1
                        moves += 1
                        print("Selected Index 1:", selectedIndex1)
                        print("Selected Index 2:", selectedIndex2)
                        printSequence = True
                elif keys[pygame.K_d]:
                    if selectedIndex2 is None or selectedIndex2 < 4:
                        selectedIndex1 = selectedIndex2
                        selectedIndex2 = selectedIndex2 + 1
                        moves += 1
                        print("Selected Index 1:", selectedIndex1)
                        print("Selected Index 2:", selectedIndex2)
                        printSequence = True
                elif keys[pygame.K_x]:
                    if selectedIndex1 is not None and selectedIndex2 is not None and abs(
                            selectedIndex1 - selectedIndex2) == 1:
                        head = swap_nodes(head, selectedIndex1, selectedIndex2)
                        moves += 1
                        printSequence = True

                clock.tick(10)


            else:
                show_completion_screen(moves)
                running = False

        pygame.quit()
if __name__ == "__main__":
    head = create_linked_list()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Sequence Arrangement Puzzle")
    play_game(screen, head)
