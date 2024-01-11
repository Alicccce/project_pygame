import pygame
import os
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
HEIGHT = 750
WIDTH = 1300


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
        super().__init__(*group)
        self.image = Bus.image
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 220
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y + 14 >= 80:
            self.rect.y -= 6
        if keys[pygame.K_s] and self.rect.y + 111 <= 730:
            self.rect.y += 6


class Object(pygame.sprite.Sprite):
    image = load_image("bus_osn.png")  # Замените "your_object_image.png" на изображение вашего объекта

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Object.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH + 10, WIDTH + 200)  # Генерация за пределами поля
        self.rect.y = random.randint(0, HEIGHT - 125)
        self.mask = pygame.mask.from_surface(self.image)

    def updates(self, speed):
        self.rect.x -= speed
        if self.rect.x + self.rect.width < 0:
            self.kill()


if __name__ == '__main__':
    pygame.init()
    size = (1300, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()


    all_sprites = pygame.sprite.Group()
    Bus(all_sprites)

    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    imtr = load_image('trop.png')

    running = True

    x, y = 0, 45
    x1, y1 = 1280, 45
    roof_g_speed = 4

    roof_g_positions = [(490, -35), (80, -35),(225, -35)]
    roof_v_positions = [(1085, -68), (720, -68), (840, -68)]

    while running:
        screen.fill((150, 190, 100))

        screen.blit(imtr, (x, y))
        screen.blit(imtr, (x1, y1))
        x -= roof_g_speed
        x1 -= roof_g_speed

        # позиции для домиков
          # Дополнительная позиция чтобы создать зацикленную анимацию

        # Проверка, выходит ли первая дорога за границы видимости
        if x + imtr.get_width() <= 0:
            x = x1 + imtr.get_width()

        # Проверка, выходит ли вторая дорога за границы видимости
        if x1 + imtr.get_width() <= 0:
            x1 = x + imtr.get_width()
        for position in roof_g_positions:
            screen.blit(imgg, position)
        for position in roof_v_positions:
            screen.blit(imgv, position)

            # Движение домиков "roof_g"
        roof_g_positions = [(x - roof_g_speed, y) for x, y in roof_g_positions]
        # При достижении края экрана, перемещаем домик в конец очереди для создания непрерывной ленты
        roof_g_positions = [((WIDTH, y) if x - 35 < -imgg.get_width() -100 else (x, y)) for x, y in roof_g_positions]


        roof_v_positions = [(x - roof_g_speed, y) for x, y in roof_v_positions]
        # Делаем то же для "roof_v"
        roof_v_positions = [((WIDTH,y) if x < - imgv.get_width() - 100 else (x, y)) for x, y in roof_v_positions]

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        all_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # for i in range(3):
        #     screen.blit(imgg, (i * 140, -35))
        # screen.blit(imgv, (420, -68))
        # for i in range(4):
        #     screen.blit(imgg, (525 + i * 140, -35))
        # screen.blit(imgv, (1085, -68))
        # screen.blit(imgg, (1191, -35))

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()
