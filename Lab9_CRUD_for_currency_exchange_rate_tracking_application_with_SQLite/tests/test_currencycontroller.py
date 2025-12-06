import unittest # импортируем unittest для создания и запуска юнит-тестов
from unittest.mock import MagicMock, patch # импортируем MagicMock для создания мок-объектов и patch для временной замены объектов
import sys # импортируем sys для работы с системными путями
import os # импортируем os для работы с файловой системой и путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта

from controllers.currencycontroller import CurrencyController # импортируем класс CurrencyController из модуля controllers.currencycontroller для тестирования его функциональности
from models.currency import Currency # импортируем класс Currency из модуля models.currency для создания тестовых объектов валют


class TestCurrencyController(unittest.TestCase):
    '''
    Класс TestCurrencyController содержит юнит-тесты для контроллера валют CurrencyController
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestCurrencyController
        Подготавливает тестовое окружение: создаёт мок-объект базы данных и контроллер валют
        '''
        self.mock_db = MagicMock() # создаём мок-объект контроллера базы данных с помощью MagicMock для имитации поведения реальной базы данных
        self.controller = CurrencyController(self.mock_db) # создаём экземпляр CurrencyController с мок-объектом базы данных в качестве зависимости
        
    def test_list_currencies(self):
        '''
        Функция test_list_currencies тестирует получение списка валют из базы данных
        Проверяет корректность работы метода read_currencies контроллера CurrencyController
        '''
        # мокируем возвращаемые данные
        mock_data = [
            {'id': 1, 'num_code': '840', 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1, 'created_at': '2024-01-01'},
            {'id': 2, 'num_code': '978', 'char_code': 'EUR', 'name': 'Евро', 'value': 91.0, 'nominal': 1, 'created_at': '2024-01-01'}
        ]
        self.mock_db.execute_query.return_value = mock_data # настраиваем мок-метод execute_query для возврата тестовых данных при вызове
        
        result = self.controller.read_currencies() # вызываем метод read_currencies контроллера CurrencyController для получения списка валют
        
        self.assertEqual(len(result), 2) # проверяем, что возвращённый список содержит 2 элемента
        self.assertEqual(result[0]['char_code'], 'USD') # проверяем, что у первого элемента символьный код равен 'USD'
        self.assertEqual(result[1]['char_code'], 'EUR') # проверяем, что у второго элемента символьный код равен 'EUR'
        self.mock_db.execute_query.assert_called_once_with("SELECT * FROM currencies ORDER BY id") # проверяем, что метод execute_query мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом для получения всех валют с сортировкой по id
    
    def test_create_currency_success(self):
        '''
        Функция test_create_currency_success тестирует успешное создание новой валюты в базе данных
        Проверяет корректность работы метода create_currency контроллера CurrencyController
        '''
        # создаём тестовый объект валюты с заданными параметрами
        currency = Currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        self.mock_db.get_last_row_id.return_value = 1 # настраиваем мок-метод get_last_row_id для возврата id 1
        
        self.mock_db.execute_query.side_effect = [[], [{'id': 1, 'char_code': 'USD', 'num_code': '840', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1}]] # настраиваем последовательные возвращаемые значения для execute_query: сначала пустой список -- валюта не найдена, затем список с созданной валютой
        
        result = self.controller.create_currency(currency) # вызываем метод create_currency контроллера для создания новой валюты
        
        self.assertEqual(result, 1) # проверяем, что метод вернул id 1
        self.mock_db.execute_update.assert_called_once() # проверяем, что метод execute_update вызывался ровно один раз
        self.mock_db.get_last_row_id.assert_called_once() # проверяем, что метод get_last_row_id вызывался ровно один раз
        
        self.assertEqual(self.mock_db.execute_query.call_count, 2) # проверяем, что метод execute_query вызывался ровно два раза (проверка существования и проверка после создания)
    
    def test_update_currency_by_char_code(self):
        '''
        Функция test_update_currency_by_char_code тестирует обновление курса валюты по символьному коду
        Проверяет корректность работы метода update_currency_by_char_code контроллера CurrencyController
        '''
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        
        result = self.controller.update_currency_by_char_code('USD', 95.0) # вызываем метод update_currency_by_char_code для обновления курса валюты USD
        
        self.assertTrue(result) # проверяем, что метод вернул True
        self.mock_db.execute_update.assert_called_once_with("UPDATE currencies SET value = ? WHERE char_code = ?", (95.0, 'USD')) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом обновления курса валюты и параметрами
    
    def test_delete_currency_success(self):
        '''
        Функция test_delete_currency_success тестирует успешное удаление валюты из базы данных
        Проверяет корректность работы метода delete_currency контроллера CurrencyController
        '''
        mock_currency = {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'num_code': '840', 'value': 90.0, 'nominal': 1} # создаём мок-объект валюты в виде словаря с тестовыми данными
        
        with patch.object(self.controller, 'read_currency_by_id', return_value=mock_currency): # временно заменяем метод read_currency_by_id контроллера на мок, возвращающий тестовую валюту
            self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
            
            result = self.controller.delete_currency(1) # вызываем метод delete_currency для удаления валюты с id 1
            
            self.assertTrue(result) # проверяем, что метод вернул True
            self.mock_db.execute_update.assert_called_once_with("DELETE FROM currencies WHERE id = ?", (1,)) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом удаления валюты и параметром id валюты 1
    
    def test_count_currencies(self):
        '''
        Функция test_count_currencies тестирует подсчёт количества валют в базе данных
        Проверяет корректность работы метода count_currencies контроллера CurrencyController
        '''
        self.mock_db.execute_query.return_value = [{'count': 5}] # настраиваем мок-метод execute_query для возврата списка с одним словарём, содержащим ключ 'count' со значением 5
        
        result = self.controller.count_currencies() # вызываем метод count_currencies для подсчёта количества валют
        
        self.assertEqual(result, 5) # проверяем, что метод вернул значение 5 -- количество валют
        self.mock_db.execute_query.assert_called_once_with("SELECT COUNT(*) as count FROM currencies") # проверяем, что метод execute_query мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом для подсчёта количества записей в таблице currencies
    
    def test_read_currency_by_char_code_found(self):
        '''
        Функция test_read_currency_by_char_code_found тестирует поиск валюты по символьному коду (когда валюта найдена)
        Проверяет корректность работы метода read_currency_by_char_code контроллера CurrencyController
        '''
        # создаём мок-объект валюты в виде списка словарей с тестовыми данными
        mock_data = [{
            'id': 1, 
            'num_code': '840', 
            'char_code': 'USD', 
            'name': 'Доллар США',
            'value': 90.0,
            'nominal': 1
        }]
        self.mock_db.execute_query.return_value = mock_data # настраиваем мок-метод execute_query для возврата тестовых данных
        
        result = self.controller.read_currency_by_char_code('USD') # вызываем метод read_currency_by_char_code для поиска валюты с кодом 'USD'
        
        self.assertIsNotNone(result) # проверяем, что результат не является None
        self.assertEqual(result['char_code'], 'USD') # проверяем, что у найденной валюты символьный код равен 'USD'
        self.assertEqual(result['name'], 'Доллар США') # проверяем, что у найденной валюты название равно 'Доллар США'
    
    def test_read_currency_by_char_code_not_found(self):
        '''
        Функция test_read_currency_by_char_code_not_found тестирует поиск валюты по символьному коду
        Проверяет корректность работы метода read_currency_by_char_code контроллера CurrencyController при отсутствии валюты
        '''
        self.mock_db.execute_query.return_value = [] # настраиваем мок-метод execute_query для возврата пустого списка
        
        result = self.controller.read_currency_by_char_code('XYZ') # вызываем метод read_currency_by_char_code для поиска несуществующей валюты с кодом 'XYZ'
        
        self.assertIsNone(result) # проверяем, что результат является None


class TestCurrencyControllerEdgeCases(unittest.TestCase):
    '''
    Класс TestCurrencyControllerEdgeCases содержит тесты граничных случаев для контроллера валют CurrencyController
    Тестирует нестандартные ситуации и обработку ошибок
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestCurrencyControllerEdgeCases
        Подготавливает тестовое окружение: создаёт мок-объект базы данных и контроллер валют
        '''
        self.mock_db = MagicMock() # создаём мок-объект контроллера базы данных с помощью MagicMock для имитации поведения реальной базы данных
        self.controller = CurrencyController(self.mock_db) # создаём экземпляр CurrencyController с мок-объектом базы данных в качестве зависимости
    
    def test_create_currency_duplicate(self):
        '''
        Функция test_create_currency_duplicate тестирует создание валюты с уже существующим символьным кодом
        Проверяет обработку дубликатов в методе create_currency контроллера CurrencyController
        '''
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём тестовый объект валюты с дублирующимся символьным кодом 'USD'
        
        with patch.object(self.controller, 'read_currency_by_char_code') as mock_read: # временно заменяем метод read_currency_by_char_code контроллера на мок
            # настраиваем мок-метод для возврата существующей валюты в виде словаря
            mock_read.return_value = {
                'id': 1, 
                'char_code': 'USD', 
                'num_code': '840', 
                'name': 'Доллар США',
                'value': 90.0,
                'nominal': 1
            }
            
            result = self.controller.create_currency(currency) # вызываем метод create_currency для создания дублирующейся валюты
            
            self.assertEqual(result, 0) # проверяем, что метод вернул 0

            mock_read.assert_called_once_with('USD') # проверяем, что метод read_currency_by_char_code вызывался ровно один раз с аргументом 'USD'
            
            self.mock_db.execute_update.assert_not_called() # проверяем, что метод execute_update не вызывался

    def test_update_currency_failure(self):
        '''
        Функция test_update_currency_failure тестирует неудачное обновление курса валюты
        Проверяет обработку ошибок в методе update_currency_by_char_code контроллера CurrencyController
        '''
        self.mock_db.execute_update.return_value = False # настраиваем мок-метод execute_update для возврата False
        
        result = self.controller.update_currency_by_char_code('USD', 95.0) # вызываем метод update_currency_by_char_code для обновления курса валюты
        
        self.assertFalse(result) # проверяем, что метод вернул False
    
    def test_get_user_subscribed_currencies(self):
        '''
        Функция test_get_user_subscribed_currencies тестирует получение валют, на которые подписан пользователь
        Проверяет корректность работы метода get_user_subscribed_currencies контроллера CurrencyController
        '''
        # создаём список мок-объектов валют с тестовыми данными для симуляции ответа базы данных
        mock_data = [
            {'id': 1, 'num_code': '840', 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1},
            {'id': 2, 'num_code': '978', 'char_code': 'EUR', 'name': 'Евро', 'value': 91.0, 'nominal': 1}
        ]
        self.mock_db.execute_query.return_value = mock_data # настраиваем мок-метод execute_query для возврата тестовых данных
        
        result = self.controller.get_user_subscribed_currencies(1) # вызываем метод get_user_subscribed_currencies для получения валют пользователя с id 1
        
        self.assertEqual(len(result), 2) # проверяем, что возвращённый список содержит 2 элемента
        self.assertEqual(result[0]['char_code'], 'USD') # проверяем, что у первого элемента символьный код равен 'USD'
        self.assertEqual(result[1]['char_code'], 'EUR') # проверяем, что у второго элемента символьный код равен 'EUR'
        
        self.mock_db.execute_query.assert_called_once() # проверяем, что метод execute_query вызывался ровно один раз
        call_args = self.mock_db.execute_query.call_args # получаем аргументы, с которыми вызывался метод execute_query
        self.assertIn('SELECT c.*', call_args[0][0])  # проверяем SQL-запрос # проверяем, что SQL-запрос содержит 'SELECT c.*'
        self.assertEqual(call_args[0][1], (1,))  # проверяем параметры # проверяем, что параметры запроса равны (1,) (id пользователя)


if __name__ == '__main__':
    unittest.main() # запускаем все тесты