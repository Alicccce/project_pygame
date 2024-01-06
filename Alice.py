import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LEVEL = {'Level 1': [[0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0]]

         }


class Board:
    def __init__(self, cell_size_y, name):
        self.width = 5
        self.height = 4
        self.board = LEVEL[name]
        self.left = 10
        self.top = 10
        self.cell_size = cell_size_y  # размер больших квадратов
        self.small_size_rect_x = 50  # ширина узких квадратов
        self.small_size_rect_y = cell_size_y  # длин. узких квадратов
        self.row_spacing = 20  # Расстояние между строками
        self.xs = ['black', 'red']

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill(BLACK)
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


pygame.init()
size = 1300, 750
screen = pygame.display.set_mode(size)
board = Board(100, 'Level 1')
board.set_view(10, 10, 100)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            board.get_click(event.pos)
    board.render(screen)
    pygame.display.flip()

pygame.quit()
