import unittest
import sys
import os

# Добавляем путь к проекту для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Author, App, User, Currency, UserCurrency


class TestAuthor(unittest.TestCase):
    """Тесты для модели Author"""
    
    def setUp(self):
        self.author = Author(name="Иван Иванов", group="P3120")
    
    def test_initialization(self):
        self.assertEqual(self.author.name, "Иван Иванов")
        self.assertEqual(self.author.group, "P3120")
    
    def test_name_setter_valid(self):
        self.author.name = "Петр Петров"
        self.assertEqual(self.author.name, "Петр Петров")
    
    def test_name_setter_invalid_type(self):
        with self.assertRaises(TypeError):
            self.author.name = 123
    
    def test_name_setter_empty(self):
        with self.assertRaises(ValueError):
            self.author.name = ""
    
    def test_group_setter_valid(self):
        self.author.group = "P3121"
        self.assertEqual(self.author.group, "P3121")
    
    def test_repr(self):
        self.assertIn("Author", repr(self.author))
        self.assertIn("Иван Иванов", repr(self.author))


class TestApp(unittest.TestCase):
    """Тесты для модели App"""
    
    def setUp(self):
        self.author = Author(name="Иван Иванов", group="P3120")
        self.app = App(name="Валютка", version="1.0.0", author=self.author)
    
    def test_initialization(self):
        self.assertEqual(self.app.name, "Валютка")
        self.assertEqual(self.app.version, "1.0.0")
        self.assertEqual(self.app.author, self.author)
    
    def test_name_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.app.name = 123
        
        with self.assertRaises(ValueError):
            self.app.name = ""
    
    def test_version_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.app.version = 123
        
        with self.assertRaises(ValueError):
            self.app.version = ""
    
    def test_author_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.app.author = "Не автор"
    
    def test_repr(self):
        self.assertIn("App", repr(self.app))
        self.assertIn("Валютка", repr(self.app))


class TestUser(unittest.TestCase):
    """Тесты для модели User"""
    
    def setUp(self):
        self.user = User(id=1, name="Алексей Петров")
    
    def test_initialization(self):
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.name, "Алексей Петров")
    
    def test_id_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.user.id = "не число"
        
        with self.assertRaises(ValueError):
            self.user.id = -1
    
    def test_name_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.user.name = 123
        
        with self.assertRaises(ValueError):
            self.user.name = ""
    
    def test_repr(self):
        self.assertIn("User", repr(self.user))
        self.assertIn("Алексей Петров", repr(self.user))


class TestCurrency(unittest.TestCase):
    """Тесты для модели Currency"""
    
    def setUp(self):
        self.currency = Currency(
            id="R01235",
            char_code="USD",
            name="Доллар США",
            value=75.5,
            nominal=1
        )
    
    def test_initialization(self):
        self.assertEqual(self.currency.id, "R01235")
        self.assertEqual(self.currency.char_code, "USD")
        self.assertEqual(self.currency.name, "Доллар США")
        self.assertEqual(self.currency.value, 75.5)
        self.assertEqual(self.currency.nominal, 1)
    
    def test_value_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.currency.value = "не число"
        
        with self.assertRaises(ValueError):
            self.currency.value = -1
    
    def test_nominal_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.currency.nominal = "не число"
        
        with self.assertRaises(ValueError):
            self.currency.nominal = 0
    
    def test_get_value_per_unit(self):
        self.currency.value = 100
        self.currency.nominal = 2
        self.assertEqual(self.currency.get_value_per_unit(), 50)
    
    def test_repr(self):
        self.assertIn("Currency", repr(self.currency))
        self.assertIn("USD", repr(self.currency))


class TestUserCurrency(unittest.TestCase):
    """Тесты для модели UserCurrency"""
    
    def setUp(self):
        self.user_currency = UserCurrency(
            id=1,
            user_id=2,
            currency_name="USD"
        )
    
    def test_initialization(self):
        self.assertEqual(self.user_currency.id, 1)
        self.assertEqual(self.user_currency.user_id, 2)
        self.assertEqual(self.user_currency.currency_name, "USD")
    
    def test_id_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.user_currency.id = "не число"
        
        with self.assertRaises(ValueError):
            self.user_currency.id = 0
    
    def test_user_id_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.user_currency.user_id = "не число"
        
        with self.assertRaises(ValueError):
            self.user_currency.user_id = -1
    
    def test_currency_name_setter_invalid(self):
        with self.assertRaises(TypeError):
            self.user_currency.currency_name = 123
    
    def test_repr(self):
        self.assertIn("UserCurrency", repr(self.user_currency))
        self.assertIn("USD", repr(self.user_currency))


if __name__ == '__main__':
    unittest.main()