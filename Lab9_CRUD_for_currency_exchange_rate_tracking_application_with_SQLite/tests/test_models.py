import unittest # импортируем unittest для создания и запуска юнит-тестов
import os # импортируем os для работы с файловой системой и путями
import sys # импортируем sys для работы с системными путями

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # добавляем родительскую папку текущего файла в системный путь Python для возможности импорта модулей проекта

from models.currency import Currency # импортируем класс Currency из модуля models.currency для тестирования модели валюты
from models.user import User # импортируем класс User из модуля models.user для тестирования модели пользователя
from models.user_currency import UserCurrency # импортируем класс UserCurrency из модуля models.user_currency для тестирования модели связи пользователь-валюта


class TestCurrencyModel(unittest.TestCase):
    '''
    Класс TestCurrencyModel содержит юнит-тесты для модели валюты Currency
    Тестирует создание объектов, валидацию данных и методы модели
    '''
    
    def test_currency_creation(self):
        '''
        Функция test_currency_creation тестирует создание объекта Currency
        Проверяет корректность инициализации всех атрибутов валюты
        '''
        # создаём объект валюты с тестовыми параметрами: числовой код -- 840, символьный код -- USD, название -- "Доллар США", курс -- 90.0 и номинал -- 1
        currency = Currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        self.assertEqual(currency.num_code, '840') # проверяем, что числовой код равен '840'
        self.assertEqual(currency.char_code, 'USD') # проверяем, что символьный код равен 'USD'
        self.assertEqual(currency.name, 'Доллар США') # проверяем, что название равно 'Доллар США'
        self.assertEqual(currency.value, 90.0) # проверяем, что значение курса равно 90.0
        self.assertEqual(currency.nominal, 1) # проверяем, что номинал равен 1
    
    def test_currency_char_code_validation(self):
        '''
        Функция test_currency_char_code_validation тестирует валидацию символьного кода валюты
        Проверяет корректное поведение при установке валидных символьных кодов
        '''
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём объект валюты с позиционными параметрами: числовой код, символьный код, название, курс и номинал

        currency.char_code = 'EUR' # устанавливаем символьный код 'EUR'
        self.assertEqual(currency.char_code, 'EUR') # проверяем, что символьный код установлен правильно
        
        currency.char_code = 'eur' # устанавливаем символьный код в нижнем регистре
        self.assertEqual(currency.char_code, 'EUR') # проверяем, что символьный код автоматически приведён к верхнему регистру
    
    def test_currency_char_code_invalid(self):
        '''
        Функция test_currency_char_code_invalid тестирует обработку невалидных символьных кодов
        Проверяет, что модель корректно выбрасывает исключения при невалидных данных
        '''
        with self.assertRaises(ValueError): # проверяем, что при создании валюты выбрасывается исключение ValueError
            Currency('840', 'US', 'Доллар США', 90.0, 1) # пытаемся создать валюту с символьным кодом из 2 символов (должно быть 3 символа)

        with self.assertRaises(ValueError): # проверяем, что при создании валюты выбрасывается исключение ValueError  
            Currency('840', 'USDD', 'Доллар США', 90.0, 1) # пытаемся создать валюту с символьным кодом из 4 символов (должно быть 3 символа)
    
    def test_currency_value_validation(self):
        '''
        Функция test_currency_value_validation тестирует валидацию курса валюты
        Проверяет корректность установки положительных значений и обработку отрицательных
        '''
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём тестовый объект валюты USD с числовым кодом -- 840, названием -- "Доллар США", курсом -- 90.0 и номиналом -- 1

        currency.value = 95.0 # устанавливаем корректное значение курса
        self.assertEqual(currency.value, 95.0) # проверяем, что значение установлено правильно
        
        with self.assertRaises(ValueError): # создаём контекстный менеджер для проверки, что в блоке кода будет выброшено исключение ValueError
            currency.value = -10.0 # пытаемся установить отрицательное значение курса
    
    def test_get_value_per_unit(self):
        '''
        Функция test_get_value_per_unit тестирует расчёт курса за единицу валюты
        Проверяет корректность вычисления стоимости одной единицы валюты с учётом номинала
        '''
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём тестовый объект валюты USD с числовым кодом -- 840, названием -- "Доллар США", курсом -- 90.0 и номиналом -- 1
        self.assertEqual(currency.get_value_per_unit(), 90.0) # проверяем, что курс за единицу равен 90.0 при номинале 1
        
        currency = Currency('392', 'JPY', 'Японская иена', 60.0, 100) # создаём тестовый объект валюты JPY с числовым кодом -- 392, названием -- "Японская иена", курсом -- 60.0 и номиналом -- 100
        self.assertEqual(currency.get_value_per_unit(), 0.6) # проверяем, что курс за единицу равен 60.0 / 100 = 0.6
    
    def test_to_dict(self):
        '''
        Функция test_to_dict тестирует преобразование объекта Currency в словарь
        Проверяет корректность сериализации всех атрибутов валюты
        '''
        currency = Currency('840', 'USD', 'Доллар США', 90.0, 1) # создаём объект валюты USD с числовым кодом -- 840, символьным кодом -- USD, названием -- "Доллар США", курсом -- 90.0 и номиналом -- 1
        result = currency.to_dict() # вызываем метод to_dict для преобразования в словарь
        
        self.assertEqual(result['num_code'], '840') # проверяем, что числовой код в словаре result равен ожидаемому значению '840'
        self.assertEqual(result['char_code'], 'USD') # проверяем, что символьный код в словаре result равен ожидаемому значению 'USD'
        self.assertEqual(result['name'], 'Доллар США') # проверяем, что название валюты в словаре result равно ожидаемому значению 'Доллар США'
        self.assertEqual(result['value'], 90.0) # проверяем, что значение курса в словаре result равно ожидаемому значению 90.0
        self.assertEqual(result['nominal'], 1) # проверяем, что номинал в словаре result равен ожидаемому значению 1
        
        self.assertIn('id', result) # проверяем наличие ключа 'id' в словаре


class TestUserModel(unittest.TestCase):
    '''
    Класс TestUserModel содержит юнит-тесты для модели пользователя User
    Тестирует создание объектов, валидацию имени и основные операции
    '''
    def test_user_creation(self):
        '''
        Функция test_user_creation тестирует создание объекта User
        Проверяет корректность инициализации атрибутов пользователя
        '''
        user = User(name="Иван Иванов") # создаём пользователя с именем "Иван Иванов"
        
        self.assertEqual(user.name, "Иван Иванов") # проверяем, что имя установлено правильно
        self.assertIsNone(user.id)  # проверяем, что id не установлен
    
    def test_user_with_id(self):
        '''
        Функция test_user_with_id тестирует создание User с указанным ID
        Проверяет корректность инициализации пользователя с предустановленным идентификатором
        '''
        user = User(name="Иван Иванов", id=1) # создаём пользователя с именем и id
        
        self.assertEqual(user.id, 1) # проверяем, что id установлен 1
        self.assertEqual(user.name, "Иван Иванов") # проверяем, что имя установлено правильно
    
    def test_user_name_validation(self):
        '''
        Функция test_user_name_validation тестирует валидацию имени пользователя
        Проверяет корректное поведение при установке валидных имён
        '''
        user = User(name="Иван Иванов")
        
        user.name = "Пётр Петров" # устанавливаем корректное имя
        self.assertEqual(user.name, "Пётр Петров") # проверяем, что имя установлено правильно
        
        user.name = "  Анна  " # устанавливаем имя с пробелами
        self.assertEqual(user.name, "Анна") # проверяем, что пробелы удалены автоматически
    
    def test_user_name_invalid(self):
        '''
        Функция test_user_name_invalid тестирует обработку невалидных имён пользователя
        Проверяет, что модель корректно выбрасывает исключения при невалидных данных
        '''
        with self.assertRaises(ValueError): # проверяем, что создание пользователя с пустым именем вызывает исключение ValueError
            User(name="") # пытаемся создать объект User с пустой строкой в качестве имени
                
        with self.assertRaises(ValueError): # проверяем, что создание пользователя с именем только из пробелов вызывает исключение ValueError
            User(name="   ") # пытаемся создать объект User со строкой, содержащей только пробелы
                
        with self.assertRaises(TypeError): # проверяем, что создание пользователя с нестроковым именем вызывает исключение TypeError
            User(name=123) # пытаемся создать объект User с числом 123 вместо строки в качестве имени


class TestUserCurrencyModel(unittest.TestCase):
    '''
    Класс TestUserCurrencyModel содержит юнит-тесты для модели связи пользователь-валюта UserCurrency
    Тестирует создание связей и валидацию идентификаторов
    '''
    def test_user_currency_creation(self):
        '''
        Функция test_user_currency_creation тестирует создание объекта связи UserCurrency
        Проверяет корректность инициализации связи между пользователем и валютой
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2) # создаём связь пользователя 1 с валютой 2
        
        self.assertEqual(user_currency.user_id, 1) # проверяем, что user_id установлен 1
        self.assertEqual(user_currency.currency_id, 2) # проверяем, что currency_id установлен 2
    
    def test_user_currency_with_id(self):
        '''
        Функция test_user_currency_with_id тестирует создание связи с указанным ID
        Проверяет корректность инициализации связи с предустановленным идентификатором
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2, id=5) # создаём связь с указанным id
        
        self.assertEqual(user_currency.id, 5) # проверяем, что id установлен 5
        self.assertEqual(user_currency.user_id, 1) # проверяем, что user_id установлен 1
        self.assertEqual(user_currency.currency_id, 2) # проверяем, что currency_id установлен 2
    
    def test_user_currency_validation(self):
        '''
        Функция test_user_currency_validation тестирует валидацию ID в связи UserCurrency
        Проверяет корректность установки положительных идентификаторов и обработку невалидных значений
        '''
        user_currency = UserCurrency(user_id=1, currency_id=2) # создаём объект связи пользователь-валюта с user_id=1 и currency_id=2 для тестирования добавления подписки
        
        user_currency.user_id = 3 # устанавливаем корректный user_id
        user_currency.currency_id = 4 # устанавливаем корректный currency_id
        
        self.assertEqual(user_currency.user_id, 3) # проверяем, что user_id установлен правильно
        self.assertEqual(user_currency.currency_id, 4) # проверяем, что currency_id установлен правильно
        
        with self.assertRaises(ValueError): # проверяем, что установка нулевого user_id вызывает исключение ValueError
            user_currency.user_id = 0 # внутри блока пытаемся установить нулевое значение для user_id объекта user_currency
                
        with self.assertRaises(ValueError): # проверяем, что установка отрицательного currency_id вызывает исключение ValueError
            user_currency.currency_id = -5 # внутри блока пытаемся установить отрицательное значение -5 для currency_id объекта user_currency


if __name__ == '__main__':
    unittest.main() # запускаем все тесты