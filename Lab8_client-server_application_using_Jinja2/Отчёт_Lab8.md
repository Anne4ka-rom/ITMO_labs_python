
# Федеральное государственное автономное образовательное учреждение высшего образования «Научно-образовательная корпорация ИТМО»  

## **ФАКУЛЬТЕТ ПРОГРАММНОЙ ИНЖЕНЕРИИ И КОМПЬЮТЕРНОЙ ТЕХНИКИ**

### **Лабораторная работа №8**

#### По дисциплине «Программирование на Python»
Работу выполнила: Романова Анна Андреевна
Группа: P3120
Преподаватель: Жуков Николай Николаевич
# **1. Цель лабораторной работы**
1. Создать простое клиент-серверное приложение на Python без серверных фреймворков.
2. Освоить работу с HTTPServer и маршрутизацию запросов.
3. Применять шаблонизатор Jinja2 для отображения данных.
4. Реализовать модели предметной области (User, Currency, UserCurrency, App, Author) с геттерами и сеттерами.
5. Структурировать код в соответствии с архитектурой MVC.
6. Получать данные о курсах валют через функцию get_currencies и отображать их пользователям.
7. Реализовать функциональность подписки пользователей на валюты и отображение динамики их изменения.
8. Научиться создавать тесты для моделей и серверной логики.
## **2. Описание предметной области**
## **Author**
- name — имя автора
- group — учебная группа
## **App**
- name — название приложения
- version — версия приложения
- author — объект Author
## **User**
- id — уникальный идентификатор
- name — имя пользователя
## **Currency**
- id — уникальный идентификатор
- num_code — цифровой код
- char_code — символьный код
- name — название валюты
- value — курс
- nominal — номинал (за сколько единиц валюты указан курс)
# **3. Структура проекта**
Lab8/
├── models/ # Модели предметной области (MVC-Model)
│ ├── __init__.py # Импорт всех моделей
│ ├── author.py # Класс Author
│ ├── app.py # Класс App
│ ├── user.py # Класс User
│ ├── currency.py # Класс Currency
│ └── user_currency.py # Класс UserCurrency
├── templates/ # Шаблоны Jinja2 (MVC-View)
│ ├── index.html # Главная страница
│ ├── users.html # Список пользователей
│ ├── user.html # Страница пользователя
│ ├── currencies.html # Курсы валют
│ └── author.html # Об авторе
├── static/ # Статические файлы
│ └── style.css # CSS стили
├── utils/ # Утилиты
│ └── currencies_api.py # Функции работы с API ЦБ РФ
├── tests/ # Тесты
│ ├── test_models.py # Тесты моделей
│ ├── test_currencies_api.py # Тесты API
│ ├── test_myapp.py # Тесты сервера
│ └── test_templates.py # Тесты шаблонов
└── myapp.py # Основной файл приложения (MVC-Controller)
# **4. Фрагменты логов**
Все модели реализованы с использованием геттеров и сеттеров для обеспечения валидации данных:
```python
class Currency:
    def __init__(self, id: str, char_code: str, name: str, value: float, nominal: int):
        self._id = None
        self._char_code = None
        self._name = None
        self._value = None
        self._nominal = None
        self.id = id
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal
    @property
    def value(self) -> float:
        return self._value
    @value.setter
    def value(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Курс должен быть числом")
        if value <= 0:
            raise ValueError("Курс должен быть положительным числом")
        self._value = float(value)
```
Особенности реализации:
- Все сеттеры проверяют тип данных
- Выполняется валидация на корректность значений
- При инициализации используются свойства для немедленной проверки
Сервер реализован на базе стандартного HTTPServer и BaseHTTPRequestHandler:
```python
class CurrencyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        if path == '/':
            self._handle_home()
        elif path == '/users':
            self._handle_users()
        elif path == '/user':
            self._handle_user(query_params)
        elif path == '/currencies':
            self._handle_currencies(query_params)
        elif path == '/author':
            self._handle_author()
        else:
            self._handle_404(f"Страница {path} не найдена")
```
Поддерживаемые маршруты:
- / - главная страница со статистикой
- /users - список всех пользователей
- /user?id=... - детальная информация о пользователе и его подписках
- /currencies - таблица курсов валют
- /author - информация об авторе
Инициализация окружения Jinja2 выполняется один раз при старте приложения:
``` python
from jinja2 import Environment, FileSystemLoader, select_autoescape
main_folder_path = os.path.dirname(os.path.abspath(__file__))
templates_folder_path = os.path.join(main_folder_path, 'templates')
env = Environment(
    loader=FileSystemLoader(templates_folder_path),
    autoescape=select_autoescape()
)
```
Преимущества такого подхода:
- Кэширование шаблонов в памяти
- Единая точка конфигурации
- Автоматическое экранирование HTML для безопасности
- Производительность за счет однократной загрузки
Использование в обработчике:
``` python
def _render_template(self, template_name: str, **context):
    template = env.get_template(template_name)
    return template.render(**context)
```
Функция для получения курсов валют из API Центрального Банка России:
```python
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    if not currency_codes:
        raise ValueError("Список кодов валют не может быть пустым")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}")
```
- Особенности реализации:
- Таймаут 10 секунд для сетевых запросов
- Проверка HTTP-статусов
- Обработка всех возможных исключений
- Возврат тестовых данных при ошибках сети
Инициализация валют при старте сервера:
``` python
def init_currencies():
    global currencies
    try:
        currencies_data = get_currencies_full_info(popular_currencies)
        currencies.clear()
        for char_code, data in currencies_data.items():
            currency = Currency(
                id=data.get('id', ''),
                char_code=char_code,
                name=data.get('name', ''),
                value=data.get('value', 0.0),
                nominal=data.get('nominal', 1)
            )
            currencies.append(currency)
    except Exception as e:
        currencies.extend(get_test_currencies())
```
# **5. Тесты**
## **Главная страница (/)**
<img width="650" height="220" alt="main" src="https://github.com/user-attachments/assets/2f76a454-3b88-4d15-9979-3e93cd8ee46c" />

Отображает статистику приложения: количество пользователей и валют, имя и группу автора
## **Список пользователей (/users)**
<img width="650" height="187" alt="users" src="https://github.com/user-attachments/assets/7c10b1be-bc3f-433b-91e2-3e9d56d59bf9" />

Таблица со списком всех пользователей, количеством их подписок и ссылками на детальную информацию
## **Страница пользователя (/user?id=1)**
<img width="650" height="430" alt="user" src="https://github.com/user-attachments/assets/6dbedf00-9626-4d1a-a21b-342f0befb18f" />

Детальная информация о пользователе и список валют, на которые он подписан
## Курсы валют (/currencies)**
<img width="650" height="322" alt="currencies" src="https://github.com/user-attachments/assets/6a7d671c-ecc6-4048-9a32-dff0b769263a" />

Таблица с 9 валютами: USD, EUR, GBP, JPY, CNY, CHF, CAD, AUD, SGD
## Об авторе (/author)
<img width="650" height="562" alt="author" src="https://github.com/user-attachments/assets/09a1661f-11cf-4808-b9fb-a21825a0c526" />

Информация об авторе приложения и о самом приложении
# 6. Тесты
## test_currencies_api.py
``` python
class TestGetCurrencies(unittest.TestCase):
    @patch('utils.currencies_api.requests.get')
    def test_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'])
    def test_empty_currency_codes(self):
        with self.assertRaises(ValueError):
            get_currencies([])
```
## test_models.py
```python
class TestAuthor(unittest.TestCase):
    def test_name_setter_invalid_type(self):
        author = Author(name="Иван", group="P3120")
        with self.assertRaises(TypeError):
            author.name = 123
    def test_name_setter_empty(self):
        author = Author(name="Иван", group="P3120")
        with self.assertRaises(ValueError):
            author.name = ""
```
## test_myapp.py
```python
class TestCurrencyRequestHandler(unittest.TestCase):
    @patch('myapp.env')
    def test_render_template_success(self, mock_env):
        handler = self.create_handler()
        mock_template = MagicMock()
        mock_template.render.return_value = 'Hello World'
        mock_env.get_template.return_value = mock_template
        result = handler._render_template('test.html', name='World')
        self.assertEqual(result, 'Hello World')
```
## test_templates.py
```python
class TestServerRoutes(unittest.TestCase):
    @patch('myapp.CurrencyRequestHandler._handle_home')
    def test_do_get_home(self, mock_handle_home):
        handler = self.create_handler_with_path('/')
        handler.do_GET()
        mock_handle_home.assert_called_once()
```
# 7. Вывод
В ходе выполнения лабораторной работы было успешно создано клиент-серверное веб-приложение для отслеживания курсов валют на чистом Python без использования фреймворков. Реализована архитектура MVC с чётким разделением моделей, представлений и контроллера, освоена работа с HTTPServer для обработки HTTP-запросов и Jinja2 для шаблонизации. Интегрирован API Центрального банка России для получения актуальных данных о валютах, реализована система подписок пользователей и написаны комплексные тесты для всех компонентов приложения. Работа продемонстрировала практическое применение принципов разработки веб-приложений, обработки внешних API и обеспечения отказоустойчивости системы.
