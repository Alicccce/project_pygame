import pygame
from source.Start_display import start
from source.Alice import game_one


def play():
    screen = pygame.display.set_mode((1300, 750))
    game_one(screen)

play()