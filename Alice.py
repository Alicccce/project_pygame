import pygame
import numpy
from pandas.core.common import flatten
import os
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, text=''):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text

    def draw(self, sc, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width and click[0] == 1:
            pygame.draw.rect(screen, (self.act_color), self.rect)
            restart()
        else:
            pygame.draw.rect(screen, (self.inact_color), self.rect)
        font = pygame.font.Font(None, 40)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def check_and_append(event_pos):
    for x, y in checkpoints:
        if abs(x - event_pos[0]) <= 30 and abs(y - event_pos[1]) <= 30:
            check.add((x, y))
            break

def restart():
    global s, check, start_ticks
    s, check = [], set()
    start_ticks = pygame.time.get_ticks()
    drawing_surface.fill((0, 0, 0, 0))
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()

    running = True
    size = (1300, 750)
    image = load_image("itog.png")
    screen = pygame.display.set_mode(size)
    drawing_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  # стартовое время в миллисекундах
    # Создаем кнопки один раз вне цикла
    button_done = Button(300, 600, 260, 50, RED, PINK, 'начать снова')
    # Определите шрифт один раз вне цикла
    font = pygame.font.Font('freesansbold.ttf', 64)

    checkpoints = [(320, 87), (221, 262), (68, 432), (441, 423), (68, 267), (263, 185),
                   (458, 103), (197, 421), (35, 317), (497, 375), (420, 495)]
    s, check = [], set()

    while running:
        millis = pygame.time.get_ticks() - start_ticks
        secs = millis // 1000
        if secs >= 31:
            secs = 30
        mins = secs // 60
        secs %= 60

        text = font.render('{}:{}'.format(mins, secs), True, WHITE, BLACK)
        textRect = text.get_rect(center=(1000, 400))

        if millis // 1000 >= 30:
            if len(s) != 11:
                tab = pygame.font.SysFont('arial', 26)
                sc_text = tab.render('Не получилось :( Попробуете выполнить задание заново?', True, WHITE, BLUE)
                cor = sc_text.get_rect(center=(900, 250))
                screen.blit(sc_text, cor)
                if button_done.draw(screen, 500, 600) == 1:
                    pygame.display.update()
            else:
                tab = pygame.font.SysFont('arial', 26)
                sc_text = tab.render('Всё GOOD', True, WHITE, BLUE)
                cor = sc_text.get_rect(center=(900, 250))
                screen.blit(sc_text, cor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(drawing_surface, BLUE, event.pos, 7.5)
                    check_and_append(event.pos)

        for ch in check:
            for hc in checkpoints:
                if ch == hc and ch not in s:
                    s.append(ch)

        screen.blit(text, textRect)
        screen.blit(image, (0, 0))
        screen.blit(drawing_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()