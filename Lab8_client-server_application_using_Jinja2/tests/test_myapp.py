import unittest # импортируем unittest для создания и запуска тестов
from unittest.mock import patch, MagicMock # импортируем patch и MagicMock для создания мок-объектов и подмены реальных функций
import sys # импортируем sys для работы с системными путями и управлением системными параметрами
import os # импортируем os для работы с операционной системой и файловыми путями
import importlib # импортируем importlib для динамической перезагрузки модулей


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # добавляем родительскую папку текущего файла в системный путь Python, чтобы можно было импортировать модули проекта

import myapp # импортируем основной модуль приложения для тестирования


class TestModels(unittest.TestCase):
    '''
    Класс TestModels содержит тесты для моделей данных приложения
    проверяет корректность работы основных моделей: Author, App, User, Currency, UserCurrency
    '''
    
    def test_author_model(self):
        '''
        Тестирование модели Author
        '''
        from models import Author # импортируем модель Author из модуля models
        author = Author(name="Романова Анна", group="P3120") # создаём экземпляр класса Author с тестовыми данными
        self.assertEqual(author.name, "Романова Анна") # проверяем, что имя автора соответствует ожидаемому значению
        self.assertEqual(author.group, "P3120") # проверяем, что группа автора соответствует ожидаемому значению
    
    def test_app_model(self):
        '''
        Тестирование модели App
        '''
        from models import App, Author # импортируем модели App и Author из модуля models
        author = Author(name="Иван Иванов", group="U978") # создаём тестового автора
        app = App(name="Банка банка", version="1.2.3", author=author) # создаём тестовое приложение
        self.assertEqual(app.name, "Банка банка") # проверяем, что название приложения соответствует ожидаемому значению
        self.assertEqual(app.version, "1.2.3") # проверяем, что версия приложения соответствует ожидаемому значению
        self.assertEqual(app.author.name, "Иван Иванов") # проверяем, что автор приложения имеет правильное имя
        self.assertEqual(app.author.group, "U978") # проверяем, что автор приложения имеет правильную группу
    
    def test_user_model(self):
        '''
        Тестирование модели User
        '''
        from models import User # импортируем модель User из модуля models
        user = User(id=1, name="Вася Васечкин") # создаём тестового пользователя
        self.assertEqual(user.id, 1) # проверяем, что идентификатор пользователя соответствует ожидаемому значению
        self.assertEqual(user.name, "Вася Васечкин") # проверяем, что имя пользователя соответствует ожидаемому значению
    
    def test_currency_model(self):
        '''
        Тестирование модели Currency
        '''
        from models import Currency # импортируем модель Currency из модуля models
        currency = Currency( # создаём тестовую валюту
            id="R01235", # идентификатор валюты
            char_code="USD", # буквенный код валюты
            num_code="840", # цифровой код валюты
            name="Доллар США", # название валюты
            value=75.5, # курс валюты
            nominal=1 # номинал валюты
        )
        self.assertEqual(currency.char_code, "USD") # проверяем, что буквенный код валюты соответствует ожидаемому значению
        self.assertEqual(currency.name, "Доллар США") # проверяем, что название валюты соответствует ожидаемому значению
        self.assertEqual(currency.value, 75.5) # проверяем, что курс валюты соответствует ожидаемому значению
        self.assertEqual(currency.nominal, 1) # проверяем, что номинал валюты соответствует ожидаемому значению
    
    def test_user_currency_model(self):
        '''
        Тестирование модели UserCurrency
        '''
        from models import UserCurrency # импортируем модель UserCurrency из модуля models
        user_currency = UserCurrency(id=1, user_id=1, currency_name="USD") # создаём тестовую связь пользователь-валюта
        self.assertEqual(user_currency.id, 1) # проверяем, что идентификатор связи соответствует ожидаемому значению
        self.assertEqual(user_currency.user_id, 1) # проверяем, что идентификатор пользователя соответствует ожидаемому значению
        self.assertEqual(user_currency.currency_name, "USD") # проверяем, что название валюты соответствует ожидаемому значению


class TestGlobalVariables(unittest.TestCase):
    '''
    Класс TestGlobalVariables содержит тесты глобальных переменных приложения
    проверяет корректность инициализации и содержания основных переменных myapp
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для перезагрузки модуля myapp
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp для изоляции тестов
    
    def test_author_information(self):
        '''
        Тестирование информации об авторе
        '''
        self.assertEqual(myapp.author_inf.name, "Романова Анна Андреевна") # проверяем, что имя автора соответствует ожидаемому значению
        self.assertEqual(myapp.author_inf.group, "P3120") # проверяем, что группа автора соответствует ожидаемому значению
    
    def test_app_information(self):
        '''
        Тестирование информации о приложении
        '''
        self.assertEqual(myapp.myapp.name, "Валютка-минутка!") # проверяем, что название приложения соответствует ожидаемому значению
        self.assertEqual(myapp.myapp.version, "1.0.0") # проверяем, что версия приложения соответствует ожидаемому значению
        self.assertEqual(myapp.myapp.author, myapp.author_inf) # проверяем, что автор приложения соответствует объекту author_inf
    
    def test_users_list(self):
        '''
        Тестирование списка пользователей
        '''
        self.assertEqual(len(myapp.users), 3) # проверяем, что количество пользователей равно 3
        
        user_ids = [user.id for user in myapp.users] # получаем список идентификаторов пользователей
        self.assertListEqual(user_ids, [1, 2, 3]) # проверяем, что идентификаторы пользователей соответствуют ожидаемым значениям
        
        user_names = [user.name for user in myapp.users] # получаем список имён пользователей
        expected_names = ["Алексей Петров", "Даниил Козлов", "Ангелина Иванченко"] # определяем ожидаемые имена пользователей
        for name in expected_names: # проверяем каждое ожидаемое имя
            self.assertIn(name, user_names) # проверяем, что имя присутствует в списке пользователей
    
    def test_user_currencies_relations(self):
        '''
        Тестирование связей между пользователями и валютами
        '''
        valid_user_ids = {user.id for user in myapp.users} # создаём множество допустимых идентификаторов пользователей
        for user_currency in myapp.user_currencies: # проходим по всем связям пользователь-валюта
            self.assertIn(user_currency.user_id, valid_user_ids) # проверяем, что идентификатор пользователя в связи является допустимым
        
        # проверяем статистику подписок
        user_1_subs = len([uc for uc in myapp.user_currencies if uc.user_id == 1]) # считаем количество подписок первого пользователя
        user_2_subs = len([uc for uc in myapp.user_currencies if uc.user_id == 2]) # считаем количество подписок второго пользователя
        user_3_subs = len([uc for uc in myapp.user_currencies if uc.user_id == 3]) # считаем количество подписок третьего пользователя
        
        self.assertEqual(user_1_subs, 2) # проверяем, что первый пользователь имеет 2 подписки (USD, EUR)
        self.assertEqual(user_2_subs, 1) # проверяем, что второй пользователь имеет 1 подписку (CNY)
        self.assertEqual(user_3_subs, 1) # проверяем, что третий пользователь имеет 1 подписку (USD)
    
    def test_file_paths(self):
        '''
        Тестирование путей к файлам
        '''
        self.assertIsInstance(myapp.main_folder_path, str) # проверяем, что путь к основной папке является строкой
        self.assertIsInstance(myapp.templates_folder_path, str) # проверяем, что путь к папке шаблонов является строкой
        self.assertIn('templates', myapp.templates_folder_path) # проверяем, что путь к папке шаблонов содержит 'templates'
    
    def test_env_initialized(self):
        '''
        Тестирование инициализации Jinja2 окружения
        '''
        self.assertIsNotNone(myapp.env) # проверяем, что переменная окружения Jinja2 не является None
        self.assertEqual(type(myapp.env).__name__, 'Environment') # проверяем, что тип переменной окружения является Environment


class TestCurrencyAPI(unittest.TestCase):
    '''
    Класс TestCurrencyAPI содержит тесты для работы с API валют
    проверяет корректность инициализации валют и обработки ошибок API
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для сброса состояния валют и ошибок
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
        myapp.currencies = [] # сбрасываем список валют
        myapp.api_error = None # сбрасываем ошибку API
    
    @patch('myapp.get_currencies') # декоратор @patch для подмены функции get_currencies
    def test_init_currencies_success(self, mock_get_currencies):
        '''
        Тестирование успешной инициализации валют
        '''
        # настраиваем мок-объект для возврата тестовых данных
        mock_get_currencies.return_value = {
            "USD": {"id": "R01235", "num_code": "840", "name": "Доллар США", "value": 75.5, "nominal": 1},
            "EUR": {"id": "R01239", "num_code": "978", "name": "Евро", "value": 90.2, "nominal": 1}
        }
        
        result = myapp.init_currencies() # вызываем функцию инициализации валют
        
        self.assertTrue(result) # проверяем, что результат инициализации True
        self.assertIsNone(myapp.api_error) # проверяем, что ошибка API отсутствует
        self.assertEqual(len(myapp.currencies), 2) # проверяем, что список валют содержит 2 элемента
        
        currency_codes = [c.char_code for c in myapp.currencies] # получаем список кодов валют
        self.assertIn("USD", currency_codes) # проверяем, что список содержит USD
        self.assertIn("EUR", currency_codes) # проверяем, что список содержит EUR
        
        usd_currency = myapp.currencies[0] # получаем первую валюту
        self.assertEqual(usd_currency.char_code, "USD") # проверяем, что код валюты -- "USD"
        self.assertEqual(usd_currency.name, "Доллар США") # проверяем, что название валюты -- "Доллар США"
        self.assertEqual(usd_currency.value, 75.5) # проверяем, что курс валюты -- 75.5
    
    @patch('myapp.get_currencies') # декоратор @patch для подмены функции get_currencies
    def test_init_currencies_failure(self, mock_get_currencies):
        '''
        Тестирование ошибки при инициализации валют
        '''
        mock_get_currencies.side_effect = Exception("Network error") # настраиваем мок-объект для вызова исключения
        
        result = myapp.init_currencies() # вызываем функцию инициализации валют
        
        self.assertFalse(result) # проверяем, что результат инициализации False
        self.assertIsNotNone(myapp.api_error) # проверяем, что ошибка API установлена
        self.assertIn("Ошибка загрузки данных", myapp.api_error) # проверяем, что сообщение об ошибке содержит текст
        self.assertEqual(len(myapp.currencies), 0) # проверяем, что список валют пуст
    
    @patch('myapp.get_currencies') # декоратор @patch для подмены функции get_currencies
    def test_init_currencies_empty_response(self, mock_get_currencies):
        '''
        Тестирование пустого ответа от API
        '''
        mock_get_currencies.return_value = {} # настраиваем мок-объект для возврата пустого словаря
        
        result = myapp.init_currencies() # вызываем функцию инициализации валют
        
        self.assertTrue(result) # проверяем, что результат инициализации True
        self.assertEqual(len(myapp.currencies), 0) # проверяем, что список валют пуст


class TestRequestHandler(unittest.TestCase):
    '''
    Класс TestRequestHandler содержит тесты для обработчика HTTP-запросов
    проверяет корректность работы методов обработчика запросов
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для подготовки данных валют
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
        # инициализируем список валют тестовыми данными
        myapp.currencies = [
            myapp.Currency(id="R01235", char_code="USD", num_code="840", name="Доллар США", value=75.5, nominal=1),
            myapp.Currency(id="R01239", char_code="EUR", num_code="978", name="Евро", value=90.2, nominal=1)
        ]
        myapp.api_error = None # сбрасываем ошибку API
    
    def test_handler_initialization(self):
        '''
        Тестирование инициализации обработчика
        '''
        handler = myapp.CurrencyRequestHandler # получаем класс обработчика запросов
        self.assertTrue(hasattr(handler, 'do_GET')) # проверяем, что класс имеет метод do_GET
        self.assertTrue(hasattr(handler, '_set_headers')) # проверяем, что класс имеет метод _set_headers
        self.assertTrue(hasattr(handler, '_render_template')) # проверяем, что класс имеет метод _render_template
    
    def test_set_headers_method(self):
        '''
        Тестирование метода установки заголовков
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler.send_response = MagicMock() # мокаем метод send_response
        mock_handler.send_header = MagicMock() # мокаем метод send_header
        mock_handler.end_headers = MagicMock() # мокаем метод end_headers
        
        myapp.CurrencyRequestHandler._set_headers(mock_handler) # вызываем метод установки заголовков
        
        mock_handler.send_response.assert_called_once_with(200) # проверяем, что send_response был вызван с кодом 200
        mock_handler.send_header.assert_called_once_with('Content-type', 'text/html; charset=utf-8') # проверяем, что send_header был вызван с правильными заголовками
        mock_handler.end_headers.assert_called_once() # проверяем, что end_headers был вызван один раз
    
    def test_render_template_method(self):
        '''
        Тестирование метода рендеринга шаблона
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        
        with patch('myapp.env') as mock_env: # подменяем переменную окружения Jinja2
            mock_template = MagicMock() # создаём мок-объект шаблона
            mock_template.render.return_value = "<html>Test</html>" # настраиваем метод render для возврата тестового HTML
            mock_env.get_template.return_value = mock_template # настраиваем метод get_template для возврата мок-шаблона
            
            result = myapp.CurrencyRequestHandler._render_template(mock_handler, "test.html", test="data") # вызываем метод рендеринга шаблона
            
            self.assertEqual(result, "<html>Test</html>") # проверяем, что результат соответствует ожидаемому
            mock_env.get_template.assert_called_once_with("test.html") # проверяем, что get_template был вызван с правильным именем шаблона
            mock_template.render.assert_called_once_with(test="data") # проверяем, что render был вызван с правильными аргументами


class TestErrorHandling(unittest.TestCase):
    '''
    Класс TestErrorHandling содержит тесты обработки ошибок
    проверяет корректность обработки HTTP ошибок и ошибок API
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для перезагрузки модуля
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
    
    def test_404_error_handling(self):
        '''
        Тестирование обработки 404 ошибки
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler.send_response = MagicMock() # мокаем метод send_response
        mock_handler.send_header = MagicMock() # мокаем метод send_header
        mock_handler.end_headers = MagicMock() # мокаем метод end_headers
        mock_handler.wfile = MagicMock() # мокаем атрибут wfile
        
        myapp.CurrencyRequestHandler._handle_404(mock_handler, "Тестовая ошибка 404") # вызываем метод обработки 404 ошибки
        
        mock_handler.send_response.assert_called_once_with(404) # проверяем, что send_response был вызван с кодом 404
        mock_handler.send_header.assert_called_once_with('Content-type', 'text/html; charset=utf-8') # проверяем, что send_header был вызван с правильными заголовками
        mock_handler.end_headers.assert_called_once() # проверяем, что end_headers был вызван один раз
        mock_handler.wfile.write.assert_called_once() # проверяем, что write был вызван
        
        html_content = mock_handler.wfile.write.call_args[0][0].decode('utf-8') # получаем HTML контент из вызова write
        self.assertIn("404 - Страница не найдена", html_content) # проверяем, что HTML содержит заголовок 404 ошибки
        self.assertIn("Тестовая ошибка 404", html_content) # проверяем, что HTML содержит сообщение об ошибке
        self.assertIn("Вернуться на главную", html_content) # проверяем, что HTML содержит ссылку на главную страницу
    
    def test_api_error_handling(self):
        '''
        Тестирование обработки ошибки API
        '''
        myapp.api_error = "Тестовая ошибка API" # устанавливаем тестовую ошибку API
        
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler.send_response = MagicMock() # мокаем метод send_response
        mock_handler.send_header = MagicMock() # мокаем метод send_header
        mock_handler.end_headers = MagicMock() # мокаем метод end_headers
        mock_handler.wfile = MagicMock() # мокаем атрибут wfile
        
        myapp.CurrencyRequestHandler._handle_api_error(mock_handler) # вызываем метод обработки ошибки API
        
        mock_handler.send_response.assert_called_once_with(503) # проверяем, что send_response был вызван с кодом 503
        mock_handler.send_header.assert_called_once_with('Content-type', 'text/html; charset=utf-8') # проверяем, что send_header был вызван с правильными заголовками
        mock_handler.end_headers.assert_called_once() # проверяем, что end_headers был вызван один раз
        mock_handler.wfile.write.assert_called_once() # проверяем, что write был вызван
        
        html_content = mock_handler.wfile.write.call_args[0][0].decode('utf-8') # получаем HTML контент из вызова write
        self.assertIn("Сервис временно недоступен", html_content) # проверяем, что HTML содержит заголовок недоступности сервиса
        self.assertIn("Тестовая ошибка API", html_content) # проверяем, что HTML содержит сообщение об ошибке API
        self.assertIn("Вернуться на главную", html_content) # проверяем, что HTML содержит ссылку на главную страницу


class TestRouteHandling(unittest.TestCase):
    '''
    Класс TestRouteHandling содержит тесты обработки маршрутов
    проверяет корректность обработки различных URL маршрутов
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для подготовки данных
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
        # инициализируем список валют тестовыми данными
        myapp.currencies = [
            myapp.Currency(id="R01235", char_code="USD", num_code="840", name="Доллар США", value=75.5, nominal=1)
        ]
        myapp.api_error = None # сбрасываем ошибку API
    
    def test_home_route_without_api_error(self):
        '''
        Тестирование главной страницы без ошибки API
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler._handle_api_error = MagicMock() # мокаем метод _handle_api_error
        mock_handler._set_headers = MagicMock() # мокаем метод _set_headers
        mock_handler._render_template = MagicMock(return_value="<html>Home</html>") # мокаем метод _render_template
        mock_handler.wfile = MagicMock() # мокаем атрибут wfile
        
        myapp.CurrencyRequestHandler._handle_home(mock_handler) # вызываем метод обработки главной страницы
        
        mock_handler._handle_api_error.assert_not_called() # проверяем, что _handle_api_error не был вызван
        mock_handler._render_template.assert_called_once() # проверяем, что _render_template был вызван один раз
        
        call_args = mock_handler._render_template.call_args # получаем аргументы вызова _render_template
        self.assertEqual(call_args[0][0], "index.html") # проверяем, что первый аргумент -- имя шаблона "index.html"
        
        context = call_args[1] # получаем контекст, переданный в шаблон
        self.assertEqual(context['myapp'], myapp.myapp) # проверяем, что контекст содержит объект приложения
        self.assertEqual(context['author'], myapp.author_inf) # проверяем, что контекст содержит информацию об авторе
        self.assertEqual(context['stats']['total_users'], 3) # проверяем, что статистика содержит правильное количество пользователей
        self.assertEqual(context['stats']['total_currencies'], 1) # проверяем, что статистика содержит правильное количество валют
    
    def test_home_route_with_api_error(self):
        '''
        Тестирование главной страницы с ошибкой API
        '''
        myapp.api_error = "API Error" # устанавливаем ошибку API
        
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler._handle_api_error = MagicMock() # мокаем метод _handle_api_error
        
        myapp.CurrencyRequestHandler._handle_home(mock_handler) # вызываем метод обработки главной страницы
        
        mock_handler._handle_api_error.assert_called_once() # проверяем, что _handle_api_error был вызван один раз
    
    def test_user_route_valid_id(self):
        '''
        Тестирование страницы пользователя с валидным ID
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        mock_handler._handle_404 = MagicMock() # мокаем метод _handle_404
        mock_handler._set_headers = MagicMock() # мокаем метод _set_headers
        mock_handler._render_template = MagicMock(return_value="<html>User</html>") # мокаем метод _render_template
        mock_handler.wfile = MagicMock() # мокаем атрибут wfile
        
        myapp.CurrencyRequestHandler._handle_user(mock_handler, {'id': ['1']}) # вызываем метод обработки страницы пользователя с id=1
        
        mock_handler._handle_404.assert_not_called() # проверяем, что _handle_404 не был вызван
        mock_handler._render_template.assert_called_once() # проверяем, что _render_template был вызван один раз
    
    def _test_user_route_error(self, query_params, expected_error):
        '''
        вспомогательный метод для тестирования ошибок пользователя
        '''
        mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика
        
        error_messages = [] # создаём список для сохранения сообщений об ошибках
        mock_handler._handle_404 = MagicMock(side_effect=lambda msg: error_messages.append(msg)) # мокаем метод _handle_404 для сохранения сообщений
        
        myapp.CurrencyRequestHandler._handle_user(mock_handler, query_params) # вызываем метод обработки страницы пользователя
        
        self.assertEqual(len(error_messages), 1) # проверяем, что было сохранено одно сообщение об ошибке
        self.assertEqual(error_messages[0], expected_error) # проверяем, что сообщение об ошибке соответствует ожидаемому
    
    def test_user_route_invalid_id(self):
        '''
        Тестирование страницы пользователя с невалидным ID
        '''
        self._test_user_route_error({'id': ['not_a_number']}, "Некорректный id пользователя") # тестируем случай с некорректным ID
    
    def test_user_route_missing_id(self):
        '''
        Тестирование страницы пользователя без ID
        '''
        self._test_user_route_error({}, "ID пользователя не передан") # тестируем случай без параметра ID
    
    def test_user_route_nonexistent_id(self):
        '''
        Тестирование страницы пользователя с несуществующим ID
        '''
        self._test_user_route_error({'id': ['999']}, "Пользователь 999 не найден") # тестируем случай с несуществующим ID


class TestServerFunctions(unittest.TestCase):
    '''
    Класс TestServerFunctions содержит тесты функций сервера
    проверяет корректность запуска и работы сервера
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для перезагрузки модуля
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
    
    @patch('myapp.init_currencies') # декоратор @patch для подмены функции init_currencies
    @patch('myapp.HTTPServer') # декоратор @patch для подмены класса HTTPServer
    def test_run_server_success(self, mock_http_server, mock_init_currencies):
        '''
        Тестирование успешного запуска сервера
        '''
        mock_init_currencies.return_value = True # настраиваем мок-функцию init_currencies для возврата True
        mock_server_instance = MagicMock() # создаём мок-объект сервера
        mock_http_server.return_value = mock_server_instance # настраиваем мок-класс HTTPServer для возврата мок-сервера
        
        def mock_serve_forever(): # создаём функцию-заглушку для serve_forever
            raise KeyboardInterrupt() # вызываем KeyboardInterrupt для имитации остановки сервера
        
        mock_server_instance.serve_forever = MagicMock(side_effect=mock_serve_forever) # настраиваем метод serve_forever для вызова исключения
        
        try: # начинаем блок обработки исключений
            myapp.run_server(port=9999) # вызываем функцию запуска сервера
        except KeyboardInterrupt: # ловим исключение, которое мы сами вызвали в мок-функции mock_serve_forever()
            pass # игнорируем KeyboardInterrupt
        
        mock_init_currencies.assert_called_once() # проверяем, что init_currencies был вызван один раз
        mock_http_server.assert_called_once_with(('', 9999), myapp.CurrencyRequestHandler) # проверяем, что HTTPServer был создан с правильными параметрами
        mock_server_instance.serve_forever.assert_called_once() # проверяем, что serve_forever был вызван один раз


class TestUserCurrencyLogic(unittest.TestCase):
    '''
    Класс TestUserCurrencyLogic содержит тесты логики работы с подписками пользователей
    проверяет корректность работы с связями пользователь-валюта
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для подготовки данных
        '''
        importlib.reload(myapp) # перезагружаем модуль myapp
        
        # инициализируем список валют тестовыми данными
        myapp.currencies = [
            myapp.Currency(id="R01235", char_code="USD", num_code="840", name="Доллар США", value=75.5, nominal=1),
            myapp.Currency(id="R01239", char_code="EUR", num_code="978", name="Евро", value=90.2, nominal=1),
            myapp.Currency(id="R01375", char_code="CNY", num_code="156", name="Китайский юань", value=10.5, nominal=1)
        ]
    
    def test_user_subscriptions_logic(self):
        '''
        Тестирование логики получения подписок пользователя
        '''
        user_subs = [uc for uc in myapp.user_currencies if uc.user_id == 1] # получаем все подписки первого пользователя
        self.assertEqual(len(user_subs), 2) # проверяем, что первый пользователь имеет 2 подписки
        
        subscribed_currencies = [] # создаём список для хранения валют, на которые подписан пользователь
        for sub in user_subs: # проходим по всем подпискам пользователя
            currency = next((c for c in myapp.currencies if c.char_code == sub.currency_name), None) # находим валюту по коду из подписки
            if currency: # если валюта найдена
                subscribed_currencies.append(currency) # добавляем валюту в список
        
        self.assertEqual(len(subscribed_currencies), 2) # проверяем, что найдено 2 валюты
        
        currency_codes = [c.char_code for c in subscribed_currencies] # получаем список кодов найденных валют
        self.assertIn("USD", currency_codes) # проверяем, что список содержит USD
        self.assertIn("EUR", currency_codes) # проверяем, что список содержит EUR


class TestPathHandling(unittest.TestCase):
    '''
    Класс TestPathHandling содержит тесты обработки путей
    проверяет корректность маршрутизации в методе do_GET
    '''
    
    def test_do_get_routing(self):
        '''
        Тестирование маршрутизации в do_GET
        '''
        # создаём список тестовых случаев
        test_cases = [
            ('/', '_handle_home'),
            ('/users', '_handle_users'),
            ('/currencies', '_handle_currencies'),
            ('/author', '_handle_author'),
            ('/unknown', '_handle_404'),
        ]
        
        for path, expected_method in test_cases: # проходим по всем тестовым случаям
            mock_handler = MagicMock(spec=myapp.CurrencyRequestHandler) # создаём мок-объект обработчика для каждого случая
            mock_handler.path = path # устанавливаем путь запроса
            
            # проходим по всем методам обработки
            for method_name in ['_handle_home', '_handle_users', '_handle_currencies', '_handle_author', '_handle_404']:
                setattr(mock_handler, method_name, MagicMock()) # устанавливаем мок-метод
            
            with patch('myapp.urlparse') as mock_urlparse, patch('myapp.parse_qs') as mock_parse_qs: # подменяем функцию urlparse и функцию parse_qs
                mock_parsed = MagicMock() # создаём мок-объект результата парсинга URL
                mock_parsed.path = path # устанавливаем путь
                mock_parsed.query = '' # устанавливаем пустой запрос
                mock_urlparse.return_value = mock_parsed # настраиваем urlparse для возврата мок-объекта
                mock_parse_qs.return_value = {} # настраиваем parse_qs для возврата пустого словаря
                
                myapp.CurrencyRequestHandler.do_GET(mock_handler) # вызываем метод do_GET
                
                getattr(mock_handler, expected_method).assert_called_once() # проверяем, что ожидаемый метод был вызван один раз


if __name__ == '__main__':
    unittest.main() # запускаем все тесты