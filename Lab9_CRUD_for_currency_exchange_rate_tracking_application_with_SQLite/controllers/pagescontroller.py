from jinja2 import Environment, FileSystemLoader # импортируем Environment и FileSystemLoader из jinja2 для работы с шаблонами
from models.author import Author # импортируем класс Author из модуля models.author для работы с данными автора
import os # импортируем os для работы с файловой системой


class PagesController:
    '''
    Класс PagesController отвечает только за рендеринг HTML-страниц
    '''
    def __init__(self):
        '''
        Функция __init__() инициализирует контроллер страниц
        '''
        main_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # получаем путь к основной папке проекта
        templates_folder_path = os.path.join(main_folder_path, 'templates') # формируем путь к папке с шаблонами
        self.env = Environment( # создаём объект окружения jinja2
            loader=FileSystemLoader(templates_folder_path), # указываем загрузчик шаблонов из файловой системы
            autoescape=True # включаем автоматическое экранирование html
        )
        
        self.author = Author(name='Романова Анна Андреевна', group='P3120') # создаём объект автора с данными
        self.app_name = 'Валютка-минутка!' # задаём название приложения
        self.app_version = '1.0.0' # задаём версию приложения
    
    def render_template(self, template_name: str, **context) -> str:
        '''
        Функция render_template рендерит шаблон Jinja2
        
        Параметры:
        template_name -- имя файла шаблона
        **context -- дополнительные параметры для передачи в шаблон
        
        Возвращает:
        строка -- отрендеренный HTML
        '''
        try: # начинаем блок обработки исключений
            template = self.env.get_template(template_name) # загружаем шаблон по имени
            return template.render(**context) # рендерим шаблон с переданным контекстом и возвращаем результат
        except Exception as e: # перехватываем исключения
            return self._render_error_page(f'Ошибка шаблона: {str(e)}') # возвращаем страницу ошибки в случае исключения
    
    def get_common_context(self) -> dict:
        '''
        Функция get_common_context возвращает общий контекст для всех страниц
        
        Возвращает:
        словарь -- общий контекст
        '''
        # возвращаем словарь с общим контекстом
        return {
            'myapp': { # раздел с информацией о приложении
                'name': self.app_name, # добавляем название приложения
                'version': self.app_version # добавляем версию приложения
            },
            'author': self.author # добавляем объект автора
        }
    
    def render_index(self, stats: dict, currencies: list) -> str:
        '''
        Функция render_index рендерит главную страницу
        
        Параметры:
        stats -- статистика приложения
        currencies -- список валют для отображения
        
        Возвращает:
        строка -- HTML главной страницы
        '''
        context = self.get_common_context() # получаем общий контекст
        context.update({ # обновляем контекст дополнительными данными
            'stats': stats, # добавляем статистику
            'currencies': currencies[:5] if currencies else [] # добавляем первые 5 валют или пустой список
        })
        
        return self.render_template('index.html', **context) # рендерим шаблон index.html с обновлённым контекстом
    
    def render_author(self) -> str:
        '''
        Функция render_author рендерит страницу об авторе
        
        Возвращает:
        строка -- HTML страницы об авторе
        '''
        context = self.get_common_context() # получаем общий контекст
        return self.render_template('author.html', **context) # рендерим шаблон author.html с общим контекстом
    
    def render_users(self, users: list, total_subscriptions: int) -> str:
        '''
        Функция render_users рендерит страницу со списком пользователей
        
        Параметры:
        users -- список пользователей
        total_subscriptions -- общее количество подписок
        
        Возвращает:
        строка -- HTML страницы пользователей
        '''
        context = self.get_common_context() # получаем общий контекст
        context.update({ # обновляем контекст дополнительными данными
            'users': users, # добавляем список пользователей
            'total_subscriptions': total_subscriptions # добавляем общее количество подписок
        })
        
        return self.render_template('users.html', **context) # рендерим шаблон users.html с обновлённым контекстом
    
    def render_user(self, user: dict, subscribed_currencies: list) -> str:
        '''
        Функция render_user рендерит страницу конкретного пользователя
        
        Параметры:
        user -- данные пользователя
        subscribed_currencies -- список подписанных валют
        
        Возвращает:
        строка -- HTML страницы пользователя или страницу 404
        '''
        if not user: # проверяем, отсутствует ли пользователь
            return self.render_404('Пользователь не найден') # возвращаем страницу 404
        
        context = self.get_common_context() # получаем общий контекст
        context.update({ # обновляем контекст дополнительными данными
            'user': user, # добавляем данные пользователя
            'subscribed_currencies': subscribed_currencies # добавляем список подписанных валют
        })
        
        return self.render_template('user.html', **context) # рендерим шаблон user.html с обновлённым контекстом
    
    def render_currencies(self, currencies: list, message: str = None, message_type: str = 'info') -> str:
        '''
        Функция render_currencies рендерит страницу со списком валют
        
        Параметры:
        currencies -- список валют
        message -- сообщение для отображения
        message_type -- тип сообщения
        
        Возвращает:
        строка -- HTML страницы валют
        '''
        context = self.get_common_context() # получаем общий контекст
        context.update({ # обновляем контекст дополнительными данными
            'currencies': currencies, # добавляем список валют
            'message': message, # добавляем сообщение
            'message_type': message_type # добавляем тип сообщения
        })
        
        return self.render_template('currencies.html', **context) # рендерим шаблон currencies.html с обновлённым контекстом
    
    def render_404(self, message: str = 'Страница не найдена') -> str:
        '''
        Функция render_404 рендерит страницу 404
        
        Параметры:
        message -- сообщение об ошибке
        
        Возвращает:
        строка -- HTML страницы 404
        '''
        context = self.get_common_context() # получаем общий контекст
        context.update({ # обновляем контекст дополнительными данными
            'error_message': message # добавляем сообщение об ошибке
        })
        
        return self._render_error_page(message, context) # вызываем внутренний метод для рендеринга страницы ошибки
    
    def _render_error_page(self, message: str, context: dict = None) -> str:
        '''
        Внутренняя функция для рендеринга страницы ошибки
        '''
        if not context: # проверяем, отсутствует ли контекст
            context = self.get_common_context() # получаем общий контекст
            context['error_message'] = message # добавляем сообщение об ошибке в контекст
        
        # возвращаем многострочную f-строку с HTML-кодом страницы ошибки, включающую в себя базовую структуру, стили, навигацию и сообщение об ошибке
        return f''' # возвращаем html-страницу ошибки как строку f-строки
        <!DOCTYPE html>
        <html>
        <head>
            <title>{context['myapp']['name']} - Ошибка</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: #d32f2f; margin: 20px 0; }}
                .nav {{ margin: 20px 0; }}
                .nav a {{ margin-right: 15px; text-decoration: none; color: #0066cc; }}
                .nav a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>{context['myapp']['name']}</h1>
            <div class='nav'>
                <a href='/'>Главная</a>
                <a href='/users'>Пользователи</a>
                <a href='/currencies'>Курсы валют</a>
                <a href='/author'>Об авторе</a>
            </div>
            <div class='error'>
                <h2>Ошибка</h2>
                <p>{message}</p>
                <a href='/'>Вернуться на главную</a>
            </div>
        </body>
        </html>
        '''