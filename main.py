import pygame
import copy

FPS = 30

# RGB
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 1

grid = []

# вместо этого можно использовать генератор списков
for row in range(12):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(12):
        grid[row].append(0)  # Append a cell
#grid[5][4] = 1
grid[5][5] = 1
#grid[5][6] = 1
#grid[6][4] = 1
grid[6][6] = 1
grid[7][4] = 1
grid[7][5] = 1
grid[7][6] = 1 #
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
src = pygame.display.set_mode((255, 255))
pygame.display.set_caption('Game of life')
clock = pygame.time.Clock()
neighbours = {}

def life(pos):
    new_pos = copy.deepcopy(pos)
    for row in range(12):
        for column in range(12):
            if pos[row][column] == 1:
                if row + 1 >= len(pos):
                    if column + 1 >= len(pos[row]):
                        neighbours[(row, column)] = [pos[row-1][column-1], pos[row-1][column], pos[row-1][0],
                              pos[row][column-1], pos[row][0],
                              pos[0][column-1], pos[0][column], pos[0][0]]
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
                '''if neighbours[(row, column)].count(1) == 3 or neighbours[(row, column)].count(1) == 2:
                    return pos'''
                if neighbours[(row, column)].count(1) < 2:
                    new_pos[row][column] = 0
                elif neighbours[(row, column)].count(1) > 3:
                    new_pos[row][column] = 0
            else:
                if row + 1 >= len(pos):
                    if column + 1 >= len(pos[row]):
                        neighbours[(row, column)] = [pos[row-1][column-1], pos[row-1][column], pos[row-1][0],
                              pos[row][column-1], pos[row][0],
                              pos[0][column-1], pos[0][column], pos[0][0]]
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
                if neighbours[(row, column)].count(1) == 3:
                    new_pos[row][column] = 1
    return new_pos


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

    for row in range(12):
        for column in range(12):
            if grid[row][column] == 1:
                color = GREEN
                pygame.draw.rect(src, color,[(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
            elif grid[row][column] == 0:
                color = BLACK
                pygame.draw.rect(src, color, [(MARGIN + WIDTH) * column + MARGIN,
                                              (MARGIN + HEIGHT) * row + MARGIN,
                                              WIDTH,
                                              HEIGHT])
    grid = life(grid)

    pygame.display.flip()
pygame.quit()
