import pygame
from pandas.core.common import flatten
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 100, 100)
LEVEL = {
    'Level 1': [
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0]
    ]
}


class Board:
    def __init__(self, cell_size_y, name, surf):
        self.width = 5
        self.height = 4
        self.board = copy.deepcopy(LEVEL[name])
        self.left = 10
        self.top = 10
        self.cell_size = cell_size_y  # размер больших квадратов
        self.small_size_rect_x = 50  # ширина узких квадратов
        self.small_size_rect_y = cell_size_y  # длин. узких квадратов
        self.row_spacing = 20  # Расстояние между строками
        self.xs = ['black', 'red']
        self.surf = surf

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        # screen.fill(BLACK)
        top_y = self.top
        for row_index, row in enumerate(self.board):
            top_x = self.left
            row_height = 0  # Высота текущей строки
            for col_index, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, WHITE, (top_x, top_y, self.small_size_rect_x, self.small_size_rect_y), 1)
                    top_x += self.small_size_rect_x
                    row_height = max(row_height, self.small_size_rect_y)
                else:
                    color = RED if cell == 5 else WHITE
                    pygame.draw.rect(screen, color, (top_x, top_y, self.cell_size, self.cell_size),
                                     1 if cell == 0 else 0)
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
                print(5)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def proov(self):
        arr = list(flatten(self.board))
        if 0 in arr:
            return False
        else:
            return True


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
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if y < mouse[1] < y + self.height and x < mouse[0] < x + self.width and click[0] == 1:
            pygame.draw.rect(self.surf, (self.act_color), (x, y, self.width, self.height))
            return 1
        else:
            pygame.draw.rect(self.surf, (self.inact_color), (x, y, self.width, self.height))


def restart(surf):
    game_one(surf)


def game_one(surf):
    pygame.init()
    running = True
    time_of_end = False
    board = Board(100, 'Level 1', surf)
    board.set_view(10, 10, 100)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()  # стартовое время в миллисекундах

    # Создаем кнопки один раз вне цикла
    button_done = Button(300, 600, 260, 50, RED, PINK, surf, 'done')
    ##button_retry = Button(500, 510, 260, 50, WHITE, 'не опять, а снова')

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
        text = font.render('{}:{}'.format(mins, secs), True, WHITE, BLACK)
        textRect = text.get_rect(center=(1000, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if secs < 15:
                    board.get_click(event.pos)

                    # board.proov()
                board.render(surf)

        # Рендеринг экрана и объектов
        surf.fill(BLACK)
        board.render(surf)
        surf.blit(text, textRect)

        if board.proov():
            time_of_end = secs
            Tab = pygame.font.SysFont('arial', 100)
            sc_Text = Tab.render('Yup', True, BLUE, WHITE)
            cOr = sc_Text.get_rect(center=(1000, 200))
            surf.blit(sc_Text, cOr)
        if millis // 1000 >= 15 and not board.proov():
            tab = pygame.font.SysFont('arial', 30)
            sc_text = tab.render('Вы нe успели! Попробуете выполнить задание заново?', True, WHITE, BLUE)
            cor = sc_text.get_rect(center=(1000, 200))
            surf.blit(sc_text, cor)
            if button_done.draw(surf, 500, 600) == 1:
                pygame.display.update()
                restart(surf)
            # button_retry.draw(surf)

        pygame.display.flip()
        clock.tick(60)  # Ограничить до 60 кадров в секунду

    pygame.quit()
