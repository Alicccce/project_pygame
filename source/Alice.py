import random
import pygame
from pandas.core.common import flatten
import copy
from source.functions import load_image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
LEVEL = {
    'Level 1': [
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0]
    ],
    'Level 2': [
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 1]

    ],
    'Level 3': [
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 1]
    ]
}  # 0 - места, которые нужно занять, 1 - разделения
pygame.mixer.init()
sound_button = pygame.mixer.Sound("resource/sounds/molti_button.mp3")
chair_xs_img = ['qub.png', 'red_qub.png']


class Board:
    def __init__(self, cell_size_y, name, surf):
        self.width, self.height = 5, 4
        self.board = copy.deepcopy(LEVEL[name])
        self.left, self.top = 10, 10
        self.cell_size = cell_size_y  # размер больших квадратов
        self.small_size_rect_x = 50  # ширина узких квадратов
        self.small_size_rect_y = cell_size_y  # длина узких квадратов
        self.row_spacing = 20  # Расстояние между строками
        self.xs = ['black', 'red']
        self.surf = surf

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        top_y = self.top
        for row_index, row in enumerate(self.board):
            top_x = self.left
            row_height = 0  # Высота текущей строки
            for col_index, cell in enumerate(row):
                if cell == 1:
                    # pygame.draw.rect(screen, WHITE, (top_x, top_y, self.small_size_rect_x, self.small_size_rect_y), 1)
                    top_x += self.small_size_rect_x
                    row_height = max(row_height, self.small_size_rect_y)
                else:
                    if cell == 0:
                        image = load_image(chair_xs_img[0])
                    elif cell == 5:
                        image = load_image(chair_xs_img[1])
                    screen.blit(image, (top_x, top_y))
                    top_x += self.cell_size
                    row_height = max(row_height, self.cell_size)
            top_y += row_height + self.row_spacing

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        top_y = self.top

        for row_index, row in enumerate(self.board):
            top_x = self.left
            row_height = 0

            # Определяем высоту строки, чтобы использовать ее позже для проверки попадания
            for cell in row:
                if cell == 1:
                    row_height = max(row_height, self.small_size_rect_y)
                else:
                    row_height = max(row_height, self.cell_size)

            # Проверяем попадание в ячейки текущей строки
            for col_index, cell in enumerate(row):
                cell_width = self.small_size_rect_x if cell == 1 else self.cell_size
                if top_x <= x < top_x + cell_width and top_y <= y < top_y + row_height:
                    return (row_index, col_index)
                top_x += cell_width

            # Переходим к следующей строке, учитывая промежуток между строками
            top_y += row_height + self.row_spacing
        return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            row, col = cell_coords
            if self.board[row][col] == 0:
                self.board[row][col] = 5

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def proov(self):  # метод, проверяющией закрашены ли все квадраты
        arr = list(flatten(self.board))
        if 0 in arr:
            return False
        else:
            return True


class Button:
    def __init__(self, x, y, width, height, act_color, inact_color, surf, text=''):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.act_color = act_color
        self.inact_color = inact_color
        self.text = text
        self.surf = surf

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


def restart(surf):
    game_one(surf)


def main(surf):
    from source.main_game import Main_game
    Main_game(surf)


def game_one(surf):
    pygame.init()
    running = True
    time_of_end = False
    a = random.choice(['Level 1', 'Level 2', 'Level 3'])
    board = Board(100, a, surf)
    board.set_view(35, 70, 100)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  # стартовое время в миллисекундах
    img_good_end = load_image('bus_good.png')
    img_bad_end = load_image('bus_bad.png')

    # Создаем кнопки один раз вне цикла
    button_done = Button(975, 650, 260, 50, RED, PINK, surf, 'не опять, а снова')
    button_contin = Button(975, 650, 260, 50, RED, PINK, surf, 'едем дальше')

    # Определите шрифт один раз вне цикла
    font = pygame.font.Font('freesansbold.ttf', 64)



    while running:

        millis = pygame.time.get_ticks() - start_ticks
        secs = millis // 1000
        if secs >= 16:
            secs = 15
        if board.proov():
            secs = time_of_end
        mins = secs // 60
        secs %= 60

        # Обновляем текст один раз на каждый тик
        text = font.render('{}:{}'.format(mins, secs), True, WHITE, (100, 100, 100))
        textRect = text.get_rect(center=(1100, 280))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if secs < 15:
                    board.get_click(event.pos)


                board.render(surf)


        # Рендеринг экрана и объектов
        surf.fill((100, 100, 100))
        surf.blit(load_image('bus_bus.png'), (5, 5))
        board.render(surf)
        surf.blit(text, textRect)

        if board.proov():
            time_of_end = secs
            surf.blit(img_good_end, (915, 350))
            if button_contin.draw2(970, 650) == 2:
                pygame.display.update()
                # СНОВА К АВТОБУСУ
        if millis // 1000 >= 15 and not board.proov():
            surf.blit(img_bad_end, (915, 350))
            if button_done.draw2(970, 650) == 2:
                pygame.display.update()

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()
