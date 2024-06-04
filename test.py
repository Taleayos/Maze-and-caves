import unittest

from cave_generation import *
from eller_algo import *
from shortest_path import *


class TestMazeCase(unittest.TestCase):
    """
        Класс, реализующий unit тестирование следующих методов:
        - генерация лабиринтов,
        - нахождение кратчайшего пути между двумя точками в лабиринте,
        - генерация пещер,
        - реализация шага клеточного алгоритма

    """

    def test_shortest_path_1(self):
        matrix1 = np.array([[0, 0, 0, 1], [1, 0, 1, 1], [0, 1, 0, 1], [0, 0, 0, 1]])
        matrix2 = np.array([[1, 0, 1, 0], [0, 0, 1, 0], [1, 1, 0, 1], [1, 1, 1, 1]])
        start_point, end_point = (0, 0), (3, 3)
        path = [(3, 3), (3, 2), (2, 2), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_shortest_path_2(self):
        matrix1 = np.array([[0, 0, 0, 1], [0, 1, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1]])
        matrix2 = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 1, 1, 1]])
        start_point, end_point = (0, 0), (3, 2)
        path = [(3, 2), (3, 1), (2, 1), (1, 1), (0, 1), (0, 0)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_shortest_path_3(self):
        matrix1 = np.array([[1, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
        matrix2 = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1]])
        start_point, end_point = (0, 0), (0, 1)
        path = [(0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (0, 0)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_shortest_path_4(self):
        matrix1 = np.array([[1, 1, 0, 1], [1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
        matrix2 = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1]])
        start_point, end_point = (0, 0), (0, 0)
        path = [(0, 0), (0, 0)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_shortest_path_5(self):
        matrix1 = np.array([[1, 0, 1, 1, 1], [0, 1, 0, 0, 0]])
        matrix2 = np.array([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])
        start_point, end_point = (0, 0), (0, 4)
        path = [(0, 4), (1, 4), (1, 3), (1, 2), (0, 2), (0, 1), (1, 1), (1, 0), (0, 0)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_shortest_path_6(self):
        matrix1 = np.array(
            [[0, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 0, 1], [1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 0, 1]])
        matrix2 = np.array(
            [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]])
        start_point, end_point = (0, 2), (4, 3)
        path = [(4, 3), (5, 3), (6, 3), (6, 2), (6, 1), (5, 1), (5, 0), (4, 0), (3, 0), (3, 1), (2, 1), (1, 1), (0, 1),
                (0, 2)]

        self.assertEqual(path, find_shortest_path(matrix1, matrix2, start_point, end_point))

    def test_eller_algo_test_1(self):
        q = [1, 0, 1, 0, 0, 0, 1, 1, 1]
        matrix1, matrix2 = generate_maze(3, 3, q)
        res = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
        res1 = np.array([[0, 0, 0], [1, 1, 0], [1, 1, 1]])

        self.assertEqual(matrix1.all(), res.all())
        self.assertEqual(matrix2.all(), res1.all())

    def test_eller_algo_test_2(self):
        q = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1]
        matrix1, matrix2 = generate_maze(4, 4, q)
        res = np.array([[1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1], [0, 0, 0, 1]])
        res1 = np.array([[0, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 1], [1, 1, 1, 1]])

        self.assertEqual(matrix1.all(), res.all())
        self.assertEqual(matrix2.all(), res1.all())

    def test_eller_algo_test_3(self):
        q = [1, 1, 1, 0, 1, 1, 0, 0, 0, 1]
        matrix1, matrix2 = generate_maze(2, 5, q)
        res = np.array([[1, 1, 1, 0, 1], [0, 0, 0, 1, 1]])
        res1 = np.array([[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]])

        self.assertEqual(matrix1.all(), res.all())
        self.assertEqual(matrix2.all(), res1.all())

    def test_eller_algo_test_4(self):
        q = [1, 1, 1, 1]
        matrix1, matrix2 = generate_maze(2, 2, q)
        res = np.array([[1, 1], [0, 1]])
        res1 = np.array([[0, 0], [1, 1]])

        self.assertEqual(matrix1.all(), res.all())
        self.assertEqual(matrix2.all(), res1.all())

    def test_cave_step1(self):
        tmp_cave = np.array([[0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 1, ]])
        birth = 2
        death = 5
        new_cave = np.array([[1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 1, 1, ]])
        res = cave_step_1(tmp_cave, birth, death)
        self.assertEqual(res.all(), new_cave.all())

    def test_cave_step2(self):
        tmp_cave = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
        birth = 4
        death = 1
        new_cave = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        res = cave_step_1(tmp_cave, birth, death)
        self.assertEqual(res.all(), new_cave.all())

    def test_cave_generation(self):
        new_cave = cave_generatuion_1(4, 4, 50)
        res = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, ]])
        self.assertNotEqual(new_cave.all(), res.all())


if __name__ == "__main__":
    unittest.main()
