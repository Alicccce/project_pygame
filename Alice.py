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
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bus.image
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 220
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y + 14 >= 0:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.y + 111 <= 750:
            self.rect.y += 5


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

    running = True

    object_speed = 5



    while running:
        screen.fill(BLACK)

        keys = pygame.key.get_pressed()
        all_sprites.update(keys)
        all_sprites.draw(screen)






        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()
