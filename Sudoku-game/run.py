# for nice user interface
import pygame
from sudoku import solveSudoko as solve
from sudoku import notPresentInRow,notPresentInCol,notPresentInSquare

import time
pygame.font.init()


def valid(board,key,pos):
    a = notPresentInRow(board,pos[0],pos[1],key)
    b = notPresentInCol(board,pos[0],pos[1],key)
    c = notPresentInSquare(board,pos[0],pos[1],key)

    if a and b and c:
        return True

    return False

    
class Grid:

    # an example taken from websudoko.com 
    board = [
        [0, 0, 0, 0, 0, 0, 4, 7, 0],
        [9, 3, 0, 0, 2, 4, 0, 5, 6],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [5, 0, 6, 0, 9, 0, 0, 1, 0],
        [3, 2, 0, 0, 6, 0, 0, 9, 7],
        [0, 7, 0, 0, 5, 0, 6, 0, 2],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [7, 9, 0, 2, 1, 0, 0, 3, 4],
        [0, 1, 2, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Box(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0),
                             (i * gap, self.height), thick)

        # sketching boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_completed(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0: # filled but not confirmed
            text = fnt.render(str(self.temp), 1, (235, 145, 0))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0): # filled value is set
            text = fnt.render(str(self.value), 1, (253, 253, 68))
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                            y + (gap/2 - text.get_height()/2)))

        if self.selected: # selected box
            pygame.draw.rect(win, (40, 40, 212), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((9, 227, 202)) # setting background color

    # Show time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time:" + format_time(time), 1, (0, 128, 0))
    win.blit(text, (400, 620))

    # Show wrong moves
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 620))

    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    mat = "" + str(minute) + "m " + str(sec) + "s"
    return mat


def game():
    
    # main window
    win = pygame.display.set_mode((600, 680)) # it is game surface
    pygame.display.set_caption("Sudoku by Piyush")

    programIcon = pygame.image.load('icon.png')
    pygame.display.set_icon(programIcon)

    board = Grid(9, 9, 600, 600)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_completed():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


game()
pygame.quit()
