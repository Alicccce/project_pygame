import pygame
import os

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
    FONT = pygame.font.SysFont("Roboto", 80)
    finished = FONT.render("Смурфики", True, "white")
    finished_rect = finished.get_rect(center=(640, 280))
    imgtr = load_image('trop.png')
    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    xx, yy = 0, 45



    while running:
        surf.fill((150, 190, 100))
        surf.blit(finished, finished_rect)
        screen.blit(imgtr, (xx, yy))
        surf.blit(imgg,(490, -35))
        surf.blit(imgg, (80, -35))
        surf.blit(imgg, (225, -35))
        surf.blit(imgv, (1085, -68))
        surf.blit(imgv, (720, -68))
        surf.blit(imgv, (840, -68))




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


screen = pygame.display.set_mode((1300, 750))
load(screen)
