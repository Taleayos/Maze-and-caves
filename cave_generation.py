import numpy as np


def cave_step_1(matrix1, birth, death):
    """ Функция для генерации пещер с использованием клеточного автомата

Правила: Если «живые» клетки окружены «живыми» клетками, количество которых меньше, чем предел «смерти», они «умирают».
Аналогично если «мертвые» клетки находятся рядом с «живыми», количество которых больше, чем предел «рождения», они становятся «живыми».

    :param matrix1: инициализированный лабиринт пещер
    :param birth: количество для рождение «мертвых» клеток (предел «рождения»)
    :param death: количество для уничтожение «живых» клеток (предел «смерти»)

    :return: лабиринт пещер на следующем шаге
    """
    h, w = matrix1.shape
    new_matrix = matrix1.copy()
    for i in range(h):
        for j in range(w):
            if matrix1[i, j] == 1 and count_cells_1(matrix1, i, j) < death:
                new_matrix[i][j] = 0
            elif matrix1[i, j] == 0 and count_cells_1(matrix1, i, j) > birth:
                new_matrix[i][j] = 1

    return new_matrix

def count_cells_1(matrix1, i, j):
    """ Функция для подсчета живых клеток вокруг текущей пещеры/клетки

    :param matrix1: инициализированный лабиринт пещер
    :param i: индекс текущей клетки
    :param j: индекс текущей клетки
    :return: количество живых клеток
    """
    count_cell = 0
    live_cell = 0
    w, h = matrix1.shape
    dx = (-1, 0, 1, 0, -1, 1, -1, 1)
    dy = (0, 1, 0, -1, -1, 1, 1, -1)
    for k in range(len(dx)):
        if w > i + dx[k] >= 0 and h > j + dy[k] >= 0:
            if matrix1[i + dx[k]][j + dy[k]] == 1:  # death
                count_cell += 1
        else:
            count_cell += 1
        live_cell = count_cell
    return live_cell


def cave_generatuion_1(rows, cols, ap):
    """ Функция для генерации лабиринта пещер

    :param rows: количество строк в лабиринте
    :param cols: количество столбцов в лабиринте
    :param ap: количество(%) живых клеток при начальной инициализации
    :return: сгенерированный лабиринт пещер
    """
    p1 = ap * 0.01
    p0 = 1 - p1
    cave = np.random.choice([0, 1], size=(rows, cols), p=[p0, p1])
    return cave