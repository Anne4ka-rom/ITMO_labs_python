import unittest # импортируем unittest для создания и запуска тестов
from unittest.mock import patch, Mock # импортируем patch и Mock из unittest.mock для мокирования объектов
import requests # импортируем библиотеку requests для тестирования сетевых ошибок
from currencies import get_currencies # импортируем тестируемую функцию get_currencies из файла currencies


class TestFunctionGetCurrencies(unittest.TestCase):
    '''
    Класс тестов для функции get_currencies()
    '''
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_success(self, mock_get):
        '''
        Тестируем случай, когда функция успешно возвращает курсы валют
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # задаем возвращаемое значение для метода json()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25, "Nominal": 1},
                "EUR": {"Value": 101.70, "Nominal": 1}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        
        result = get_currencies(['USD', 'EUR']) # вызываем тестируемую функцию get_currencies с аргументами
        
        self.assertEqual(result, {'USD': 93.25, 'EUR': 101.70}) # проверяем, что функция возвращает правильный результат
    
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_missing_currency(self, mock_get):
        '''
        Тестируем случай, когда запрашиваемая валюта не существует
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # создаем данные только с USD, без EUR
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        
        with self.assertRaises(KeyError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение KeyError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD', 'XYZ']) # вызываем функцию, один из кодов валют которой не существует
        
        self.assertIn("Валюта 'XYZ' отсутствует в данных", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_invalid_json(self, mock_get):
        '''
        Тестируем случай, когда JSON некорректен
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        mock_response.json.side_effect = ValueError("Некорректный JSON") # настраиваем side_effect чтобы метод json() вызывал исключение
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        
        with self.assertRaises(ValueError) as context: # проверяем, что внутри блока кода будет вызвано исключение ValueError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        
        self.assertIn("Некорректный JSON", str(context.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_missing_valute_key(self, mock_get):
        '''
        Тестируем случай, отсутствует ключ 'Valute'
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        mock_response.json.return_value = {"SomeOtherKey": {}} # устанавливаем мок-объекта mock_response, который имитирует отсутствие обязательного ключа "Valute"
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        
        with self.assertRaises(KeyError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение KeyError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        
        self.assertIn("Ключ 'Valute' отсутствует", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_connection_error(self, mock_get):
        '''
        Тестируем случай, когда происходит ошибка соединения
        '''
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed") # настраиваем side_effect чтобы requests.get вызывал исключение
        
        with self.assertRaises(ConnectionError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение ConnectionError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        
        self.assertIn("API недоступен", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст

    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_invalid_value_type(self, mock_get):
        '''
        Тестируем случай, когда значение курса имеет неверный тип
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # задаем возвращаемое значение для метода json(), но вместо числа другой тип (строка)
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": "not_a_number"}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        
        with self.assertRaises(TypeError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение TypeError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        
        self.assertIn("неверный тип", str(error_message.exception).lower()) # проверяем, что сообщение об ошибке содержит нужный текст


if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()