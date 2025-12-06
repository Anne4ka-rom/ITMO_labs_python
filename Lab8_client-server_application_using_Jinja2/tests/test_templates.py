import unittest
import sys
import os
from jinja2 import Environment, FileSystemLoader

# Добавляем путь к проекту для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Author, App, User, Currency


class TestTemplates(unittest.TestCase):
    """Тесты для шаблонов Jinja2"""
    
    def setUp(self):
        # Настраиваем окружение Jinja2
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(templates_path))
        
        # Создаем тестовые данные
        self.author = Author(name="Тест Автор", group="P3120")
        self.app = App(name="Тест Приложение", version="1.0.0", author=self.author)
        self.user = User(id=1, name="Тест Пользователь")
        self.currency = Currency(
            id="TEST001",
            char_code="USD",
            name="Доллар США",
            value=75.5,
            nominal=1
        )
    
    def test_index_template(self):
        """Проверка шаблона index.html"""
        template = self.env.get_template('index.html')
        
        context = {
            'myapp': self.app,
            'author': self.author,
            'stats': {'total_users': 3, 'total_currencies': 9}
        }
        
        html = template.render(**context)
        
        # Проверяем, что переменные подставляются
        self.assertIn(self.app.name, html)
        self.assertIn(self.author.name, html)
        self.assertIn('Пользователей', html)
        self.assertIn('Валют в системе', html)
    
    def test_users_template(self):
        """Проверка шаблона users.html"""
        template = self.env.get_template('users.html')
        
        users = [
            User(id=1, name="Пользователь 1"),
            User(id=2, name="Пользователь 2")
        ]
        
        user_currencies = [
            type('obj', (object,), {'user_id': 1, 'currency_name': 'USD'})(),
            type('obj', (object,), {'user_id': 1, 'currency_name': 'EUR'})()
        ]
        
        context = {
            'myapp': self.app,
            'users': users,
            'user_currencies': user_currencies,
            'currencies': [self.currency]
        }
        
        html = template.render(**context)
        
        # Проверяем отображение пользователей
        self.assertIn('Пользователь 1', html)
        self.assertIn('Пользователь 2', html)
        self.assertIn('Список пользователей', html)
    
    def test_user_template(self):
        """Проверка шаблона user.html"""
        template = self.env.get_template('user.html')
        
        subscribed_currencies = [self.currency]
        
        context = {
            'myapp': self.app,
            'user': self.user,
            'subscribed_currencies': subscribed_currencies,
            'user_subs': []
        }
        
        html = template.render(**context)
        
        # Проверяем отображение пользователя и валют
        self.assertIn(self.user.name, html)
        self.assertIn('Доллар США', html)
        self.assertIn('Профиль пользователя', html)
    
    def test_currencies_template(self):
        """Проверка шаблона currencies.html"""
        template = self.env.get_template('currencies.html')
        
        # Создаем 9 валют, как в вашем приложении
        currencies = [
            Currency(id="R01235", char_code="USD", name="Доллар США", value=76.0937, nominal=1),
            Currency(id="R01239", char_code="EUR", name="Евро", value=88.7028, nominal=1),
            Currency(id="R01035", char_code="GBP", name="Фунт стерлингов", value=101.7601, nominal=1),
            Currency(id="R01820", char_code="JPY", name="Иен", value=49.0737, nominal=100),
            Currency(id="R01375", char_code="CNY", name="Юань", value=10.7328, nominal=1),
            Currency(id="R01775", char_code="CHF", name="Швейцарский франк", value=94.7736, nominal=1),
            Currency(id="R01350", char_code="CAD", name="Канадский доллар", value=54.5396, nominal=1),
            Currency(id="R01020", char_code="AUD", name="Австралийский доллар", value=50.374, nominal=1),
            Currency(id="R01625", char_code="SGD", name="Сингапурский доллар", value=58.7097, nominal=1)
        ]
        
        context = {
            'myapp': self.app,
            'currencies': currencies
        }
        
        html = template.render(**context)
        
        # Проверяем заголовок
        self.assertIn('Курсы валют', html)
        
        # Проверяем отображение всех 9 валют в таблице
        for currency in currencies:
            self.assertIn(currency.char_code, html)
            self.assertIn(currency.name, html)
            
            # Форматируем значение так же, как в шаблоне
            # В шаблоне используется форматирование без лишних нулей
            # 50.374 остается как 50.374, а не 50.3740
            formatted_value = ("%.4f" % currency.value).rstrip('0').rstrip('.')
            if formatted_value.endswith('.'):
                formatted_value = formatted_value[:-1]
                
            # Ищем в формате "XX.XXX руб."
            self.assertIn(f"{formatted_value} руб.", html)
            
            self.assertIn(str(currency.nominal), html)
        
        # Проверяем подсчет количества валют
        self.assertIn(f"({len(currencies)})", html)
    
    def test_author_template(self):
        """Проверка шаблона author.html"""
        template = self.env.get_template('author.html')
        
        context = {
            'myapp': self.app,
            'author': self.author
        }
        
        html = template.render(**context)
        
        # Проверяем отображение информации об авторе
        self.assertIn('Об авторе', html)
        self.assertIn(self.author.name, html)
        self.assertIn(self.author.group, html)
        self.assertIn('О приложении', html)
    
    def test_template_variables(self):
        """Проверка передачи переменных в шаблоны"""
        templates_to_test = ['index.html', 'users.html', 'user.html', 
                           'currencies.html', 'author.html']
        
        for template_name in templates_to_test:
            try:
                template = self.env.get_template(template_name)
                
                # Базовый контекст для всех шаблонов
                context = {
                    'myapp': self.app,
                    'author': self.author
                }
                
                # Добавляем специфичные переменные
                if template_name == 'index.html':
                    context['stats'] = {'total_users': 3, 'total_currencies': 9}
                elif template_name == 'users.html':
                    context['users'] = [self.user]
                    context['user_currencies'] = []
                    context['currencies'] = []
                elif template_name == 'user.html':
                    context['user'] = self.user
                    context['subscribed_currencies'] = []
                    context['user_subs'] = []
                elif template_name == 'currencies.html':
                    context['currencies'] = [self.currency]
                
                # Рендерим шаблон
                html = template.render(**context)
                
                # Проверяем, что шаблон рендерится без ошибок
                self.assertIsInstance(html, str)
                self.assertGreater(len(html), 0)
                
            except Exception as e:
                self.fail(f"Ошибка в шаблоне {template_name}: {e}")


if __name__ == '__main__':
    unittest.main()