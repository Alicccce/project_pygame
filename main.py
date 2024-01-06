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
        self.left = 20
        self.top = 20
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, WHITE, (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        self.t = (str(x), str(y))
        if self.left < x < (self.cell_size * 29) + self.left and self.top < y < (self.cell_size * 20) + self.top:
            self.on_click(self.t)

    def on_click(self, cell_coords):
        x1, y1 = int(cell_coords[0]), int(cell_coords[1])
        x2 = (x1 - self.left) // (self.cell_size)
        y2 = (y1 - self.top) // (self.cell_size)
        self.pood(x2, y2)

    def pood(self, x2, y2):
        if self.board[y2][x2] == 0:
            pygame.draw.rect(screen, RED, (self.left + self.cell_size * x2, self.top + self.cell_size * y2, self.cell_size, self.cell_size))
            self.board[y2][x2] = 1
        elif self.board[y2][x2] == 1:
            pygame.draw.rect(screen, BLUE, (self.left + self.cell_size * x2, self.top + self.cell_size * y2, self.cell_size, self.cell_size))
            self.board[y2][x2] = 2
        elif self.board[y2][x2] == 2:
            pygame.draw.rect(screen, BLACK, (self.left + self.cell_size * x2, self.top + self.cell_size * y2, self.cell_size, self.cell_size))
            self.board[y2][x2] = 0

    def get_click(self, mouse_pos):
        self.get_cell(mouse_pos)


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


if __name__ == '__main__':
    pygame.init()
    #board = Board(29, 20)
    running = True
    size = wid, heigh = 1300, 750
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    secs, mins, k = 0, 0, 0
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render('{}:{}'.format(mins, secs), True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect(center=(600, 400))
    clock = pygame.time.Clock()

    while running:
        #m = True
        clock.tick(1)
        secs += 1
        screen.blit(text, textRect)
        score = pygame.time.get_ticks() // 1000
        if score == 17:
            secs = 0
        if 0 <= k <= 15:
            k += 1
            if k == 16:
                k += 1
            else:
                text = font.render('{}:{}'.format(mins, secs), True, (255, 255, 255), (0, 0, 0))
        if k == 17:
            tab = pygame.font.SysFont('arial', 50)
            sc_text = tab.render('Вы не успели! Попробуете выполнить задание заново?', 1, WHITE, BLUE)
            pos = sc_text.get_rect(center=(600, 290))
            screen.blit(sc_text, pos)

            button = Button(500, 510, 260, 50, (255, 255, 255), 'не опять, а снова')
            button.draw(screen)


        for event in pygame.event.get():
            button = Button(500, 510, 260, 50, (255, 255, 255), 'не опять, а снова')
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.x <= event.pos[0] <= button.width + button.x and \
                        button.y <= event.pos[1] <= button.y + button.height:
                    running = True

            #if event.type == pygame.MOUSEBUTTONDOWN:
             #   board.get_click(event.pos)
        #board.render(screen)
        pygame.display.flip()