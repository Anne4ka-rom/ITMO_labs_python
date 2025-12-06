import sqlite3 # импортируем sqlite3 для работы с базой данных sqlite
import os # импортируем os для работы с файловой системой
from typing import List, Dict, Any, Optional # импортируем типы данных для аннотаций типов


class DatabaseController:
    '''
    Класс databasecontroller управляет подключением к базе данных и операциями с ней
    '''
    
    def __init__(self, db_path: str = ':memory:'):
        '''
        Функция __init__() инициализирует подключение к базе данных
        
        Параметры:
        db_path -- путь к файлу базы данных
        '''
        self.connection = sqlite3.connect(db_path, check_same_thread=False) # создаём подключение к базе данных с отключением проверки потока
        self.connection.row_factory = sqlite3.Row # устанавливаем фабрику строк для возврата словарей вместо кортежей
        self.cursor = self.connection.cursor() # создаём курсор для выполнения sql-запросов

        self.cursor.execute('PRAGMA foreign_keys = ON') # активируем поддержку внешних ключей в sqlite

        if db_path == ':memory:': # проверяем, используем ли мы базу в памяти
            print('используется база данных sqlite в памяти') # выводим сообщение об использовании базы в памяти
        else: # если используется файловая база
            print(f'используется файловая база данных: {db_path}') # выводим путь к файлу базы данных
        
        self._create_tables() # вызываем метод для создания таблиц в базе данных
        self._insert_initial_data() # вызываем метод для вставки начальных данных
    
    def _create_tables(self):
        '''
        Функция _create_tables создаёт таблицы в базе данных
        '''
        # sql-запрос для создания таблицы пользователей с автоматическим инкрементом id
        users_table_sql = '''
        create table if not exists users (
            id integer primary key autoincrement,
            name text not null
        )
        ''' 
        
        # sql-запрос для создания таблицы валют с уникальными символьными кодами
        currencies_table_sql = '''
        create table if not exists currencies (
            id integer primary key autoincrement,
            num_code text not null,
            char_code text not null unique,
            name text not null,
            value real not null,
            nominal integer not null default 1,
            created_at timestamp default current_timestamp
        )
        '''
        
        # sql-запрос для создания индекса по полю char_code таблицы currencies
        index_char_code_sql = '''
        create index if not exists idx_currencies_char_code 
        ON currencies(char_code)
        '''
        
        # sql-запрос для создания таблицы связей с каскадным удалением и уникальными парами
        currencies_user_sql = '''
        create table if not exists currencies_user (
            id integer primary key autoincrement,
            user_id integer not null,
            currency_id integer not null,
            foreign key(user_id) references users(id) ON delete cascade,
            foreign key(currency_id) references currencies(id) ON delete cascade,
            unique(user_id, currency_id)
        )
        '''
        
        # sql-запрос для создания индекса по полю user_id таблицы currencies_user
        index_user_id_sql = '''
        create index if not exists idx_currencies_user_user_id 
        ON currencies_user(user_id)
        '''
        
        # sql-запрос для создания индекса по полю currency_id таблицы currencies_user
        index_currency_id_sql = '''
        create index if not exists idx_currencies_user_currency_id 
        ON currencies_user(currency_id)
        '''
        
        # создаём список всех sql-запросов
        queries = [
            users_table_sql,
            currencies_table_sql,
            index_char_code_sql,
            currencies_user_sql,
            index_user_id_sql,
            index_currency_id_sql
        ]
        
        for query in queries: # перебираем каждый запрос в списке
            cleaned_query = '\n'.join(line.strip() for line in query.strip().split('\n')) # очищаем запрос от лишних отступов
            try: # начинаем блок обработки исключений
                self.cursor.execute(cleaned_query) # выполняем очищенный sql-запрос
            except sqlite3.Error as e: # перехватываем ошибки sqlite
                print(f'ошибка при выполнении запроса: {e}') # выводим сообщение об ошибке
                print(f'запрос: {cleaned_query}') # выводим ошибочный запрос
                raise # повторно вызываем исключение
        
        self.connection.commit() # фиксируем изменения в базе данных
        print('таблицы созданы или уже существуют') # выводим сообщение о создании таблиц
    
    def _insert_initial_data(self):
        '''
        Функция _insert_initial_data вставляет начальные данные в базу данных
        '''
        try: # начинаем блок обработки исключений
            self.cursor.execute('SELECT count(*) as count from users') # выполняем запрос для подсчёта пользователей
            users_count = self.cursor.fetchone()[0] # получаем количество пользователей
            
            self.cursor.execute('SELECT count(*) as count from currencies') # выполняем запрос для подсчёта валют
            currencies_count = self.cursor.fetchone()[0] # получаем количество валют
            
            if users_count > 0 and currencies_count > 0: # проверяем, есть ли уже данные в обеих таблицах
                print('начальные данные уже существуют в базе') # выводим сообщение
                return # завершаем функцию
            
            print('вставляем начальные данные...') # выводим сообщение о начале вставки
            
            # создаём список словарей с данными пользователей
            users_data = [
                {'name': 'Алексей Петров'},
                {'name': 'Даниил Козлов'},
                {'name': 'Ангелина Иванченко'}
            ]
            
            for user_data in users_data: # перебираем каждого пользователя
                self.cursor.execute('insert or ignore into users (name) values (:name)', user_data) # выполняем sql-запрос для вставки записи в таблицу users с использованием именованных параметров, игнорируя конфликты
            
            # создаём список словарей с данными валют
            currencies_data = [
                {'num_code': '840', 'char_code': 'USD', 'name': 'Доллар сша', 'value': 90.0, 'nominal': 1},
                {'num_code': '978', 'char_code': 'EUR', 'name': 'Евро', 'value': 91.0, 'nominal': 1},
                {'num_code': '156', 'char_code': 'CNY', 'name': 'Китайский юань', 'value': 12.5, 'nominal': 1},
                {'num_code': '826', 'char_code': 'GBP', 'name': 'Фунт стерлингов', 'value': 115.0, 'nominal': 1},
                {'num_code': '392', 'char_code': 'JPY', 'name': 'Японская иена', 'value': 0.6, 'nominal': 100},
                {'num_code': '398', 'char_code': 'KZT', 'name': 'Казахстанский тенге', 'value': 0.2, 'nominal': 100}
            ]
            
            for currency_data in currencies_data: # перебираем каждую валюту
                self.cursor.execute(''' 
                    insert or ignore into currencies (num_code, char_code, name, value, nominal) 
                    values (:num_code, :char_code, :name, :value, :nominal)
                ''', currency_data) # выполняем многострочный sql-запрос для вставки или игнорирования записи в таблицу currencies с использованием именованных параметров
            
            self.cursor.execute('SELECT id, char_code from currencies') # получаем id и символьные коды валют
            currency_map = {row['char_code']: row['id'] for row in self.cursor.fetchall()} # создаём словарь для сопоставления кодов и id
            
            self.cursor.execute('SELECT id from users order by id') # получаем id пользователей
            user_ids = [row['id'] for row in self.cursor.fetchall()] # создаём список id пользователей
            
            subscriptions_data = [] # создаём пустой список для данных подписок
            if len(user_ids) >= 3: # проверяем, что у нас есть минимум 3 пользователя
                
                # создаём список подписок
                subscriptions_data = [
                    {'user_id': user_ids[0], 'currency_id': currency_map.get('USD')},
                    {'user_id': user_ids[0], 'currency_id': currency_map.get('EUR')},
                    {'user_id': user_ids[1], 'currency_id': currency_map.get('CNY')},
                    {'user_id': user_ids[2], 'currency_id': currency_map.get('USD')},
                    {'user_id': user_ids[2], 'currency_id': currency_map.get('GBP')},
                ]
            
            for subscription_data in subscriptions_data: # перебираем каждую подписку
                if subscription_data['currency_id']: # проверяем, что валюта найдена
                    self.cursor.execute('''
                        insert or ignore into currencies_user (user_id, currency_id) 
                        values (:user_id, :currency_id)
                    ''', subscription_data) # выполняем многострочный sql-запрос для вставки или игнорирования записи в таблицу связей currencies_user с использованием именованных параметров
            
            self.connection.commit() # фиксируем изменения в базе данных
            print('начальные данные успешно добавлены') # выводим сообщение об успехе
            
        except Exception as e: # перехватываем любые исключения
            print(f'ошибка при добавлении начальных данных: {e}') # выводим сообщение об ошибке
            import traceback # импортируем модуль для трассировки
            traceback.print_exc() # выводим трассировку стека
            self.connection.rollback() # откатываем изменения в случае ошибки
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, any]]:
        '''
        Функция execute_query выполняет sql-запрос и возвращает результат
        '''
        try: # начинаем блок обработки исключений
            self.cursor.execute(query, params) # выполняем sql-запрос с параметрами
            result = self.cursor.fetchall() # получаем все результаты запроса
            
            if result: # проверяем, есть ли результаты
                rows = [] # создаём пустой список для строк
                for row in result: # перебираем каждую строку результата
                    row_dict = {} # создаём пустой словарь для текущей строки
                    for idx, col in enumerate(self.cursor.description): # перебираем каждую колонку
                        col_name = col[0] # получаем имя колонки
                        col_value = row[idx] # получаем значение колонки
                        row_dict[col_name] = col_value # добавляем пару ключ-значение в словарь
                    rows.append(row_dict) # добавляем словарь в список строк
                return rows # возвращаем список словарей
            return [] # возвращаем пустой список, если нет результатов
        except Exception as e: # перехватываем исключения
            print(f'ошибка выполнения запроса: {e}, запрос: {query}, параметры: {params}') # выводим сообщение об ошибке
            return [] # возвращаем пустой список в случае ошибки
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        '''
        Функция execute_update выполняет sql-запрос на изменение данных
        '''
        try: # начинаем блок обработки исключений
            print(f'debug execute_update: запрос={query}, params={params}') # выводим отладочную информацию
            self.cursor.execute(query, params) # выполняем sql-запрос
            rowcount = self.cursor.rowcount # получаем количество изменённых строк
            print(f'debug execute_update: rowcount={rowcount}') # выводим количество изменённых строк
            self.connection.commit() # фиксируем изменения
            return True # возвращаем True при успехе
        except sqlite3.Error as e: # перехватываем ошибки sqlite
            print(f'ошибка sqlite при выполнении запроса на обновление: {e}') # выводим сообщение об ошибке
            print(f'запрос: {query}') # выводит запрос
            print(f'параметры: {params}') # выводит параметры
            self.connection.rollback() # откатываем изменения
            return False # возвращаем False при ошибке
        except Exception as e: # перехватываем другие исключения
            print(f'общая ошибка при выполнении запроса на обновление: {e}') # выводим сообщение об ошибке
            print(f'запрос: {query}') # выводит запрос
            print(f'параметры: {params}') # выводит параметры
            self.connection.rollback() # откатываем изменения
            return False # возвращаем False при ошибке
    
    def execute_many(self, query: str, params_list: list[tuple]) -> bool:
        '''
        Функция execute_many выполняет sql-запрос для нескольких наборов параметров
        '''
        try: # начинаем блок обработки исключений
            self.cursor.executemany(query, params_list) # выполняем запрос для нескольких наборов параметров
            self.connection.commit() # фиксируем изменения
            return True # возвращаем True при успехе
        except Exception as e: # перехватываем исключения
            print(f'ошибка выполнения executemany: {e}, запрос: {query}') # выводим сообщение об ошибке
            self.connection.rollback() # откатываем изменения
            return False # возвращаем False при ошибке
    
    def get_last_row_id(self) -> int:
        '''
        Функция get_last_row_id возвращает id последней вставленной записи
        '''
        try: # начинаем блок обработки исключений
            self.cursor.execute('SELECT last_insert_rowid() as id') # выполняем запрос для получения id последней записи
            result = self.cursor.fetchone() # получаем результат
            return result[0] if result else 0 # возвращаем id или 0 если результата нет
        except Exception as e: # перехватываем исключения
            print(f'ошибка при получении id последней записи: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае ошибки
    
    def get_row_count(self) -> int:
        '''
        Функция get_row_count возвращает количество измененных строк в последней операции
        '''
        try: # начинаем блок обработки исключений
            return self.cursor.rowcount # возвращаем количество изменённых строк
        except Exception as e: # перехватываем исключения
            print(f'ошибка при получении количества строк: {e}') # выводим сообщение об ошибке
            return 0 # возвращаем 0 в случае ошибки
    
    def close(self):
        '''
        Функция close закрывает подключение к базе данных
        '''
        if self.connection: # проверяем, существует ли подключение
            self.connection.close() # закрываем подключение
            print('подключение к базе данных закрыто') # выводим сообщение
    
    def __del__(self):
        '''
        Функция __del__ вызывается при уничтожении объекта
        '''
        self.close() # закрываем подключение при уничтожении объекта