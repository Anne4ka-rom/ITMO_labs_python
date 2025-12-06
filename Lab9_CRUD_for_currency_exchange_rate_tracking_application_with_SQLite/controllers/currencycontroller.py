import sqlite3 # импортируем sqlite3 для работы с базой данных sqlite
from models.currency import Currency # импортируем класс currency из модуля models.currency для работы с объектами валют


class CurrencyController:
    '''
    Класс currencycontroller представляет собой контроллер для управления валютами в базе данных
    '''
    
    def __init__(self, db_controller):
        '''
        Функция __init__ инициализирует контроллер валют
        
        Параметры:
        db_controller -- контроллер базы данных
        '''
        self.db_controller = db_controller # сохраняем контроллер базы данных в атрибуте класса для дальнейшего использования
    
    def create_currency(self, currency: Currency) -> int:
        '''
        Функция create_currency создаёт новую валюту в базе данных
        
        Параметры:
        currency -- объект currency для создания записи в базе данных
        
        Возвращает:
        id созданной валюты или 0 в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            existing = self.read_currency_by_char_code(currency.char_code) # вызываем метод для проверки существования валюты по символьному коду
            if existing: # проверяем, существует ли уже валюта с таким символьным кодом
                print(f'валюта с кодом {currency.char_code} уже существует') # выводим сообщение об ошибке
                return 0 # возвращаем 0, так как валюта уже существует
            
            # определяем sql-запрос для вставки новой валюты в таблицу currencies
            query = '''
                insert into currencies (num_code, char_code, name, value, nominal) 
                values (?, ?, ?, ?, ?)
            '''
            params = (currency.num_code, currency.char_code, currency.name, currency.value, currency.nominal) # подготавливаем Параметры для запроса из объекта currency
            print(f'debug: добавляем валюту {currency.char_code} с параметрами: {params}') # выводим отладочную информацию о добавляемой валюте
            success = self.db_controller.execute_update(query, params) # выполняем запрос на обновление базы данных через db_controller
            if success: # проверяем успешность выполнения запроса
                currency_id = self.db_controller.get_last_row_id() # получаем id последней добавленной записи
                print(f'debug: валюта добавлена, last_row_id = {currency_id}') # выводим отладочную информацию о добавлении валюты
                check_query = 'SELECT id, char_code FROM currencies WHERE id = ?' # создаём запрос для проверки добавленной записи
                check_result = self.db_controller.execute_query(check_query, (currency_id,)) # выполняем запрос проверки
                if check_result: # проверяем результат запроса проверки
                    print(f'debug: проверка успешна, найдена валюта: {check_result[0]}') # выводим отладочную информацию об успешной проверке
                    print(f'валюта {currency.char_code} добавлена с id: {currency_id}') # выводим информационное сообщение о добавлении валюты
                    return currency_id # возвращаем id созданной валюты
                else: # если запрос проверки не вернул результата
                    print(f'debug: проверка не прошла, валюта не найдена') # выводим отладочную информацию о неудачной проверке
                    return 0 # возвращаем 0, так как валюта не была найдена после добавления
            else: # если запрос на обновление не выполнился успешно
                print(f'debug: execute_update вернул False') # выводим отладочную информацию о неудачном выполнении запроса
                return 0 # возвращаем 0, так как выполнение запроса не удалось
        except Exception as e: # перехватываем исключение
            print(f'ошибка при создании валюты: {e}') # выводим сообщение об ошибке
            import traceback # импортируем модуль traceback для трассировки стека
            traceback.print_exc() # выводим трассировку стека для отладки
            return 0 # возвращаем 0 в случае исключения
    
    def read_currencies(self) -> list:
        '''
        Функция read_currencies читает все валюты из базы данных
        
        Возвращает:
        список словарей с информацией о валютах
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('SELECT * FROM currencies ORDER BY id') # выполняем sql-запрос для получения всех валют из таблицы currencies с сортировкой по id
            currencies = [] # создаём пустой список для хранения валют
            for row in result: # перебираем каждую строку результата
                currencies.append({ # добавляем новый словарь в список currencies
                    'id': row['id'], # извлекаем значение поля id
                    'num_code': row['num_code'], # извлекаем значение поля num_code
                    'char_code': row['char_code'], # извлекаем значение поля char_code
                    'name': row['name'], # извлекаем значение поля name
                    'value': row['value'], # извлекаем значение поля value
                    'nominal': row['nominal'], # извлекаем значение поля nominal
                    'created_at': row.get('created_at', '') # извлекаем значение поля created_at или пустую строку если поле отсутствует
                })
            return currencies # возвращаем список валют
        except Exception as e: # перехватываем исключение
            print(f'ошибка при чтении валют: {e}') # выводим сообщение об ошибке
            return [] # возвращаем пустой список в случае исключения
    
    def read_currency_by_id(self, currency_id: int) -> dict:
        '''
        Функция read_currency_by_id читает валюту по id
        
        Параметры:
        currency_id -- id валюты
        
        Возвращает:
        словарь с информацией о валюте или None если не найдена
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('SELECT * FROM currencies WHERE id = ?', (currency_id,)) # выполняем sql-запрос для получения валюты по указанному id
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                row = result[0] # получаем первую строку результата
                return { # возвращаем словарь с данными валюты
                    'id': row['id'], # извлекаем значение поля id
                    'num_code': row['num_code'], # извлекаем значение поля num_code
                    'char_code': row['char_code'], # извлекаем значение поля char_code
                    'name': row['name'], # извлекаем значение поля name
                    'value': row['value'], # извлекаем значение поля value
                    'nominal': row['nominal'] # извлекаем значение поля nominal
                }
            return None # возвращаем None, если валюта не найдена
        except Exception as e: # перехватываем исключение
            print(f'ошибка при чтении валюты по id: {e}') # выводим сообщение об ошибке
            return None # возвращаем None в случае исключения
    
    def read_currency_by_char_code(self, char_code: str) -> dict:
        '''
        Функция read_currency_by_char_code читает валюту по символьному коду
        
        Параметры:
        char_code -- символьный код валюты (например, usd, eur)
        
        Возвращает:
        словарь с информацией о валюте или None если не найдена
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('SELECT * FROM currencies WHERE char_code = ?', (char_code.upper(),)) # выполняем sql-запрос для получения валюты по символьному коду, преобразуя код к верхнему регистру
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                row = result[0] # получаем первую строку результата
                return { # возвращаем словарь с данными валюты
                    'id': row['id'], # извлекаем значение поля id
                    'num_code': row['num_code'], # извлекаем значение поля num_code
                    'char_code': row['char_code'], # извлекаем значение поля char_code
                    'name': row['name'], # извлекаем значение поля name
                    'value': row['value'], # извлекаем значение поля value
                    'nominal': row['nominal'] # извлекаем значение поля nominal
                }
            return None # возвращаем None, если валюта не найдена
        except Exception as e: # перехватываем исключение
            print(f'ошибка при чтении валюты по символьному коду: {e}') # выводим сообщение об ошибке
            return None # возвращаем None в случае исключения
    
    def update_currency(self, currency_id: int, currency: Currency) -> bool:
        '''
        Функция update_currency обновляет валюту в базе данных
        
        Параметры:
        currency_id -- id валюты для обновления
        currency -- объект currency с новыми данными
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений

            # определяем sql-запрос для обновления данных валюты
            query = '''
                UPDATE currencies 
                SET num_code = ?, char_code = ?, name = ?, value = ?, nominal = ? 
                WHERE id = ?
            '''
            params = (currency.num_code, currency.char_code, currency.name, currency.value, currency.nominal, currency_id) # подготавливаем параметры для запроса
            return self.db_controller.execute_update(query, params) # выполняем запрос обновления и возвращаем результат
        except Exception as e: # перехватываем исключение
            print(f'ошибка при обновлении валюты: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def update_currency_by_char_code(self, char_code: str, new_value: float) -> bool:
        '''
        Функция update_currency_by_char_code обновляет курс валюты по символьному коду
        
        Параметры:
        char_code -- символьный код валюты
        new_value -- новое значение курса
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'UPDATE currencies SET value = ? WHERE char_code = ?' # определяем sql-запрос для обновления курса валюты по символьному коду
            params = (new_value, char_code.upper()) # подготавливаем параметры для запроса
            success = self.db_controller.execute_update(query, params) # выполняем запрос обновления
            if success: # проверяем успешность выполнения операции
                print(f'курс валюты {char_code} обновлён до {new_value}') # выводим информационное сообщение об успешном обновлении курса
            return success # возвращаем результат выполнения операции
        except Exception as e: # перехватываем исключение
            print(f'ошибка при обновлении курса валюты: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def delete_currency(self, currency_id: int) -> bool:
        '''
        Функция delete_currency удаляет валюту из базы данных
        
        Параметры:
        currency_id -- id валюты для удаления
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            currency = self.read_currency_by_id(currency_id) # получаем информацию о валюте по id
            if not currency: # проверяем существует ли валюта
                print(f'валюта с id {currency_id} не найдена') # выводим сообщение об ошибке
                return False # возвращаем False, так как валюта не найдена
            query = 'DELETE FROM currencies WHERE id = ?' # определяем sql-запрос для удаления валюты
            params = (currency_id,) # подготавливаем параметры для запроса
            success = self.db_controller.execute_update(query, params) # выполняем запрос удаления
            if success: # проверяем успешность выполнения операции
                print(f'валюта {currency['char_code']} удалена') # выводим информационное сообщение об успешном удалении валюты
            return success # возвращаем результат выполнения операции
        except Exception as e: # перехватываем исключение
            print(f'ошибка при удалении валюты: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def count_currencies(self) -> int:
        '''
        Функция count_currencies возвращает количество валют в базе данных
        
        Возвращает:
        количество валют
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('SELECT COUNT(*) as count FROM currencies') # выполняем sql-запрос для подсчёта количества валют в таблице
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                return result[0]['count'] if result[0]['count'] is not None else 0 # возвращаем количество валют или 0, если значение None
            return 0 # возвращаем 0, если результат пустой
        except Exception as e: # перехватываем исключение
            print(f'ошибка при подсчёте валют: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае исключения
    
    def get_user_subscribed_currencies(self, user_id: int) -> list:
        '''
        Функция get_user_subscribed_currencies получает список валют, на которые подписан пользователь
        
        Параметры:
        user_id -- id пользователя
        
        Возвращает:
        список словарей с информацией о валютах
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            
            # определяем sql-запрос для получения валют, на которые подписан пользователь
            query = '''
                SELECT c.* 
                FROM currencies c
                join currencies_user cu on c.id = cu.currency_id
                WHERE cu.user_id = ?
                ORDER BY c.char_code
            '''
            result = self.db_controller.execute_query(query, (user_id,)) # выполняем запрос с указанием id пользователя
            currencies = [] # создаём пустой список для хранения валют
            for row in result: # перебираем каждую строку результата
                currencies.append({ # добавляем новый словарь в список currencies
                    'id': row['id'], # извлекаем значение поля id
                    'num_code': row['num_code'], # извлекаем значение поля num_code
                    'char_code': row['char_code'], # извлекаем значение поля char_code
                    'name': row['name'], # извлекаем значение поля name
                    'value': row['value'], # извлекаем значение поля value
                    'nominal': row['nominal'] # извлекаем значение поля nominal
                })
            return currencies # возвращаем список валют пользователя
        except Exception as e: # перехватываем исключение
            print(f'ошибка при получении валют пользователя: {e}') # выводим сообщение об ошибке
            return [] # возвращаем пустой список в случае исключения
    
    def get_currencies_with_subscription_info(self, user_id: int = None) -> list:
        '''
        Функция get_currencies_with_subscription_info получает все валюты с информацией о подписке пользователя
        
        Параметры:
        user_id -- id пользователя
        
        Возвращает:
        список валют с True/False подписки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            currencies = self.read_currencies() # получаем все валюты из базы данных
            if user_id is None: # проверяем, передан ли id пользователя
                for currency in currencies: # перебираем каждую валюту в списке
                    currency['is_subscribed'] = False # устанавливаем флаг подписки в False для всех валют, если user_id не указан
                return currencies # возвращаем список валют
            subscribed_currencies = self.get_user_subscribed_currencies(user_id) # получаем валюты, на которые подписан пользователь
            subscribed_ids = {c['id'] for c in subscribed_currencies} # создаём множество id подписанных валют
            for currency in currencies: # перебираем каждую валюту в списке
                currency['is_subscribed'] = currency['id'] in subscribed_ids # устанавливаем флаг подписки в True, если id валюты есть в множестве подписанных
            return currencies # возвращаем список валют с информацией о подписке
        except Exception as e: # перехватываем исключение
            print(f'ошибка при получении валют с информацией о подписках: {e}') # выводим сообщение об ошибке
            return [] # возвращаем пустой список в случае исключения