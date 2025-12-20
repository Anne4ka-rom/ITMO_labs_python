import unittest # импортируем unittest для создания и запуска юнит-тестов
import sys # импортируем sys для работы с системными путями и управлением системными параметрами
import os # импортируем os для работы с операционной системой и файловыми путями
from unittest.mock import patch, Mock # импортируем patch и Mock из unittest.mock для создания мок-объектов и подмены реальных функций в тестах
import requests # импортируем библиотеку requests для работы с HTTP-запросами
import json # импортируем json для работы с JSON-данными и обработки JSON-ошибок

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python, чтобы можно было импортировать модули проекта

from utils.currencies_api import get_currencies # импортируем тестируемую функцию get_currencies из модуля currencies_api


class TestGetCurrencies(unittest.TestCase):
    '''
    Класс TestGetCurrencies содержит юнит-тесты для функции get_currencies из модуля currencies_api
    Тестирует различные сценарии работы функции, включая успешное выполнение и обработку ошибок
    '''
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_network_error(self, mock_get):
        '''
        Тестирование обработки сетевой ошибки функцией get_currencies
        Проверяет, что функция корректно обрабатывает исключения сетевого уровня и преобразует их в ConnectionError
        '''
        mock_get.side_effect = requests.exceptions.RequestException("Network error") # настраиваем мок-объект, чтобы он вызывал исключение RequestException при вызове
        with self.assertRaises(ConnectionError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение ConnectionError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет ConnectionError из-за сетевой ошибки
    
    def test_empty_currency_codes(self):
        '''
        Тестирование вызова функции get_currencies с пустым списком кодов валют
        Проверяет, что функция валидирует входные данные и вызывает ValueError при попытке запроса пустого списка валют
        '''
        with self.assertRaises(ValueError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение ValueError
            get_currencies([]) # вызываем тестируемую функцию с пустым списком, ожидаем, что она вызовет ValueError, так как нечего запрашивать
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_successful_response(self, mock_get):
        '''
        Тестирование успешного получения курсов валют функцией get_currencies
        Проверяет, что функция корректно обрабатывает валидный JSON-ответ от API, извлекает необходимые данные о валютах и возвращает их в ожидаемой структуре
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.return_value = { # настраиваем метод json мок-объекта для возврата тестовых данных в формате JSON
            "Valute": { # ключ "Valute" содержит словарь с данными о валютах
                "USD": { # данные о долларе США
                    "ID": "R01235", # идентификатор валюты в системе ЦБ РФ
                    "NumCode": "840", # цифровой код валюты
                    "CharCode": "USD", # буквенный код валюты
                    "Nominal": 1, # номинал
                    "Name": "Доллар США", # полное название валюты на русском языке
                    "Value": 75.5 # текущий курс к рублю
                },
                "EUR": { # данные о евро
                    "ID": "R01239", # идентификатор валюты в системе ЦБ РФ
                    "NumCode": "978", # цифровой код валюты
                    "CharCode": "EUR", # буквенный код валюты
                    "Nominal": 1, # номинал
                    "Name": "Евро", # полное название валюты на русском языке
                    "Value": 85.3 # текущий курс к рублю
                }
            }
        }
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата нашего мок-ответа
        
        result = get_currencies(['USD', 'EUR']) # вызываем тестируемую функцию с кодами валют USD и EUR
        
        self.assertEqual(result['USD']['value'], 75.5) # проверяем, что курс USD равен ожидаемому значению 75.5
        self.assertEqual(result['USD']['name'], 'Доллар США') # проверяем, что название USD соответствует ожидаемому
        self.assertEqual(result['USD']['char_code'], 'USD') # проверяем, что буквенный код USD соответствует ожидаемому
        self.assertEqual(result['USD']['num_code'], '840') # проверяем, что цифровой код USD соответствует ожидаемому
        self.assertEqual(result['USD']['nominal'], 1) # проверяем, что номинал USD равен ожидаемому значению 1
        
        self.assertEqual(result['EUR']['value'], 85.3) # проверяем, что курс EUR равен ожидаемому значению 85.3
        self.assertEqual(result['EUR']['name'], 'Евро') # проверяем, что название EUR соответствует ожидаемому
        mock_get.assert_called_once() # проверяем, что метод requests.get был вызван ровно один раз
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_invalid_json_response(self, mock_get):
        '''
        Тестирование обработки некорректного JSON-ответа функцией get_currencies
        Проверяет, что функция корректно обрабатывает случаи, когда API возвращает невалидный JSON, и преобразует JSONDecodeError в более общее ValueError
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0) # настраиваем метод json мок-объекта для вызова исключения JSONDecodeError
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        with self.assertRaises(ValueError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение ValueError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет ValueError из-за некорректного JSON
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_missing_valute_key(self, mock_get):
        '''
        Тестирование обработки ответа с отсутствующим ключом 'Valute' функцией get_currencies
        Проверяет, что функция корректно обрабатывает случаи, когда структура ответа API не соответствует ожидаемой, и вызывает KeyError для индикации проблемы с данными
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.return_value = {} # настраиваем метод json мок-объекта для возврата пустого словаря
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        with self.assertRaises(KeyError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение KeyError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет KeyError из-за отсутствия ключа "Valute" в данных
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_missing_currency_in_data(self, mock_get):
        '''
        Тестирование обработки отсутствия запрошенной валюты в данных API функцией get_currencies
        Проверяет, что функция корректно обрабатывает случаи, когда API не возвращает данные по одной из запрошенных валют, и вызывает KeyError для индикации отсутствия данных
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.return_value = { # настраиваем метод json мок-объекта для возврата тестовых данных
            "Valute": { # ключ "Valute" содержит словарь с данными о валютах
                "EUR": { # данные о евро
                    "ID": "R01239", # идентификатор валюты в системе ЦБ РФ
                    "NumCode": "978", # цифровой код валюты
                    "CharCode": "EUR", # буквенный код валюты
                    "Nominal": 1, # номинал
                    "Name": "Евро", # полное название валюты на русском языке
                    "Value": 85.3 # текущий курс к рублю
                }
            }
        }
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        with self.assertRaises(KeyError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение KeyError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет KeyError из-за отсутствия USD в данных
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_invalid_currency_value_type(self, mock_get):
        '''
        Тестирование обработки некорректного типа значения курса функцией get_currencies
        Проверяет, что функция валидирует тип данных в ответе API и вызывает TypeError при получении строкового значения вместо числового для курса валюты
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.return_value = { # настраиваем метод json мок-объекта для возврата тестовых данных
            "Valute": { # ключ "Valute" содержит словарь с данными о валютах
                "USD": { # данные о долларе США
                    "ID": "R01235", # идентификатор валюты в системе ЦБ РФ
                    "NumCode": "840", # цифровой код валюты
                    "CharCode": "USD", # буквенный код валюты
                    "Nominal": 1, # номинал
                    "Name": "Доллар США", # полное название валюты на русском языке
                    "Value": "не число" # некорректное значение курса
                }
            }
        }
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        with self.assertRaises(TypeError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение TypeError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет TypeError из-за неверного типа данных курса
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_http_error(self, mock_get):
        '''
        Тестирование обработки HTTP ошибок функцией get_currencies
        Проверяет, что функция корректно обрабатывает HTTP статус-коды ошибок и преобразует их в ConnectionError
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found") # настраиваем метод raise_for_status мок-объекта для вызова исключения HTTPError
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        with self.assertRaises(ConnectionError): # проверяем, что при выполнении следующего блока кода будет вызвано исключение ConnectionError
            get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'], ожидаем, что она вызовет ConnectionError из-за HTTP ошибки
    
    @patch('utils.currencies_api.requests.get') # декоратор @patch для подмены функции requests.get на мок-объект во время выполнения теста
    def test_partial_currency_data(self, mock_get):
        '''
        Тестирование обработки частичных данных о валюте функцией get_currencies
        Проверяет, что функция корректно обрабатывает случаи, когда API возвращает неполные данные по валюте, и устанавливает значения по умолчанию для отсутствующих полей, обеспечивая работоспособность
        '''
        mock_response = Mock() # создаём мок-объект для имитации HTTP-ответа
        mock_response.json.return_value = { # настраиваем метод json мок-объекта для возврата тестовых данных с неполной информацией
            "Valute": { # ключ "Valute" содержит словарь с данными о валютах
                "USD": { # данные о долларе США с пропущенными полями
                    "ID": "R01235", # идентификатор валюты в системе ЦБ РФ
                    "CharCode": "USD", # буквенный код валюты
                    "Value": 75.5 # текущий курс к рублю
                }
            }
        }
        mock_get.return_value = mock_response # настраиваем мок-объект requests.get для возврата мок-ответа
        
        result = get_currencies(['USD']) # вызываем тестируемую функцию с параметром ['USD'] для проверки обработки частичных данных
        
        self.assertEqual(result['USD']['value'], 75.5) # проверяем, что курс USD равен ожидаемому значению 75.5
        self.assertEqual(result['USD']['char_code'], 'USD') # проверяем, что буквенный код USD соответствует ожидаемому
        self.assertEqual(result['USD']['name'], '')  # проверяем, что строка пустая по умолчанию для отсутствующего поля Name
        self.assertEqual(result['USD']['nominal'], 1)  # проверяем, что значение по умолчанию 1 для отсутствующего поля Nominal
        self.assertEqual(result['USD']['num_code'], '')  # проверяем, что строка пустая по умолчанию для отсутствующего поля NumCode


if __name__ == '__main__':
    unittest.main() # запускаем все тесты