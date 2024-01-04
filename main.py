import pygame



pygame.init()
width, height = 600, 800
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)