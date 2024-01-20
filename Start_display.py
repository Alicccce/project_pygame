import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
HEIGHT, WIDTH = 750, 1300


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image

class Button(pygame.sprite.Sprite):
    image = load_image("start.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(*group)
        self.image = Button.image
        self.rect = self.image.get_rect()
        self.rect.x = 480
        self.rect.y = 350
        self.mask_bus = pygame.mask.from_surface(self.image)

    def update(self, keys):
        pass

def load(surf):
    pygame.init()
    pygame.font.init()
    running = True
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("Roboto", 80)
    finished = FONT.render("Смурфики", True, "white")
    finished_rect = finished.get_rect(center=(640, 280))
    Button(all_sprites)
    imgtr = load_image('trop.png')
    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    roof_g_positions = [(490, -35), (80, -35), (225, -35)]
    roof_v_positions = [(1085, -68), (720, -68), (840, -68)]
    xx, yy = 0, 45
    for x,y in roof_g_positions:
        sprite = pygame.sprite.Sprite()
        sprite.image = imgg
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = x
        sprite.rect.y = y
    for x,y in roof_v_positions:
        sprite = pygame.sprite.Sprite()
        sprite.image = imgv
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = x
        sprite.rect.y = y



    while running:
        surf.fill((150, 190, 100))
        screen.blit(imgtr, (xx, yy))






        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        all_sprites.draw(surf)
        all_sprites.update(keys)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


screen = pygame.display.set_mode((1300, 750))
load(screen)
