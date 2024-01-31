import pygame
import os
from source.main_game import Main_game


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
HEIGHT, WIDTH = 750, 1300
pygame.mixer.init()
sound_button = pygame.mixer.Sound("resource/sounds/molti_button.mp3")

def load_image(name, colorkey=None):
    fullname = os.path.join('resource/data', name)
    image = pygame.image.load(fullname)
    return image

class Button(pygame.sprite.Sprite):
    image = load_image('game_over.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Button.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 340

    def update(self, keys, surf):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_x, mouse_y) and click[0]:
            sound_button.play()
            Main_game(surf)
            pygame.quit()


def end(surf):
    pygame.init()
    pygame.font.init()
    running = True
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    FONT = pygame.font.SysFont("Roboto", 65)
    finished = FONT.render('Вы проехали все остановки и не попались!', True, BLACK)
    again = FONT.render('Нажмите на кнопку, если хотите сыграть ещё раз', True, BLACK)
    Button(all_sprites)
    imgtr = load_image('trop.png')
    imgg = load_image('roof_g.png')
    imgv = load_image('roof_v.png')
    roof_g_positions = [(490, -35), (80, -35), (225, -35)]
    roof_v_positions = [(1085, -68), (720, -68), (840, -68)]
    xx, yy = 0, 45

    for x, y in roof_g_positions:
        sprite = pygame.sprite.Sprite()
        sprite.image = imgg
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = x
        sprite.rect.y = y



    for x, y in roof_v_positions:
        sprite = pygame.sprite.Sprite()
        sprite.image = imgv
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = x
        sprite.rect.y = y
    sound = 0

    while running:
        if sound == 0:
            sound_button.play()
            sound += 1
        surf.fill((150, 190, 100))
        surf.blit(imgtr, (xx, yy))
        surf.blit(finished, (150, 215))
        surf.blit(again, (120, 545))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        all_sprites.draw(surf)
        all_sprites.update(keys, surf)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()



