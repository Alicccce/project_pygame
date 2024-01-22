import pygame
from Alice import game_one
from Start_display import start
from game_two import game_two

def play():
    screen = pygame.display.set_mode((1300, 750))
    game_two(screen)

play()