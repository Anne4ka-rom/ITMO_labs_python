class Currency:
    '''
    Класс Currency представляет валюту с её характеристиками
    Инкапсулирует данные о валюте и предоставляет методы для работы с ними
    '''
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int, id: int = None):
        '''
        Функция __init__() инициализирует новый экземпляр класса Currency
        
        Параметры:
        num_code -- цифровой код валюты
        char_code -- символьный код валюты
        name -- название валюты
        value -- курс валюты
        nominal -- номинал валюты
        id -- уникальный идентификатор валюты (опционально)
        '''
        self.__id = None # устанавливаем начальное значение приватного атрибута __id как None
        self.__num_code = None # устанавливаем начальное значение приватного атрибута __num_code как None
        self.__char_code = None # устанавливаем начальное значение приватного атрибута __char_code как None
        self.__name = None # устанавливаем начальное значение приватного атрибута __name как None
        self.__value = None # устанавливаем начальное значение приватного атрибута __value как None
        self.__nominal = None # устанавливаем начальное значение приватного атрибута __nominal как None
        
        if id is not None: # проверяем, осутствует ли параметр id
            self.id = id # вызываем сеттер id для установки идентификатора с валидацией
        self.num_code = num_code # вызываем сеттер num_code для установки цифрового кода с валидацией
        self.char_code = char_code # вызываем сеттер char_code для установки символьного кода с валидацией
        self.name = name # вызываем сеттер name для установки названия с валидацией
        self.value = value # вызываем сеттер value для установки курса с валидацией
        self.nominal = nominal # вызываем сеттер nominal для установки номинала с валидацией
    
    @property # декоратор @property для создания свойства
    def id(self) -> int:
        '''
        Функция id() возвращает уникальный идентификатор валюты в виде целого числа
        '''
        return self.__id # возвращаем значение приватного атрибута __id
    
    @id.setter # декоратор setter для свойства id
    def id(self, value: int):
        '''
        Функция id() устанавливает уникальный идентификатор валюты с валидацией
        
        Параметры:
        value -- новый уникальный идентификатор валюты
        
        Вызывает:
        TypeError -- если значение не является целым числом
        ValueError -- если значение не является положительным числом
        '''
        if not isinstance(value, int): # проверяем, является ли значение чем-то кроме целого числа
            raise TypeError('ID должен быть целым числом') # вызываем исключение TypeError
        if value <= 0: # проверяем, является ли значение не положительным
            raise ValueError('ID должен быть положительным числом') # вызываем исключение ValueError
        self.__id = value # устанавливаем значение приватного атрибута __id
    
    @property # декоратор @property для создания свойства
    def num_code(self) -> str:
        '''
        Функция num_code() возвращает цифровой код валюты в строковом виде
        '''
        return self.__num_code # возвращаем значение приватного атрибута __num_code
    
    @num_code.setter # декоратор setter для свойства num_code
    def num_code(self, value: str):
        '''
        Функция num_code() устанавливает цифровой код валюты с валидацией
        
        Параметры:
        value -- новый цифровой код валюты
        
        Вызывает:
        TypeError -- если значение не является строкой
        '''
        if not isinstance(value, str): # проверяем, является ли значение чем-то кроме строки
            raise TypeError('Цифровой код должен быть строкой') # вызываем исключение TypeError
        self.__num_code = value.strip() # устанавливаем значение приватного атрибута __num_code, удаляя лишние пробелы
    
    @property # декоратор @property для создания свойства
    def char_code(self) -> str:
        '''
        Функция char_code() возвращает символьный код валюты в строковом виде
        '''
        return self.__char_code # возвращаем значение приватного атрибута __char_code
    
    @char_code.setter # декоратор setter для свойства char_code
    def char_code(self, value: str):
        '''
        Функция char_code() устанавливает символьный код валюты с валидацией
        
        Параметры:
        value -- новый символьный код валюты
        
        Вызывает:
        TypeError -- если значение не является строкой
        ValueError -- если длина кода не равна 3 символам
        '''
        if not isinstance(value, str): # проверяем, является ли значение чем-то кроме строки
            raise TypeError('Символьный код должен быть строкой') # вызываем исключение TypeError
        if len(value.strip()) != 3: # проверяем, что длина строки после удаления пробелов не равна 3 символам
            raise ValueError('Код валюты должен состоять из 3 символов') # вызываем исключение ValueError
        self.__char_code = value.strip().upper() # устанавливаем значение приватного атрибута __char_code, удаляя пробелы и переводя в верхний регистр
    
    @property # декоратор @property для создания свойства
    def name(self) -> str:
        '''
        Функция name() возвращает название валюты в строковом виде
        '''
        return self.__name # возвращаем значение приватного атрибута __name
    
    @name.setter # декоратор setter для свойства name
    def name(self, value: str):
        '''
        Функция name() устанавливает название валюты с валидацией
        
        Параметры:
        value -- новое название валюты
        
        Вызывает:
        TypeError -- если значение не является строкой
        '''
        if not isinstance(value, str): # проверяем, является ли значение чем-то кроме строки
            raise TypeError('Название должно быть строкой') # вызываем исключение TypeError
        self.__name = value.strip() # устанавливаем значение приватного атрибута __name, удаляя лишние пробелы
    
    @property # декоратор @property для создания свойства
    def value(self) -> float:
        '''
        Функция value() возвращает курс валюты в виде числа с плавающей точкой
        '''
        return self.__value # возвращаем значение приватного атрибута __value
    
    @value.setter # декоратор setter для свойства value
    def value(self, value: float):
        '''
        Функция value() устанавливает курс валюты с валидацией
        
        Параметры:
        value -- новый курс валюты
        
        Вызывает:
        TypeError -- если значение не является числом
        ValueError -- если значение не является положительным числом
        '''
        if not isinstance(value, (int, float)): # проверяем, является ли значение чем-то кроме числа
            raise TypeError('Курс должен быть числом') # вызываем исключение TypeError
        if value <= 0: # проверяем, является ли значение не положительным
            raise ValueError('Курс должен быть положительным числом') # вызываем исключение ValueError
        self.__value = float(value) # устанавливаем значение приватного атрибута __value, преобразуя к типу float
    
    @property # декоратор @property для создания свойства
    def nominal(self) -> int:
        '''
        Функция nominal() возвращает номинал валюты в виде целого числа
        '''
        return self.__nominal # возвращаем значение приватного атрибута __nominal
    
    @nominal.setter # декоратор setter для свойства nominal
    def nominal(self, value: int):
        '''
        Функция nominal() устанавливает номинал валюты с валидацией
        
        Параметры:
        value -- новый номинал валюты
        
        Вызывает:
        TypeError -- если значение не является целым числом
        ValueError -- если значение не является положительным целым числом
        '''
        if not isinstance(value, int): # проверяем, является ли значение чем-то кроме целого числа
            raise TypeError('Номинал должен быть целым числом') # вызываем исключение TypeError
        if value <= 0: # проверяем, является ли значение не положительным
            raise ValueError('Номинал должен быть положительным числом') # вызываем исключение ValueError
        self.__nominal = value # устанавливаем значение приватного атрибута __nominal
    
    def get_value_per_unit(self) -> float:
        '''
        Функция get_value_per_unit() рассчитывает курс за единицу валюты путём деления общего курса на номинал
        
        Возвращает:
        число с плавающей точкой -- курс за одну единицу валюты
        '''
        return self.value / self.nominal # возвращаем результат деления курса на номинал
    
    def to_dict(self) -> dict:
        '''
        Функция to_dict() преобразует объект Currency в словарь
        
        Возвращает:
        словарь с данными валюты
        '''
        # возвращаем словарь с данными валюты
        return {
            'id': self.id, # добавляем id в словарь
            'num_code': self.num_code, # добавляем num_code в словарь
            'char_code': self.char_code, # добавляем char_code в словарь
            'name': self.name, # добавляем name в словарь
            'value': self.value, # добавляем value в словарь
            'nominal': self.nominal # добавляем nominal в словарь
        }
    
    @classmethod # декоратор @classmethod для создания метода класса
    def from_dict(cls, data: dict):
        '''
        Функция from_dict() создаёт объект Currency из словаря
        
        Параметры:
        data -- словарь с данными валюты
        
        Возвращает:
        Currency -- новый объект Currency
        '''
        # создаём и возвращаем новый объект класса Currency
        return cls(
            id=data.get('id'), # передаём id из словаря
            num_code=data.get('num_code'), # передаём num_code из словаря
            char_code=data.get('char_code'), # передаём char_code из словаря
            name=data.get('name'), # передаём name из словаря
            value=data.get('value'), # передаём value из словаря
            nominal=data.get('nominal') # передаём nominal из словаря
        )
    
    def __repr__(self):
        '''
        Функция __repr__() возвращает строковое представление объекта для отладки
        '''
        return f"Currency(id={self.id}, num_code='{self.num_code}', char_code='{self.char_code}', name='{self.name}', value={self.value}, nominal={self.nominal})" # возвращаем строку с информацией об объекте Currency