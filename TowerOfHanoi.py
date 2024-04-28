import pygame, sys, time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

game_done = False
framerate = 60

steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)


def blit_text(screen, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255, 0, 0)):
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)


def menu_screen():
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:

        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (323, 122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320, 120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30,
                  color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(60)

star_images = {
    '3': pygame.transform.scale(pygame.image.load('photos/star3.png'), (100, 100)),
    '2': pygame.transform.scale(pygame.image.load('photos/star2.png'), (100, 100)),
    '1': pygame.transform.scale(pygame.image.load('photos/star1.png'), (100, 100)),
    '0': pygame.transform.scale(pygame.image.load('photos/star0.png'), (100, 100))
}

def game_over():
    global screen, steps
    screen.fill(white)
    min_steps = 2 ** n_disks - 1

    # Display "You Won!" at the top of the screen
    blit_text(screen, 'You Won!', (320, 50), font_name='sans serif', size=36, color=gold)
    blit_text(screen, 'You Won!', (322, 52), font_name='sans serif', size=36, color=gold)

    # Determine the number of stars
    if steps <= min_steps:
        stars = '3'
    elif steps <= 1.25 * min_steps:
        stars = '2'
    elif steps <= 1.5 * min_steps:
        stars = '1'
    else:
        stars = '0'

    star_image = star_images[stars]
    star_rect = star_image.get_rect(center=(320, 150))
    screen.blit(star_image, star_rect)

    # Display "Your Steps" and "Minimum Steps" at the bottom of the screen
    blit_text(screen, 'Your Steps: ' + str(steps), (320, 300), font_name='mono', size=24, color=black)
    blit_text(screen, 'Minimum Steps: ' + str(min_steps), (320, 330), font_name='mono', size=24, color=red)
    if min_steps == steps:
        blit_text(screen, 'You finished in minimum steps!', (320, 280), font_name='mono', size=24, color=black)

    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def draw_towers():
    global screen
    for xpos in range(40, 460 + 1, 200):
        pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, grey, pygame.Rect(xpos + 75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)


def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks - i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height + 3
        width -= 23


def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, blue, disk['rect'])
    return


def draw_ptr():
    ptr_points = [(towers_midx[pointing_at] - 7, 440), (towers_midx[pointing_at] + 7, 440),
                  (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return


def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()


def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()


menu_screen()
make_disks()

while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at + 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at - 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] > disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top - 23)
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400 - 23)
                    steps += 1
    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: ' + str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.display.flip()
    if not floating: check_won()
    clock.tick(framerate)