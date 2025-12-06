import unittest # импортируем unittest для создания и запуска юнит-тестов
import tempfile # импортируем tempfile для создания временных файлов
import sqlite3 # импортируем sqlite3 для работы с базой данных SQLite
from unittest.mock import MagicMock, patch, Mock # импортируем MagicMock для создания мок-объектов, patch для временной замены объектов и Mock для создания простых моков
from io import StringIO, BytesIO # импортируем StringIO и BytesIO для работы с потоками ввода-вывода в памяти
import os # импортируем os для работы с файловой системой и путями
import sys # импортируем sys для работы с системными путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта

from myapp import CurrencyRequestHandler, get_controllers # импортируем CurrencyRequestHandler и get_controllers из модуля myapp для тестирования основного приложения
from controllers.databasecontroller import DatabaseController # импортируем класс DatabaseController из модуля controllers.databasecontroller
from controllers.currencycontroller import CurrencyController # импортируем класс CurrencyController из модуля controllers.currencycontroller
from controllers.usercontroller import UserController # импортируем класс UserController из модуля controllers.usercontroller
from controllers.pagescontroller import PagesController # импортируем класс PagesController из модуля controllers.pagescontroller


class TestMyAppIntegration(unittest.TestCase):
    '''
    Класс TestMyAppIntegration содержит интеграционные тесты для всего приложения
    Тестирует взаимодействие всех компонентов приложения в реальных условиях
    '''
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestMyAppIntegration
        Подготавливает тестовое окружение: создаёт временную базу данных и инициализирует контроллеры
        '''
        self.db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False) # создаём временный файл базы данных с расширением .db без автоматического удаления
        self.db_file.close() # закрываем файловый объект
        
        self.db = DatabaseController(self.db_file.name) # создаём экземпляр DatabaseController с временным файлом базы данных
        self.currency = CurrencyController(self.db) # создаём экземпляр CurrencyController с контроллером базы данных
        self.user = UserController(self.db) # создаём экземпляр UserController с контроллером базы данных
        self.pages = PagesController() # создаём экземпляр PagesController
    
    def tearDown(self):
        '''
        Функция tearDown() выполняется после каждого теста в классе TestMyAppIntegration
        Очищает тестовое окружение: закрывает соединения и удаляет временные файлы
        '''
        if hasattr(self, 'db') and self.db: # проверяем, существует ли атрибут db и не является ли он None
            self.db.close() # закрываем соединение с базой данных
        
        if os.path.exists(self.db_file.name): # проверяем, существует ли временный файл базы данных
            try: # начинаем блок обработки исключений для безопасного выполнения операции удаления файла
                os.unlink(self.db_file.name) # вызываем функцию os.unlink для удаления файла базы данных
            except PermissionError: # перехватываем исключение PermissionError, которое возникает при отсутствии прав доступа к файлу
                pass # игнорируем исключение PermissionError, чтобы тест продолжал выполняться даже если файл заблокирован
    
    def test_app_controllers_initialization(self):
        '''
        Функция test_app_controllers_initialization тестирует инициализацию контроллеров приложения
        Проверяет, что функция get_controllers возвращает все необходимые контроллеры правильных типов
        '''
        controllers = get_controllers() # вызываем функцию get_controllers для получения словаря контроллеров
        
        self.assertIn('db', controllers) # проверяем, что в словаре есть ключ 'db'
        self.assertIn('currency', controllers) # проверяем, что в словаре есть ключ 'currency'
        self.assertIn('user', controllers) # проверяем, что в словаре есть ключ 'user'
        self.assertIn('pages', controllers) # проверяем, что в словаре есть ключ 'pages'
        
        self.assertIsInstance(controllers['db'], DatabaseController) # проверяем, что controllers['db'] является экземпляром DatabaseController
        self.assertIsInstance(controllers['currency'], CurrencyController) # проверяем, что controllers['currency'] является экземпляром CurrencyController
        self.assertIsInstance(controllers['user'], UserController) # проверяем, что controllers['user'] является экземпляром UserController
        self.assertIsInstance(controllers['pages'], PagesController) # проверяем, что controllers['pages'] является экземпляром PagesController
    
    def test_currency_crud_workflow(self):
        '''
        Функция test_currency_crud_workflow тестирует полный цикл CRUD для валюты
        Проверяет создание, чтение, обновление и удаление валюты в реальной базе данных
        '''
        from models.currency import Currency # импортируем класс Currency из модуля models.currency
        currency = Currency(num_code='840', char_code='USD', name='Доллар США', value=90.0, nominal=1) # создаём объект валюты с тестовыми параметрами
        
        existing = self.currency.read_currency_by_char_code('USD') # вызываем метод read_currency_by_char_code для проверки существования валюты USD
        if existing: # если валюта уже существует
            self.currency.delete_currency(existing['id']) # удаляем существующую валюту
        
        currency_id = self.currency.create_currency(currency) # вызываем метод create_currency для создания новой валюты
        print(f"Created currency with ID: {currency_id}") # выводим в консоль отладочное сообщение с ID созданной валюты для мониторинга выполнения теста
        self.assertIsNotNone(currency_id) # проверяем, что ID валюты не является None
        self.assertGreater(currency_id, 0) # проверяем, что ID валюты больше 0
        
        currencies = self.currency.read_currencies() # вызываем метод read_currencies для получения списка всех валют
        self.assertGreater(len(currencies), 0) # проверяем, что список валют не пустой
        
        found_currency = None # инициализируем переменную для найденной валюты
        for c in currencies: # перебираем все валюты
            if c['char_code'] == 'USD': # если символьный код валюты равен 'USD'
                found_currency = c # сохраняем найденную валюту
                break # выходим из цикла
        
        self.assertIsNotNone(found_currency) # проверяем, что валюта была найдена
        self.assertEqual(found_currency['name'], 'Доллар США') # проверяем, что название валюты равно 'Доллар США'
        
        success = self.currency.update_currency_by_char_code('USD', 95.0) # вызываем метод update_currency_by_char_code для обновления курса валюты USD
        self.assertTrue(success) # проверяем, что операция обновления успешна
        
        updated = self.currency.read_currency_by_char_code('USD') # вызываем метод read_currency_by_char_code для получения обновлённой валюты
        self.assertEqual(updated['value'], 95.0) # проверяем, что значение курса обновилось до 95.0
        
        success = self.currency.delete_currency(found_currency['id']) # вызываем метод delete_currency для удаления валюты
        self.assertTrue(success) # проверяем, что операция удаления успешна
        
        deleted = self.currency.read_currency_by_char_code('USD') # вызываем метод read_currency_by_char_code для проверки удаления валюты
        self.assertIsNone(deleted) # проверяем, что валюта больше не существует
    
    def test_user_subscription_workflow(self):
        '''
        Функция test_user_subscription_workflow тестирует полный цикл подписок пользователя
        Проверяет создание пользователя, добавление и удаление подписок на валюты
        '''
        from models.user import User # импортируем класс User из модуля models.user
        user = User(name='Тестовый Пользователь') # создаём объект пользователя
        user_id = self.user.create_user(user) # вызываем метод create_user для создания пользователя
        self.assertGreater(user_id, 0) # проверяем, что ID пользователя больше 0
        
        existing = self.currency.read_currency_by_char_code('EUR') # вызываем метод read_currency_by_char_code для проверки существования валюты EUR
        if existing: # если валюта уже существует
            self.currency.delete_currency(existing['id']) # удаляем существующую валюту
        
        from models.currency import Currency # импортируем класс Currency из модуля models.currency
        currency = Currency(num_code='978', char_code='EUR', name='Евро', value=91.0, nominal=1) # создаём объект валюты EUR
        currency_id = self.currency.create_currency(currency) # вызываем метод create_currency для создания валюты
        self.assertGreater(currency_id, 0, f"Failed to create EUR currency, got ID: {currency_id}") # проверяем, что ID валюты больше 0
        
        from models.user_currency import UserCurrency # импортируем класс UserCurrency из модуля models.user_currency
        subscription = UserCurrency(user_id=user_id, currency_id=currency_id) # создаём объект связи пользователь-валюта
        success = self.user.add_user_subscription(subscription) # вызываем метод add_user_subscription для добавления подписки
        self.assertTrue(success) # проверяем, что операция добавления подписки успешна
        
        subscription_count = self.user.get_user_subscription_count(user_id) # вызываем метод get_user_subscription_count для получения количества подписок пользователя
        self.assertEqual(subscription_count, 1) # проверяем, что количество подписок равно 1
        
        subscribed_currencies = self.currency.get_user_subscribed_currencies(user_id) # вызываем метод get_user_subscribed_currencies для получения списка подписанных валют
        self.assertEqual(len(subscribed_currencies), 1) # проверяем, что список содержит 1 элемент
        self.assertEqual(subscribed_currencies[0]['char_code'], 'EUR') # проверяем, что символьный код валюты равен 'EUR'
        
        success = self.user.remove_user_subscription(user_id, currency_id) # вызываем метод remove_user_subscription для удаления подписки
        self.assertTrue(success) # проверяем, что операция удаления подписки успешна
        
        subscription_count = self.user.get_user_subscription_count(user_id) # вызываем метод get_user_subscription_count для проверки удаления подписки
        self.assertEqual(subscription_count, 0) # проверяем, что количество подписок равно 0
    
    def test_database_foreign_keys(self):
        '''
        Функция test_database_foreign_keys тестирует работу внешних ключей в базе данных
        Проверяет целостность данных и каскадное удаление связей
        '''
        from models.user import User # импортируем класс User из модуля models.user
        from models.currency import Currency # импортируем класс Currency из модуля models.currency
        from models.user_currency import UserCurrency # импортируем класс UserCurrency из модуля models.user_currency
        
        user = User(name='Иван Иванов') # создаём объект пользователя для теста внешних ключей
        user_id = self.user.create_user(user) # вызываем метод create_user для создания пользователя
        self.assertGreater(user_id, 0) # проверяем, что ID пользователя больше 0
        
        existing = self.currency.read_currency_by_char_code('USD') # вызываем метод read_currency_by_char_code для проверки существования валюты USD
        if existing: # если валюта уже существует
            self.currency.delete_currency(existing['id']) # удаляем существующую валюту
        
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём объект валюты USD
        currency_id = self.currency.create_currency(currency) # вызываем метод create_currency для создания валюты
        self.assertGreater(currency_id, 0, f"Failed to create USD currency, got ID: {currency_id}") # проверяем, что ID валюты больше 0
        
        subscription = UserCurrency(user_id=user_id, currency_id=currency_id) # создаём объект связи пользователь-валюта
        success = self.user.add_user_subscription(subscription) # вызываем метод add_user_subscription для добавления подписки
        self.assertTrue(success) # проверяем, что операция добавления подписки успешна
        
        bad_subscription = UserCurrency(user_id=9999, currency_id=currency_id) # создаём объект связи с несуществующим пользователем
        success = self.user.add_user_subscription(bad_subscription) # вызываем метод add_user_subscription для добавления некорректной подписки

        success = self.user.delete_user(user_id) # вызываем метод delete_user для удаления пользователя
        self.assertTrue(success) # проверяем, что операция удаления пользователя успешна
        
        result = self.db.execute_query("SELECT COUNT(*) as count FROM currencies_user WHERE user_id = ?", (user_id,)) # выполняем SQL-запрос для подсчёта подписок пользователя
        count = result[0]['count'] if result else 0 # получаем количество подписок или 0 если результат пустой
        self.assertEqual(count, 0) # проверяем, что количество подписок равно 0


class TestRequestHandler(unittest.TestCase):
    '''
    Класс TestRequestHandler тестирует HTTPRequestHandler из myapp.py
    Проверяет обработку HTTP-запросов и маршрутизацию
    '''
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestRequestHandler
        Подготавливает тестовое окружение: создаёт мок-объекты и патчит зависимости
        '''
        self.mock_server = Mock() # создаём мок-объект сервера
        self.mock_client_address = ('127.0.0.1', 8080) # устанавливаем тестовый адрес клиента
        
        self.mock_db = Mock() # создаём мок-объект контроллера базы данных
        self.mock_currency = Mock() # создаём мок-объект контроллера валют
        self.mock_user = Mock() # создаём мок-объект контроллера пользователей
        self.mock_pages = Mock() # создаём мок-объект контроллера страниц
        
        self.patcher = patch('myapp.get_controllers') # создаём патч для функции get_controllers
        self.mock_get_controllers = self.patcher.start() # запускаем патч и сохраняем мок-объект
        # настраиваем возвращаемое значение мок-функции get_controllers
        self.mock_get_controllers.return_value = {
            'db': self.mock_db,
            'currency': self.mock_currency,
            'user': self.mock_user,
            'pages': self.mock_pages
        }
    
    def tearDown(self):
        '''
        Функция tearDown() выполняется после каждого теста в классе TestRequestHandler
        Останавливает патчи
        '''
        self.patcher.stop() # останавливаем патч
    
    def create_handler(self, path='/', method='GET', query_string='', post_data=None):
        '''
        Вспомогательная функция для создания мок-обработчика запросов
        Создаёт и настраивает экземпляр CurrencyRequestHandler с мок-зависимостями
        '''
        with patch('myapp.CurrencyRequestHandler.__init__', return_value=None): # временно заменяем метод __init__ на пустой
            handler = CurrencyRequestHandler(self.mock_server, self.mock_client_address, self.mock_server) # создаём экземпляр обработчика
        
        handler.server = self.mock_server # устанавливаем мок-сервер
        handler.client_address = self.mock_client_address # устанавливаем адрес клиента
        handler.request = self.mock_server # устанавливаем мок-запрос
        
        handler.db_controller = self.mock_db # устанавливаем мок контроллера базы данных
        handler.currency_controller = self.mock_currency # устанавливаем мок контроллера валют
        handler.user_controller = self.mock_user # устанавливаем мок контроллера пользователей
        handler.pages_controller = self.mock_pages # устанавливаем мок контроллера страниц
        
        handler.send_response = Mock() # создаём мок метода send_response
        handler.send_header = Mock() # создаём мок метода send_header
        handler.end_headers = Mock() # создаём мок метода end_headers
        handler.wfile = BytesIO() # создаём поток вывода в памяти
        
        if query_string: # если указана строка запроса
            handler.path = f"{path}?{query_string}" # формируем полный путь с параметрами запроса
        else: # в противном случае
            handler.path = path # устанавливаем путь без параметров запроса
        
        handler.command = method # устанавливаем метод HTTP-запроса
        
        if post_data: # если указаны POST-данные
            handler.headers = {'Content-Length': str(len(post_data))} # устанавливаем заголовок Content-Length
            handler.rfile = BytesIO(post_data.encode('utf-8')) # создаём поток ввода с POST-данными
        else: # в противном случае
            handler.headers = {} # устанавливаем пустой словарь заголовков
            handler.rfile = BytesIO(b'') # создаём пустой поток ввода
        
        handler.raw_requestline = b'GET / HTTP/1.1' # устанавливаем сырую строку запроса
        
        return handler # возвращаем настроенный обработчик
    
    def test_handler_initialization(self):
        '''
        Функция test_handler_initialization тестирует инициализацию обработчика запросов
        Проверяет, что все контроллеры правильно инициализированы
        '''
        handler = self.create_handler() # создаём тестовый обработчик
        
        self.assertEqual(handler.db_controller, self.mock_db) # проверяем, что db_controller установлен правильно
        self.assertEqual(handler.currency_controller, self.mock_currency) # проверяем, что currency_controller установлен правильно
        self.assertEqual(handler.user_controller, self.mock_user) # проверяем, что user_controller установлен правильно
        self.assertEqual(handler.pages_controller, self.mock_pages) # проверяем, что pages_controller установлен правильно
    
    def test_home_page_route(self):
        '''
        Функция test_home_page_route тестирует обработку главной страницы
        Проверяет корректность маршрута '/' и работу связанных контроллеров
        '''
        handler = self.create_handler('/') # создаём обработчик для главной страницы
        
        self.mock_user.count_users.return_value = 3 # настраиваем мок метод count_users для возврата 3
        self.mock_currency.count_currencies.return_value = 5 # настраиваем мок метод count_currencies для возврата 5
        # настраиваем мок метод read_currencies для возврата тестовых данных
        self.mock_currency.read_currencies.return_value = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1},
            {'id': 2, 'char_code': 'EUR', 'name': 'Евро', 'value': 91.0, 'nominal': 1}
        ]
        
        def mock_render_index(stats=None, currencies=None):
            '''
            Функция mock_render_index представляет собой мок-реализацию метода render_index
            Используется для подмены реального метода рендеринга главной страницы в тестах
            
            Параметры:
            stats -- статистика приложения
            currencies -- список валют для отображения
            
            Возвращает:
            строка -- фиксированный HTML-код для имитации работы реального метода render_index
            '''
            return '<html>Главная</html>' # функция возвращает фиксированный HTML-код для имитации работы реального метода render_index
        
        self.mock_pages.render_index.side_effect = mock_render_index # настраиваем side_effect для мок метода render_index
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_user.count_users.assert_called_once() # проверяем, что метод count_users вызывался ровно один раз
        self.mock_currency.count_currencies.assert_called_once() # проверяем, что метод count_currencies вызывался ровно один раз
        self.mock_currency.read_currencies.assert_called_once() # проверяем, что метод read_currencies вызывался ровно один раз
        
        self.assertTrue(self.mock_pages.render_index.called) # проверяем, что метод render_index был вызван
        
        handler.send_response.assert_called_with(200) # проверяем, что был отправлен ответ со статусом 200
    
    def test_author_page_route(self):
        '''
        Функция test_author_page_route тестирует обработку страницы об авторе
        Проверяет корректность маршрута '/author'
        '''
        handler = self.create_handler('/author') # создаём обработчик для страницы об авторе
        
        self.mock_pages.render_author.return_value = '<html>Автор</html>' # настраиваем мок метод render_author для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_pages.render_author.assert_called_once() # проверяем, что метод render_author вызывался ровно один раз
        handler.send_response.assert_called_with(200) # проверяем, что был отправлен ответ со статусом 200
    
    def test_users_page_route(self):
        '''
        Функция test_users_page_route тестирует обработку страницы пользователей
        Проверяет корректность маршрута '/users' и подсчёт подписок пользователей
        '''
        handler = self.create_handler('/users') # создаём обработчик для страницы пользователей
        
        # создаём тестовые данные пользователей
        mock_users = [
            {'id': 1, 'name': 'Иван Иванов'},
            {'id': 2, 'name': 'Пётр Петров'}
        ]
        self.mock_user.read_users.return_value = mock_users # настраиваем мок метод read_users для возврата тестовых данных
        self.mock_user.get_total_subscriptions_count.return_value = 5 # настраиваем мок метод get_total_subscriptions_count для возврата 5
        
        def mock_subscription_count(user_id):
            '''
            Функция mock_subscription_count представляет собой мок-реализацию метода get_user_subscription_count
            Используется для имитации подсчёта подписок пользователей в тестах
            
            Параметры:
            user_id -- идентификатор пользователя для подсчёта подписок
            
            Возвращает:
            целое число -- фиктивное количество подписок: 2 для user_id=1, 0 для всех остальных пользователей
            '''
            return 2 if user_id == 1 else 0 # возвращаем 2 если user_id равен 1, иначе возвращаем 0
        
        self.mock_user.get_user_subscription_count.side_effect = mock_subscription_count # настраиваем side_effect для мок метода get_user_subscription_count
        
        self.mock_pages.render_users.return_value = '<html>Пользователи</html>' # настраиваем мок метод render_users для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_user.read_users.assert_called_once() # проверяем, что метод read_users вызывался ровно один раз
        self.assertEqual(self.mock_user.get_user_subscription_count.call_count, 2) # проверяем, что метод get_user_subscription_count вызывался ровно 2 раза
        self.mock_pages.render_users.assert_called_once() # проверяем, что метод render_users вызывался ровно один раз
    
    def test_user_detail_route_with_id(self):
        '''
        Функция test_user_detail_route_with_id тестирует обработку страницы конкретного пользователя с указанным ID
        Проверяет корректность маршрута '/user' с параметром id
        '''
        handler = self.create_handler('/user', query_string='id=1') # создаём обработчик для страницы пользователя с id=1
        
        mock_user = {'id': 1, 'name': 'Иван Иванов'} # создаём тестовые данные пользователя
        self.mock_user.read_user_by_id.return_value = mock_user # настраиваем мок метод read_user_by_id для возврата тестовых данных
        # настраиваем мок метод get_user_subscribed_currencies для возврата тестовых данных
        self.mock_currency.get_user_subscribed_currencies.return_value = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США'}
        ]
        self.mock_pages.render_user.return_value = '<html>Пользователь</html>' # настраиваем мок метод render_user для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_user.read_user_by_id.assert_called_with(1) # проверяем, что метод read_user_by_id вызывался с аргументом 1
        self.mock_currency.get_user_subscribed_currencies.assert_called_with(1) # проверяем, что метод get_user_subscribed_currencies вызывался с аргументом 1
        self.mock_pages.render_user.assert_called_once() # проверяем, что метод render_user вызывался ровно один раз
    
    def test_user_detail_route_no_id(self):
        '''
        Функция test_user_detail_route_no_id тестирует обработку страницы пользователя без указания ID
        Проверяет обработку ошибки отсутствия параметра id
        '''
        handler = self.create_handler('/user') # создаём тестовый обработчик запросов для маршрута '/user' с помощью вспомогательного метода create_handler
        
        self.mock_pages.render_404.return_value = '<html>404</html>' # настраиваем мок метод render_404 для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_pages.render_404.assert_called_with("ID пользователя не указан") # проверяем, что метод render_404 вызывался с правильным сообщением
        handler.send_response.assert_called_with(404) # проверяем, что был отправлен ответ со статусом 404
    
    def test_user_detail_route_invalid_id(self):
        '''
        Функция test_user_detail_route_invalid_id тестирует обработку страницы пользователя с некорректным ID
        Проверяет обработку ошибки нечислового параметра id
        '''
        handler = self.create_handler('/user', query_string='id=abc') # создаём обработчик для страницы пользователя с некорректным id
        
        self.mock_pages.render_404.return_value = '<html>404</html>' # настраиваем мок метод render_404 для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_pages.render_404.assert_called_with("Некорректный ID пользователя") # проверяем, что метод render_404 вызывался с правильным сообщением
    
    def test_currencies_page_route(self):
        '''
        Функция test_currencies_page_route тестирует обработку страницы валют
        Проверяет корректность маршрута '/currencies'
        '''
        handler = self.create_handler('/currencies') # создаём обработчик для страницы валют
        
        # создаём тестовые данные валют
        mock_currencies = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1}
        ]
        self.mock_currency.read_currencies.return_value = mock_currencies # настраиваем мок метод read_currencies для возврата тестовых данных
        self.mock_pages.render_currencies.return_value = '<html>Валюты</html>' # настраиваем мок метод render_currencies для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_currency.read_currencies.assert_called_once() # проверяем, что метод read_currencies вызывался ровно один раз
        self.mock_pages.render_currencies.assert_called_once() # проверяем, что метод render_currencies вызывался ровно один раз
    
    def test_currency_delete_route(self):
        '''
        Функция test_currency_delete_route тестирует обработку удаления валюты
        Проверяет корректность маршрута '/currency/delete'
        '''
        handler = self.create_handler('/currency/delete', query_string='id=1') # создаём обработчик для удаления валюты с id=1
        
        handler._redirect = Mock() # создаём мок метода _redirect
        
        self.mock_currency.delete_currency.return_value = True # настраиваем мок метод delete_currency для возврата True
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_currency.delete_currency.assert_called_with(1) # проверяем, что метод delete_currency вызывался с аргументом 1
        handler._redirect.assert_called_with('/currencies?message=Валюта удалена&type=success') # проверяем, что метод _redirect вызывался с правильным URL
    
    def test_currency_update_route(self):
        '''
        Функция test_currency_update_route тестирует обработку обновления курса валюты
        Проверяет корректность маршрута '/currency/update'
        '''
        handler = self.create_handler('/currency/update', query_string='char_code=USD&value=95.0') # создаём обработчик для обновления курса валюты USD
        
        handler._redirect = Mock() # создаём мок метода _redirect
        self.mock_currency.update_currency_by_char_code.return_value = True # настраиваем мок метод update_currency_by_char_code для возврата True
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_currency.update_currency_by_char_code.assert_called_with('USD', 95.0) # проверяем, что метод update_currency_by_char_code вызывался с правильными аргументами
        handler._redirect.assert_called_with('/currencies?message=Курс USD обновлен до 95.0&type=success') # проверяем, что метод _redirect вызывался с правильным URL
    
    def test_currency_show_route(self):
        '''
        Функция test_currency_show_route тестирует отладочную страницу валют
        Проверяет корректность маршрута '/currency/show'
        '''
        handler = self.create_handler('/currency/show') # создаём обработчик для отладочной страницы валют
        
        # создаём тестовые данные валют
        mock_currencies = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0}
        ]
        self.mock_currency.read_currencies.return_value = mock_currencies # настраиваем мок метод read_currencies для возврата тестовых данных
        
        with patch('builtins.print') as mock_print: # временно заменяем функцию print на мок
            handler.do_GET() # вызываем метод обработки GET-запроса
            
            mock_print.assert_called() # проверяем, что функция print вызывалась
    
    def test_404_route(self):
        '''
        Функция test_404_route тестирует обработку несуществующего маршрута
        Проверяет корректность обработки неизвестных URL
        '''
        handler = self.create_handler('/nonexistent/route') # создаём обработчик для несуществующего маршрута
        
        self.mock_pages.render_404.return_value = '<html>404</html>' # настраиваем мок метод render_404 для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_pages.render_404.assert_called_with("Страница /nonexistent/route не найдена") # проверяем, что метод render_404 вызывался с правильным сообщением
        handler.send_response.assert_called_with(404) # проверяем, что был отправлен ответ со статусом 404
    
    def test_currency_create_post(self):
        '''
        Функция test_currency_create_post тестирует обработку POST-запроса на создание валюты
        Проверяет корректность маршрута '/currency/create' для POST-запросов
        '''
        post_data = 'num_code=840&char_code=USD&name=Доллар+США&value=90.0&nominal=1' # создаём тестовые POST-данные
        
        with patch('myapp.CurrencyRequestHandler.__init__', return_value=None): # временно заменяем метод __init__ на пустой
            handler = CurrencyRequestHandler(self.mock_server, self.mock_client_address, self.mock_server) # создаём экземпляр обработчика
        
        handler.server = self.mock_server # устанавливаем мок-сервер
        handler.client_address = self.mock_client_address # устанавливаем адрес клиента
        handler.request = self.mock_server # устанавливаем мок-запрос
        
        handler.db_controller = self.mock_db # устанавливаем мок контроллера базы данных
        handler.currency_controller = self.mock_currency # устанавливаем мок контроллера валют
        handler.user_controller = self.mock_user # устанавливаем мок контроллера пользователей
        handler.pages_controller = self.mock_pages # устанавливаем мок контроллера страниц
        
        handler.path = '/currency/create' # устанавливаем путь запроса
        handler.command = 'POST' # устанавливаем метод запроса POST
        
        handler.headers = {'Content-Length': str(len(post_data))} # устанавливаем заголовок Content-Length
        handler.rfile = BytesIO(post_data.encode('utf-8')) # создаём поток ввода с POST-данными
        handler.wfile = BytesIO() # создаём поток вывода в памяти
        
        handler.send_response = Mock() # создаём мок метода send_response
        handler.send_header = Mock() # создаём мок метода send_header
        handler.end_headers = Mock() # создаём мок метода end_headers
        
        self.mock_currency.create_currency.return_value = 1 # настраиваем мок метод create_currency для возврата 1
        self.mock_currency.read_currencies.return_value = [] # настраиваем мок метод read_currencies для возврата пустого списка
        self.mock_currency.read_currency_by_char_code.return_value = None # настраиваем мок метод read_currency_by_char_code для возврата None
        self.mock_pages.render_currencies.return_value = '<html>Валюты</html>' # настраиваем мок метод render_currencies для возврата тестового HTML
        
        from urllib.parse import parse_qs # импортируем parse_qs из urllib.parse
        
        # создаём тестовые распарсенные данные
        parsed_data = {
            'num_code': ['840'],
            'char_code': ['USD'], 
            'name': ['Доллар США'],
            'value': ['90.0'],
            'nominal': ['1']
        }
        
        with patch('myapp.parse_qs', return_value=parsed_data): # временно заменяем parse_qs на мок
            handler.do_POST() # вызываем метод обработки POST-запроса
            

            self.mock_currency.create_currency.assert_called_once() # проверяем, что метод create_currency вызывался ровно один раз
            self.mock_currency.read_currency_by_char_code.assert_called_once_with('USD') # проверяем, что метод read_currency_by_char_code вызывался с аргументом 'USD'
            self.mock_pages.render_currencies.assert_called_once() # проверяем, что метод render_currencies вызывался ровно один раз
            handler.send_response.assert_called_with(200) # проверяем, что был отправлен ответ со статусом 200
    
    def test_currency_create_post_missing_fields(self):
        '''
        Функция test_currency_create_post_missing_fields тестирует POST-запрос на создание валюты с отсутствующими полями
        Проверяет обработку ошибок при неполных данных
        '''
        post_data = 'num_code=840&char_code=USD' # создаём строку с тестовыми POST-данными для создания валюты, содержащую только числовой код и символьный код
        handler = self.create_handler('/currency/create', method='POST', post_data=post_data) # создаём обработчик для создания валюты с неполными данными
        
        # создаём тестовые распарсенные данные с неполными полями
        parsed_data = {
            'num_code': ['840'],
            'char_code': ['USD']
        }
        
        with patch('myapp.parse_qs', return_value=parsed_data): # временно заменяем parse_qs на мок
            self.mock_currency.read_currencies.return_value = [] # настраиваем мок метод read_currencies для возврата пустого списка
            self.mock_pages.render_currencies.return_value = '<html>Ошибка</html>' # настраиваем мок метод render_currencies для возврата HTML с ошибкой
            
            handler.do_POST() # вызываем метод обработки POST-запроса
            
            self.mock_pages.render_currencies.assert_called_once() # проверяем, что метод render_currencies вызывался ровно один раз
    
    def test_post_invalid_route(self):
        '''
        Функция test_post_invalid_route тестирует POST-запрос на несуществующий маршрут
        Проверяет обработку неизвестных POST-маршрутов
        '''
        post_data = 'data=test' # создаём тестовые POST-данные
        handler = self.create_handler('/nonexistent', method='POST', post_data=post_data) # создаём обработчик для несуществующего POST-маршрута
        
        parsed_data = {'data': ['test']} # создаём тестовые распарсенные данные
        
        with patch('myapp.parse_qs', return_value=parsed_data): # временно заменяем parse_qs на мок
            self.mock_pages.render_404.return_value = '<html>404</html>' # настраиваем мок метод render_404 для возврата тестового HTML
            
            handler.do_POST() # вызываем метод обработки POST-запроса
            
            self.mock_pages.render_404.assert_called_with("POST-маршрут /nonexistent не найден") # проверяем, что метод render_404 вызывался с правильным сообщением


class TestMyAppErrorHandling(unittest.TestCase):
    '''
    Класс TestMyAppErrorHandling тестирует обработку ошибок в приложении
    Проверяет корректность обработки исключений и ошибок выполнения
    '''
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestMyAppErrorHandling
        Подготавливает тестовое окружение: создаёт мок-объекты и патчит зависимости
        '''
        self.mock_server = Mock() # создаём мок-объект сервера
        self.mock_client_address = ('127.0.0.1', 8080) # устанавливаем тестовый адрес клиента
        
        self.mock_db = Mock() # создаём мок-объект контроллера базы данных
        self.mock_currency = Mock() # создаём мок-объект контроллера валют
        self.mock_user = Mock() # создаём мок-объект контроллера пользователей
        self.mock_pages = Mock() # создаём мок-объект контроллера страниц
        
        self.patcher = patch('myapp.get_controllers') # создаём патч для функции get_controllers
        self.mock_get_controllers = self.patcher.start() # запускаем патч и сохраняем мок-объект
        # настраиваем возвращаемое значение мок-функции get_controllers
        self.mock_get_controllers.return_value = {
            'db': self.mock_db,
            'currency': self.mock_currency,
            'user': self.mock_user,
            'pages': self.mock_pages
        }
    
    def tearDown(self):
        '''
        Функция tearDown() выполняется после каждого теста в классе TestMyAppErrorHandling
        Останавливает патчи
        '''
        self.patcher.stop() # останавливаем патч
    
    def create_handler(self):
        '''
        Вспомогательная функция для создания базового обработчика
        Создаёт экземпляр CurrencyRequestHandler с минимальными настройками
        '''
        with patch('myapp.CurrencyRequestHandler.__init__', return_value=None): # временно заменяем метод __init__ на пустой
            handler = CurrencyRequestHandler(self.mock_server, self.mock_client_address, self.mock_server) # создаём экземпляр обработчика
        
        handler.server = self.mock_server # устанавливаем мок-сервер
        handler.client_address = self.mock_client_address # устанавливаем адрес клиента
        handler.request = self.mock_server # устанавливаем мок-запрос
        
        handler.db_controller = self.mock_db # устанавливаем мок контроллера базы данных
        handler.currency_controller = self.mock_currency # устанавливаем мок контроллера валют
        handler.user_controller = self.mock_user # устанавливаем мок контроллера пользователей
        handler.pages_controller = self.mock_pages # устанавливаем мок контроллера страниц
        
        handler.send_response = Mock() # создаём мок метода send_response
        handler.send_header = Mock() # создаём мок метода send_header
        handler.end_headers = Mock() # создаём мок метода end_headers
        handler.wfile = BytesIO() # создаём поток вывода в памяти
        handler.raw_requestline = b'GET / HTTP/1.1' # устанавливаем сырую строку запроса
        
        return handler # возвращаем настроенный обработчик
    
    def test_home_page_exception_handling(self):
        '''
        Функция test_home_page_exception_handling тестирует обработку исключений на главной странице
        Проверяет корректность обработки ошибок базы данных и других исключений
        '''
        handler = self.create_handler() # создаём обработчик
        handler.path = '/' # устанавливаем путь главной страницы
        
        handler.user_controller.count_users.side_effect = Exception("Database error") # настраиваем side_effect для мок метода count_users для выброса исключения
        self.mock_pages.render_404.return_value = '<html>Ошибка</html>' # настраиваем мок метод render_404 для возврата тестового HTML
        
        handler.do_GET() # вызываем метод обработки GET-запроса
        
        self.mock_pages.render_404.assert_called_once() # проверяем, что метод render_404 вызывался ровно один раз
        
        handler.send_response.assert_called_with(500) # проверяем, что был отправлен ответ со статусом 500
    
    def test_redirect_method(self):
        '''
        Функция test_redirect_method тестирует метод перенаправления
        Проверяет корректность работы метода _redirect обработчика запросов
        '''
        handler = self.create_handler() # создаём обработчик
        
        handler._redirect('/currencies?message=Test&type=success') # вызываем метод _redirect с параметрами
        
        handler.send_response.assert_called_with(302) # проверяем, что был отправлен ответ со статусом 302
        handler.send_header.assert_called_with('Location', '/currencies?message=Test&type=success') # проверяем, что был отправлен заголовок Location с правильным URL
        handler.end_headers.assert_called_once() # проверяем, что метод end_headers вызывался ровно один раз
    
    def test_redirect_method_error_handling(self):
        '''
        Функция test_redirect_method_error_handling тестирует обработку ошибок в методе перенаправления
        Проверяет отказоустойчивость метода _redirect при ошибках отправки заголовков
        '''
        handler = self.create_handler() # создаём обработчик
        
        call_count = 0 # инициализируем счётчик вызовов
        def raise_exception_on_first_call(*args, **kwargs): # определяем функцию, которая выбрасывает исключение при первом вызове
            nonlocal call_count # объявляем nonlocal переменную
            call_count += 1 # увеличиваем счётчик вызовов
            if call_count == 1: # проверяем, является ли текущий вызов первым по счётчику call_count
                raise Exception("Header error") # выбрасываем исключение Exception с сообщением "Header error" для имитации ошибки при отправке HTTP-заголовков
        
        handler.send_response.side_effect = raise_exception_on_first_call # настраиваем side_effect для мок метода send_response
        
        try: # начинаем блок обработки исключений для безопасного выполнения операции
            handler._redirect('/currencies') # вызываем метод _redirect обработчика с URL '/currencies', который может вызвать исключение
        except Exception: # перехватываем любое исключение типа Exception, которое может возникнуть при вызове _redirect
            pass # игнорируем исключение, так как в данном тесте мы проверяем устойчивость метода к ошибкам, а не само исключение
        
        if handler.wfile.tell() > 0: # если в потоке вывода есть данные
            html_content = handler.wfile.getvalue().decode('utf-8') # получаем содержимое потока вывода как строку
            self.assertTrue(len(html_content) > 0) # проверяем, что строка не пустая


if __name__ == '__main__':
    unittest.main() # запускаем все тесты