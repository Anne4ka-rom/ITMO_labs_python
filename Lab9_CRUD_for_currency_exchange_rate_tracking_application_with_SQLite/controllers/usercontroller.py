from models.user import User # импортируем класс User из модуля models.user для работы с объектами пользователей
from models.user_currency import UserCurrency # импортируем класс UserCurrency из модуля models.user_currency для работы с объектами подписок


class UserController:
    '''
    Класс UserController управляет пользователями и их подписками в базе данных
    '''
    
    def __init__(self, db_controller):
        '''
        Функция __init__ инициализирует контроллер пользователей
        
        Параметры:
        db_controller -- контроллер базы данных
        '''
        self.db_controller = db_controller # сохраняем контроллер базы данных в атрибуте класса для дальнейшего использования
    
    def create_user(self, user: User) -> int:
        '''
        Функция create_user создаёт нового пользователя в базе данных
        
        Параметры:
        user -- объект User для создания
        
        Возвращает:
        id созданного пользователя или 0 в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'INSERT INTO users (name) VALUES (?)' # определяем sql-запрос для вставки нового пользователя
            params = (user.name,) # подготавливаем параметры для запроса
            
            success = self.db_controller.execute_update(query, params) # выполняем запрос на обновление базы данных
            
            if success: # проверяем успешность выполнения запроса
                user_id = self.db_controller.get_last_row_id() # получаем id последней добавленной записи
                print(f'пользователь {user.name} добавлен с id: {user_id}') # выводим информационное сообщение
                return user_id # возвращаем id созданного пользователя
            else: # если запрос не выполнился успешно
                print(f'ошибка при добавлении пользователя {user.name}') # выводим сообщение об ошибке
                return 0 # возвращаем 0
        except Exception as e: # перехватываем исключение
            print(f'ошибка при создании пользователя: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае исключения
    
    def read_users(self) -> list:
        '''
        Функция read_users читает всех пользователей из базы данных
        
        Возвращает:
        список словарей с информацией о пользователях
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('select * FROM users order by id') # выполняем sql-запрос для получения всех пользователей с сортировкой по id
            
            users = [] # создаём пустой список для хранения пользователей
            for row in result: # перебираем каждую строку результата
                users.append({ # добавляем новый словарь в список users
                    'id': row['id'], # извлекаем значение поля id
                    'name': row['name'] # извлекаем значение поля name
                })
            
            return users # возвращаем список пользователей
        except Exception as e: # перехватываем исключение
            print(f'ошибка при чтении пользователей: {e}') # выводим сообщение об ошибке
            return [] # возвращаем пустой список в случае исключения
    
    def read_user_by_id(self, user_id: int) -> dict:
        '''
        Функция read_user_by_id читает пользователя по id
        
        Параметры:
        user_id -- id пользователя
        
        Возвращает:
        словарь с информацией о пользователе или None если не найден
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('select * FROM users WHERE id = ?', (user_id,)) # выполняем sql-запрос для получения пользователя по указанному id
            
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                row = result[0] # получаем первую строку результата
                return { # возвращаем словарь с данными пользователя
                    'id': row['id'], # извлекаем значение поля id
                    'name': row['name'] # извлекаем значение поля name
                }
            return None # возвращаем None, если пользователь не найден
        except Exception as e: # перехватываем исключение
            print(f'ошибка при чтении пользователя по id: {e}') # выводим сообщение об ошибке
            return None # возвращаем None в случае исключения
    
    def update_user(self, user_id: int, user: User) -> bool:
        '''
        Функция update_user обновляет пользователя в базе данных
        
        Параметры:
        user_id -- id пользователя для обновления
        user -- объект User с новыми данными
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'UPDATE users SET name = ? WHERE id = ?' # определяем sql-запрос для обновления данных пользователя
            params = (user.name, user_id) # подготавливаем параметры для запроса
            
            success = self.db_controller.execute_update(query, params) # выполняем запрос обновления
            if success: # проверяем успешность выполнения операции
                print(f'пользователь с id {user_id} обновлен') # выводим информационное сообщение об успешном обновлении
            return success # возвращаем результат выполнения операции
        except Exception as e: # перехватываем исключение
            print(f'ошибка при обновлении пользователя: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def delete_user(self, user_id: int) -> bool:
        '''
        Функция delete_user удаляет пользователя из базы данных
        
        Параметры:
        user_id -- id пользователя для удаления
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'DELETE FROM users WHERE id = ?' # определяем sql-запрос для удаления пользователя
            params = (user_id,) # подготавливаем параметры для запроса
            
            success = self.db_controller.execute_update(query, params) # выполняем запрос удаления
            if success: # проверяем успешность выполнения операции
                print(f'пользователь с id {user_id} удален') # выводим информационное сообщение об успешном удалении
            return success # возвращаем результат выполнения операции
        except Exception as e: # перехватываем исключение
            print(f'ошибка при удалении пользователя: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def count_users(self) -> int:
        '''
        Функция count_users возвращает количество пользователей в базе данных
        
        Возвращает:
        количество пользователей
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('select count(*) as count FROM users') # выполняем sql-запрос для подсчёта количества пользователей в таблице
            
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                return result[0]['count'] if result[0]['count'] is not None else 0 # возвращаем количество пользователей или 0, если значение None
            return 0 # возвращаем 0, если результат пустой
        except Exception as e: # перехватываем исключение
            print(f'ошибка при подсчёте пользователей: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае исключения
    
    def get_user_subscription_count(self, user_id: int) -> int:
        '''
        Функция get_user_subscription_count возвращает количество подписок пользователя
        
        Параметры:
        user_id -- id пользователя
        
        Возвращает:
        количество подписок
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('select count(*) as count FROM currencies_user WHERE user_id = ?', (user_id,)) # выполняем sql-запрос для подсчёта подписок пользователя
            
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                return result[0]['count'] if result[0]['count'] is not None else 0 # возвращаем количество подписок или 0, если значение None
            return 0 # возвращаем 0, если результат пустой
        except Exception as e: # перехватываем исключение
            print(f'ошибка при подсчёте подписок пользователя: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае исключения
    
    def add_user_subscription(self, user_currency: UserCurrency) -> bool:
        '''
        Функция add_user_subscription добавляет подписку пользователя на валюту
        
        Параметры:
        user_currency -- объект UserCurrency
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'INSERT OR IGNORE INTO currencies_user (user_id, currency_id) VALUES (?, ?)' # определяем sql-запрос для добавления подписки с игнорированием конфликтов
            params = (user_currency.user_id, user_currency.currency_id) # подготавливаем параметры для запроса
            
            success = self.db_controller.execute_update(query, params) # выполняем запрос добавления
            if success and self.db_controller.get_row_count() > 0: # проверяем успешность выполнения операции и что были затронуты строки
                print(f'добавлена подписка: пользователь {user_currency.user_id} -> валюта {user_currency.currency_id}') # выводим информационное сообщение об успешном добавлении
                return True # возвращаем True при успешном добавлении
            else: # если запрос не выполнился успешно или не затронул строки
                print(f'подписка уже существует или ошибка') # выводим сообщение об ошибке
                return False # возвращаем False
        except Exception as e: # перехватываем исключение
            print(f'ошибка при добавлении подписки: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def remove_user_subscription(self, user_id: int, currency_id: int) -> bool:
        '''
        Функция remove_user_subscription удаляет подписку пользователя на валюту
        
        Параметры:
        user_id -- id пользователя
        currency_id -- id валюты
        
        Возвращает:
        True если успешно, False в случае ошибки
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            query = 'DELETE FROM currencies_user WHERE user_id = ? AND currency_id = ?' # определяем sql-запрос для удаления подписки
            params = (user_id, currency_id) # подготавливаем параметры для запроса
            
            success = self.db_controller.execute_update(query, params) # выполняем запрос удаления
            if success: # проверяем успешность выполнения операции
                print(f'удалена подписка: пользователь {user_id} -> валюта {currency_id}') # выводим информационное сообщение об успешном удалении
            return success # возвращаем результат выполнения операции
        except Exception as e: # перехватываем исключение
            print(f'ошибка при удалении подписки: {e}') # выводим сообщение об ошибке
            return False # возвращаем False в случае исключения
    
    def get_total_subscriptions_count(self) -> int:
        '''
        Функция get_total_subscriptions_count возвращает общее количество подписок в системе
        
        Возвращает:
        общее количество подписок
        '''
        try: # начинаем блок try-catch для обработки возможных исключений
            result = self.db_controller.execute_query('select count(*) as count FROM currencies_user') # выполняем sql-запрос для подсчёта всех подписок
            
            if result and len(result) > 0: # проверяем что результат не пустой и содержит хотя бы одну запись
                return result[0]['count'] if result[0]['count'] is not None else 0 # возвращаем количество подписок или 0, если значение None
            return 0 # возвращаем 0, если результат пустой
        except Exception as e: # перехватываем исключение
            print(f'ошибка при подсчёте всех подписок: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае исключения