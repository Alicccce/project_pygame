import pygame
from source.Start_display import start



def play():
    screen = pygame.display.set_mode((1300, 750))
    start(screen)

play()