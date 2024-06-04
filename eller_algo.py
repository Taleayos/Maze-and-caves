import random

import numpy as np


def generate_maze(rows, cols, q=None):
    """
    Функция генерации лабиринта по заданным параметрам.
    В основе реализации аглоритм Эллера - математический генератор лабиринтов,
    в которых между каждыми двумя точками существует единственный путь, то есть лабиринтов без циклов.
    Организован как цикл добавления новых строк. Строка содержит одно и то же количество ячеек,
    которое произвольно задаётся в начале.
    Клетки относятся к множествам, которые служат для контроля возможности прохода между ячейками.
    На момент генерации текущей строки клетки одного множества соединены между собой,
    одновременно клетки из разных множеств находятся в изолированных между собой частях лабиринта.
    В общем, стенки лабиринта генерируются случайным образом, но при соблюдении определённых правил,
    которые гарантируют отсутствие зацикливаний.

    :param rows: (int) количество строк в лабиринте
    :param cols: (int) количество столбцов в лабиринте
    :param q: (list) список значений ячеек (0 или 1) для первоначальной инициализации матрицы лабиринта.
    Значение по умолчанию - None, для рандомной инициалтзации ячеек

    :return: np.matrix1 - матрица значений ячеек, которые имеют (1) или не имеют (0) правую стенку,
            np.matrix2 - матрица значений ячеек, которые имеют (1) или не имеют (0) нижнюю стенку
    """
    rarr, barr = [], []

    sets, right, bottom = [0] * cols, [1] * cols, [0] * cols

    counter = 1
    for i in range(rows):
        for j in range(cols):
            if bottom[j] == 1:
                sets[j] = 0

            if sets[j] == 0:
                sets[j] = counter
                counter += 1

            right[j], bottom[j] = 1, 0

        for j in range(cols - 1):
            v = random.randint(0, 1) if not q else q.pop(0)
            if v == 0 and sets[j] != sets[j + 1]:
                right[j] = 0
                s = sets[j + 1]
                for k in range(cols):
                    if sets[k] == s:
                        sets[k] = sets[j]

        for j in range(cols):
            h = random.randint(0, 1) if not q else q.pop(0)
            if h == 1 and len([bottom[k] for k in range(cols) if sets[k] == sets[j] and bottom[k] == 0]) > 1:
                bottom[j] = 1

        if i == rows - 1:
            for j in range(cols):
                bottom[j] = 1
            for j in range(cols - 1):
                if sets[j] != sets[j + 1]:
                    right[j] = 0
                    s = sets[j + 1]
                    for k in range(cols):
                        if sets[k] == s:
                            sets[k] = sets[j]

        rarr.append(right[:])
        barr.append(bottom[:])

    return np.array(rarr), np.array(barr)


if __name__ == "__main__":
    x, y = generate_maze(6, 6)
    print(type(x))
    print(x)
