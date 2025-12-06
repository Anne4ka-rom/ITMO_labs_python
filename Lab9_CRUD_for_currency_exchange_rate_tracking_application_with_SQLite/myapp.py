from http.server import HTTPServer, BaseHTTPRequestHandler # импортируем HTTPServer и BaseHTTPRequestHandler для создания HTTP-сервера
from urllib.parse import urlparse, parse_qs, quote # импортируем функции для парсинга URL и кодирования строк
from controllers.databasecontroller import DatabaseController # импортируем класс DatabaseController для работы с базой данных
from controllers.currencycontroller import CurrencyController # импортируем класс CurrencyController для управления валютами
from controllers.usercontroller import UserController # импортируем класс UserController для управления пользователями
from controllers.pagescontroller import PagesController # импортируем класс PagesController для рендеринга HTML-страниц
from models.currency import Currency # импортируем класс Currency для создания объектов валют
from models.user import User # импортируем класс User для создания объектов пользователей

_controllers = None # глобальная переменная для хранения контроллеров в режиме синглтона

def get_controllers():
    '''
    Функция get_controllers возвращает общие контроллеры для всех запросов
    Реализует паттерн синглтон для создания контроллеров один раз при запуске сервера
    
    Возвращает:
    словарь со всеми контроллерами приложения: db, currency, user, pages
    '''
    global _controllers # объявляем использование глобальной переменной
    if _controllers is None: # если контроллеры ещё не инициализированы
        db = DatabaseController(':memory:') # создаём экземпляр DatabaseController с базой данных в памяти
        # инициализируем словарь контроллеров
        _controllers = {
            'db': db, # добавляем контроллер базы данных в словарь
            'currency': CurrencyController(db), # создаём контроллер валют с контроллером базы данных
            'user': UserController(db), # создаём контроллер пользователей с контроллером базы данных
            'pages': PagesController() # создаём контроллер страниц
        }
        print("Контроллеры инициализированы (база в памяти)") # выводим сообщение об инициализации контроллеров
    return _controllers # возвращаем словарь контроллеров


class CurrencyRequestHandler(BaseHTTPRequestHandler):
    '''
    Класс CurrencyRequestHandler наследует BaseHTTPRequestHandler и обрабатывает HTTP-запросы
    Реализует обработку всех маршрутов приложения и взаимодействие с контроллерами
    '''
    def __init__(self, *args, **kwargs):
        '''
        Конструктор класса CurrencyRequestHandler
        Инициализирует контроллеры приложения из синглтона
        
        Параметры:
        *args -- позиционные аргументы для родительского конструктора
        **kwargs -- именованные аргументы для родительского конструктора
        '''
        controllers = get_controllers() # получаем контроллеры из функции get_controllers
        self.db_controller = controllers['db'] # сохраняем контроллер базы данных
        self.currency_controller = controllers['currency'] # сохраняем контроллер валют
        self.user_controller = controllers['user'] # сохраняем контроллер пользователей
        self.pages_controller = controllers['pages'] # сохраняем контроллер страниц
        super().__init__(*args, **kwargs) # вызываем конструктор родительского класса BaseHTTPRequestHandler
    
    def do_GET(self):
        '''
        Функция do_GET обрабатывает все GET-запросы
        Выполняет маршрутизацию по пути запроса и вызывает соответствующие обработчики
        '''
        parsed_path = urlparse(self.path) # парсим путь запроса с помощью urlparse
        path = parsed_path.path # извлекаем путь из распарсенного URL
        query_params = parse_qs(parsed_path.query) # парсим параметры запроса с помощью parse_qs

        if path == '/': # если путь -- корневой
            self._handle_home() # вызываем обработчик главной страницы
        elif path == '/author': # если путь -- страница об авторе
            self._handle_author() # вызываем обработчик страницы об авторе
        elif path == '/users': # если путь -- страница пользователей
            self._handle_users() # вызываем обработчик страницы пользователей
        elif path == '/user': # если путь -- страница конкретного пользователя
            self._handle_user(query_params) # вызываем обработчик страницы пользователя с параметрами
        elif path == '/currencies': # если путь -- страница валют
            self._handle_currencies(query_params) # вызываем обработчик страницы валют с параметрами
        elif path == '/currency/delete': # если путь -- удаление валюты
            self._handle_currency_delete(query_params) # вызываем обработчик удаления валюты
        elif path == '/currency/update': # если путь -- обновление курса валюты
            self._handle_currency_update(query_params) # вызываем обработчик обновления курса валюты
        elif path == '/currency/show': # если путь -- отладочная страница валют
            self._handle_currency_show() # вызываем обработчик отладочной страницы валют
        else: # если путь не соответствует ни одному известному маршруту
            self._handle_404(f"Страница {path} не найдена") # вызываем обработчик ошибки 404
    
    def do_POST(self):
        '''
        Функция do_POST обрабатывает все POST-запросы
        Выполняет маршрутизацию POST-запросов и обработку данных формы
        '''
        parsed_path = urlparse(self.path) # парсим путь запроса
        path = parsed_path.path # извлекаем путь
        
        content_length = int(self.headers.get('Content-Length', 0)) # получаем длину содержимого из заголовков
        post_data = self.rfile.read(content_length).decode('utf-8') # читаем данные POST-запроса из потока ввода
        query_params = parse_qs(post_data) # парсим данные POST-запроса
        
        if path == '/currency/create': # если путь -- создание валюты через POST
            self._handle_currency_create_post(query_params) # вызываем обработчик создания валюты
        else: # если путь не соответствует известному POST-маршруту
            self._handle_404(f"POST-маршрут {path} не найден") # вызываем обработчик ошибки 404
    
    def _send_response(self, content: str, status_code: int = 200, content_type: str = 'text/html; charset=utf-8'):
        ''''
        Функция _send_response() отправляет HTTP-ответ
        Формирует и отправляет ответ с заданным содержимым и статусом

        Параметры:
        content -- содержимое ответа
        status_code -- HTTP-код статуса ответа
        content_type -- тип содержимого ответа
        '''
        self.send_response(status_code) # отправляем код статуса HTTP
        self.send_header('Content-type', content_type) # отправляем заголовок Content-Type
        self.end_headers() # завершаем отправку заголовков
        self.wfile.write(content.encode('utf-8')) # записываем содержимое ответа в поток вывода
    
    def _handle_home(self):
        '''
        Функция _handle_home() обрабатывает главную страницу
        Получает статистику и список валют, рендерит главную страницу
        '''
        try: # начинаем блок обработки исключений для безопасного получения данных
            total_users = self.user_controller.count_users() # получаем общее количество пользователей
            total_currencies = self.currency_controller.count_currencies() # получаем общее количество валют
            currencies = self.currency_controller.read_currencies() # получаем список валют

            # вызываем рендеринг главной страницы
            html_content = self.pages_controller.render_index(
                stats={'total_users': total_users, 'total_currencies': total_currencies}, # передаём статистику
                currencies=currencies # передаём список валют
            )
            self._send_response(html_content) # отправляем ответ с HTML-страницей
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            self._send_response(self.pages_controller.render_404(f"Ошибка: {str(e)}"), 500) # отправляем страницу ошибки со статусом 500
    
    def _handle_author(self):
        '''
        Функция _handle_author() обрабатывает страницу об авторе
        Рендерит страницу с информацией об авторе приложения
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операций рендеринга и отправки ответа
            html_content = self.pages_controller.render_author() # вызываем метод render_author контроллера страниц для рендеринга HTML-страницы об авторе
            self._send_response(html_content) # вызываем метод _send_response для отправки рендеренного HTML-кода клиенту
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            self._send_response(f"Ошибка: {str(e)}", 500) # отправляем клиенту простой текст с сообщением об ошибке и HTTP-статусом 500
    
    def _handle_users(self):
        '''
        Функция _handle_users() обрабатывает страницу со списком пользователей
        Получает список пользователей и количество их подписок, рендерит страницу
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операций с пользователями и рендеринга
            users = self.user_controller.read_users() # вызываем метод read_users контроллера пользователей для получения списка всех пользователей из базы данных
            total_subscriptions = self.user_controller.get_total_subscriptions_count() # вызываем метод get_total_subscriptions_count контроллера пользователей для получения общего количества подписок на валюты
            
            for user in users: # перебираем всех пользователей в полученном списке
                user['subscription_count'] = self.user_controller.get_user_subscription_count(user['id']) # для каждого пользователя добавляем поле subscription_count с количеством его подписок, полученным через метод get_user_subscription_count
            
            html_content = self.pages_controller.render_users(users, total_subscriptions) # вызываем метод render_users контроллера страниц для рендеринга HTML-страницы со списком пользователей, передавая список пользователей и общее количество подписок
            self._send_response(html_content) # вызываем метод _send_response для отправки рендеренного HTML-кода клиенту
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            self._send_response(self.pages_controller.render_404(f"Ошибка: {str(e)}"), 500) # отправляем клиенту страницу 404 с сообщением об ошибке и HTTP-статусом 500

    def _handle_user(self, query_params: dict):
        '''
        Функция _handle_user() обрабатывает страницу информации о пользователе
        Получает данные пользователя по ID и его подписки на валюты

        Параметры:
        query_params -- словарь параметров запроса
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операций получения и обработки данных пользователя
            user_id = query_params.get('id', [None])[0] # получаем значение параметра 'id' из словаря query_params, если параметр отсутствует -- используем [None] и берем первый элемент
            
            if not user_id: # проверяем, был ли указан ID пользователя
                html_content = self.pages_controller.render_404("ID пользователя не указан") # вызываем метод render_404 контроллера страниц для рендеринга страницы 404 с сообщением о необходимости указать ID
                self._send_response(html_content, 404) # отправляем рендеренную страницу 404 клиенту с HTTP-статусом 404
                return # завершаем выполнение функции
            
            user_id = int(user_id) # преобразуем строковое значение ID в целое число для использования в запросах к базе данных
            
            user = self.user_controller.read_user_by_id(user_id) # вызываем метод read_user_by_id контроллера пользователей для получения данных пользователя по его ID
            subscribed_currencies = self.currency_controller.get_user_subscribed_currencies(user_id) # вызываем метод get_user_subscribed_currencies контроллера валют для получения списка валют, на которые подписан пользователь
            
            html_content = self.pages_controller.render_user(user, subscribed_currencies) # вызываем метод render_user контроллера страниц для рендеринга HTML-страницы пользователя с его данными и списком подписок
            self._send_response(html_content) # отправляем рендеренный HTML-код клиенту с HTTP-статусом 200
        except ValueError: # перехватываем исключение ValueError, которое возникает при неудачном преобразовании строки в число
            html_content = self.pages_controller.render_404("Некорректный ID пользователя") # вызываем метод render_404 для рендеринга страницы 404 с сообщением о некорректном ID
            self._send_response(html_content, 404) # отправляем страницу 404 клиенту с HTTP-статусом 404
        except Exception as e: # перехватываем любое другое исключение и сохраняем его в переменной e
            self._send_response(self.pages_controller.render_404(f"Ошибка: {str(e)}"), 500) # отправляем клиенту страницу 404 с сообщением об ошибке и HTTP-статусом 500
    
    def _handle_currencies(self, query_params: dict):
        '''
        Функция _handle_currencies() обрабатывает страницу со списком валют
        Получает список валют и отображает их в таблице

        Параметры:
        query_params -- словарь параметров запроса
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операций получения и отображения списка валют
            message = query_params.get('message', [None])[0] # получаем значение параметра 'message' из словаря query_params, если параметр отсутствует -- используем [None] и берем первый элемент
            message_type = query_params.get('type', ['info'])[0] # получаем значение параметра 'type' из словаря query_params, если параметр отсутствует - используем значение по умолчанию ['info'] и берем первый элемент
            
            currencies = self.currency_controller.read_currencies() # вызываем метод read_currencies контроллера валют для получения списка всех валют из базы данных
            
            html_content = self.pages_controller.render_currencies(currencies, message, message_type) # вызываем метод render_currencies контроллера страниц для рендеринга HTML-страницы со списком валют, передавая список валют, сообщение и тип сообщения
            self._send_response(html_content) # отправляем рендеренный HTML-код клиенту с HTTP-статусом 200
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            self._send_response(self.pages_controller.render_404(f"Ошибка: {str(e)}"), 500) # отправляем клиенту страницу 404 с сообщением об ошибке и HTTP-статусом 500
    
    def _handle_currency_delete(self, query_params: dict):
        '''
        Функция _handle_currency_delete() обрабатывает удаление валюты
        Удаляет валюту по ID и выполняет перенаправление

        Параметры:
        query_params -- словарь параметров запроса
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операции удаления валюты
            currency_id = query_params.get('id', [None])[0] # получаем значение параметра 'id' из словаря query_params, если параметр отсутствует -- используем [None] и берем первый элемент
            
            if not currency_id: # проверяем, был ли указан ID валюты
                redirect_url = '/currencies?message=ID валюты не указан&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке и типом ошибки
                self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления на сформированный URL
                return # завершаем выполнение функции
            
            currency_id = int(currency_id) # преобразуем строковое значение ID в целое число для использования в запросах к базе данных
            
            success = self.currency_controller.delete_currency(currency_id) # вызываем метод delete_currency контроллера валют для удаления валюты по её ID, результат сохраняем в переменной success
            
            if success: # проверяем, было ли удаление успешным
                redirect_url = '/currencies?message=Валюта удалена&type=success' # формируем URL для перенаправления на страницу валют с сообщением об успешном удалении и типом success
            else: # если удаление не удалось
                redirect_url = f'/currencies?message=Ошибка удаления валюты&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке удаления и типом error
            
            self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления на сформированный URL
        except ValueError: # перехватываем исключение ValueError, которое возникает при неудачном преобразовании строки в число
            redirect_url = '/currencies?message=Некорректный ID валюты&type=error' # формируем URL для перенаправления на страницу валют с сообщением о некорректном ID валюты
            self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления
        except Exception as e: # перехватываем любое другое исключение и сохраняем его в переменной e
            redirect_url = f'/currencies?message=Ошибка: {str(e)[:50]}&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке, ограничивая длину сообщения до 50 символов
            self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления
    
    def _handle_currency_update(self, query_params: dict):
        '''
        Функция _handle_currency_update() обрабатывает обновление курса валюты
        Обновляет курс валюты по символьному коду и выполняет перенаправление

        Параметры:
        query_params -- словарь параметров запроса
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операции обновления курса валюты
            char_code = query_params.get('char_code', [None])[0] # получаем значение параметра 'char_code' из словаря query_params, если параметр отсутствует -- используем [None] и берем первый элемент
            value_str = query_params.get('value', [None])[0] # получаем значение параметра 'value' из словаря query_params, если параметр отсутствует -- используем [None] и берем первый элемент
            
            if not char_code or not value_str: # проверяем, были ли указаны символьный код валюты и новое значение курса
                redirect_url = '/currencies?message=Не указан код валюты или значение&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке отсутствия данных
                self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления
                return # завершаем выполнение функции
            
            try: # начинаем вложенный блок try для безопасного преобразования строки в число
                value = float(value_str) # преобразуем строковое значение курса в число с плавающей точкой для использования в запросах к базе данных
            except ValueError: # перехватываем исключение ValueError, которое возникает при неудачном преобразовании строки в число
                redirect_url = f'/currencies?message=Некорректное значение: {value_str}&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке преобразования
                self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления
                return # завершаем выполнение функции

            success = self.currency_controller.update_currency_by_char_code(char_code, value) # вызываем метод update_currency_by_char_code контроллера валют для обновления курса валюты по её символьному коду
            
            if success: # проверяем, было ли обновление успешным
                redirect_url = f'/currencies?message=Курс {char_code} обновлен до {value}&type=success' # формируем URL для перенаправления на страницу валют с сообщением об успешном обновлении
            else: # если обновление не удалось
                redirect_url = f'/currencies?message=Валюта {char_code} не найдена&type=error' # формируем URL для перенаправления на страницу валют с сообщением об ошибке поиска валюты
            
            self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления на сформированный URL
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            redirect_url = f'/currencies?message=Ошибка: {str(e)[:50]}&type=error' # формируем URL для перенаправления на страницу валют с сообщением об общей ошибке, ограничивая длину до 50 символов
            self._redirect(redirect_url) # вызываем метод _redirect для выполнения HTTP-перенаправления
    
    def _handle_currency_create_post(self, query_params: dict):
        '''
        Функция _handle_currency_create_post() обрабатывает создание новой валюты через POST-запрос
        Создаёт новую валюту на основе данных формы

        Параметры:
        query_params -- словарь параметров POST-запроса
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операции создания новой валюты через POST-запрос
            num_code = query_params.get('num_code', [''])[0] # получаем значение параметра 'num_code' из словаря query_params, если параметр отсутствует -- используем [''] и берем первый элемент
            char_code = query_params.get('char_code', [''])[0] # получаем значение параметра 'char_code' из словаря query_params, если параметр отсутствует -- используем [''] и берем первый элемент
            name = query_params.get('name', [''])[0] # получаем значение параметра 'name' из словаря query_params, если параметр отсутствует -- используем [''] и берем первый элемент
            value_str = query_params.get('value', [''])[0] # получаем значение параметра 'value' из словаря query_params, если параметр отсутствует -- используем [''] и берем первый элемент
            nominal_str = query_params.get('nominal', [''])[0] # получаем значение параметра 'nominal' из словаря query_params, если параметр отсутствует -- используем [''] и берем первый элемент
            
            if not all([num_code, char_code, name, value_str, nominal_str]): # проверяем, что все обязательные поля заполнены
                currencies = self.currency_controller.read_currencies() # вызываем метод read_currencies контроллера валют для получения текущего списка валют
                html_content = self.pages_controller.render_currencies( # вызываем метод render_currencies контроллера страниц для рендеринга страницы валют с сообщением об ошибке
                    currencies=currencies, # передаём текущий список валют
                    message="Please fill all fields", # сообщение об ошибке
                    message_type='error' # тип сообщения -- ошибка
                )
                self._send_response(html_content) # отправляем рендеренную страницу клиенту
                return # завершаем выполнение функции
            
            try: # начинаем вложенный блок try для безопасного преобразования строк в числа
                value = float(value_str) # преобразуем строковое значение курса в число с плавающей точкой
                nominal = int(nominal_str) # преобразуем строковое значение номинала в целое число
            except ValueError: # перехватываем исключение ValueError, которое возникает при неудачном преобразовании строки в число
                currencies = self.currency_controller.read_currencies() # получаем текущий список валют для отображения
                # рендерим страницу валют с сообщением об ошибке преобразования
                html_content = self.pages_controller.render_currencies(
                    currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                    message="Invalid numeric values", # сообщение об ошибке
                    message_type='error' # тип сообщения -- ошибка
                )
                self._send_response(html_content) # отправляем ответ клиенту
                return # завершаем выполнение функции
            
            if len(char_code.strip()) != 3: # проверяем, что символьный код после удаления пробелов состоит ровно из 3 символов
                currencies = self.currency_controller.read_currencies() # получаем текущий список валют
                html_content = self.pages_controller.render_currencies( # рендерим страницу валют с сообщением об ошибке длины кода
                    currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                    message="Currency code must be 3 characters", # сообщение об ошибке
                    message_type='error' # тип сообщения -- ошибка
                )
                self._send_response(html_content) # отправляем ответ клиенту
                return # завершаем выполнение функции
            
            existing_currency = self.currency_controller.read_currency_by_char_code(char_code) # вызываем метод read_currency_by_char_code для проверки существования валюты с таким символьным кодом
            if existing_currency: # если валюта с таким символьным кодом уже существует
                currencies = self.currency_controller.read_currencies() # получаем текущий список валют
                # рендерим страницу валют с сообщением о дублировании валюты
                html_content = self.pages_controller.render_currencies(
                    currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                    message=f"Currency {char_code} already exists", # сообщение об ошибке с указанием символьного кода
                    message_type='error' # тип сообщения -- ошибка
                )
                self._send_response(html_content) # отправляем ответ клиенту
                return # завершаем выполнение функции
            
            # создаём объект валюты с полученными и обработанными данными
            currency = Currency(
                num_code=num_code.strip(), # числовой код с удалением пробелов по краям
                char_code=char_code.strip().upper(), # символьный код с удалением пробелов и приведением к верхнему регистру
                name=name.strip(), # название с удалением пробелов по краям
                value=value, # преобразованное значение курса
                nominal=nominal # преобразованный номинал
            )
            
            currency_id = self.currency_controller.create_currency(currency) # вызываем метод create_currency контроллера валют для создания новой валюты в базе данных
            
            currencies = self.currency_controller.read_currencies() # получаем обновлённый список валют после создания новой
            
            if currency_id and currency_id > 0: # проверяем, что ID созданной валюты существует и больше 0
                # рендерим страницу валют с сообщением об успешном создании
                html_content = self.pages_controller.render_currencies(
                    currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                    message=f"Currency {char_code} added successfully!", # сообщение об успехе с указанием символьного кода
                    message_type='success' # тип сообщения -- успех
                )
            else: # если создание валюты не удалось
                # рендерим страницу валют с сообщением об ошибке создания
                html_content = self.pages_controller.render_currencies(
                    currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                    message=f"Error adding currency {char_code}", # сообщение об ошибке с указанием символьного кода
                    message_type='error' # тип сообщения -- ошибка
                )
            
            self._send_response(html_content) # отправляем рендеренную страницу клиенту
                
        except Exception as e: # перехватываем любое другое исключение, которое не было перехвачено ранее
            print(f"Error: {e}") # выводим полную информацию об ошибке в консоль сервера для отладки
            currencies = self.currency_controller.read_currencies() # получаем список валют для отображения даже при ошибке
            # рендерим страницу валют с сообщением об общей ошибке
            html_content = self.pages_controller.render_currencies(
                currencies=currencies, # передаём список валют в качестве аргумента для метода render_currencies
                message=f"Error: {str(e)[:50]}", # сообщение об ошибке с ограничением длины до 50 символов
                message_type='error' # тип сообщения -- ошибка
            )
            self._send_response(html_content) # отправляем ответ клиенту
    
    def _handle_currency_show(self):
        '''
        Функция _handle_currency_show() обрабатывает отладочную страницу валют
        Отображает список валют в консоли сервера для отладки
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операций отладочной страницы валют
            currencies = self.currency_controller.read_currencies() # вызываем метод read_currencies контроллера валют для получения полного списка валют из базы данных
            
            print("\nТЕКУЩИЕ ВАЛЮТЫ В БАЗЕ") # выводим заголовок блока в консоль сервера для визуального разделения отладочной информации
            for currency in currencies: # перебираем все валюты в полученном списке
                print(f"ID: {currency['id']}, Код: {currency['char_code']}, Название: {currency['name']}, Курс: {currency['value']}") # выводим подробную информацию о каждой валюте в консоль сервера в формате: ID, символьный код, название и курс
            print("-----------------------------------\n") # выводим разделитель в консоль сервера для завершения блока отладочной информации
            
            # многострочная строка с HTML-кодом отладочной страницы, которая будет отправлена клиенту
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Валюты (отладка)</title>
            </head>
            <body>
                <h1>Валюты в базе данных (отладка)</h1>
                <p>Информация выведена в консоль сервера</p>
                <a href="/currencies">Вернуться к таблице валют</a>
            </body>
            </html>
            '''
            
            self._send_response(html) # вызываем метод _send_response для отправки HTML-страницы клиенту с HTTP-статусом 200
        except Exception as e: # перехватываем любое исключение и сохраняем его в переменной e
            self._send_response(f"Ошибка: {str(e)}", 500) # отправляем клиенту простой текст с сообщением об ошибке и HTTP-статусом 500
    
    def _handle_404(self, message: str):
        '''
        Функция _handle_404() обрабатывает 404 ошибку
        Рендерит страницу с сообщением об ошибке 404

        Параметры:
        message -- сообщение об ошибке для отображения на странице
        '''
        try: # начинаем блок обработки исключений для безопасного рендеринга и отправки страницы 404
            html_content = self.pages_controller.render_404(message) # вызываем метод render_404 контроллера страниц для рендеринга HTML-страницы ошибки 404 с переданным сообщением
            self._send_response(html_content, 404) # отправляем рендеренную страницу 404 клиенту с HTTP-статусом 404
        except Exception as e: # перехватываем исключение, которое может возникнуть при рендеринге страницы 404
            self._send_response(f"Ошибка 404: {message}<br>Дополнительная ошибка: {str(e)}", 404) # отправляем клиенту простой HTML с оригинальным сообщением об ошибке 404 и дополнительной информацией о произошедшем исключении, также с HTTP-статусом 404
    
    def _redirect(self, url: str):
        '''
        Функция _redirect() выполняет перенаправление
        Отправляет HTTP-ответ 302 с заголовком Location

        Параметры:
        url -- URL для перенаправления
        '''
        try: # начинаем блок обработки исключений для безопасного выполнения операции HTTP-перенаправления
            if '?' in url: # проверяем, содержит ли URL строку параметров запроса -- '?'
                base_url, query_string = url.split('?', 1) # разделяем URL на две части по первому символу '?': базовый URL и строку параметров

                from urllib.parse import quote # импортируем функцию quote из модуля urllib.parse для кодирования URL
                safe_query = quote(query_string, safe='=&') # кодируем строку параметров, сохраняя символы '=' и '&' без изменений для сохранения структуры параметров
                safe_url = f"{base_url}?{safe_query}" # объединяем базовый URL с закодированной строкой параметров, формируя безопасный URL
            else: # если URL не содержит параметров запроса
                safe_url = url # используем исходный URL без изменений, так как кодирование не требуется
                
            self.send_response(302) # отправляем HTTP-статус 302, который указывает на временное перенаправление
            self.send_header('Location', safe_url) # отправляем HTTP-заголовок 'Location' с безопасным URL, куда клиент должен выполнить перенаправление
            self.end_headers() # завершаем отправку HTTP-заголовков
            print(f"Перенаправление на: {safe_url}") # выводим информационное сообщение в консоль сервера для отладки
        except Exception as e: # перехватываем любое исключение, которое может возникнуть при выполнении перенаправления
            print(f"Ошибка при перенаправлении: {e}") # выводим сообщение об ошибке в консоль сервера для отладки

            self.send_response(200) # отправляем HTTP-статус 200 вместо 302, так как прямое перенаправление не удалось
            self.send_header('Content-type', 'text/html; charset=utf-8') # отправляем HTTP-заголовок 'Content-Type' с указанием типа содержимого и кодировки
            self.end_headers() # завершаем отправку HTTP-заголовков
            # многострочная строка с HTML-кодом страницы, которая выполняет автоматическое перенаправление через meta-тег refresh
            html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Success</title>
                <meta http-equiv="refresh" content="1;url=/currencies">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .success {{ color: #4CAF50; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Currency added successfully!</h1>
                <div class="success">
                    <p>Redirecting to currencies page...</p>
                    <p>If redirection doesn't work, <a href="/currencies">click here</a></p>
                </div>
            </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8')) # записываем HTML-код, закодированный в UTF-8, в выходной поток для отправки клиенту
    
    def log_message(self, format: str, *args):
        '''
        Функция log_message() переопределяет логирование
        Выводит сообщения лога в консоль вместо стандартного вывода

        Параметры:
        format -- форматная строка для сообщения
        *args -- аргументы для форматной строки
        '''
        print(f"{self.address_string()} - {format % args}") # выводим сообщение лога в консоль


def run_server(port: int = 8000):
    '''
    Функция run_server() запускает HTTP-сервер
    Инициализирует контроллеры и запускает сервер на указанном порту

    Параметры:
    port -- порт для запуска сервера
    '''
    server_address = ('', port) # создаём кортеж с адресом сервера: пустая строка означает все доступные сетевые интерфейсы, port - номер порта для прослушивания
    
    print("Инициализация контроллеров") # выводим информационное сообщение в консоль о начале инициализации контроллеров приложения
    get_controllers() # вызываем функцию get_controllers для создания и инициализации всех контроллеров приложения перед запуском сервера
        
    def handler(*args, **kwargs): 
        '''
        Функция handler представляет собой фабрику обработчиков запросов
        Создаёт новый экземпляр CurrencyRequestHandler для каждого входящего HTTP-запроса
        
        Параметры:
        *args -- позиционные аргументы, передаваемые конструктору CurrencyRequestHandler
        **kwargs -- именованные аргументы, передаваемые конструктору CurrencyRequestHandler
        
        Возвращает:
        CurrencyRequestHandler -- новый экземпляр обработчика HTTP-запросов для текущего соединения
        '''
        return CurrencyRequestHandler(*args, **kwargs) # создаёт и возвращает новый экземпляр CurrencyRequestHandler с переданными аргументами
        
    httpd = HTTPServer(server_address, handler) # создаём экземпляр HTTP-сервера с указанным адресом и функцией-обработчиком
    
    try: # начинаем блок обработки исключений для безопасного выполнения операции HTTP-перенаправления
        print(f"\n{'-'*50}") # выводим разделитель
        print("Сервер запущен") # выводим сообщение о запуске сервера
        print(f"{'-'*50}") # выводим разделитель
        print(f"Порт: {port}") # выводим порт сервера
        print("Тип базы данных: SQLite in-memory (:memory:)") # выводим тип базы данных
        print("База сохраняется в течение всей работы сервера") # выводим информацию о сохранении базы
        print(f"{'-'*50}") # выводим разделитель
        print(f"\nДоступные маршруты:") # выводим заголовок списка маршрутов
        print(f"  http://localhost:{port}/ - Главная страница") # выводим маршрут главной страницы
        print(f"  http://localhost:{port}/author - Об авторе") # выводим маршрут страницы об авторе
        print(f"  http://localhost:{port}/users - Список пользователей") # выводим маршрут страницы пользователей
        print(f"  http://localhost:{port}/user?id=1 - Страница пользователя") # выводим маршрут страницы пользователя
        print(f"  http://localhost:{port}/currencies - Список валют") # выводим маршрут страницы валют
        print(f"  http://localhost:{port}/currency/show - Отладка") # выводим маршрут отладочной страницы
        print(f"{'-'*50}\n") # выводим разделитель
        
        httpd.serve_forever() # запускаем сервер в бесконечном цикле обработки запросов
    except KeyboardInterrupt: # перехватываем исключение KeyboardInterrupt, которое возникает при нажатии пользователем Ctrl+C в терминале
        print("\nСервер остановлен") # выводим сообщение об остановке сервера
        httpd.server_close() # закрываем соединение сервера


if __name__ == '__main__':
    run_server() # запускаем сервер