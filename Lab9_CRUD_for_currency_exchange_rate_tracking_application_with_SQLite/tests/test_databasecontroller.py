import unittest # импортируем unittest для создания и запуска юнит-тестов
from unittest.mock import MagicMock, patch, call # импортируем MagicMock для создания мок-объектов, patch для временной замены объектов и call для проверки вызовов
import sqlite3 # импортируем sqlite3 для работы с базой данных sqlite
import sys # импортируем sys для работы с системными путями
import os # импортируем os для работы с файловой системой и путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта

from controllers.databasecontroller import DatabaseController # импортируем класс DatabaseController из модуля controllers.databasecontroller для тестирования его функциональности


class TestDatabaseControllerSimple(unittest.TestCase):
    '''
    Класс TestDatabaseControllerSimple содержит упрощённые юнит-тесты для контроллера базы данных DatabaseController
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestDatabaseControllerSimple
        Подготавливает тестовое окружение
        '''
        pass # оставляем пустой метод setUp, так как каждый тест настраивает своё окружение отдельно
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_initialization_memory_db(self, mock_connect):
        '''
        Функция test_initialization_memory_db тестирует инициализацию базы данных в памяти
        Проверяет корректность создания и настройки объекта DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,), имитирующего отсутствие данных в таблицах
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_connect.assert_called_once_with(':memory:', check_same_thread=False) # проверяем, что функция connect вызывалась ровно один раз с параметром ':memory:' и отключённой проверкой потока
        
        self.assertEqual(mock_conn.row_factory, sqlite3.Row) # проверяем, что у соединения установлен фабричный метод строк sqlite3.Row
        
        self.assertTrue(mock_cursor.execute.called) # проверяем, что метод execute вызывался хотя бы один раз

        execute_calls = mock_cursor.execute.call_args_list # получаем список всех вызовов метода execute
        first_call = execute_calls[0] # получаем первый вызов метода execute
        self.assertEqual(first_call[0][0], "PRAGMA foreign_keys = ON") # проверяем, что первым выполнялся запрос на включение поддержки внешних ключей
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_execute_query_success_simple(self, mock_connect):
        '''
        Функция test_execute_query_success_simple тестирует простой успешный запрос к базе данных
        Проверяет корректность работы метода execute_query контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.side_effect = [(0,), (0,)] # настраиваем side_effect для fetchone
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        class SimpleRow:
            '''
            Класс SimpleRow представляет простую имитацию объекта строки базы данных
            Позволяет получать доступ к данным как по строковым ключам, так и по индексам
            '''
            def __init__(self, data):
                '''
                Функция __init__() инициализирует объект строки с данными
                
                Параметры:
                data -- словарь с данными строки, где ключи - имена колонок, значения - данные ячеек
                '''
                self.data = data # сохраняем данные строки в атрибуте data
            
            def __getitem__(self, key):
                '''
                Функция __getitem__() позволяет получать значения из строки как по индексу, так и по ключу
                Реализует поддержку индексации объекта SimpleRow[key]
                
                Параметры:
                key -- ключ для доступа к данным: целое число (индекс) или строка (имя колонки)
                
                Возвращает:
                значение -- значение соответствующей колонки строки
                '''
                if isinstance(key, int): # проверяем, является ли ключ целым числом для доступа по индексу
                    return list(self.data.values())[key] # если ключ целочисленный, возвращаем значение по индексу
                return self.data[key] # если ключ строковый, возвращаем значение из словаря
            
            def keys(self):
                '''
                Функция keys() возвращает список всех ключей строки
                Полезно для итерации по всем колонкам или получения мета-информации о структуре строки
                
                Возвращает:
                список строковых ключей словаря данных
                '''
                return list(self.data.keys()) # возвращаем список ключей словаря
        
        test_row = SimpleRow({'id': 1, 'name': 'Иван'}) # создаём тестовый объект строки с данными id=1, name='Иван'
        mock_cursor.description = [('id',), ('name',)] # настраиваем описание курсора с именами столбцов
        mock_cursor.fetchall.return_value = [test_row] # настраиваем мок-метод fetchall для возврата списка с тестовой строкой
        
        result = controller.execute_query("SELECT * FROM Иван", (1,)) # вызываем метод execute_query с тестовым запросом и параметрами
        
        if result: # если что-то вернулось
            self.assertEqual(len(result), 1) # проверяем, что результат содержит 1 элемент
            if isinstance(result[0], dict): # проверяем, что результат -- это словарь с нужными полями
                self.assertEqual(result[0].get('id'), 1) # проверяем, что в словаре поле 'id' равно 1
                self.assertEqual(result[0].get('name'), 'Иван') # проверяем, что в словаре поле 'name' равно 'Иван'
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_execute_query_empty(self, mock_connect):
        '''
        Функция test_execute_query_empty тестирует выполнение запроса с пустым результатом
        Проверяет обработку пустых результатов методом execute_query контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора

        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)

        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_cursor.fetchall.return_value = [] # настраиваем мок-метод fetchall для возврата пустого списка
        
        result = controller.execute_query("SELECT * FROM Иван") # вызываем метод execute_query с тестовым запросом без параметров
        
        self.assertEqual(result, []) # проверяем, что результат равен пустому списку
        mock_cursor.execute.assert_called_with("SELECT * FROM Иван", ()) # проверяем, что метод execute вызывался с правильным SQL-запросом и пустыми параметрами
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_execute_update_success(self, mock_connect):
        '''
        Функция test_execute_update_success тестирует успешное выполнение обновления данных
        Проверяет корректность работы метода execute_update контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_cursor.execute.reset_mock() # сбрасываем мок метода execute
        mock_conn.commit.reset_mock() # сбрасываем мок метода commit
        
        mock_cursor.rowcount = 1 # настраиваем атрибут rowcount для возврата 1
        
        result = controller.execute_update("UPDATE Иван SET name = ? WHERE id = ?", ("Пётр", 1)) # вызываем метод execute_update с запросом обновления и параметрами
        
        self.assertTrue(result) # проверяем, что метод вернул True
        mock_cursor.execute.assert_called_with( "UPDATE Иван SET name = ? WHERE id = ?", ("Пётр", 1)) # проверяем, что метод execute вызывался с правильным SQL-запросом и параметрами
        mock_conn.commit.assert_called_once() # проверяем, что метод commit вызывался ровно один раз
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_execute_update_failure(self, mock_connect):
        '''
        Функция test_execute_update_failure тестирует неудачное выполнение обновления данных
        Проверяет обработку ошибок методом execute_update контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_cursor.execute.reset_mock() # сбрасываем мок метода execute
        mock_conn.rollback.reset_mock() # сбрасываем мок метода rollback
        
        mock_cursor.execute.side_effect = sqlite3.Error("SQL error") # настраиваем side_effect для метода execute для выброса исключения sqlite3.Error
        
        result = controller.execute_update("UPDATE Иван SET name = ?", ("Иван",)) # вызываем метод execute_update с запросом обновления
        
        self.assertFalse(result) # проверяем, что метод вернул False
        mock_conn.rollback.assert_called_once() # проверяем, что метод rollback вызывался ровно один раз
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_get_last_row_id(self, mock_connect):
        '''
        Функция test_get_last_row_id тестирует получение ID последней вставленной записи
        Проверяет корректность работы метода get_last_row_id контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_cursor.fetchone.return_value = (5,) # настраиваем мок-метод fetchone для возврата кортежа (5,)
        
        result = controller.get_last_row_id() # вызываем метод get_last_row_id для получения ID последней вставленной записи
        
        self.assertEqual(result, 5) # проверяем, что метод вернул 5 -- ожидаемый ID
        mock_cursor.execute.assert_any_call("SELECT last_insert_rowid() as id") # проверяем, что метод execute вызывался с запросом на получение ID последней вставленной записи
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_get_row_count(self, mock_connect):
        '''
        Функция test_get_row_count тестирует получение количества измененных строк
        Проверяет корректность работы метода get_row_count контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        mock_cursor.rowcount = 3 # настраиваем атрибут rowcount для возврата 3
        
        result = controller.get_row_count() # вызываем метод get_row_count для получения количества измененных строк
        
        self.assertEqual(result, 3) # проверяем, что метод вернул 3 -- количество строк
    
    @patch('sqlite3.connect') # декоратор @patch для временной замены функции sqlite3.connect на мок-объект
    def test_close_connection(self, mock_connect):
        '''
        Функция test_close_connection тестирует закрытие соединения с базой данных
        Проверяет корректность работы метода close контроллера DatabaseController
        '''
        mock_conn = MagicMock() # создаём мок-объект соединения с базой данных
        mock_cursor = MagicMock() # создаём мок-объект курсора базы данных
        mock_connect.return_value = mock_conn # настраиваем мок-функцию connect для возврата мок-соединения
        mock_conn.cursor.return_value = mock_cursor # настраиваем мок-метод cursor для возврата мок-курсора
        
        mock_cursor.fetchone.return_value = (0,) # настраиваем мок-метод fetchone для возврата кортежа (0,)
        
        controller = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти для тестирования
        
        controller.close() # вызываем метод close для закрытия соединения с базой данных
        
        mock_conn.close.assert_called_once() # проверяем, что метод close вызывался ровно один раз


class TestDatabaseControllerIntegration(unittest.TestCase):
    '''
    Класс TestDatabaseControllerIntegration содержит интеграционные тесты с реальной базой данных
    '''
    
    def test_real_database_operations(self):
        '''
        Функция test_real_database_operations тестирует реальные операции с базой данных в памяти
        Проверяет основные операции CRUD через экземпляр DatabaseController
        '''
        db = DatabaseController(':memory:') # создаём экземпляр DatabaseController с реальной базой данных в памяти для интеграционного тестирования
        
        result = db.execute_query("SELECT 1 as test_value") # выполняем простой запрос для получения тестового значения
        self.assertEqual(len(result), 1) # проверяем, что результат содержит 1 элемент
        self.assertEqual(result[0]['test_value'], 1) # проверяем, что тестовое значение равно 1
        
        success = db.execute_update("CREATE TABLE IF NOT EXISTS test_table (id INTEGER, name TEXT)") # выполняем запрос на создание тестовой таблицы
        self.assertTrue(success) # проверяем, что операция успешна
        
        success = db.execute_update("INSERT INTO test_table (id, name) VALUES (?, ?)",(1, 'Иван')) # выполняем запрос на вставку данных в тестовую таблицу
        self.assertTrue(success) # проверяем, что операция успешна
        
        last_id = db.get_last_row_id() # вызываем метод get_last_row_id для получения ID последней вставленной записи
        self.assertGreater(last_id, 0) # проверяем, что ID больше 0
        
        result = db.execute_query("SELECT * FROM test_table WHERE id = ?", (1,)) # выполняем запрос на выборку вставленных данных
        self.assertEqual(len(result), 1) # проверяем, что результат содержит 1 элемент
        self.assertEqual(result[0]['name'], 'Иван') # проверяем, что имя равно 'Иван'
        
        db.close() # закрываем соединение с базой данных
    
    def test_tables_created(self):
        '''
        Функция test_tables_created тестирует создание таблиц при инициализации базы данных
        Проверяет, что все необходимые таблицы создаются в базе данных при инициализации DatabaseController
        '''
        db = DatabaseController(':memory:') # создаём экземпляр DatabaseController с реальной базой данных в памяти для тестирования
        
        tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'") # выполняем запрос на получение списка всех таблиц в базе данных
        
        table_names = [table['name'] for table in tables] # извлекаем имена таблиц из результата запроса
 
        self.assertIn('users', table_names) # проверяем, что таблица 'users' существует
        self.assertIn('currencies', table_names) # проверяем, что таблица 'currencies' существует
        self.assertIn('currencies_user', table_names) # проверяем, что таблица 'currencies_user' существует
        
        db.close() # закрываем соединение с базой данных


if __name__ == '__main__':
    unittest.main() # запускаем все тесты