import pygame
import os
import sys
from random import *
from load_img import load

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 100, 100)
LIGHT_GREEN = (100, 200, 100)
HEIGHT, WIDTH = 750, 1300
col_stat = choice([4, 9, 7, 5])
speed_car = 14

pygame.mixer.init()
sound_boom = pygame.mixer.Sound("sounds/avaria2.ogg")
sound_button = pygame.mixer.Sound("sounds/molti_button.mp3")
# pygame.mixer.music.load('sounds/fon_mus.mp3')
pygame.mixer.music.load('sounds/super_musick.mp3')

sprts_cars = pygame.sprite.Group()  # группа спрайтов машинок
all_sprites = pygame.sprite.Group()


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


def smena(x, y, surf):  # функция вывода "окончания" основной игры
    buyt = Button(500, 600, 260, 50, GREEN, LIGHT_GREEN, surf, 'играть')
    buyt.draw(500, 600)
    tab = pygame.font.SysFont('arial', 26)
    sc_text = tab.render('Авария! Вы проиграли. Попробуете снова?', True, BLACK, (90, 200, 70))
    surf.blit(sc_text, (430, 500))
    s = pygame.transform.scale(load_image('yup.jpg'), (200, 200))
    surf.blit(s, (530, 250))
    bu = pygame.transform.scale(load_image('boo.png'), (200, 200))  # картинка взрыва
    surf.blit(bu, (x - 70, y - 50))


def restart(surf):
    global speed_car
    speed_car = 12
    Main_game(surf)


def over(surf):
    from End_display import end
    end(surf)


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, surf, text=''):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text
        self.surf = surf

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width:
            pygame.draw.rect(self.surf, (self.act_color), self.rect)
            if click[0] == 1:
                sound_button.play()
                restart(self.surf)
        else:
            pygame.draw.rect(self.surf, (self.inact_color), self.rect)
        font = pygame.font.Font(None, 35)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surf.blit(text_surf, text_rect)


class Bus(pygame.sprite.Sprite):
    image = load_image('bus_osn.png')

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(*group)
        self.image = Bus.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT // 2 + 15
        self.mask_bus = pygame.mask.from_surface(self.image)

    def update(self, keys, surf):
        # ниже контроль движения автобуса
        if keys[pygame.K_w] and self.rect.y + 14 >= 85 and speed_car != 0:
            self.rect.y -= 6
        if keys[pygame.K_s] and self.rect.y + 111 <= 728 and speed_car != 0:
            self.rect.y += 6


class Cars(pygame.sprite.Sprite):
    def __init__(self, all_sprites, name, ox_per, for_x, l):  # name = ('png', (x, y))
        super().__init__(all_sprites)
        self.ox_per, self.l = ox_per, l
        self.image = load_image(name[0])  # считываем назвнаие
        self.rect = self.image.get_rect()
        self.rect.x = name[1][0]  # считаваем абциссу
        self.rect.y = name[1][1]  # считаваем ординату
        self.mask_car = pygame.mask.from_surface(self.image)
        self.add(sprts_cars)  # добавление текущей машинки в список спрайтов
        self.forx = for_x
        self.forx.append(self.rect.x)# добавление "использованной" координаты х для машинки
        self.boom = 0

    def update(self, speed, bus):
        global speed_car, col_stat
        cor_y = [90, 200, 310, 420, 530, 640]
        self.rect.x -= speed_car
        p = choice(self.ox_per)  # выбор абциссы старта машинки при достижении левой границы
        if pygame.sprite.collide_mask(self, bus):  # если машинки сталкнулись
            if self.boom == 0:
                sound_boom.play()
                self.boom += 1
            smena(self.rect.x, self.rect.y, screen)
            speed_car = 0
        # далее проверяется то, когда машинки заезжают за стену
        if self.rect.x + self.rect.width < 0 and p not in self.forx:
            self.rect.x = (p)
            self.rect.y = choice(cor_y)
            if len(self.ox_per) == self.l:
                if col_stat >= 1:
                    col_stat -= 1
                else:
                    over(screen)
                    pygame.mixer.music.stop()
                pygame.mixer.music.stop()
                load(screen)
                pygame.quit()
            self.forx.append(self.rect.x)
            self.ox_per.remove(self.rect.x)


def Main_game(surf):
    global screen, speed_car
    pygame.display.flip()
    pygame.mixer.music.play()


    for_x = []  # список "занятых" абцисс машинок
    ox = 0
    ox = [i for i in range(WIDTH + 10, WIDTH + 5001, 150)]  # ось ох (координата машинки),
    # которая генерирется и появляется на n_ом расстоянии от осн. экрана

    sprts_cars = pygame.sprite.Group()  # группа спрайтов машинок
    all_sprites = pygame.sprite.Group()

    pygame.init()
    screen = surf
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    bus = Bus(all_sprites)
    l = choice([3, 14, 9])

    cor_y = [90, 200, 310, 420, 530, 640]  # список ординат для полос дороги
    x1, x2 = ox_operations(ox)[0], ox_operations(ox)[0]
    x3, x4 = ox_operations(ox)[0], ox_operations(ox)[0]
    x5, x6 = ox_operations(ox)[0], ox_operations(ox)[0]
    for name in [('red_car.png', (x1, choice(cor_y))),
                 ('yel_car.png', (x2, choice(cor_y))),
                 ('gray_car.png', (x3, choice(cor_y))),
                 ('black_car.png', (x4, choice(cor_y))),
                 ('purp_car.png', (x5, choice(cor_y))),
                 ('white_car.png', (x6, choice(cor_y)))]:
        Cars(all_sprites, name, ox, for_x, l)  # передаём в name имя файла и координаты запуска

    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    imgtr = load_image('trop.png')

    running = True

    xx, yy = 0, 45  # координаты расположения изображения дороги
    X1, Y1 = 1280, 45
    roof_g_speed = 5
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
        all_sprites.update(keys, bus)
        all_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.display.update()