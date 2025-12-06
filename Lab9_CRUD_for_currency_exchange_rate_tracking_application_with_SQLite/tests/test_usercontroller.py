import unittest # импортируем unittest для создания и запуска юнит-тестов
from unittest.mock import MagicMock # импортируем MagicMock для создания мок-объектов
import os # импортируем os для работы с файловой системой и путями
import sys # импортируем sys для работы с системными путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта

from controllers.usercontroller import UserController # импортируем класс UserController из модуля controllers.usercontroller для тестирования его функциональности
from models.user import User # импортируем класс User из модуля models.user для создания тестовых объектов пользователей
from models.user_currency import UserCurrency # импортируем класс UserCurrency из модуля models.user_currency для тестирования связей пользователь-валюта


class TestUserController(unittest.TestCase):
    '''
    Класс TestUserController содержит юнит-тесты для контроллера пользователей UserController
    Тестирует управление пользователями и их подписками на валюты
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestUserController
        Подготавливает тестовое окружение: создаёт мок-объект базы данных и контроллер пользователей
        '''
        self.mock_db = MagicMock() # создаём мок-объект контроллера базы данных с помощью MagicMock для имитации поведения реальной базы данных
        self.controller = UserController(self.mock_db) # создаём экземпляр UserController с мок-объектом базы данных в качестве зависимости
    
    def test_create_user_success(self):
        '''
        Функция test_create_user_success тестирует успешное создание пользователя
        Проверяет корректность работы метода create_user контроллера UserController
        '''
        user = User(name="Иван Иванов") # создаём тестовый объект пользователя с именем "Иван Иванов"
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        self.mock_db.get_last_row_id.return_value = 1 # настраиваем мок-метод get_last_row_id для возврата id 1
        
        result = self.controller.create_user(user) # вызываем метод create_user контроллера UserController для создания нового пользователя
        
        self.assertEqual(result, 1) # проверяем, что метод вернул id 1
        self.mock_db.execute_update.assert_called_once_with("INSERT INTO users (name) VALUES (?)", ("Иван Иванов",)) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом для создания пользователя и параметрами
    
    def test_read_users(self):
        '''
        Функция test_read_users тестирует получение списка пользователей из базы данных
        Проверяет корректность работы метода read_users контроллера UserController
        '''
        # создаём тестовые данные пользователей в виде списка словарей
        mock_data = [
            {'id': 1, 'name': 'Иван Иванов'},
            {'id': 2, 'name': 'Пётр Петров'}
        ]
        self.mock_db.execute_query.return_value = mock_data # настраиваем мок-метод execute_query для возврата тестовых данных
        
        result = self.controller.read_users() # вызываем метод read_users контроллера UserController для получения списка пользователей
        
        self.assertEqual(len(result), 2) # проверяем, что возвращённый список содержит 2 элемента
        self.assertEqual(result[0]['name'], 'Иван Иванов') # проверяем, что у первого элемента имя равно 'Иван Иванов'
        self.assertEqual(result[1]['name'], 'Пётр Петров') # проверяем, что у второго элемента имя равно 'Пётр Петров'
    
    def test_read_user_by_id_found(self):
        '''
        Функция test_read_user_by_id_found тестирует поиск пользователя по ID, когда пользователь найден
        Проверяет корректность работы метода read_user_by_id контроллера UserController
        '''
        mock_data = [{'id': 1, 'name': 'Иван Иванов'}] # создаём тестовые данные пользователя в виде списка с одним словарём
        self.mock_db.execute_query.return_value = mock_data # настраиваем мок-метод execute_query для возврата тестовых данных
        
        result = self.controller.read_user_by_id(1) # вызываем метод read_user_by_id контроллера для поиска пользователя с id 1
        
        self.assertIsNotNone(result) # проверяем, что результат не является None
        self.assertEqual(result['id'], 1) # проверяем, что у найденного пользователя id равен 1
        self.assertEqual(result['name'], 'Иван Иванов') # проверяем, что у найденного пользователя имя равно 'Иван Иванов'
    
    def test_read_user_by_id_not_found(self):
        '''
        Функция test_read_user_by_id_not_found тестирует поиск пользователя по ID, когда пользователь не найден
        Проверяет корректность работы метода read_user_by_id контроллера UserController при отсутствии пользователя
        '''
        self.mock_db.execute_query.return_value = [] # настраиваем мок-метод execute_query для возврата пустого списка
        
        result = self.controller.read_user_by_id(999) # вызываем метод read_user_by_id для поиска несуществующего пользователя с id=999
        
        self.assertIsNone(result) # проверяем, что результат является None
    
    def test_update_user_success(self):
        '''
        Функция test_update_user_success тестирует успешное обновление пользователя
        Проверяет корректность работы метода update_user контроллера UserController
        '''
        user = User(name="Вася Васечкин") # создаём тестовый объект пользователя с новым именем
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        
        result = self.controller.update_user(1, user) # вызываем метод update_user контроллера для обновления пользователя с id=1
        
        self.assertTrue(result) # проверяем, что метод вернул True
        self.mock_db.execute_update.assert_called_once_with("UPDATE users SET name = ? WHERE id = ?", ("Вася Васечкин", 1)) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом обновления пользователя и параметрами
    
    def test_delete_user_success(self):
        '''
        Функция test_delete_user_success тестирует успешное удаление пользователя из базы данных
        Проверяет корректность работы метода delete_user контроллера UserController
        '''
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        
        result = self.controller.delete_user(1) # вызываем метод delete_user контроллера для удаления пользователя с id=1
        
        self.assertTrue(result) # проверяем, что метод вернул True
        self.mock_db.execute_update.assert_called_once_with("DELETE FROM users WHERE id = ?", (1,)) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом удаления пользователя и параметром id пользователя -- 1
    
    def test_count_users(self):
        '''
        Функция test_count_users тестирует подсчёт количества пользователей в базе данных
        Проверяет корректность работы метода count_users контроллера UserController
        '''
        self.mock_db.execute_query.return_value = [{'count': 3}] # настраиваем мок-метод execute_query для возврата списка с одним словарём, содержащим ключ 'count' со значением 3
        
        result = self.controller.count_users() # вызываем метод count_users для подсчёта количества пользователей
        
        self.assertEqual(result, 3) # проверяем, что метод вернул значение 3 -- количество пользователей
    
    def test_get_user_subscription_count(self):
        '''
        Функция test_get_user_subscription_count тестирует подсчёт подписок пользователя
        Проверяет корректность работы метода get_user_subscription_count контроллера UserController
        '''
        self.mock_db.execute_query.return_value = [{'count': 2}] # настраиваем мок-метод execute_query для возврата списка с одним словарём, содержащим ключ 'count' со значением 2
        
        result = self.controller.get_user_subscription_count(1) # вызываем метод get_user_subscription_count для подсчёта подписок пользователя с id=1
        
        self.assertEqual(result, 2) # проверяем, что метод вернул значение 2 -- количество подписок пользователя
    
    def test_add_user_subscription_success(self):
        '''
        Функция test_add_user_subscription_success тестирует успешное добавление подписки пользователя на валюту
        Проверяет корректность работы метода add_user_subscription контроллера UserController
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2) # создаём тестовую связь пользователь-валюта
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        self.mock_db.get_row_count.return_value = 1 # настраиваем мок-метод get_row_count для возврата 1
        
        result = self.controller.add_user_subscription(user_currency) # вызываем метод add_user_subscription контроллера для добавления подписки
        
        self.assertTrue(result) # проверяем, что метод вернул True
        
        self.mock_db.execute_update.assert_called_once() # проверяем, что метод execute_update вызывался ровно один раз
        
        call_args = self.mock_db.execute_update.call_args # получаем аргументы, с которыми вызывался метод execute_update
        
        sql_query = call_args[0][0] # получаем SQL-запрос из аргументов вызова
        self.assertIn("INSERT OR IGNORE INTO currencies_user", sql_query) # проверяем, что SQL-запрос содержит конструкцию "INSERT OR IGNORE INTO currencies_user"
        self.assertIn("user_id", sql_query) # проверяем, что SQL-запрос содержит поле "user_id"
        self.assertIn("currency_id", sql_query) # проверяем, что SQL-запрос содержит поле "currency_id"
        self.assertIn("VALUES (?, ?)", sql_query) # проверяем, что SQL-запрос содержит "VALUES (?, ?)""
        
        self.assertEqual(call_args[0][1], (1, 2)) # проверяем, что параметры запроса равны 1, 2
    
    def test_add_user_subscription_success_alternative(self):
        '''
        Функция test_add_user_subscription_success_alternative -- альтернативный тест успешного добавления подписки
        Проверяет корректность работы метода add_user_subscription контроллера UserController более гибким способом
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2) # создаём тестовую связь пользователь-валюта
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        self.mock_db.get_row_count.return_value = 1 # настраиваем мок-метод get_row_count для возврата 1
        
        result = self.controller.add_user_subscription(user_currency) # вызываем метод add_user_subscription контроллера для добавления подписки
        
        self.assertTrue(result) # проверяем, что метод вернул True
        
        self.assertEqual(self.mock_db.execute_update.call_count, 1) # проверяем, что метод execute_update вызывался ровно один раз
        
        actual_sql = self.mock_db.execute_update.call_args[0][0] # получаем фактический SQL-запрос из аргументов вызова
        self.assertIn("currencies_user", actual_sql) # проверяем, что SQL-запрос содержит имя таблицы -- 'currencies_user'
        self.assertIn("user_id", actual_sql) # проверяем, что SQL-запрос содержит поле -- 'user_id'
        self.assertIn("currency_id", actual_sql) # проверяем, что SQL-запрос содержит поле -- 'currency_id'
        
        actual_params = self.mock_db.execute_update.call_args[0][1] # получаем фактические параметры запроса
        self.assertEqual(actual_params, (1, 2)) # проверяем, что параметры равны 1, 2
    
    def test_remove_user_subscription_success(self):
        '''
        Функция test_remove_user_subscription_success тестирует успешное удаление подписки пользователя на валюту
        Проверяет корректность работы метода remove_user_subscription контроллера UserController
        '''
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        
        result = self.controller.remove_user_subscription(1, 2) # вызываем метод remove_user_subscription контроллера для удаления подписки пользователя 1 на валюту 2
        
        self.assertTrue(result) # проверяем, что метод вернул True
        self.mock_db.execute_update.assert_called_once_with("DELETE FROM currencies_user WHERE user_id = ? AND currency_id = ?", (1, 2)) # проверяем, что метод execute_update мок-объекта базы данных вызывался ровно один раз с правильным SQL-запросом удаления подписки и параметрами


class TestUserControllerEdgeCases(unittest.TestCase):
    '''
    Класс TestUserControllerEdgeCases содержит тесты граничных случаев для контроллера пользователей UserController
    Тестирует нестандартные ситуации и обработку ошибок
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestUserControllerEdgeCases
        Подготавливает тестовое окружение: создаёт мок-объект базы данных и контроллер пользователей
        '''
        self.mock_db = MagicMock() # создаём мок-объект контроллера базы данных с помощью MagicMock для имитации поведения реальной базы данных
        self.controller = UserController(self.mock_db) # создаём экземпляр UserController с мок-объектом базы данных в качестве зависимости
    
    def test_create_user_failure(self):
        '''
        Функция test_create_user_failure тестирует неудачное создание пользователя
        Проверяет обработку ошибок в методе create_user контроллера UserController
        '''
        user = User(name="Иван Иванов") # создаём тестовый объект пользователя
        
        self.mock_db.execute_update.return_value = False # настраиваем мок-метод execute_update для возврата False
        
        result = self.controller.create_user(user) # вызываем метод create_user контроллера для создания пользователя
        
        self.assertEqual(result, 0)  # проверяем, что метод вернул 0 при ошибке
    
    def test_add_user_subscription_duplicate(self):
        '''
        Функция test_add_user_subscription_duplicate тестирует добавление уже существующей подписки
        Проверяет обработку дубликатов в методе add_user_subscription контроллера UserController
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2) # создаём тестовую связь пользователь-валюта
        
        self.mock_db.execute_update.return_value = True # настраиваем мок-метод execute_update для возврата True
        self.mock_db.get_row_count.return_value = 0  # настраиваем мок-метод get_row_count для возврата 0
        
        result = self.controller.add_user_subscription(user_currency) # вызываем метод add_user_subscription для добавления дублирующейся подписки
        
        self.assertFalse(result) # проверяем, что метод вернул False для дубликата


if __name__ == '__main__':
    unittest.main() # запускаем все тесты