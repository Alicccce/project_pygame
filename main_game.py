import pygame
import os
import sys
from random import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 100, 100)
LIGHT_GREEN = (100, 200, 100)
HEIGHT, WIDTH = 750, 1300
for_x = [] # список "занятых" абцисс машинок
prov = True
ox = [i for i in range(WIDTH + 10, WIDTH + 5001, 150)] # ось ох (координата машинки),
# которая генерирется и появляется на n_ом расстоянии от осн. экрана

sprts_cars = pygame.sprite.Group() # группа спрайтов машинок
#sound = pygame.mixer.Sound('avaria2.wav')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существцует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def ox_operations(s):  # функция генерации абциссы на старте у машинки
    if s != []:
        x = choice(s)
        s.remove(x)
        return x, s


def smena(x, y): # функция вывода "окончания" основной игры
    global bu
    buyt = Button(500, 600, 260, 50, GREEN, LIGHT_GREEN, 'done')
    buyt.draw(500, 600)
    s = pygame.transform.scale(load_image('yup.jpg'), (200, 200))
    screen.blit(s, (530, 250))
    bu = pygame.transform.scale(load_image('boo.png'), (200, 200)) # картинка взрыва
    screen.blit(bu, (x - 70, y - 50))


def restart():
    speed_car = 12
    ox_per = ox
    bu.convert_alpha()
    pygame.display.update()


class the_next_stat_is(pygame.sprite.Sprite):
    image = load_image('stat.png')

    def __init__(self, all_sprites, ox_per):
        super().__init__(all_sprites)
        self.ox_per = ox_per
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 700
        self.mask_car = pygame.mask.from_surface(self.image)

    def update(self, speed):
        global speed_car
        self.rect.x -= speed_car
        p = choice(self.ox_per)  # выбор абциссы старта машинки при достижении левой границы
        if self.rect.x + self.rect.width < 0 and p not in for_x:
            self.rect.x = (p)
            self.rect.y = 640


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, text=''):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width and click[0] == 1:
            pygame.draw.rect(screen, (self.act_color), self.rect)
            restart()
        else:
            pygame.draw.rect(screen, (self.inact_color), self.rect)
        font = pygame.font.Font(None, 35)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


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
        global speed_car
        # ниже контроль движения автобуса
        if keys[pygame.K_w] and self.rect.y + 14 >= 100 and speed_car != 0:
            self.rect.y -= 6
        if keys[pygame.K_s] and self.rect.y + 111 <= 745 and speed_car != 0:
            self.rect.y += 6


class Cars(pygame.sprite.Sprite):
    def __init__(self, all_sprites, name, ox_per):  # name = ('png', (x, y))
        super().__init__(all_sprites)
        self.ox_per = ox_per
        self.image = load_image(name[0])  # считываем назвнаие
        self.rect = self.image.get_rect()
        self.rect.x = name[1][0]  # считаваем абциссу
        self.rect.y = name[1][1]  # считаваем ординату
        self.mask_car = pygame.mask.from_surface(self.image)
        self.add(sprts_cars) # добавление текущей машинки в список спрайтов
        for_x.append(self.rect.x) # добавление "использованной" координаты х для машинки

    def update(self, speed):
        global speed_car, ox_per
        cor_y = [90, 200, 310, 420, 530, 640]
        self.rect.x -= speed_car
        p = choice(self.ox_per)  # выбор абциссы старта машинки при достижении левой границы
        if pygame.sprite.collide_mask(self, bus): # если машинки сталкнулись
            smena(self.rect.x, self.rect.y)
            speed_car = 0
        # далее проверяется то, когда машинки заезжают за стену
        if self.rect.x + self.rect.width < 0 and p not in for_x:
            self.rect.x = (p)
            self.rect.y = choice(cor_y)
            if len(self.ox_per) == 1:
                the_next_stat_is(all_sprites, self.ox_per)
                speed_car = 0
            else:
                for_x.append(self.rect.x), self.ox_per.remove(self.rect.x)


if __name__ == '__main__':
    size = (1300, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    all_sprites = pygame.sprite.Group()
    bus = Bus(all_sprites)

    cor_y = [90, 200, 310, 420, 530, 640] # список ординат для полос дороги
    x1, x2 = ox_operations(ox)[0], ox_operations(ox)[0]
    x3, x4 = ox_operations(ox)[0], ox_operations(ox)[0]
    x5, x6 = ox_operations(ox)[0], ox_operations(ox)[0]
    for name in [('red_car.png', (x1, choice(cor_y))),
                 ('yel_car.png', (x2, choice(cor_y))),
                 ('gray_car.png', (x3, choice(cor_y))),
                 ('black_car.png', (x4, choice(cor_y))),
                 ('purp_car.png', (x5, choice(cor_y))),
                 ('white_car.png', (x6, choice(cor_y)))]:
            Cars(all_sprites, name, ox)  # передаём в name имя файла и координаты запуска

    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    imgtr = load_image('trop.png')

    running = True

    xx, yy = 0, 45 # координаты расположения изображения дороги
    X1, Y1 = 1280, 45
    speed_car = 12
    roof_g_speed = 4
    roof_g_positions = [(490, -35), (80, -35), (225, -35)]
    roof_v_positions = [(1085, -68), (720, -68), (840, -68)]

    while running:
        screen.fill((150, 190, 100))

        screen.blit(imgtr, (xx, yy))
        screen.blit(imgtr, (X1, Y1))
        xx -= roof_g_speed
        X1 -= roof_g_speed
        # позиции для домиков (крыш) и дороги
        # Дополнительная позиция чтобы создать зацикленную анимацию

        # Проверка, выходит ли первая дорога за границы видимости
        if xx + imgtr.get_width() <= 0:
            xx = X1 + imgtr.get_width()
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

    pygame.display.update()