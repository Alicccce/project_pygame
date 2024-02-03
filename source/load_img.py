import random
import pygame
import os
from source.Alice import game_one
from source.functions import load_image


def two(surf):
    from source.game_two import game_two
    game_two(surf)



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
OBSCHIY = (10, 200, 150)
load_fraze_img = ['load_dorog1.png', 'load_kl.png']


def load_image(name, colorkey=None):
    fullname = os.path.join('resource/data', name)
    image = pygame.image.load(fullname)
    return image


def load(surf):
    pygame.init()
    pygame.font.init()
    running = True
    size = (1300, 750)
    clock = pygame.time.Clock()

    start_ticks = pygame.time.get_ticks()

    img_bus_load = load_image('bus_mini.png')
    angle = 0
    FONT = pygame.font.SysFont("Roboto", 80)
    finished = FONT.render("Загрузка", True, "white")
    finished_rect = finished.get_rect(center=(640, 280))

    rch = random.choice([1, 2])

    while running:
        surf.fill(OBSCHIY)
        rotated_img = pygame.transform.rotozoom(img_bus_load, angle, 1)
        surf.blit(finished, finished_rect)
        angle += 1
        if angle >= 360:
            angle = 0

        millis = pygame.time.get_ticks() - start_ticks
        secs = millis // 1000
        if secs >= 16:
            secs = 15
        mins = secs // 60
        secs %= 60


        if rch == 1:
            imag = load_image(load_fraze_img[1])
            surf.blit(imag, (450, 465))
        else:
            imag = load_image(load_fraze_img[0])
            surf.blit(imag, (450, 465))
        if secs == 4:
            if rch == 1:
                game_one(surf)
            elif rch == 2:
                two(surf)



        surf.blit(rotated_img, (size[0] // 2 - rotated_img.get_width() // 2, size[1] // 2 - rotated_img.get_height() // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()