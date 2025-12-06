from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies_full_info


main_folder_path = os.path.dirname(os.path.abspath(__file__)) # находим путь к папке проекта (Lab8)
templates_folder_path = os.path.join(main_folder_path, 'templates') # находим путь к папке templates внутри папки проекта
env = Environment( # создаём окружение Jinja2, отвечающее за шаблоны
    loader=FileSystemLoader(templates_folder_path), # загружаем путь к шаблонам
    autoescape=select_autoescape() # экранируем HTML для безопасности
)

author_inf = Author(name="Романова Анна Андреевна", group="P3120") # задаём информацию об авторе для класса Author
myapp = App(name="Валютка-минутка!", version="1.0.0", author=author_inf) # задаём информацию об приложении для класса App

# создаём список пользователей с их номерами id и именами name
users = [
    User(id=1, name="Алексей Петров"),
    User(id=2, name="Даниил Козлов"),
    User(id=3, name="Ангелина Иванченко"),
]

# создаём список валют
currencies = []

# создаём список валют, на которые подписаны пользователи с номером id, номером пользователя user_id и именем валюты currency_name
user_currencies = [
    UserCurrency(id=1, user_id=1, currency_name="USD"),
    UserCurrency(id=2, user_id=1, currency_name="EUR"),
    UserCurrency(id=3, user_id=2, currency_name="CNY"),
    UserCurrency(id=4, user_id=3, currency_name="USD"),
]

def init_currencies():
    '''
    Функция init_currencies нициализирует валюты при запуске
    '''
    global currencies # объявляем глобальную переменную currencies
    
    try: # начинаем блок try для обработки всех исключений
        currencies_data = get_currencies_full_info() # получаем информацию о валютах из API
        
        currencies.clear() # очищаем список перед заполнением
        
        for char_code, data in currencies_data.items(): # проходимся по информации о валютах, берём их символьный код (char_code) и другую информацию (data)
            currency = Currency( # создаём объект Currency для каждой валюты с информацией о ней
                id=data.get('id', ''), # номер валюты
                char_code=char_code, # символьный код валюты
                name=data.get('name', ''), # название валюты
                value=data.get('value', 0.0), # курс валюты к рублю
                nominal=data.get('nominal', 1) # номинал валюты
            )
            currencies.append(currency) # добавляем валюту в список
        
    except Exception as e: # перехватываем любую ошибку и записываем информацию о ней в e
        # создаём тестовые данные
        test_data = [
            Currency(id="ERROR01", char_code="USD", name="Доллар США", value=75.5, nominal=1),
            Currency(id="ERROR02", char_code="EUR", name="Евро", value=85.3, nominal=1),
            Currency(id="ERROR03", char_code="CNY", name="Юань", value=11.8, nominal=10),
        ]
        currencies.extend(test_data) # добавляем тестовые данные в список валют


class CurrencyRequestHandler(BaseHTTPRequestHandler):
    '''
    Класс-обработчик HTTP-запросов
    '''
    def _set_headers(self, content_type='text/html; charset=utf-8'):
        '''
        Установка HTTP-заголовков ответа
        '''
        self.send_response(200) # отправляем статус 200 (OK)
        self.send_header('Content-type', content_type) # устанавливаем тип отправляемых данныых
        self.end_headers() # завершаем добавление заголовков
    
    def _render_template(self, template_name: str, **context):
        '''
        Рендеринг шаблона Jinja2 с переданным контекстом
        '''
        try: # начинаем блок try для обработки всех исключений
            template = env.get_template(template_name) # загружаем шаблон по имени
            return template.render(**context) # рендерим шаблон в готовый HTML, подставляя переданные данные
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
        Обработка всех GET-запросов
        '''
        parsed_path = urlparse(self.path) # делаем парсинг URL
        path = parsed_path.path # извлекаем путь
        query_params = parse_qs(parsed_path.query) # разбираем параметры запроса
        
        # маршрутизация
        if path == '/':
            self._handle_home() # вызываем метод для отображения главной страницы
        elif path == '/users':
            self._handle_users() # вызываем метод для отображения страницы со списком всех пользователей
        elif path == '/user':
            self._handle_user(query_params) # вызываем метод для отображения страницы с детальной информацией о конкретном пользователе
        elif path == '/currencies':
            self._handle_currencies(query_params) # вызываем метод для отображения страницы с курсами валют
        elif path == '/author':
            self._handle_author() # вызываем метод для отображения страницы "Об авторе"
        else:
            self._handle_404(f"Страница {path} не найдена") # вызываем метод для обработки ошибки "страница не найдена"
    
    def _handle_home(self):
        '''
        Главная страница
        '''
        stats = { # создаём статистику для отображения на главной странице
            'total_users': len(users), # указываем количество пользователей
            'total_currencies': len(currencies), # указываем количество валют
        }
        
        html_content = self._render_template( # рендерим шаблон главной страницы
            "index.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            author=author_inf, # передаём объект автора
            stats=stats # передаём статистику
        )
        
        self._set_headers() # устанавливаем заголовки ответа
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML
    
    def _handle_users(self):
        '''
        Список пользователей
        '''
        html_content = self._render_template( # рендерим шаблон страницы со списком всех пользователей
            "users.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            users=users, # передаём объект списка пользователей
            user_currencies=user_currencies, # передаём объект подписок пользователей
            currencies=currencies # передаём объект списка валют
        )
        
        self._set_headers() # устанавливаем заголовки ответа
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML

    def _handle_user(self, query_params):
        '''
        Информация о пользователе
        '''
        user_id = query_params.get('id', [None])[0] # извлекаем номер (id) пользователя из параметров запроса
        
        if not user_id: # проверяем, был ли передан номер id пользователя
            self._handle_404("ID пользователя не передан") # показываем страницу 404 с ошибкой
            return # завершаем выполнение метода
        
        try: # начинаем блок try для обработки всех исключений
            user_id = int(user_id) # преобразуем id в целое число
            user = next((u for u in users if u.id == user_id), None) # ищем пользователя с таким номером в списке users
            
            if not user: # проверяем, не нашёлся ли такой пользователь
                self._handle_404(f"Пользователь {user_id} не найден") # показываем страницу 404 с ошибкой
                return
            
            user_subs = [uc for uc in user_currencies if uc.user_id == user_id] # находим подписки этого пользователя
            
            subscribed_currencies = [] # создаём пустой список для хранения валют, на которые подписан пользователь
            for sub in user_subs: # проходим по всем подпискам пользователя
                currency = next((c for c in currencies if c.char_code == sub.currency_name), None) # для каждой подписки ищем соответствующую валюту
                if currency: # проверяем, найдена ли валюта
                    subscribed_currencies.append(currency) # добавляем валюту в список
            
            html_content = self._render_template( # рендерим шаблон страницы с детальной информацией о конкретном пользователе
                "user.html", # передаём имя файла шаблона
                myapp=myapp, # передаём объект приложения
                user=user, # передаём объект пользователя
                subscribed_currencies=subscribed_currencies, # передаём список валют пользователя
                user_subs=user_subs # передаём список подписок пользователя
            )
            
            self._set_headers() # устанавливаем заголовки ответа
            self.wfile.write(html_content.encode('utf-8')) # отправляем HTML
            
        except ValueError: # обрабатываем исключение ValueError
            self._handle_404("Некорректный id пользователя") # показываем страницу 404 с ошибкой
    
    def _handle_currencies(self, query_params):
        '''
        Обработка запроса на список валют
        '''
        html_content = self._render_template( # рендерим шаблон страницы с курсами валют
            "currencies.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            currencies=currencies, # передаём объект списка валют
        )
        
        self._set_headers() # устанавливаем заголовки ответа
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML
    
    def _handle_author(self):
        '''
        Обработка запроса на информацию об авторе
        '''
        html_content = self._render_template( # рендерим шаблон страницы "Об авторе"
            "author.html", # передаём имя файла шаблона
            myapp=myapp, # передаём объект приложения
            author=author_inf # передаём объект автора
        )
        
        self._set_headers() # устанавливаем заголовки ответа
        self.wfile.write(html_content.encode('utf-8')) # отправляем HTML
    
    def _handle_404(self, path):
        '''
        Обработка 404 ошибки (страница не найдена)
        '''
        self.send_response(404) # отправляем статус 404
        self.send_header('Content-type', 'text/html; charset=utf-8') # устанавливаем HTTP-заголовок
        self.end_headers() # завершаем добавление заголовков

        # возвращаем HTML-страницу с ошибкой        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>404 - Not Found</title></head>
        <body>
            <h1>404 - Страница не найдена</h1>
            <p>{path}</p>
            <a href="/">Вернуться на главную</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8')) # отправляем HTML с сообщением об ошибке


def run_server(port=8000):
    '''
    Запуск HTTP-сервера
    '''
    init_currencies() # инициализируем валюты при старте сервера
    
    server_address = ('', port) # создаём адрес, на котором будет работать сервер
    httpd = HTTPServer(server_address, CurrencyRequestHandler) # создаём экземпляр HTTP-сервера
    
    try: # начинаем блок try для обработки всех исключений
        httpd.serve_forever() # запускаем сервер в бесконечном цикле
    except KeyboardInterrupt: # обрабатываем исключение KeyboardInterrupt
        pass # завершаем работу сервера без сообщения


if __name__ == '__main__':
    run_server() # вызываем главную функцию