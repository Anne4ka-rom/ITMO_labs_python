class UserCurrency:
    '''
    Класс UserCurrency представляет связь пользователя с валютой
    Инкапсулирует данные о предпочтениях пользователя по валютам
    '''
    def __init__(self, user_id: int, currency_id: int, id: int = None):
        '''
        Функция __init__() инициализирует новый экземпляр класса UserCurrency
        
        Параметры:
        user_id -- идентификатор пользователя
        currency_id -- идентификатор валюты
        id -- уникальный идентификатор записи (опционально)
        
        Вызывает:
        TypeError -- если id, user_id или currency_id не целые числа
        ValueError -- если id, user_id или currency_id не положительные числа
        '''
        self.__id = None # устанавливаем начальное значение приватного атрибута __id как None
        self.__user_id = None # устанавливаем начальное значение приватного атрибута __user_id как None
        self.__currency_id = None # устанавливаем начальное значение приватного атрибута __currency_id как None
        
        if id is not None: # проверяем, отсутствует ли параметр id
            self.id = id # вызываем сеттер id для установки идентификатора записи с валидацией
        self.user_id = user_id # вызываем сеттер user_id для установки идентификатора пользователя с валидацией
        self.currency_id = currency_id # вызываем сеттер currency_id для установки идентификатора валюты с валидацией
    
    @property # декоратор @property для создания свойства
    def id(self) -> int:
        '''
        Функция id() возвращает уникальный идентификатор записи в виде целого числа
        '''
        return self.__id # возвращаем значение приватного атрибута __id
    
    @id.setter # декоратор setter для свойства id
    def id(self, value: int):
        '''
        Функция id() устанавливает уникальный идентификатор записи с валидацией
        
        Параметры:
        value -- новый уникальный идентификатор записи
        
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
    def user_id(self) -> int:
        '''
        Функция user_id() возвращает идентификатор пользователя в виде целого числа
        '''
        return self.__user_id # возвращаем значение приватного атрибута __user_id
    
    @user_id.setter # декоратор setter для свойства user_id
    def user_id(self, value: int):
        '''
        Функция user_id() устанавливает идентификатор пользователя с валидацией
        
        Параметры:
        value -- новый идентификатор пользователя
        
        Вызывает:
        TypeError -- если значение не является целым числом
        ValueError -- если значение не является положительным числом
        '''
        if not isinstance(value, int): # проверяем, является ли значение чем-то кроме целого числа
            raise TypeError('ID пользователя должен быть целым числом') # вызываем исключение TypeError
        if value <= 0: # проверяем, является ли значение не положительным
            raise ValueError('ID пользователя должен быть положительным числом') # вызываем исключение ValueError
        self.__user_id = value # устанавливаем значение приватного атрибута __user_id
    
    @property # декоратор @property для создания свойства
    def currency_id(self) -> int:
        '''
        Функция currency_id() возвращает идентификатор валюты в виде целого числа
        '''
        return self.__currency_id # возвращаем значение приватного атрибута __currency_id
    
    @currency_id.setter # декоратор setter для свойства currency_id
    def currency_id(self, value: int):
        '''
        Функция currency_id() устанавливает идентификатор валюты с валидацией
        
        Параметры:
        value -- новый идентификатор валюты
        
        Вызывает:
        TypeError -- если значение не является целым числом
        ValueError -- если значение не является положительным числом
        '''
        if not isinstance(value, int): # проверяем, является ли значение чем-то кроме целого числа
            raise TypeError('ID валюты должен быть целым числом') # вызываем исключение TypeError
        if value <= 0: # проверяем, является ли значение не положительным
            raise ValueError('ID валюты должен быть положительным числом') # вызываем исключение ValueError
        self.__currency_id = value # устанавливаем значение приватного атрибута __currency_id
    
    def to_dict(self) -> dict:
        '''
        Функция to_dict() преобразует объект UserCurrency в словарь
        
        Возвращает:
        словарь с данными связи пользователь-валюта
        '''
        # возвращаем словарь с данными связи пользователь-валюта
        return {
            'id': self.id, # добавляем id в словарь
            'user_id': self.user_id, # добавляем user_id в словарь
            'currency_id': self.currency_id # добавляем currency_id в словарь
        }
    
    @classmethod # декоратор @classmethod для создания метода класса
    def from_dict(cls, data: dict):
        '''
        Функция from_dict() создаёт объект UserCurrency из словаря
        
        Параметры:
        data -- словарь с данными связи пользователь-валюта
        
        Возвращает:
        UserCurrency -- новый объект UserCurrency
        '''
        # создаём и возвращаем новый объект класса UserCurrency
        return cls(
            id=data.get('id'), # передаём id из словаря
            user_id=data.get('user_id'), # передаём user_id из словаря
            currency_id=data.get('currency_id') # передаём currency_id из словаря
        )
    
    def __repr__(self):
        '''
        Функция __repr__() возвращает строковое представление объекта для отладки
        '''
        return f"UserCurrency(id={self.id}, user_id={self.user_id}, currency_id={self.currency_id})" # возвращаем строку с информацией об объекте UserCurrency