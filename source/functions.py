import os
import sys
import pygame

def load_image(name, colorkey=None):
    fullname = os.path.join('resource/data', name)
    # если файл не существцует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image