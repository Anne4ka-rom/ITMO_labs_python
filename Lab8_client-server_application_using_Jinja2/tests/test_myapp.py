import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
from io import BytesIO

# Добавляем путь к проекту для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем глобальные переменные напрямую
import myapp
from myapp import CurrencyRequestHandler, init_currencies
from models import Currency


class TestCurrencyRequestHandler(unittest.TestCase):
    """Тесты для обработчика HTTP-запросов"""
    
    def create_handler(self):
        """Создает обработчик с правильно замоканными атрибутами"""
        # Создаем полностью замоканный сокет
        mock_socket = MagicMock()
        
        # Создаем BytesIO для rfile и wfile
        mock_rfile = BytesIO()
        mock_wfile = BytesIO()
        
        # Замокаем makefile для возврата BytesIO объектов
        mock_socket.makefile.return_value = mock_rfile
        
        # Создаем обработчик с замоканным сокетом
        handler = CurrencyRequestHandler(mock_socket, ('127.0.0.1', 8000), None)
        
        # Устанавливаем wfile напрямую
        handler.wfile = mock_wfile
        
        # Устанавливаем необходимые атрибуты для парсинга запроса
        handler.raw_requestline = b'GET / HTTP/1.1\r\n'
        handler.requestline = 'GET / HTTP/1.1'
        handler.command = 'GET'
        handler.path = '/'
        handler.request_version = 'HTTP/1.1'
        
        # Замокаем parse_request, чтобы он не пытался читать из сокета
        handler.parse_request = MagicMock(return_value=True)
        
        return handler
    
    @patch('myapp.env')  # Мокаем глобальный env из myapp
    def test_set_headers(self, mock_env):
        """Проверка установки заголовков"""
        handler = self.create_handler()
        
        # Мокаем методы
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        
        handler._set_headers()
        
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_called_with('Content-type', 'text/html; charset=utf-8')
        handler.end_headers.assert_called()
    
    @patch('myapp.env')
    def test_render_template_success(self, mock_env):
        """Проверка успешного рендеринга шаблона"""
        handler = self.create_handler()
        
        # Настраиваем цепочку вызовов для глобального env
        mock_template = MagicMock()
        mock_template.render.return_value = 'Hello World'
        mock_env.get_template.return_value = mock_template
        
        result = handler._render_template('test.html', name='World')
        
        self.assertEqual(result, 'Hello World')
        mock_env.get_template.assert_called_with('test.html')
        mock_template.render.assert_called_with(name='World')
    
    @patch('myapp.env')
    def test_render_template_error(self, mock_env):
        """Проверка обработки ошибки рендеринга"""
        handler = self.create_handler()
        
        # Настраиваем глобальный env для вызова ошибки
        mock_env.get_template.side_effect = Exception('Template error')
        
        result = handler._render_template('nonexistent.html')
        
        self.assertIn('Ошибка шаблона', result)
        self.assertIn('Template error', result)
    
    @patch('myapp.env')
    def test_handle_404(self, mock_env):
        """Проверка обработки 404 ошибки"""
        handler = self.create_handler()
        
        # Мокаем методы
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = MagicMock()
        
        handler._handle_404('/test')
        
        handler.send_response.assert_called_with(404)
        handler.send_header.assert_called_with('Content-type', 'text/html; charset=utf-8')
        handler.end_headers.assert_called()
        handler.wfile.write.assert_called()


class TestServerRoutes(unittest.TestCase):
    """Тесты маршрутизации сервера"""
    
    def create_handler_with_path(self, path='/'):
        """Создает обработчик для тестирования конкретного пути"""
        # Создаем полностью замоканный сокет
        mock_socket = MagicMock()
        
        # Создаем BytesIO для rfile и wfile
        mock_rfile = BytesIO()
        mock_wfile = BytesIO()
        
        # Замокаем makefile для возврата BytesIO объектов
        mock_socket.makefile.return_value = mock_rfile
        
        # Создаем обработчик с замоканным сокетом
        handler = CurrencyRequestHandler(mock_socket, ('127.0.0.1', 8000), None)
        
        # Устанавливаем wfile напрямую
        handler.wfile = mock_wfile
        
        # Устанавливаем путь и другие атрибуты
        handler.path = path
        handler.raw_requestline = f'GET {path} HTTP/1.1\r\n'.encode()
        handler.requestline = f'GET {path} HTTP/1.1'
        handler.command = 'GET'
        handler.request_version = 'HTTP/1.1'
        
        # Замокаем parse_request, чтобы он не пытался читать из сокета
        handler.parse_request = MagicMock(return_value=True)
        
        return handler
    
    @patch('myapp.CurrencyRequestHandler._handle_home')
    @patch('myapp.env')
    def test_do_get_home(self, mock_env, mock_handle_home):
        """Проверка маршрута /"""
        handler = self.create_handler_with_path('/')
        handler.do_GET()
        mock_handle_home.assert_called_once()
    
    @patch('myapp.CurrencyRequestHandler._handle_users')
    @patch('myapp.env')
    def test_do_get_users(self, mock_env, mock_handle_users):
        """Проверка маршрута /users"""
        handler = self.create_handler_with_path('/users')
        handler.do_GET()
        mock_handle_users.assert_called_once()
    
    @patch('myapp.CurrencyRequestHandler._handle_currencies')
    @patch('myapp.env')
    def test_do_get_currencies(self, mock_env, mock_handle_currencies):
        """Проверка маршрута /currencies"""
        handler = self.create_handler_with_path('/currencies')
        handler.do_GET()
        mock_handle_currencies.assert_called_once()
    
    @patch('myapp.CurrencyRequestHandler._handle_author')
    @patch('myapp.env')
    def test_do_get_author(self, mock_env, mock_handle_author):
        """Проверка маршрута /author"""
        handler = self.create_handler_with_path('/author')
        handler.do_GET()
        mock_handle_author.assert_called_once()
    
    @patch('myapp.CurrencyRequestHandler._handle_404')
    @patch('myapp.env')
    def test_do_get_not_found(self, mock_env, mock_handle_404):
        """Проверка несуществующего маршрута"""
        handler = self.create_handler_with_path('/nonexistent')
        handler.do_GET()
        mock_handle_404.assert_called_once()


class TestInitCurrencies(unittest.TestCase):
    """Тесты инициализации валют"""
    
    def setUp(self):
        """Сохраняем исходное состояние"""
        self.original_currencies = myapp.currencies.copy()
    
    def tearDown(self):
        """Восстанавливаем исходное состояние"""
        myapp.currencies.clear()
        myapp.currencies.extend(self.original_currencies)
    
    @patch('myapp.get_currencies_full_info')
    def test_init_currencies_success(self, mock_get_info):
        """Проверка успешной инициализации валют"""
        # Очищаем список валют
        myapp.currencies.clear()
        
        # Мокаем ответ API
        mock_data = {
            'USD': {'id': 'R01235', 'name': 'Доллар США', 'value': 75.5, 'nominal': 1},
            'EUR': {'id': 'R01239', 'name': 'Евро', 'value': 85.3, 'nominal': 1}
        }
        mock_get_info.return_value = mock_data
        
        init_currencies()
        
        # Проверяем, что валюты добавились
        self.assertEqual(len(myapp.currencies), 2)
        self.assertEqual(myapp.currencies[0].char_code, 'USD')
        self.assertEqual(myapp.currencies[0].name, 'Доллар США')
        self.assertEqual(myapp.currencies[0].value, 75.5)
        self.assertEqual(myapp.currencies[1].char_code, 'EUR')
        self.assertEqual(myapp.currencies[1].name, 'Евро')
        self.assertEqual(myapp.currencies[1].value, 85.3)
    
    @patch('myapp.get_currencies_full_info')
    def test_init_currencies_error(self, mock_get_info):
        """Проверка инициализации валют при ошибке API"""
        # Очищаем список валют
        myapp.currencies.clear()
        
        # Мокаем ошибку API
        mock_get_info.side_effect = Exception('API error')
        
        init_currencies()
        
        # Должны добавиться тестовые данные
        self.assertGreater(len(myapp.currencies), 0)


if __name__ == '__main__':
    unittest.main()