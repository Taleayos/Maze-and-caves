import numpy as np


def find_shortest_path(matrix1, matrix2, start_point, end_point):
    """
    Функция для нахождения кратчайшего пути из одной точки лабиринта в другую.
    Использует волновой алгоритм для нахождения кратчайшего пути

    :param matrix1:  матрица значений ячеек, которые имеют (1) или не имеют (0) правую стенку
    :param matrix2: матрица значений ячеек, которые имеют (1) или не имеют (0) нижнюю стенку
    :param start_point: координаты начальной точки в формате индекса стартовой ячейк (х, у)
    :param end_point: короодинаты конечной точки в формате индекса последней ячейки (х, у)

    :return: list(tuple) список координат точек для построения кратчайшего пути
    """
    if start_point == end_point:
        return [start_point, end_point]
    path_matrix = make_path_matrix(matrix1, matrix2, start_point, end_point)
    path = [end_point]
    count = path_matrix[end_point]
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while count > 1:
        i, j = end_point
        new_steps = steps.copy()
        for i_s, j_s in steps:
            if matrix1.shape[0] > i + i_s > 0 and matrix1.shape[1] > j + j_s > 0:
                if matrix2[i_s + i, j_s + j] == 1 and i_s == -1 and j_s == 0:
                    new_steps.remove((-1, 0))
                if matrix2[i, j] == 1 and (1, 0) in new_steps:
                    new_steps.remove((1, 0))
                if matrix1[i_s + i, j_s + j] == 1 and i_s == 0 and j_s == -1:
                    new_steps.remove((0, -1))
                if matrix1[i, j] == 1 and (0, 1) in new_steps:
                    new_steps.remove((0, 1))
        for i_step, j_step in new_steps:
            if (0 > i + i_step or i + i_step >= matrix1.shape[0]
                or 0 > j + j_step or j + j_step >= matrix1.shape[1]) \
                    or (i + i_step, j + j_step) in path:
                continue
            elif path_matrix[end_point[0] + i_step, end_point[1] + j_step] == path_matrix[end_point] - 1:
                end_point = (end_point[0] + i_step, end_point[1] + j_step)
                path.append(end_point)
                count -= 1
                break
    # print(path)
    return path

def make_path_matrix(matrix1, matrix2, start_point, end_point):
    """Функция волнового алгоритма для заполнения матрицы значениями,
    помогающими найти кратчайших путь от одной точки до другой


    :param matrix1:  матрица значений ячеек, которые имеют (1) или не имеют (0) правую стенку
    :param matrix2: матрица значений ячеек, которые имеют (1) или не имеют (0) нижнюю стенку
    :param start_point: координаты начальной точки в формате индекса стартовой ячейк (х, у)
    :param end_point: короодинаты конечной точки в формате индекса последней ячейки (х, у)

    :return: np.matrix матрица волнового алгоритма
    """
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    step_stack = [start_point]
    tmp_stack = []
    path_matrix = np.array([[0 for _ in range(matrix1.shape[1])] for _ in range(matrix1.shape[0])])
    step_count = 1
    path_matrix[*start_point] = step_count
    stop_flag = True
    visited = set()
    visited.add(start_point)
    while stop_flag:
        for start_point in step_stack:
            i, j = start_point
            step_count = path_matrix[i, j] + 1
            visited.add(start_point)
            new_steps = steps.copy()
            if matrix1[i, j] == 1:
                new_steps.remove((0, 1))
            if matrix2[i, j] == 1:
                new_steps.remove((1, 0))
            for i_step, j_step in steps:
                if ((0 > i + i_step or i + i_step >= path_matrix.shape[0]
                    or 0 > j + j_step or j + j_step >= path_matrix.shape[1])
                        and (i_step, j_step) in new_steps):
                    new_steps.remove((i_step, j_step))
                elif (i + i_step, j + j_step) in visited and (i_step, j_step) in new_steps:
                    new_steps.remove((i_step, j_step))
                elif (i_step, j_step) == (0, -1) and matrix1[i + i_step, j + j_step] == 1 and (i_step, j_step) in new_steps:
                    new_steps.remove((i_step, j_step))
                elif (i_step, j_step) == (-1, 0) and matrix2[i + i_step, j + j_step] == 1 and (i_step, j_step) in new_steps:
                    new_steps.remove((i_step, j_step))


            for i_step, j_step in new_steps:
                if (start_point[0] + i_step, start_point[1] + j_step) == end_point or len(visited) == matrix1.shape[0] * matrix1.shape[1]:
                    stop_flag = False
                    path_matrix[start_point[0] + i_step, start_point[1] + j_step] = step_count
                    break
                path_matrix[i + i_step, j + j_step] = step_count
                tmp_stack.append((i + i_step, j + j_step))
        step_stack = tmp_stack.copy()
        tmp_stack.clear()
    return path_matrix

if __name__ == "__main__":
    matrix1 = np.array([[0, 0, 0, 1], [1, 0, 1, 1], [0, 1, 0, 1], [0, 0, 0, 1]])
    matrix2 = np.array([[1, 0, 1, 0],[0, 0, 1, 0],[1, 1, 0, 1],[1, 1, 1, 1]])
    start = (0, 0)
    end = (3, 3)
    find_shortest_path(matrix1, matrix2, start, end)