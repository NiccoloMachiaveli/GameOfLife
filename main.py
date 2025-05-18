import pygame
import copy

FPS = 30

# RGB
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 20
HEIGHT = 20
SIZE = 12

MARGIN = 1

grid = []

for row in range(SIZE):
    grid.append([])
    for column in range(SIZE):
        grid[row].append(0)

grid[5][5] = 1
grid[6][6] = 1
grid[7][4] = 1
grid[7][5] = 1
grid[7][6] = 1

pygame.init()
pygame.mixer.init()
src = pygame.display.set_mode((255, 255))
pygame.display.set_caption('Game of life')
clock = pygame.time.Clock()
neighbours = {}


def defining_neighbors(pos, row, column):
    if row + 1 >= len(pos):
        if column + 1 >= len(pos[row]):
            neighbours[(row, column)] = [pos[row - 1][column - 1], pos[row - 1][column], pos[row - 1][0],
                                         pos[row][column - 1], pos[row][0],
                                         pos[0][column - 1], pos[0][column], pos[0][0]]
        else:
            neighbours[(row, column)] = [pos[row - 1][column - 1], pos[row - 1][column], pos[row - 1][column + 1],
                                         pos[row][column - 1], pos[row][column + 1],
                                         pos[0][column - 1], pos[0][column], pos[0][column + 1]]
    elif column + 1 >= len(pos):
        neighbours[(row, column)] = [pos[row - 1][column - 1], pos[row - 1][column], pos[row - 1][0],
                                     pos[row][column - 1], pos[row][0],
                                     pos[row + 1][column - 1], pos[row + 1][column], pos[row + 1][0]]
    else:
        neighbours[(row, column)] = [pos[row - 1][column - 1], pos[row - 1][column], pos[row - 1][column + 1],
                                     pos[row][column - 1], pos[row][column + 1],
                                     pos[row + 1][column - 1], pos[row + 1][column], pos[row + 1][column + 1]]


def life(pos):
    new_pos = copy.deepcopy(pos)
    for row in range(SIZE):
        for column in range(SIZE):
            if pos[row][column] == 1:
                defining_neighbors(pos, row, column)
                if neighbours[(row, column)].count(1) < 2:
                    new_pos[row][column] = 0
                elif neighbours[(row, column)].count(1) > 3:
                    new_pos[row][column] = 0
            else:
                defining_neighbors(pos, row, column)
                if neighbours[(row, column)].count(1) == 3:
                    new_pos[row][column] = 1
    return new_pos


def drawing(color):
    pygame.draw.rect(src, color, [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])


run = True
while run:
    # держим цикл на правильной скорости
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            print(life(grid))
            run = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            my_pos = e.pos
            column = my_pos[0] // (WIDTH + MARGIN)
            row = my_pos[1] // (HEIGHT + MARGIN)
            grid[row][column] = 1

    for row in range(SIZE):
        for column in range(SIZE):
            if grid[row][column] == 1:
                drawing(GREEN)
            elif grid[row][column] == 0:
                drawing(BLACK)
    grid = life(grid)

    pygame.display.flip()
pygame.quit()
