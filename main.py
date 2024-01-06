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
        self.small_size_rect_x = 30  # ширина узких квадратов
        self.small_size_rect_y = cell_size_y  # длин. узких квадратов
        self.stroka = 2 #проверка на какой строчке находится рендж в создании сетки
        self.xs = ['black', 'red']

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill((0, 0, 0))
        for i in self.board:
            self.stroka += 1
            top_x = self.left
            top_y = self.top + self.cell_size * self.stroka
            for j in i:
                if j == 1:
                    pygame.draw.rect(screen, 'white', (top_x, top_y, self.small_size_rect_x, self.small_size_rect_y), 1)
                    top_x += self.small_size_rect_x
                else:
                    pygame.draw.rect(screen, 'white', (top_x, top_y, self.cell_size, self.cell_size), 1)
                    top_x += self.cell_size

    # def get_cell(self, mouse_pos):
    #     x, y = mouse_pos
    #     if self.left <= x <= self.left + self.cell_size * self.width and self.top <= y <= self.top + self.cell_size * self.height:
    #         col = (x - self.left) // self.cell_size
    #         row = (y - self.top) // self.cell_size
    #         return (row, col)
    #
    #     else:
    #         return None
    #
    # def on_click(self, cell_coords):
    #     if cell_coords is not None:
    #         row, col = cell_coords
    #         if self.board[row][col] == 0:
    #             self.board[row][col] = 1
    #
    # def get_click(self, mouse_pos):
    #     cell = self.get_cell(mouse_pos)
    #     self.on_click(cell)


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
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     board.get_click(event.pos)
    board.render(screen)
    pygame.display.flip()

pygame.quit()
