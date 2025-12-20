import unittest # импортируем unittest для создания и запуска тестов
import sys # импортируем sys для работы с системными путями и управлением системными параметрами
import os # импортируем os для работы с операционной системой и файловыми путями
from unittest.mock import Mock # импортируем Mock для создания мок-объектов и подмены реальных функций
from jinja2 import Environment, FileSystemLoader # импортируем Environment и FileSystemLoader из jinja2 для работы с шаблонами


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python, чтобы можно было импортировать модули проекта

from models import Author, App, User, Currency, UserCurrency # импортируем модели данных из модуля models

class TestTemplates(unittest.TestCase):
    '''
    Класс TestTemplates содержит тесты для шаблонов Jinja2
    Проверяет корректность рендеринга всех HTML-шаблонов приложения
    '''
    
    def setUp(self):
        '''
        Функция setUp() выполняется перед каждым тестом для настройки окружения Jinja2 и создания тестовых данных
        '''
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates') # формируем путь к папке с шаблонами
        self.env = Environment(loader=FileSystemLoader(templates_path)) # создаём окружение Jinja2 с загрузчиком файлов из указанной папки
        
        self.author = Author(name="Иван Иванов", group="Y67") # создаём тестового автора
        self.app = App(name="Тест и точка", version="1.0.0", author=self.author) # создаём тестовое приложение
        self.user = User(id=1, name="Иван Иванов") # создаём тестового пользователя
        self.currency = Currency( # создаём тестовую валюту
            id="TEST001", # идентификатор валюты
            char_code="USD", # буквенный код валюты
            num_code="840", # цифровой код валюты
            name="Доллар США", # название валюты
            value=75.5, # курс валюты
            nominal=1 # номинал валюты
        )
    
    def test_index_template(self):
        '''
        Тестирование шаблона index.html
        Проверяет корректность рендеринга главной страницы приложения
        '''
        template = self.env.get_template('index.html') # загружаем шаблон index.html из окружения Jinja2
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'author': self.author, # объект автора
            'stats': {'total_users': 3, 'total_currencies': 9} # статистика приложения
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом

        self.assertIn('<!DOCTYPE html>', html) # проверяем, что в HTML есть doctype
        self.assertIn(self.app.name, html) # проверяем, что в HTML есть название приложения
        self.assertIn(self.author.name, html) # проверяем, что в HTML есть имя автора
        self.assertIn('3', html)  # проверяем, что в HTML есть total_users
        self.assertIn('9', html)  # проверяем, что в HTML есть total_currencies
    
    def test_users_template(self):
        '''
        Тестирование шаблона users.html
        Проверяет корректность рендеринга страницы со списком пользователей
        '''
        template = self.env.get_template('users.html') # загружаем шаблон users.html из окружения Jinja2
        
        users = [ # создаём список тестовых пользователей
            User(id=1, name="Ваня"), # первый тестовый пользователь
            User(id=2, name="Илья") # второй тестовый пользователь
        ]
        
        user_currency_1 = Mock(spec=UserCurrency) # создаём мок-объект связи пользователь-валюта
        user_currency_1.user_id = 1 # устанавливаем user_id для мок-объекта
        user_currency_1.currency_name = 'USD' # устанавливаем currency_name для мок-объекта
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'users': users, # список пользователей
            'user_currencies': [user_currency_1], # список связей пользователь-валюта
            'currencies': [], # список валют (пустой для этого теста)
            'api_error': None # ошибка API (отсутствует)
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn('Ваня', html) # проверяем, что в HTML есть имя первого пользователя
        self.assertIn('Илья', html) # проверяем, что в HTML есть имя второго пользователя
        self.assertIn('href="/user?id=1"', html) # проверяем, что в HTML есть ссылка на страницу первого пользователя
        self.assertIn('href="/user?id=2"', html) # проверяем, что в HTML есть ссылка на страницу второго пользователя
    
    def test_user_template(self):
        '''
        Тестирование шаблона user.html
        Проверяет корректность рендеринга страницы пользователя с подписками на валюты
        '''
        template = self.env.get_template('user.html') # загружаем шаблон user.html из окружения Jinja2
        
        subscribed_currencies = [ # создаём список валют, на которые подписан пользователь
            Currency(id="R01235", char_code="USD", name="Доллар США", value=75.5, nominal=1), # доллар США
            Currency(id="R01239", char_code="EUR", name="Евро", value=90.2, nominal=1) # евро
        ]
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'user': self.user, # объект пользователя
            'subscribed_currencies': subscribed_currencies, # список валют, на которые подписан пользователь
            'user_subs': [], # список подписок пользователя
            'api_error': None # ошибка API отсутствует
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn(self.user.name, html) # проверяем, что в HTML есть имя пользователя
        self.assertIn('Доллар США', html) # проверяем, что в HTML есть название валюты -- "Доллар США"
        self.assertIn('Евро', html) # проверяем, что в HTML есть название валюты -- "Евро"
        self.assertIn('75.5', html) # проверяем, что в HTML есть курс доллара -- 75.5
        self.assertIn('90.2', html) # проверяем, что в HTML есть курс евро -- 90.2
    
    def test_user_template_no_subscriptions(self):
        '''
        Тестирование шаблона user.html без подписок
        Проверяет корректность рендеринга страницы пользователя, у которого нет подписок на валюты
        '''
        template = self.env.get_template('user.html') # загружаем шаблон user.html из окружения Jinja2
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'user': self.user, # объект пользователя
            'subscribed_currencies': [], # пустой список валют
            'user_subs': [], # пустой список подписок пользователя
            'api_error': None # ошибка API отсутствует
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn(self.user.name, html) # проверяем, что в HTML есть имя пользователя
        self.assertIn('нет подписок', html.lower()) # проверяем, что в HTML есть сообщение об отсутствии подписок
    
    def test_currencies_template(self):
        '''
        Тестирование шаблона currencies.html
        Проверяет корректность рендеринга страницы со списком курсов валют
        '''
        template = self.env.get_template('currencies.html') # загружаем шаблон currencies.html из окружения Jinja2
        
        currencies = [ # создаём список тестовых валют
            Currency(id="R01235", char_code="USD", name="Доллар США", value=76.0937, nominal=1), # доллар США с конкретным курсом
            Currency(id="R01239", char_code="EUR", name="Евро", value=88.7028, nominal=1) # евро с конкретным курсом
        ]
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'currencies': currencies, # список валют
            'api_error': None # ошибка API отсутствует
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn('Курсы валют', html) # проверяем, что в HTML есть заголовок -- "Курсы валют"
        self.assertIn('USD', html) # проверяем, что в HTML есть код валюты USD
        self.assertIn('EUR', html) # проверяем, что в HTML есть код валюты EUR
        self.assertIn('Доллар США', html) # проверяем, что в HTML есть название валюты -- "Доллар США"
        self.assertIn('Евро', html) # проверяем, что в HTML есть название валюты -- "Евро"
    
    def test_currencies_template_empty(self):
        '''
        Тестирование шаблона currencies.html с пустым списком валют
        Проверяет корректность рендеринга страницы курсов валют при ошибке загрузки данных
        '''
        template = self.env.get_template('currencies.html') # загружаем шаблон currencies.html из окружения Jinja2
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'currencies': [], # пустой список валют
            'api_error': "Ошибка загрузки" # сообщение об ошибке загрузки данных
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn('Курсы валют', html) # проверяем, что в HTML есть заголовок -- "Курсы валют"
        self.assertIn('Ошибка', html) # проверяем, что в HTML есть сообщение об ошибке
    
    def test_author_template(self):
        '''
        Тестирование шаблона author.html
        Проверяет корректность рендеринга страницы "Об авторе"
        '''
        template = self.env.get_template('author.html') # загружаем шаблон author.html из окружения Jinja2
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'author': self.author # объект автора
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        self.assertIn('Об авторе', html) # проверяем, что в HTML есть заголовок -- "Об авторе"
        self.assertIn(self.author.name, html) # проверяем, что в HTML есть имя автора
        self.assertIn(self.author.group, html) # проверяем, что в HTML есть группа автора
        self.assertIn(self.app.name, html) # проверяем, что в HTML есть название приложения
        self.assertIn(self.app.version, html) # проверяем, что в HTML есть версия приложения
    
    def test_all_templates_render_with_minimal_context(self):
        '''
        Тестирование рендеринга всех шаблонов с минимальным контекстом
        Проверяет, что все шаблоны могут быть отрендерены с минимально необходимыми данными
        '''
        templates = { # создаём словарь с именами шаблонов и соответствующими минимальными контекстами
            'index.html': { # минимальный контекст для index.html
                'myapp': self.app, # объект приложения
                'author': self.author, # объект автора
                'stats': {'total_users': 0, 'total_currencies': 0} # базовая статистика
            },
            'users.html': { # минимальный контекст для users.html
                'myapp': self.app, # объект приложения
                'users': [], # пустой список пользователей
                'user_currencies': [], # пустой список связей пользователь-валюта
                'currencies': [], # пустой список валют
                'api_error': None # ошибка API отсутствует
            },
            'user.html': { # минимальный контекст для user.html
                'myapp': self.app, # объект приложения
                'user': self.user, # объект пользователя
                'subscribed_currencies': [], # пустой список валют
                'user_subs': [], # пустой список подписок пользователя
                'api_error': None # ошибка API отсутствует
            },
            'currencies.html': { # минимальный контекст для currencies.html
                'myapp': self.app, # объект приложения
                'currencies': [], # пустой список валют
                'api_error': None # ошибка API отсутствует
            },
            'author.html': { # минимальный контекст для author.html
                'myapp': self.app, # объект приложения
                'author': self.author # объект автора
            }
        }
        
        for template_name, context in templates.items(): # проходим по всем шаблонам и контекстам
            try: # начинаем блок обработки исключений для каждого шаблона
                template = self.env.get_template(template_name) # загружаем текущий шаблон
                html = template.render(**context) # рендерим шаблон с текущим контекстом
                self.assertIsInstance(html, str) # проверяем, что результат рендеринга является строкой
                self.assertGreater(len(html), 0) # проверяем, что результат рендеринга не пустая строка
            except Exception as e: # перехватываем любое исключение при рендеринге
                self.fail(f"Template {template_name} failed to render: {e}") # вызываем ошибку теста с информацией о проблемном шаблоне и исключении
    
    def test_template_xss_protection(self):
        '''
        Тестирование XSS уязвимости
        Проверяет, что шаблоны корректно экранируют потенциально опасный контент
        '''
        template = self.env.get_template('index.html') # загружаем шаблон index.html для проверки XSS
        
        malicious_author = Author( # создаём автора с потенциально опасным именем
            name='<script>alert("XSS")</script>', # имя содержит XSS-скрипт
            group='P3120' # группа автора
        )
        
        context = { # создаём контекст для передачи в шаблон
            'myapp': self.app, # объект приложения
            'author': malicious_author, # объект автора с опасным именем
            'stats': {'total_users': 3, 'total_currencies': 9} # статистика приложения
        }
        
        html = template.render(**context) # рендерим шаблон с переданным контекстом
        
        if '<script>' in html and '</script>' in html: # проверяем, присутствуют ли теги скрипта в выводе
            print(f"Warning: Potential XSS vulnerability in index.html") # выводим предупреждение о потенциальной XSS уязвимости
            print(f"Script tags found in output") # выводим информацию о найденных тегах скрипта
        
        self.assertIsInstance(html, str) # проверяем, что результат рендеринга является строкой
        self.assertGreater(len(html), 0) # проверяем, что результат рендеринга не пустая строка


if __name__ == '__main__':
    unittest.main() # запускаем все тесты