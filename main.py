import pygame
# from Alice import game_one
# from Start_display import start
# from game_two import game_two
from main_game import Main_game
def play():
    screen = pygame.display.set_mode((1300, 750))
    Main_game(screen)

play()

