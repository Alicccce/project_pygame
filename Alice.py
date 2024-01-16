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
for_x = []
need = []
ox = [i for i in range(WIDTH + 10, WIDTH + 5001, 150)]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существцует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def ox_operations(s): # функция генерации абциссы на старте у машинки
    if s != []:
        x = choice(s)
        s.remove(x)
        return x, s


class Bus(pygame.sprite.Sprite):
    image = load_image("bus_osn.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(*group)
        self.image = Bus.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT // 2 + 15
        self.mask_bus = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y + 14 >= 80:
            self.rect.y -= 6
        if keys[pygame.K_s] and self.rect.y + 111 <= 730:
            self.rect.y += 6


class Cars(pygame.sprite.Sprite):
    def __init__(self, g_sprts, name, ox_per): # ('png', (x, y))
        super().__init__()
        self.ox_per = ox_per
        self.image = load_image(name[0]) # считываем назвнаие
        self.rect = self.image.get_rect()
        self.rect.x = name[1][0] # считаваем абциссу
        self.rect.y = name[1][1] # считаваем ординату
        self.mask_car = pygame.mask.from_surface(self.image)
        g_sprts.add(self)
        for_x.append(self.rect.x)
        need.append(self.rect)

    def update(self, speed):
        # m = load_image("bus_osn.png").get_rect()
        m = Bus().rect
        #if not pygame.mask.from_surface(load_image("bus_osn.png")).overlap(self.mask_car, (1, 1)):
        #if not (m.get_at((load_image("bus_osn.png").get_rect().x, load_image("bus_osn.png").get_rect().y)) == self.mask_car.get_at((self.rect.x, self.rect.y))):
        #if not ((load_image("bus_osn.png").get_rect().x == self.rect.x) or (load_image("bus_osn.png").get_rect().y == self.rect.y)):
        #for i in need:
        if not self.rect.colliderect(m):
            cor_y = [90, 200, 310, 420, 530, 640]
            self.rect.x -= 12
            p = choice(self.ox_per) # выбор абциссы старта машинки при достижении левой границы
            if self.rect.x + self.rect.width < 0 and p not in for_x:
                self.rect.x = (p)
                self.rect.y = choice(cor_y)
                for_x.append(self.rect.x), self.ox_per.remove(self.rect.x)
        else:
            screen.fill((100, 200, 100))
            #restart_mayb(self.rect)
            self.rect.x = name[1][0]
            self.rect.y = name[1][1]


if __name__ == '__main__':
    pygame.init()
    size = (1300, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    all_sprites = pygame.sprite.Group()
    Bus(all_sprites)

    cor_y = [90, 200, 310, 420, 530, 640]
    x1, x2 = ox_operations(ox)[0], ox_operations(ox)[0]
    x3, x4 = ox_operations(ox)[0], ox_operations(ox)[0]
    x5, x6 = ox_operations(ox)[0], ox_operations(ox)[0]
    for name in [('red_car.png', (x1, choice(cor_y))),
                 ('yel_car.png', (x2, choice(cor_y))),
                 ('gray_car.png', (x3, choice(cor_y))),
                 ('black_car.png', (x4, choice(cor_y))),
                 ('purp_car.png', (x5, choice(cor_y))),
                 ('white_car.png', (x6, choice(cor_y)))]:
        Cars(all_sprites, name, ox) # передаём в name имя файла и координаты запуска

    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    imgtr = load_image('trop.png')

    running = True

    xx, yy = 0, 45
    X1, Y1 = 1280, 45
    roof_g_speed = 6
    roof_g_positions = [(490, -35), (80, -35), (225, -35)]
    roof_v_positions = [(1085, -68), (720, -68), (840, -68)]

    screen.blit(imgtr, (xx, yy))

    while running:
        screen.fill((150, 190, 100))

        screen.blit(imgtr, (xx, yy))
        screen.blit(imgtr, (X1, Y1))
        xx -= roof_g_speed
        X1 -= roof_g_speed

        # позиции для домиков
        # Дополнительная позиция чтобы создать зацикленную анимацию

        # Проверка, выходит ли первая дорога за границы видимости
        if xx + imgtr.get_width() <= 0:
            xx = X1 + imgtr.get_width()

        # Проверка, выходит ли вторая дорога за границы видимости
        if X1 + imgtr.get_width() <= 0:
            X1 = xx + imgtr.get_width()
        for position in roof_g_positions:
            screen.blit(imgg, position)
        for position in roof_v_positions:
            screen.blit(imgv, position)

        # Движение домиков "roof_g"
        roof_g_positions = [(x - roof_g_speed, y) for x, y in roof_g_positions]
        # При достижении края экрана, перемещаем домик в конец очереди для создания непрерывной ленты
        roof_g_positions = [((WIDTH, y) if x - 35 < -imgg.get_width() - 100 else (x, y)) for x, y in roof_g_positions]

        roof_v_positions = [(x - roof_g_speed, y) for x, y in roof_v_positions]
        # Делаем то же для "roof_v"
        roof_v_positions = [((WIDTH, y) if x < - imgv.get_width() - 100 else (x, y)) for x, y in roof_v_positions]


        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        all_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()