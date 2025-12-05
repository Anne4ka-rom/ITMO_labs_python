import unittest # импортируем unittest для создания и запуска тестов
import io # импортируем io для работы со строковыми потоками ввода-вывода
import sys # импортируем sys для работы с системными потоками ввода-вывода
import logging # импортируем logging для логирования
from logger import logger # импортируем тестируемый декоратор


class TestLogger(unittest.TestCase):
    '''
    Класс тестов декоратора logger
    '''
    def test_logger_with_stdout(self):
        """
        Тестирование декоратора @logger() с использованием sys.stdout
        Проверяет, что декоратор без параметров пишет логи в стандартный вывод
        """
        stdout = sys.stdout # сохраняем оригинальный поток стандартного вывода, чтобы потом можно было восстановить его после временного перенаправления вывода в другой поток
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        sys.stdout = stream # перенаправляем sys.stdout в наш stream
    
        try: # начинаем блок try для обработки всех исключений
            @logger # применяем декоратор к тестовой функции
            def multiply_x_on_number(x): # создаем тестовую функцию multiply_x_on_number
                return x * 3 # возвращаем результат тестовой функции
            
            result = multiply_x_on_number(5) # вызываем декорированную функцию
            logs = stream.getvalue()

            self.assertEqual(result, 15) # проверяем, что функция возвращает правильный результат
            self.assertIn("INFO: Вызов функции multiply_x_on_number", logs)
            self.assertIn("с аргументами: 5", logs)
            self.assertIn("INFO: Функция multiply_x_on_number успешно завершилась", logs)
            self.assertIn("Результат: 15", logs)
        finally: # выполняем следующий блок кода даже если появилось исключение
            sys.stdout = stdout  # восстанавливаем stdout даже при провале теста

    def test_logger_with_stringio(self):
        """
        Тестирование декоратора @logger() с явным указанием потока вывода StringIO
        Проверяет, что декоратор с параметром handle=stream пишет логи в указанный поток StringIO
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом

        @logger(handle=stream) # применяем декоратор к тестовой функции
        def add_numbers(a, b): # создаем тестовую функцию add_numbers
            return a + b # возвращаем результат тестовой функции

        result = add_numbers(8, 4) # вызываем декорированную функцию
        logs = stream.getvalue() # извлекаем все, что было записано в stream

        self.assertEqual(result, 12) # проверяем, что функция возвращает правильный результат
        self.assertIn("INFO: Вызов функции add_numbers", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 8, 4", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция add_numbers успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn("Результат: 12", logs) # проверяем, что в логах зафиксирован результат выполнения
    
    def test_logger_with_logging(self):
        """
        Тестирование декоратора @logger() с использованием модуля logging
        Проверяет, что декоратор может работать с объектами logging.Logger и правильно форматирует сообщения
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        
        test_logger = logging.getLogger("test_logger") # создаем объект логгера в модуле logging и настраиваем его
        test_logger.setLevel(logging.INFO) # устанавливаем уровень логирования INFO
        test_logger.handlers.clear() # очищаем все предыдущие обработчики (чтобы не дублировался вывод)
        
        handler = logging.StreamHandler(stream) # создаем обработчик, который направляет логи в stream
        formatter = logging.Formatter("%(levelname)s: %(message)s") # настраиваем формат вывода (уровень: сообщение)
        handler.setFormatter(formatter) # устанавливаем formatter для обработчика, который определяет как будут выглядеть логируемые сообщения
        test_logger.addHandler(handler) # добавляем обработчик к логгеру
        
        @logger(handle=test_logger) # применяем декоратор к тестовой функции
        def multiply_numbers(a, b): # создаем тестовую функцию multiply_numbers
            return a * b # возвращаем результат тестовой функции
        
        result = multiply_numbers(9, 8) # вызываем декорированную функцию
        logs = stream.getvalue() # извлекаем все, что было записано в stream
        
        self.assertEqual(result, 72) # проверяем, что функция возвращает правильный результат
        self.assertIn("INFO: Вызов функции multiply_numbers", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 9, 8", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция multiply_numbers успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn("Результат: 72", logs) # проверяем, что в логах зафиксирован результат выполнения
    
    def test_logger_exception_handling(self):
        """
        Тестирование логирования исключений
        Проверяет, что декоратор корректно логирует ошибки и пробрасывает исключения
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом

        @logger(handle=stream) # применяем декоратор к тестовой функции
        def error_function(): # создаем тестовую функцию error_function
            raise ValueError("Ошибка") # выбрасываем исключение
        
        with self.assertRaises(ValueError) as error_message: # проверяем, что функция вызывает ValueError, и сохраняем контекст исключения в error_message
            error_function() # вызываем функцию error_function, выбрасывающую исключение
        
        logs = stream.getvalue() # извлекаем все, что было записано в stream
        
        self.assertRegex(logs, r"ERROR") # проверяем, что в логах есть строка ERROR
        self.assertEqual(str(error_message.exception), "Ошибка") # проверяем, что сообщение исключения соответствует ожидаемому

    def test_logger_with_different_arguments(self): 
        """Тестирование логирования разных типов аргументов"""
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        
        @logger(handle=stream) # применяем декоратор к тестовой функции
        def return_different_arguments(a, b=10, *args, **kwargs): # создаем тестовую функцию test_logger_with_different_arguments
            return f"a={a}, b={b}, args={args}, kwargs={kwargs}" # возвращаем результат тестовой функции
        
        return_different_arguments(1, 'hello', 3, 4, x=5, y=[6, 7], z={'s': 5, 'n': 30})
        logs = stream.getvalue() # проверяем, что функция возвращает правильный результат
        
        # проверяем, что repr() корректно обрабатывает разные типы
        self.assertIn("'hello'", logs)  # это -- строка
        self.assertIn("[6, 7]", logs)  # это -- список
        self.assertIn("{'s': 5, 'n': 30}", logs)  # это -- словарь

        # проверяем корректность логов
        self.assertIn("INFO: Вызов функции return_different_arguments", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 1, 'hello', 3, 4, x=5, y=[6, 7], z={'s': 5, 'n': 30}", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция return_different_arguments успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn('Результат: "a=1, b=hello, args=(3, 4), kwargs={\'x\': 5, \'y\': [6, 7], \'z\': {\'s\': 5, \'n\': 30}}"', logs) # проверяем, что в логах зафиксирован результат выполнения


if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()