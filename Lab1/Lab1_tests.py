import unittest # импортируем библиотеку для проверки тестов
import Lab1_code # импортируем файл с кодом, который будем проверять


class Tests_for_my_code(unittest.TestCase): # создаём класс тестов для нашей программы
    def test_same_elements(self): # тест одинаковых элементов в списке
        self.assertEqual(Lab1_code.target([3, 3, 3, 3], 6), [0, 1])

    def test_empty_list(self): # тест пустого списка
        self.assertEqual(Lab1_code.target([], 10), None)

    def test_latters(self): # тест списка из букв
        self.assertEqual(Lab1_code.target(['q', 'r', 'h'], 'qr'), None)

    def test_float_nums(self): # тест чисел с плавующей точкой
        self.assertEqual(Lab1_code.target([0.6, 0.8, 0.8877663452], 0.6), None)

    def test_target_not_num(self): # тест target, являющегося не числом
        self.assertEqual(Lab1_code.target([1, 3, 88, 45], 'a'), None)

    def test_not_nums(self): # тусе target, являющегося числом с плавующей точкой
        self.assertEqual(Lab1_code.target([45, 87, 6, 55], 46.8), None)

    def test_same_sum(self): # тест одинаковых сумм
        self.assertEqual(Lab1_code.target([11, 5, 3, 3, 4, 4], 7), [2, 4])

    def test_all_sums_true(self): # тест, где все суммы подходят
        self.assertEqual(Lab1_code.target([1, 8, 2, 7, 6], 8), [0, 3])

    def test_zero_and_num(self): # тест суммы числа и 0
        self.assertEqual(Lab1_code.target([0, 9, 4, 6, 7, 5], 9), [0, 1])

    def test_num_is_target(self): # тест, где все нули
        self.assertEqual(Lab1_code.target([0, 0, 0, 0], 0), [0, 1])

    def test_less_than_zero(self): # тест суммы отрицательных чисел
        self.assertEqual(Lab1_code.target([-1, -34, -3], -4), [0, 2])

    def test_large_nums(self): # тест двовольно больших чисел 
        self.assertEqual(Lab1_code.target([23456765, 2777778282828, 300000, 789000, 4558585885], 1089000), [2, 3])

    def test_normal(self): # обыкновенный тест
        self.assertEqual(Lab1_code.target([2, 34, 62, 1, 24], 96), [1, 2])

    def test_both_type_nums(self): # тест списка из положительных и отрицательных чисел
        self.assertEqual(Lab1_code.target([-1, 4, 45, -3, 2, 9, 4], 8), [0, 5])



if __name__ == '__main__':
    unittest.main()