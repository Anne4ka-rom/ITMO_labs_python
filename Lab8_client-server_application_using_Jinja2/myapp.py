from http.server import HTTPServer, BaseHTTPRequestHandler # импортируем HTTPServer и BaseHTTPRequestHandler из http.server для создания HTTP-сервера
from urllib.parse import urlparse, parse_qs # импортируем urlparse и parse_qs из urllib.parse для разбора URL и параметров запроса
from jinja2 import Environment, FileSystemLoader, select_autoescape # импортируем Environment, FileSystemLoader и select_autoescape из jinja2 для работы с шаблонами
import os # импортируем os для работы с операционной системой и файловыми путями

from models import Author, App, User, Currency, UserCurrency # импортируем модели данных из модуля models
from utils.currencies_api import get_currencies # импортируем функцию get_currencies из модуля utils.currencies_api для получения курсов валют с API ЦБ РФ


main_folder_path = os.path.dirname(os.path.abspath(__file__)) # находим путь к папке проекта, используя абсолютный путь текущего файла
templates_folder_path = os.path.join(main_folder_path, 'templates') # находим путь к папке templates внутри папки проекта, объединяя путь к проекту и имя папки шаблонов
env = Environment( # создаём окружение Jinja2, отвечающее за шаблоны
    loader=FileSystemLoader(templates_folder_path), # загружаем путь к шаблонам, указывая FileSystemLoader на папку templates
    autoescape=select_autoescape() # экранируем HTML для безопасности, автоматически включая экранирование для предотвращения XSS-атак
)

author_inf = Author(name="Романова Анна Андреевна", group="P3120") # задаём информацию об авторе для класса Author, создавая объект Author с именем и группой
myapp = App(name="Валютка-минутка!", version="1.0.0", author=author_inf) # задаём информацию о приложении для класса App, создавая объект App с названием, версией и автором

# создаём список пользователей с их номерами id и именами name
users = [
    User(id=1, name="Алексей Петров"), # создаём первого пользователя с id=1 и именем "Алексей Петров"
    User(id=2, name="Даниил Козлов"), # создаём второго пользователя с id=2 и именем "Даниил Козлов"
    User(id=3, name="Ангелина Иванченко"), # создаём третьего пользователя с id=3 и именем "Ангелина Иванченко"
]

currencies = [] # создаём пустой список для хранения объектов Currency, который будет заполнен при инициализации валют

# создаём список валют, на которые подписаны пользователи с номером id, номером пользователя user_id и именем валюты currency_name
user_currencies = [
    UserCurrency(id=1, user_id=1, currency_name="USD"), # создаём подписку первого пользователя на USD с id=1
    UserCurrency(id=2, user_id=1, currency_name="EUR"), # создаём подписку первого пользователя на EUR с id=2
    UserCurrency(id=3, user_id=2, currency_name="CNY"), # создаём подписку второго пользователя на CNY с id=3
    UserCurrency(id=4, user_id=3, currency_name="USD"), # создаём подписку третьего пользователя на USD с id=4
]

api_error = None # создаём глобальную переменную для хранения ошибки API, инициализируя её значением None

def init_currencies():
    '''
    Функция init_currencies нициализирует валюты при запуске
    '''
    global api_error, currencies # объявляем глобальные переменные api_error и currencies для возможности их изменения внутри функции
    
    try: # начинаем блок try для обработки всех исключений
        currencies_data = get_currencies(["USD", "EUR", "CNY", "GBP", "JPY", "KZT"]) # получаем информацию о валютах из API, передавая список кодов валют
        
        currencies.clear() # очищаем список перед заполнением, удаляя все существующие элементы из списка currencies
        
        for char_code, data in currencies_data.items(): # проходимся по информации о валютах, берём их символьный код char_code и другую информацию data
            currency = Currency(  # создаём объект Currency для каждой валюты с информацией о ней
                id=data.get('id', ''), # номер валюты, используя метод get для безопасного доступа с значением по умолчанию ''
                char_code=char_code, # символьный код валюты, берём из ключа словаря
                num_code=data.get('num_code', ''), # цифровой код валюты, используя метод get для безопасного доступа с значением по умолчанию ''
                name=data.get('name', ''), # название валюты, используя метод get для безопасного доступа с значением по умолчанию ''
                value=data.get('value', 0.0), # курс валюты к рублю, используя метод get для безопасного доступа с значением по умолчанию 0.0
                nominal=data.get('nominal', 1) # номинал валюты, используя метод get для безопасного доступа с значением по умолчанию 1
            )
            currencies.append(currency) # добавляем валюту в список, помещая созданный объект Currency в список currencies
        api_error = None # очищаем ошибку при успешной загрузке, устанавливая api_error в None
        return True # возвращаем успешный статус, указывая что инициализация прошла успешно
        
    except Exception as e: # перехватываем любую ошибку и записываем информацию о ней в e
        api_error = f"Ошибка загрузки данных с сайта ЦБ РФ: {str(e)}" # создаём сообщение об ошибке API, включая текст исключения
        currencies.clear() # очищаем список валют, удаляя все элементы из списка currencies при ошибке
        return False # возвращаем статус ошибки, указывая что инициализация не удалась


class CurrencyRequestHandler(BaseHTTPRequestHandler):
    '''
    Класс CurrencyRequestHandler наследует BaseHTTPRequestHandler и обрабатывает HTTP-запросы
    '''
    def _set_headers(self, content_type='text/html; charset=utf-8'):
        '''
        Функция _set_headers устанавливает HTTP-заголовки ответа
        '''
        self.send_response(200) # отправляем статус 200 клиенту
        self.send_header('Content-type', content_type) # устанавливаем тип отправляемых данных, указывая content-type
        self.end_headers() # завершаем добавление заголовков, сигнализируя что все заголовки отправлены
    
    def _render_template(self, template_name: str, **context):
        '''
        Функция _render_template рендерит шаблон Jinja2 с переданным контекстом
        '''
        try: # начинаем блок try для обработки всех исключений
            template = env.get_template(template_name) # загружаем шаблон по имени из окружения Jinja2
            return template.render(**context) # рендерим шаблон в готовый HTML, подставляя переданные данные через распаковку словаря context
        except Exception as e: # перехватываем любую ошибку и записываем информацию о ней в e
            # возвращаем HTML-страницу с ошибкой
            return f"""
            <!DOCTYPE html>
            <html>
            <head><title>Ошибка</title></head>
            <body>
                <h1>Ошибка шаблона</h1>
                <p>{str(e)}</p>
            </body>
            </html>
            """
    
    def do_GET(self):
        '''
        Функция do_GET обрабатывает все GET-запросы
        '''
        parsed_path = urlparse(self.path) # делаем парсинг URL, разбирая путь запроса на компоненты
        path = parsed_path.path # извлекаем путь из распарсенного URL
        query_params = parse_qs(parsed_path.query) # разбираем параметры запроса, преобразуя строку запроса в словарь
        if path in ['/', '/currencies', '/user', '/users']: # проверяем, находится ли путь в списке путей, требующих актуальных данных о валютах
            init_currencies() # вызываем функцию инициализации валют для получения актуальных курсов
        
        # маршрутизация
        if path == '/': # проверяем, является ли путь корневым
            self._handle_home() # вызываем метод для отображения главной страницы
        elif path == '/users': # проверяем, является ли путь '/users'
            self._handle_users() # вызываем метод для отображения страницы со списком всех пользователей
        elif path == '/user': # проверяем, является ли путь '/user'
            self._handle_user(query_params) # вызываем метод для отображения страницы с детальной информацией о конкретном пользователе, передавая параметры запроса
        elif path == '/currencies': # проверяем, является ли путь '/currencies'
            self._handle_currencies(query_params) # вызываем метод для отображения страницы с курсами валют, передавая параметры запроса
        elif path == '/author': # проверяем, является ли путь '/author'
            self._handle_author() # вызываем метод для отображения страницы "Об авторе"
        else: # если путь не соответствует ни одному из известных маршрутов
            self._handle_404(f"Страница {path} не найдена") # вызываем метод для обработки ошибки "страница не найдена", передавая сообщение с путём
    
    def _handle_home(self):
        '''
        Функция _handle_home обрабатывает главную страницу
        '''
        if api_error: # проверяем, установлена ли глобальная переменная api_error
            self._handle_api_error() # вызываем метод обработки ошибки API
            return # завершаем выполнение метода
        
        stats = { # создаём статистику для отображения на главной странице
            'total_users': len(users), # указываем количество пользователей, вычисляя длину списка users
            'total_currencies': len(currencies), # указываем количество валют, вычисляя длину списка currencies
        }
        
        html_content = self._render_template( # рендерим шаблон главной страницы
            "index.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            author=author_inf, # передаём объект автора
            stats=stats # передаём статистику
        )
        
        self._set_headers() # устанавливаем заголовки ответа, вызывая метод _set_headers
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML, кодируя строку в UTF-8 и записывая в выходной поток

    def _handle_users(self):
        '''
        Функция _handle_users обрабатывает страницу со списком пользователей
        '''
        if api_error: # проверяем, установлена ли глобальная переменная api_error
            self._handle_api_error() # вызываем метод обработки ошибки API
            return # завершаем выполнение метода
        
        html_content = self._render_template( # рендерим шаблон страницы со списком всех пользователей
            "users.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            users=users, # передаём объект списка пользователей
            user_currencies=user_currencies, # передаём объект подписок пользователей
            currencies=currencies # передаём объект списка валют
        )
        
        self._set_headers() # устанавливаем заголовки ответа, вызывая метод _set_headers
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML, кодируя строку в UTF-8 и записывая в выходной поток

    def _handle_user(self, query_params):
        '''
        Функция _handle_user обрабатывает страницу информации о пользователе
        '''
        if api_error: # проверяем, установлена ли глобальная переменная api_error
            self._handle_api_error() # вызываем метод обработки ошибки API
            return # завершаем выполнение метода
        
        user_id = query_params.get('id', [None])[0] # извлекаем номер id пользователя из параметров запроса, получая значение по ключу 'id' или None
    
        if not user_id: # проверяем, не является ли user_id пустым или None
            self._handle_404("ID пользователя не передан") # показываем страницу 404 с ошибкой, вызывая метод _handle_404 с сообщением
            return # завершаем выполнение метода
        
        try: # начинаем блок try для обработки всех исключений
            user_id = int(user_id) # преобразуем id в целое число, пытаясь преобразовать строку в int
            user = next((u for u in users if u.id == user_id), None) # ищем пользователя с таким номером в списке users, используя генератор и функцию next
            
            if not user: # проверяем, не нашёлся ли такой пользователь
                self._handle_404(f"Пользователь {user_id} не найден") # показываем страницу 404 с ошибкой, вызывая метод _handle_404 с сообщением
                return # завершаем выполнение метода
            
            user_subs = [uc for uc in user_currencies if uc.user_id == user_id] # находим подписки этого пользователя, фильтруя список user_currencies по user_id
            
            subscribed_currencies = [] # создаём пустой список для хранения валют, на которые подписан пользователь
            for sub in user_subs: # проходим по всем подпискам пользователя
                currency = next((c for c in currencies if c.char_code == sub.currency_name), None) # для каждой подписки ищем соответствующую валюту по коду
                if currency: # проверяем, найдена ли валюта
                    subscribed_currencies.append(currency) # добавляем валюту в список подписанных валют
            
            html_content = self._render_template( # рендерим шаблон страницы с детальной информацией о конкретном пользователе
                "user.html", # передаём имя файла шаблона
                myapp=myapp, # передаём объект приложения
                user=user, # передаём объект пользователя
                subscribed_currencies=subscribed_currencies, # передаём список валют пользователя
                user_subs=user_subs # передаём список подписок пользователя
            )
            
            self._set_headers() # устанавливаем заголовки ответа, вызывая метод _set_headers
            self.wfile.write(html_content.encode('utf-8')) # отправляем HTML, кодируя строку в UTF-8 и записывая в выходной поток
            
        except ValueError: # обрабатываем исключение ValueError
            self._handle_404("Некорректный id пользователя") # показываем страницу 404 с ошибкой, вызывая метод _handle_404 с сообщением

    def _handle_currencies(self, query_params):
        '''
        Функция _handle_currencies обрабатывает запрос на список валют
        '''
        if api_error: # проверяем, установлена ли глобальная переменная api_error
            self._handle_api_error() # вызываем метод обработки ошибки API
            return # завершаем выполнение метода
        
        html_content = self._render_template( # рендерим шаблон страницы с курсами валют
            "currencies.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            currencies=currencies, # передаём объект списка валют
        )
        
        self._set_headers() # устанавливаем заголовки ответа, вызывая метод _set_headers
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML, кодируя строку в UTF-8 и записывая в выходной поток
    
    def _handle_author(self):
        '''
        Функция _handle_author обрабатывает запрос на страницу об авторе
        '''
        html_content = self._render_template( # рендерим шаблон страницы об авторе
            "author.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            author=author_inf # передаём объект автора
        )
        
        self._set_headers() # устанавливаем заголовки ответа, вызывая метод _set_headers
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML, кодируя строку в UTF-8 и записывая в выходной поток
    
    def _handle_404(self, message):
        '''
        Функция _handle_404 обрабатывает 404 ошибку (страница не найдена)
        '''
        self.send_response(404) # отправляем статус 404 клиенту
        self.send_header('Content-type', 'text/html; charset=utf-8') # устанавливаем HTTP-заголовок, указывая content-type
        self.end_headers() # завершаем добавление заголовков

        # возвращаем HTML-страницу с ошибкой        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>404 - Not Found</title></head>
        <body>
            <h1>404 - Страница не найдена</h1>
            <p>{message}</p>
            <a href="/">Вернуться на главную</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8')) # отправляем HTML с сообщением об ошибке, кодируя строку в UTF-8 и записывая в выходной поток

    def _handle_api_error(self):
        '''
        Функция _handle_api_error обрабатывает ошибку API (сервис недоступен)
        '''
        self.send_response(503) # отправляем статус 503 клиенту
        self.send_header('Content-type', 'text/html; charset=utf-8') # устанавливаем HTTP-заголовок, указывая content-type
        self.end_headers() # завершаем добавление заголовков

        # возвращаем HTML-страницу с ошибкой API
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Ошибка API</title></head>
        <body>
            <h1>Сервис временно недоступен</h1>
            <p>{api_error}</p>
            <p>Пожалуйста, попробуйте обновить страницу позже.</p>
            <a href="/">Вернуться на главную</a>
        </body>
        </html>
        """

        self.wfile.write(html.encode('utf-8')) # отправляем HTML с сообщением об ошибке API, кодируя строку в UTF-8 и записывая в выходной поток

def run_server(port=8000):
    '''
    Функция run_server запускает HTTP-сервер
    '''
    init_currencies() # инициализируем валюты при старте сервера, вызывая функцию init_currencies
    
    server_address = ('', port) # создаём адрес, на котором будет работать сервер, используя пустой хост и указанный порт
    httpd = HTTPServer(server_address, CurrencyRequestHandler) # создаём экземпляр HTTP-сервера, передавая адрес и класс-обработчик
    
    try: # начинаем блок try для обработки всех исключений
        print(f"Сервер запущен на порту {port}") # выводим сообщение о запуске сервера с указанием порта
        print(f"Состояние API: {'Ошибка!' if api_error else 'OK'}") # выводим состояние API, проверяя значение api_error
        if api_error: # проверяем, есть ли ошибка API
            print(f"Сообщение об ошибке: {api_error}") # выводим сообщение об ошибке, если она есть
        httpd.serve_forever() # запускаем сервер в бесконечном цикле, начинаем слушать запросы
    except KeyboardInterrupt: # обрабатываем исключение KeyboardInterrupt
        print("\nСервер остановлен") # выводим сообщение об остановке сервера


if __name__ == '__main__':
    run_server() # вызываем главную функцию, запуская сервер при непосредственном выполнении файла