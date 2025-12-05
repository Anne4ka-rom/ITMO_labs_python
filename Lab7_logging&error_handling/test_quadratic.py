import unittest # импортируем unittest для создания и запуска тестов
from quadratic import solve_quadratic # импортируем тестируемую функцию solve_quadratic из файла quadratic


class TestSolveQuadratic(unittest.TestCase):
    '''Класс тестов для функции solve_quadratic()'''
    
    def test_two_roots(self):
        '''
        Тестируем случай, когда уравнения имеет два корня
        '''
        roots = solve_quadratic(1, -3, 2) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        
        self.assertIsNotNone(roots)# проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 2) # проверяем, что возвращаемых корней два
        self.assertAlmostEqual(roots[0], 2.0) # проверяем, что первый корень должен быть 2.0 + небольшая погрешность
        self.assertAlmostEqual(roots[1], 1.0) # проверяем, что второй корень должен быть 1.0 + небольшая погрешность
    
    def test_one_root(self):
        '''
        Тестируем случай, когда уравнения имеет один корень
        '''
        roots = solve_quadratic(1, 2, 1) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        
        self.assertIsNotNone(roots) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots[0], -1.0) # проверяем, что корень должен быть -1.0 + небольшая погрешность
    
    def test_no_real_roots(self):
        '''
        Тестируем случай, когда уравнения не имеет действительных корней
        '''
        roots = solve_quadratic(1, 1, 1) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        
        self.assertIsNone(roots) # проверяем, что функция вернула None

    def test_linear_equation(self):
        '''
        Тестируем случай, когда уравнения линейно
        '''
        roots = solve_quadratic(0, 2, -4) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        
        self.assertIsNotNone(roots) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots[0], 2.0) # проверяем, что корень должен быть 2.0 + небольшая погрешность
    
    def test_invalid_type(self):
        '''
        Тестируем случай, когда в уравнении содержится неккоректный тип данных
        '''
        with self.assertRaises(TypeError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение TypeError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            solve_quadratic("abc", 2, 3) # вызываем функцию с некорректным (строковым) типом данных
        
        self.assertIn("Коэффициент 'a' должен быть числом", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    
    def test_a_and_b_zero(self):
        '''
        Тестируем случай, когда в уравнении a=0 и b=0
        '''
        with self.assertRaises(ValueError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение ValueError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            solve_quadratic(0, 0, 1) # вызываем функцию, где a=0 и b=0
        
        self.assertIn("Оба коэффициента a и b равны нулю", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст

    def test_extreme_numbers(self):
        '''
        Тестируем случай, когда коэффициенты очень большие/малые
        '''
        roots_small = solve_quadratic(1e-10, 2e-10, 1e-10) # вызываем функцию solve_quadratic с очень малыми коэффициентами для уравнения
        self.assertIsNotNone(roots_small) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots_small), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots_small[0], -1.0, places=6) # проверяем, что корень должен быть -1.0 + небольшая погрешность

        roots_large = solve_quadratic(1e10, 2e10, 1e10) # вызываем функцию solve_quadratic с очень большими коэффициентами для уравнения
        self.assertIsNotNone(roots_large)  # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots_large), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots_large[0], -1.0, places=6) # проверяем, что корень должен быть -1.0 + небольшая погрешность

if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()