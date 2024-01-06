import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.small_size_rect_x = 20
        self.small_size_rect_y = 50
        self.xs = ['black', 'red']

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 0:
                    pygame.draw.rect(screen, 'white',
                                     (self.left + self.cell_size * j + self.small_size_rect_x * j,
                                      self.top + self.cell_size * i + self.small_size_rect_y * i,
                                      self.cell_size, self.cell_size), 1)
                    pygame.draw.rect(screen, 'white', (self.left + self.cell_size * j + self.small_size_rect_x * j - self.small_size_rect_x,
                                                       self.top + self.cell_size * i + self.small_size_rect_y * i,
                                                       self.small_size_rect_x, self.small_size_rect_y), 1)
                    # pygame.draw.rect(screen, self.xs[self.board[i][j]],
                    #                  (1 + self.left + self.cell_size * j, 1 + self.top + self.cell_size * i,
                    #                   self.cell_size - 2, self.cell_size - 2))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= self.left + self.cell_size * self.width and self.top <= y <= self.top + self.cell_size * self.height:
            col = (x - self.left) // self.cell_size
            row = (y - self.top) // self.cell_size
            return (row, col)

        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is not None:
            row, col = cell_coords
            if self.board[row][col] == 0:
                self.board[row][col] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


pygame.init()
size = 1300, 750
screen = pygame.display.set_mode(size)
board = Board(5, 4)
board.set_view(10, 10, 100)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            board.get_click(event.pos)
    board.render(screen)
    pygame.display.flip()

pygame.quit()
