import unittest # импортируем библиотеку для проверки тестов
import Lab3_code # импортируем файл с кодом, который будем проверять


class Tests_for_my_code(unittest.TestCase): # создаём класс тестов для нашей программы
    def test_common_test(self): # обычный тест
        self.assertEqual(Lab3_code.gen_bin_tree(2, 11), {11: [{121: [{14641: []}, {14643: []}]}, {123: [{15129: []}, {15131: []}]}]})

    def test_height_is_0(self): # тест: высота дерева равна 0
        self.assertEqual(Lab3_code.gen_bin_tree(0, 3), {3: []})

    def test_large_tree(self): # тест: довольно большое дерево (большое значение высоты)
        self.assertEqual(Lab3_code.gen_bin_tree(4, 8), {8: [{64: [{4096: [{16777216: [{281474976710656: []}, {281474976710658: []}]}, {16777218: [{281475043819524: []}, {281475043819526: []}]}]}, {4098: [{16793604: [{282025135308816: []}, {282025135308818: []}]}, {16793606: [{282025202483236: []}, {282025202483238: []}]}]}]}, {66: [{4356: [{18974736: [{360040606269696: []}, {360040606269698: []}]}, {18974738: [{360040682168644: []}, {360040682168646: []}]}]}, {4358: [{18992164: [{360702293402896: []}, {360702293402898: []}]}, {18992166: [{360702369371556: []}, {360702369371558: []}]}]}]}]})

    def test_height_is_str(self): # тест: высота является строкой
        self.assertEqual(Lab3_code.gen_bin_tree('fghjhgg', 3), None)

    def test_height_is_float(self): # тест: высота является вещественным числом
        self.assertEqual(Lab3_code.gen_bin_tree(4.90, 3), None)

    def test_root_is_str(self): # тест: корень дерева является строкой
        self.assertEqual(Lab3_code.gen_bin_tree(3, 'fghdjks'), None)

    def test_root_is_float(self): # тест: корень дерева является вещественным числом
        self.assertEqual(Lab3_code.gen_bin_tree(2, 21.8788666), None)

    def test_root_is_0(self): # тест: корень дерева равен 0
        self.assertEqual(Lab3_code.gen_bin_tree(3, 0), {0: [{0: [{0: [{0: []}, {2: []}]}, {2: [{4: []}, {6: []}]}]}, {2: [{4: [{16: []}, {18: []}]}, {6: [{36: []}, {38: []}]}]}]})

    def test_height_is_less_than_0(self): # тест: высота - отрицательное число
        self.assertEqual(Lab3_code.gen_bin_tree(-6, 8), None)

    def test_root_is_less_than_0(self): # тест: корень дерева - отрицательное число
        self.assertEqual(Lab3_code.gen_bin_tree(2, -7), {-7: [{49: [{2401: []}, {2403: []}]}, {51: [{2601: []}, {2603: []}]}]})

if __name__ == '__main__':
    unittest.main()