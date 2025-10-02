import unittest # импортируем библиотеку для проверки тестов
import Lab2_code # импортируем файл с кодом, который будем проверять


class Tests_for_my_code(unittest.TestCase): # создаём класс тестов для нашей программы
    def test_target_is_str(self): # тест: target - строка
        self.assertEqual(Lab2_code.guess_func('fffgfgv', [1, 2, 3], 'bin'), None)
    
    def test_target_is_float(self): # тест: target - вещественное число
        self.assertEqual(Lab2_code.guess_func(0.2, [1, 2, 3], 'seq'), None)

    def test_nums_is_str(self): # тест: nums состоит из строк
        self.assertEqual(Lab2_code.guess_func(5, ['s', '3', 'df'], 'bin'), None)

    def test_nums_is_float(self): # тест: nums состоит из вещественных чисел
        self.assertEqual(Lab2_code.guess_func(90, [0.5, 43.88888, 7.3], 'seq'), None)

    def test_type_is_int(self): # тест: type - целое число
        self.assertEqual(Lab2_code.guess_func(90, [89, 90, 100, 101, 123, 8], 9), None)

    def test_type_is_float(self): # тест: type - вещественное число
        self.assertEqual(Lab2_code.guess_func(90, [89, 90, 100, 101, 123, 8], 90.7), None)

    def test_type_is_str_but_not_seq_or_bin(self): # тест: type - строка, не являющаяся bin или seq
        self.assertEqual(Lab2_code.guess_func(90, [89, 90, 100, 101, 123, 8], 'yes'), None)

    def test_empty_list(self): # тест: nums - пустой список
        self.assertEqual(Lab2_code.guess_func(2, [], 'bin'), None)

    def test_target_not_in_list(self): # тест: target нет в списке
        self.assertEqual(Lab2_code.guess_func(2, [3, 4, 5], 'seq'), None)

    def test_all_nums_in_list_is_target_seq(self): # тест: nums состоит из целых одинаковых чисел, равных target для type = 'seq'
        self.assertEqual(Lab2_code.guess_func(2, [2, 2, 2, 2], 'seq'), [2, 1])

    def test_all_nums_in_list_is_target_bin(self): # тест: nums состоит из целых одинаковых чисел, равных target для type = 'bin'
        self.assertEqual(Lab2_code.guess_func(2, [2, 2, 2, 2], 'bin'), [2, 1])

    def test_common_test_bin(self): # обычный тест для type = 'bin'
        self.assertEqual(Lab2_code.guess_func(24, [20, 21, 22, 23, 24, 25, 26, 27, 28], 'bin'), [24, 1])

    def test_common_test_seq(self): # обычный тест для type = 'seq'
        self.assertEqual(Lab2_code.guess_func(24, [20, 21, 22, 23, 24, 25, 26, 27, 28], 'seq'), [24, 5])

    def test_nums_in_list_less_than_0_seq(self): # тест: nums состоит из отрицательных чисел для type = 'seq'
        self.assertEqual(Lab2_code.guess_func(-4, [-2, -3, -5, -4, -10], 'seq'), [-4, 3])

    def test_nums_in_list_less_than_0_bin(self): # тест: nums состоит из отрицательных чисел для type = 'bin'
        self.assertEqual(Lab2_code.guess_func(-4, [-2, -3, -5, -4, -10], 'bin'), [-4, 1])

    def test_big_nums_in_list_seq(self): # тест: nums состоит из очень больших и маленьких чисел для type = 'seq'
        self.assertEqual(Lab2_code.guess_func(3000000, [10000000030339, -367890, 3000000, -4873534432729202000, -103333333344444], 'seq'), [3000000, 4])

    def test_big_nums_in_list_bin(self): # тест: nums состоит из очень больших и маленьких чисел для type = 'bin'
        self.assertEqual(Lab2_code.guess_func(3000000, [10000000030339, -367890, 3000000, -4873534432729202000, -103333333344444], 'bin'), [3000000, 3])

    def test_in_list_more_than_one_number_bin(self):  # тест: в nums содержится больше одного target-а для type = 'bin'
        self.assertEqual(Lab2_code.guess_func(4, [1, 2, 5, 6, 4, 8, 9, 23, 45, 4], 'bin'), [4, 2])

    def test_in_list_more_than_one_number_seq(self): # тест: в nums содержится больше одного target-а для type = 'seq'
        self.assertEqual(Lab2_code.guess_func(4, [1, 2, 5, 6, 4, 8, 9, 23, 45, 4], 'seq'), [4, 3])


if __name__ == '__main__':
    unittest.main()
