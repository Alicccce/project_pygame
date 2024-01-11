import pygame
import os
import sys
from random import *


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
HEIGHT = 750
WIDTH = 1300
for_y = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bus(pygame.sprite.Sprite):
    image = load_image("bus_osn.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bus.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT // 2 - 35
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y + 14 >= 80:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.y + 111 <= 730:
            self.rect.y += 5


class Cars(pygame.sprite.Sprite):
    def __init__(self, g_sprts, name): # ('png', (x, y))
        super().__init__()
        self.image = load_image(name[0]) # считываем назвнаие
        self.rect = self.image.get_rect()
        self.rect.x = name[1][0] # считаваем неизменную абциссу
        #self.rect.y = name[1][1]
        # ТУТ problem !
        if name[1][1] not in for_y: # сравнение с предыдущими ординатами
            self.rect.y = name[1][1]
        else:
            #if (name[1][1] + randint(50, 300)) != for_y[]
            self.rect.y = (name[1][1] + 300) or (name[1][1] - 300)
            for_y.append(self.rect.y) # "запоминаем" ординату
        for_y.append(self.rect.y) # "запоминаем" ординату
        g_sprts.add(self)

    def update(self, speed):
        self.rect.x -= 5
        if self.rect.x + self.rect.width < 0:
            self.rect.x = randint(WIDTH + 10, WIDTH + 500)
            self.rect.y = randint(85, HEIGHT - 110)


if __name__ == '__main__':
    pygame.init()
    size = (1300, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    all_sprites = pygame.sprite.Group()
    Bus(all_sprites)
    for name in [('red_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110))),
                 ('yel_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110))),
                 ('gray_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110))),
                 ('black_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110))),
                 ('purp_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110))),
                 ('white_car.png', (randint(WIDTH + 10, WIDTH + 500), randint(85, HEIGHT - 110)))]:
        Cars(all_sprites, name) # передаём в name имя файла и координаты запуска
    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    imgtr = load_image('trop.png')

    running = True

    while running:
        screen.fill((150, 190, 100))

        x1, y1 = 0, 45
        screen.blit(imgtr, (x1, y1))

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        all_sprites.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        for i in range(3):
            screen.blit(imgg, (i * 140, -35))
        screen.blit(imgv, (420, -68))
        for i in range(4):
            screen.blit(imgg, (525 + i * 140, -35))
        screen.blit(imgv, (1085, -68))
        screen.blit(imgg, (1191, -35))


        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()