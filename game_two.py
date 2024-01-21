import pygame
import os
import sys

def main(surf):
    from main_game import Main_game
    Main_game(surf)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
k = 0


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, surf, text=''):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text
        self.surf = surf

    def draw(self, win, x, y):
        global k
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width and click[0] == 1:
            pygame.draw.rect(self.surf, (self.act_color), (x, y, self.width, self.height))
            restart(self.surf)
            k += 1

        else:
            pygame.draw.rect(self.surf, (self.inact_color), (x, y, self.width, self.height))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def check_and_append(event_pos, checkpoints, check):
    for x, y in checkpoints:
        if abs(x - event_pos[0]) <= 30 and abs(y - event_pos[1]) <= 30:
            check.add((x, y))
            break


def restart(surf):
    game_two(surf)


def game_two(surf):
    global k
    pygame.init()

    running = True
    size = (1300, 750)
    image = load_image("itog.png")
    screen = surf
    drawing_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  # стартовое время в миллисекундах
    # Создаем кнопки один раз вне цикла
    button_done = Button(300, 600, 260, 50, RED, PINK, surf, 'done')
    # Определите шрифт один раз вне цикла
    font = pygame.font.Font('freesansbold.ttf', 64)

    checkpoints = [(320, 87), (221, 262), (68, 432), (441, 423), (68, 267), (263, 185), (458, 103), (197, 421),
                   (35, 317),
                   (497, 375), (420, 495)]
    s = []
    check = set()

    time_stop = 20
    time_of_end = 0
    freeze_timer = False  # Flag to control frozen timer

    while running:
        screen.fill((100, 150, 50))
        millis = pygame.time.get_ticks() - start_ticks
        secs = millis // 1000
        if secs >= time_stop + 1:
            secs = time_stop
        if len(s) == 11:
            if not freeze_timer:  # Freeze the timer only once
                freeze_timer = True
                time_of_end = secs

            secs = time_of_end

        mins = secs // 60
        secs %= 60

        # text = font.render('{}:{}'.format(mins, secs), True, WHITE, BLACK)
        # textRect = text.get_rect(center=(1000, 400))

        if millis // 1000 >= time_stop:
            if len(s) != 11:
                tab = pygame.font.SysFont('arial', 26)
                sc_text = tab.render('Не получилось :( Попробуете выполнить задание заново?', True, WHITE, BLUE)
                cor = sc_text.get_rect(center=(900, 250))
                screen.blit(sc_text, cor)
                print(k)
                if button_done.draw(screen, 500, 600) == 1:
                    pygame.display.update()
                else:
                    main(surf)

        if len(s) == 11 and freeze_timer:
            time_of_end = secs
            freeze_timer = True
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
                if pygame.mouse.get_pressed()[0] and (millis // 1000 < time_stop and len(s) != 11):
                    pygame.draw.circle(drawing_surface, BLUE, event.pos, 7.5)
                    check_and_append(event.pos, checkpoints, check)

        for ch in check:
            for hc in checkpoints:
                if ch == hc and ch not in s:
                    s.append(ch)

        # Render the new timer text
        text = font.render('{}:{}'.format(mins, secs), True, WHITE)
        textRect = text.get_rect(center=(1000, 400))

        screen.blit(text, textRect)
        screen.blit(image, (0, 0))
        screen.blit(drawing_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()