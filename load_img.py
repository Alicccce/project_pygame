import random
import pygame
import os
from Alice import game_one


def two(surf):
    from game_two import game_two
    game_two(surf)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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

    while running:
        surf.fill((10, 200, 150))
        rotated_img = pygame.transform.rotozoom(img_bus_load, angle, 1)
        surf.blit(finished, finished_rect)
        angle += 1  #
        if angle >= 360:
            angle = 0

        millis = pygame.time.get_ticks() - start_ticks
        secs = millis // 1000
        if secs >= 16:
            secs = 15
        mins = secs // 60
        secs %= 60

        if secs == 4:
            print(3)
            two(surf)



        surf.blit(rotated_img,
                  (size[0] // 2 - rotated_img.get_width() // 2, size[1] // 2 - rotated_img.get_height() // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


