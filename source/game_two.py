import pygame
from source.functions import load_image


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
k = 3

pygame.mixer.init()
sound_button = pygame.mixer.Sound("resource/sounds/molti_button.mp3")
sound_end= pygame.mixer.Sound("resource/sounds/game_over_sound.mp3")


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, surf, text=''):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text
        self.surf = surf

    def draw(self, x, y, perem):
        global k
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width and perem == 1:
            pygame.draw.rect(self.surf, (self.act_color), self.rect)
            if click[0] == 1:
                k -= 1
                if k == 0:
                    sound_button.play()
                    game(self.surf)
                else:
                    sound_button.play()
                    restart(self.surf)
                return 1

        else:
            pygame.draw.rect(self.surf, (self.inact_color), self.rect)
        font = pygame.font.Font(None, 35)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surf.blit(text_surf, text_rect)


    def draw2(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width:
            pygame.draw.rect(self.surf, (self.act_color), self.rect)
            if click[0] == 1:
                sound_button.play()
                main(self.surf)
                return 2
        else:
            pygame.draw.rect(self.surf, (self.inact_color), self.rect)
        font = pygame.font.Font(None, 35)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surf.blit(text_surf, text_rect)


def main(surf):
    from source.main_game import Main_game
    Main_game(surf)





def check_and_append(event_pos, checkpoints, check):
    for x, y in checkpoints:
        if abs(x - event_pos[0]) <= 15 and abs(y - event_pos[1]) <= 15:
            check.add((x, y))
            break

def game(surf):
    from source.Start_display import start
    start(surf)

def restart(surf):
    game_two(surf)


def game_two(surf):
    global k
    pygame.init()

    running = True
    size = (1300, 750)
    image = load_image('itog.png')
    screen = surf
    drawing_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  # стартовое время в миллисекундах
    # Создаем кнопки один раз вне цикла
    button_done = Button(830, 600, 260, 50, RED, PINK, surf, 'ещё раз')
    button_doneliv = Button(830, 600, 260, 50, RED, PINK, surf, 'вернуться')
    button_contin = Button(830, 600, 260, 50, RED, PINK, surf, 'едем дальше')
    # Определите шрифт один раз вне цикла
    font = pygame.font.Font('freesansbold.ttf', 64)

    checkpoints = [(320, 87), (221, 262), (68, 432), (441, 423), (68, 267), (263, 185), (458, 103), (197, 421),
                   (35, 317),
                   (497, 375), (420, 495)]
    s, check = [], set()
    heart_xs = ['hert3.png', 'hert2.png', 'hert.png']
    heart_img = load_image(heart_xs[k-1])
    time_stop = 20
    time_of_end = 0
    freeze_timer = False  # Flag to control frozen timer

    while running:
        screen.fill((100, 150, 50))
        screen.blit(heart_img, (1165, 5))
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

        if millis // 1000 >= time_stop:
            if len(s) != 11:
                if k == 0:
                    tab = pygame.font.SysFont('arial', 26)
                    sc_text = tab.render('Вы потратили все жизни и проиграли.. Начните заново !', True, WHITE, BLUE)
                    screen.blit(sc_text, (640, 320))
                    button_doneliv.draw(830, 600, 1)
                else:
                    tab = pygame.font.SysFont('arial', 26)
                    sc_text = tab.render('Не получилось :( Попробуете выполнить задание заново?', True, WHITE, BLUE)
                    screen.blit(sc_text, (640, 320))
                    button_done.draw(830, 600, 1)

        if len(s) == 11 and freeze_timer:
            time_of_end = secs
            freeze_timer = True
            tab = pygame.font.SysFont('arial', 26)
            sc_text = tab.render('Вам удалось закрасить все необходимые места!', True, BLUE, WHITE)
            screen.blit(sc_text, (640, 320))
            if button_contin.draw2(830, 600) == 2:
                pygame.display.update()

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
        textRect = text.get_rect(center=(900, 250))

        screen.blit(text, textRect)
        screen.blit(image, (0, 0))
        screen.blit(drawing_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()

