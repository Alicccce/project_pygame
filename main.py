import pygame
from source.Start_display import start
# from source.Alice import game_one
# from source.game_two import game_two
# from source.load_img import load

def play():
    screen = pygame.display.set_mode((1300, 750))
    start(screen)

play()