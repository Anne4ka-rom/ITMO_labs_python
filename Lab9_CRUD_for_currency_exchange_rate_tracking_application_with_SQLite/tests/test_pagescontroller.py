import unittest # импортируем unittest для создания и запуска юнит-тестов
from unittest.mock import MagicMock, patch # импортируем MagicMock для создания мок-объектов и patch для временной замены объектов
import sys # импортируем sys для работы с системными путями
import os # импортируем os для работы с файловой системой и путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта
from controllers.pagescontroller import PagesController # импортируем класс PagesController из модуля controllers.pagescontroller для тестирования его функциональности
from models.author import Author # импортируем класс Author из модуля models.author для тестирования модели автора


class TestPagesController(unittest.TestCase):
    '''
    Класс TestPagesController содержит юнит-тесты для контроллера страниц PagesController
    Тестирует рендеринг HTML-страниц и обработку шаблонов
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом в классе TestPagesController
        Подготавливает тестовое окружение: создаёт мок-объекты для зависимостей контроллера
        '''
        with patch('os.path.dirname') as mock_dirname: # временно заменяем функцию os.path.dirname на мок-объект
            mock_dirname.return_value = '/Страница 1/path' # настраиваем мок-функцию dirname для возврата тестового пути
            self.controller = PagesController() # создаём экземпляр PagesController с подменённым путём

        self.mock_template = MagicMock() # создаём мок-объект шаблона Jinja2
        self.mock_env = MagicMock() # создаём мок-объект окружения Jinja2
        self.controller.env = self.mock_env # заменяем реальный env контроллера на мок-объект
    
    def test_render_template_success(self):
        '''
        Функция test_render_template_success тестирует успешный рендеринг шаблона
        Проверяет корректность работы метода render_template контроллера PagesController при нормальных условиях
        '''
        self.mock_env.get_template.return_value = self.mock_template # настраиваем мок-метод get_template для возврата мок-шаблона
        self.mock_template.render.return_value = "<html>Страница 1</html>" # настраиваем мок-метод render для возврата тестового HTML
        
        result = self.controller.render_template('Страница 1.html', title='Страница 1') # вызываем метод render_template для рендеринга тестового шаблона
        
        self.assertEqual(result, "<html>Страница 1</html>") # проверяем, что метод вернул ожидаемый HTML
        self.mock_env.get_template.assert_called_once_with('Страница 1.html') # проверяем, что метод get_template вызывался ровно один раз с именем шаблона 'Страница 1.html'
        self.mock_template.render.assert_called_once_with(title='Страница 1') # проверяем, что метод render вызывался ровно один раз с параметром title='Страница 1'
    
    def test_render_template_error(self):
        '''
        Функция test_render_template_error тестирует рендеринг шаблона с ошибкой
        Проверяет обработку исключений в методе render_template контроллера PagesController
        '''
        self.mock_env.get_template.side_effect = Exception("Template error") # настраиваем side_effect для метода get_template для выброса исключения
        
        result = self.controller.render_template('Страница 1.html') # вызываем метод render_template с именем несуществующего или ошибочного шаблона
        
        self.assertIn("Ошибка", result) # проверяем, что в результате содержится слово "Ошибка"
        self.assertIn("Template error", result) # проверяем, что в результате содержится текст ошибки
    
    def test_render_index(self):
        '''
        Функция test_render_index тестирует рендеринг главной страницы
        Проверяет корректность работы метода render_index контроллера PagesController
        '''
        stats = {'total_users': 3, 'total_currencies': 5} # создаём тестовую статистику
        # создаём тестовый список валют
        currencies = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США', 'value': 90.0, 'nominal': 1},
            {'id': 2, 'char_code': 'EUR', 'name': 'Евро', 'value': 91.0, 'nominal': 1}
        ]
        
        self.controller.render_template = MagicMock(return_value="<html>Index</html>") # временно заменяем метод render_template на мок, возвращающий тестовый HTML
        
        result = self.controller.render_index(stats, currencies) # вызываем метод render_index с тестовыми данными
        
        self.assertEqual(result, "<html>Index</html>") # проверяем, что метод вернул ожидаемый HTML
        self.controller.render_template.assert_called_once() # проверяем, что метод render_template вызывался ровно один раз
        
        call_args = self.controller.render_template.call_args # получаем аргументы, с которыми вызывался метод render_template
        
        self.assertEqual(call_args[0][0], 'index.html') # проверяем, что первый аргумент -- имя шаблона 'index.html'
        
        self.assertEqual(call_args[1]['stats'], stats) # проверяем, что передан параметр stats
        self.assertEqual(call_args[1]['currencies'], currencies) # проверяем, что передан параметр currencies
        
        self.assertIn('myapp', call_args[1]) # проверяем наличие общего контекста приложения
        self.assertIn('author', call_args[1]) # проверяем наличие информации об авторе
    
    def test_render_users(self):
        '''
        Функция test_render_users тестирует рендеринг страницы пользователей
        Проверяет корректность работы метода render_users контроллера PagesController
        '''
        # создаём тестовый список пользователей
        users = [
            {'id': 1, 'name': 'Иван Иванов', 'subscription_count': 2},
            {'id': 2, 'name': 'Петр Петров', 'subscription_count': 0}
        ]
        
        self.controller.render_template = MagicMock(return_value="<html>Users</html>") # временно заменяем метод render_template на мок
        
        result = self.controller.render_users(users, total_subscriptions=5) # вызываем метод render_users с тестовыми данными
        
        self.assertEqual(result, "<html>Users</html>") # проверяем, что метод вернул ожидаемый HTML
        
        self.controller.render_template.assert_called_once() # проверяем, что метод render_template вызывался ровно один раз
        
        call_args = self.controller.render_template.call_args # получаем аргументы вызова метода render_template
        
        # Проверяем основные аргументы
        self.assertEqual(call_args[0][0], 'users.html') # проверяем, что шаблон -- 'users.html'
        self.assertEqual(call_args[1]['users'], users) # проверяем, что передан параметр users
        self.assertEqual(call_args[1]['total_subscriptions'], 5) # проверяем, что передан параметр total_subscriptions со значением 5
        
        self.assertIn('myapp', call_args[1]) # проверяем наличие общего контекста приложения
        self.assertIn('author', call_args[1]) # проверяем наличие информации об авторе
    
    def test_render_user_found(self):
        '''
        Функция test_render_user_found тестирует рендеринг страницы пользователя (когда пользователь найден)
        Проверяет корректность работы метода render_user контроллера PagesController
        '''
        user = {'id': 1, 'name': 'Иван Иванов'} # создаём тестовый объект пользователя
        # создаём тестовый список подписанных валют
        subscribed_currencies = [
            {'id': 1, 'char_code': 'USD', 'name': 'Доллар США'}
        ]
        
        self.controller.render_template = MagicMock(return_value="<html>User</html>") # временно заменяем метод render_template на мок
        
        result = self.controller.render_user(user, subscribed_currencies) # вызываем метод render_user с тестовыми данными
        
        self.assertEqual(result, "<html>User</html>") # проверяем, что метод вернул ожидаемый HTML
        
        self.controller.render_template.assert_called_once() # проверяем, что метод render_template вызывался ровно один раз
        
        call_args = self.controller.render_template.call_args # получаем аргументы вызова метода render_template
        
        self.assertEqual(call_args[0][0], 'user.html') # проверяем, что шаблон -- 'user.html'
        self.assertEqual(call_args[1]['user'], user) # проверяем, что передан параметр user
        self.assertEqual(call_args[1]['subscribed_currencies'], subscribed_currencies) # проверяем, что передан параметр subscribed_currencies
        
        self.assertIn('myapp', call_args[1]) # проверяем наличие общего контекста приложения
        self.assertIn('author', call_args[1]) # проверяем наличие информации об авторе
    
    def test_render_user_not_found(self):
        '''
        Функция test_render_user_not_found тестирует рендеринг страницы пользователя, когда он не найден
        Проверяет обработку отсутствия пользователя в методе render_user контроллера PagesController
        '''
        self.controller.render_404 = MagicMock(return_value="<html>404</html>") # временно заменяем метод render_404 на мок
        
        result = self.controller.render_user(None, []) # вызываем метод render_user с None вместо пользователя
        
        self.assertEqual(result, "<html>404</html>") # проверяем, что метод вернул HTML страницы 404
        self.controller.render_404.assert_called_once_with("Пользователь не найден") # проверяем, что метод render_404 вызывался ровно один раз с сообщением "Пользователь не найден"
    
    def test_render_404(self):
        '''
        Функция test_render_404 тестирует рендеринг страницы 404
        Проверяет корректность работы метода render_404 контроллера PagesController
        '''

        original_render_error = self.controller._render_error_page # сохраняем ссылку на оригинальный метод _render_error_page
        
        self.controller._render_error_page = MagicMock(return_value="<html>404 Страница не найдена</html>") # временно заменяем внутренний метод _render_error_page на мок
        
        result = self.controller.render_404("Страница не найдена") # вызываем метод render_404 с тестовым сообщением
        
        self.assertIsInstance(result, str) # проверяем, что результат является строкой
        self.assertIn("404", result)  # проверяем что есть "404" в результате
        
        self.controller._render_error_page.assert_called_once() # проверяем, что мок-метод _render_error_page вызывался ровно один раз
        
        self.controller._render_error_page = original_render_error # восстанавливаем оригинальный метод _render_error_page
    
    def test_get_common_context(self):
        '''
        Функция test_get_common_context тестирует получение общего контекста для всех страниц
        Проверяет корректность работы метода get_common_context контроллера PagesController
        '''
        context = self.controller.get_common_context() # вызываем метод get_common_context для получения общего контекста
        
        self.assertIn('myapp', context) # проверяем наличие раздела 'myapp' в контексте
        self.assertIn('author', context) # проверяем наличие раздела 'author' в контексте
        
        self.assertEqual(context['myapp']['name'], 'Валютка-минутка!') # проверяем название приложения
        self.assertEqual(context['myapp']['version'], '1.0.0') # проверяем версию приложения
        
        self.assertIsInstance(context['author'], Author) # проверяем, что author является экземпляром класса Author
        self.assertEqual(context['author'].name, 'Романова Анна Андреевна') # проверяем имя автора
        self.assertEqual(context['author'].group, 'P3120') # проверяем группу автора


if __name__ == '__main__':
    unittest.main() # запускаем все тесты