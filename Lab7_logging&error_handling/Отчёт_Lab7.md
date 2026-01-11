
# Федеральное государственное автономное образовательное учреждение высшего образования «Научно-образовательная корпорация ИТМО»  

## **ФАКУЛЬТЕТ ПРОГРАММНОЙ ИНЖЕНЕРИИ И КОМПЬЮТЕРНОЙ ТЕХНИКИ**

### **Лабораторная работа №7**

### По дисциплине «Программирование на Python»
**Работу выполнила:** Романова Анна Андреевна
**Группа:** P3120
**Преподаватель:** Жуков Николай Николаевич

# **1. Цель лабораторной работы**

- освоить принципы разработки декораторов с параметрами;
- научиться разделять ответственность функций (бизнес-логика) и декораторов (сквозная логика);
- научиться обрабатывать исключения, возникающие при работе с внешними API;
- освоить логирование в разные типы потоков (sys.stdout, io.StringIO, logging);
- научиться тестировать функцию и поведение логирования.
# **2. Текст задания**
## **1. Задание**
### **1.1. Реализовать декоратор logger, который:**
### Характеристики
Декоратор должен:
1. **быть параметризуемым**  
    Сигнатура:
def logger(func=None, *, handle=sys.stdout):
2. **вести логирование одним из трёх вариантов** (в зависимости от аргумента handle):
### Вариант 1 — обычный поток вывода (по умолчанию)
@logger
def f(...):
...
handle = sys.stdout
Логирование производится методом handle.write(...).
### Вариант 2 — любой объект, реализующий интерфейс файла, например:
stream = io.StringIO()
@logger(handle=stream)
def f():
...
В этом случае логирование идёт в StringIO.
### Вариант 3 — объект модуля logging
log = logging.getLogger("L1")
@logger(handle=log)
def f():
...
В этом случае декоратор должен логировать через:
- log.info(),
- log.error().
→ Декоратор сам определяет способ логирования:  
**если передан logging.Logger — логируем через logging, иначе — через .write().**
### Обязанности декоратора
1. При вызове функции — логировать:
    - уровень **INFO**: старт вызова + аргументы;
    - уровень **INFO**: успешное завершение + результат.
2. При возникновении исключения — логировать:
    - уровень **ERROR**: текст и тип исключения,
    - затем **повторно выбросить исключение**.
3. Не изменять сигнатуру вызываемой функции (использовать functools.wraps).
## **2. Реализовать функцию get_currencies**
Функция должна содержать **только бизнес-логику**:
### 2.1. Функция:
def get_currencies(currency_codes: list, url=..., ...) -> dict:
...
### 2.2. Что должна делать:
1. Делать запрос к API ЦБ РФ (или тестовому URL).
2. Извлекать словарь Valute.
3. Возвращать словарь вида:
{"USD": 93.25, "EUR": 101.7}
### 2.3. Когда должна выбрасывать исключения:

|**Ситуация**|**Исключение**|
|---|---|
|API недоступен|ConnectionError|
|Некорректный JSON|ValueError|
|Нет ключа “Valute”|KeyError|
|Валюта отсутствует в данных|KeyError|
|Курс валюты имеет неверный тип|TypeError|

**Функция не должна логировать — только выбрасывать исключения.**  
Всё логирование выполняется декоратором.
## **3. Обернуть функцию декоратором**
@logger(handle=sys.stdout) # или @logger(), или @logger(handle=logging_obj)
def get_currencies(...):
...
## **4. Самостоятельная часть**
Реализовать файл-логирование:
- создать логгер logging.getLogger("currency");
- настроить его на запись в файл;
- передать его как аргумент handle=:
file_logger = logging.getLogger("currency_file")
@logger(handle=file_logger)
def get_currencies(...):
...
## **5. Демонстрационный пример (см. колаб в теме курса)**
Создать функцию solve_quadratic(a, b, c) и обернуть её в логирующий декоратор.
Продемонстрировать:
- INFO для двух корней,
- WARNING для дискриминанта < 0,
- ERROR для некорректных данных (a = "abc"),
- CRITICAL можно использовать для полностью невозможной ситуации (например, оба коэффициента a=b=0).
## **6. Тестирование**
### **6.1. Тестирование функции get_currencies**
Использовать модуль unittest:
### Проверить:
- корректный возврат реальных курсов;
- поведение при несуществующей валюте;
- выброс соответствующих исключений:
    - ConnectionError,
    - ValueError,
    - KeyError.
С помощью:
with self.assertRaises(ConnectionError):
get_currencies(...)
### **6.2. Тестирование поведения декоратора (логгера)**
Использовать io.StringIO():
#### Пример подготовки:
self.stream = io.StringIO()
@logger(handle=self.stream)
def test_function(x):
return x * 2
#### Проверки:
##### **1. Логи при успешном выполнении**
- сообщение о старте (INFO)
- сообщение об окончании (INFO)
- аргументы и возвращаемое значение записаны.
##### **2. Логи при ошибках**
- вызвать декорированную функцию с ошибкой;
- проверить self.assertRegex(self.stream.getvalue(), "ERROR");
- проверить, что исключение проброшено.
### **6.3. Пример теста с контекстом (из задания)**
class TestStreamWrite(unittest.TestCase):
def setUp(self):
self.stream = io.StringIO()
@logger(handle=self.stream)
def wrapped():
return get_currencies(['USD'], url="https://invalid")
self.wrapped = wrapped
def test_logging_error(self):
with self.assertRaises(ConnectionError):
self.wrapped()
logs = self.stream.getvalue()
self.assertIn("ERROR", logs)
self.assertIn("ConnectionError", logs)
# **3. Исходный код программы**
## **Файл logger.py**
```python
import functools # импортируем functools для сохранения информации о функции при декорировании
import sys # импортируем sys для работы с системными потоками ввода-вывода
import logging # импортируем logging для логирования
from typing import Callable, Any # импортируем типы данных для аннотаций
def logger(function: Callable = None, *, handle=sys.stdout) -> Callable:
    '''
    Декоратор logger() добавляет логирование вызовов функций с гибкой настройкой вывода (логирует аргументы функции, результат выполнения и возникающие исключения)
    Параметры:
    function -- декорируемая функция
    handle -- обработчик вывода логов (по умолчанию sys.stdout)
    Возвращает:
    Callable -- декорированная функция с добавленным логированием
    '''
    def decorator(f: Callable) -> Callable:
        '''
        Функция decorator() создает обертку для логирования исходной функции
        Параметры:
        f -- исходная функция для декорирования
        Возвращает:
        Callable -- функция-обертка с логированием
        '''
        @functools.wraps(f) # используем wraps для сохранения информации об оригинальной функции
        def wrapper(*args, **kwargs) -> Any:
            '''
            Функция wrapper() заменяет оригинальную функцию, добавляя логирование
            Параметры:
            *args -- позиционные аргументы оригинальной функции
            **kwargs -- именованные аргументы оригинальной функции
            Возвращает:
            Any -- результат выполнения оригинальной функции
            '''
            if handle is sys.__stdout__: # проверяем, является ли переданный обработчик handle системным стандартным выводом по умолчанию -- sys.__stdout__
                actual_handle = sys.stdout # присваиваем переменной actual_handle текущий объект стандартного вывода sys.stdout
            else: # в противном случае
                actual_handle = handle # присваиваем переменной actual_handle объект обработчика логов handle
            # используем repr для любого объекта, чтобы получить его представление
            args_repr = [repr(a) for a in args] # преобразуем позиционные аргументы в строки типа repr()
            kwargs_repr = [f"{key}={repr(value)}" for key, value in kwargs.items()] # преобразуем именованные аргументы в строки вида key=repr(value)
            all_args = ", ".join(args_repr + kwargs_repr) # объединяем все аргументы в одну строку через запятую
            if isinstance(actual_handle, logging.Logger): # проверяем, является ли actual_handle объектом logging.Logger, и логируем вызов функции
                actual_handle.info(f"Вызов функции {f.__name__} с аргументами: {all_args}") # используем метод info() логгера для объектов logging.Logger
            else: # в противном случае
                actual_handle.write(f"INFO: Вызов функции {f.__name__} с аргументами: {all_args}\n") # используем метод write() логгера для файловых объектов
            try: # начинаем блок try для обработки всех исключений
                result = f(*args, **kwargs) # в result храним вызов оригинальной функции f(*args, **kwargs) с переданными аргументами
                if isinstance(actual_handle, logging.Logger): # проверяем, является ли actual_handle объектом logging.Logger, и логируем успешное завершение
                    actual_handle.info(f"Функция {f.__name__} успешно завершилась. Результат: {repr(result)}") # используем метод info() логгера для объектов logging.Logger
                else: # в противном случае
                    actual_handle.write(f"INFO: Функция {f.__name__} успешно завершилась. Результат: {repr(result)}\n") # используем метод write() логгера для файловых объектов
                return result # возвращаем результат
            except Exception as e: # если произошло исключение
                if isinstance(actual_handle, logging.Logger): # проверяем, является ли actual_handle объектом logging.Logger, и логируем вызов исключения функции
                    actual_handle.error(f"Функция {f.__name__} вызвала исключение {type(e).__name__}: {str(e)}") # используем метод error() логгера для объектов logging.Logger
                else: # в противном случае
                    actual_handle.write(f"ERROR: Функция {f.__name__} вызвала исключение {type(e).__name__}: {str(e)}\n") # используем метод write() логгера для файловых объектов
                raise # пробрасываем исключение дальше
        return wrapper # возвращаем функцию-обертку
    if function is None: # проверяем, как был вызван декоратор
        return decorator # для @logger или @logger(handle=...) возвращаем функцию-декоратор decorator
    return decorator(function) # для @logger над функцией применяем decorator к function и возвращаем результат
```
## **Файл currencies.py**
```python
import requests # импортируем библиотеку requests для выполнения HTTP-запросов
import json #импортируем библиотеку json для работы с JSON-форматом
from typing import Dict, List # импортируем типы данных для аннотаций
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    """
    Функция get_currencies() выполняет запрос к указанному API Центрального банка России, получает курсы запрошенных валют и возвращает их в виде словаря
    Параметры:
    currency_codes -- список кодов валют для получения
    url -- URL API ЦБ РФ
    Возвращает:
    Dict[str, float] -- словарь, где ключи -- коды валют, значения -- курсы этих валют
    Исключения:
    ConnectionError -- проблемы с сетевым соединением или HTTP-ошибка
    ValueError -- некорректный JSON в ответе
    KeyError -- отсутствие ключа 'Valute' или запрошенной валюты в данных
    TypeError -- неверный тип данных курса валюты
    """
    if not currency_codes: # проверяем, что список входных данных currency_codes не пустой
        raise ValueError("Список кодов валют не может быть пустым") # преобразуем техническую ошибку в пользовательское исключение ValueError
    try: # начинаем блок try для обработки всех исключений
        response = requests.get(url, timeout=10) # выполняем GET-запрос к API с timeout=10 секунд (защита от зависания)
        response.raise_for_status() # проверяем HTTP-статус ответа (вызываем исключение при статусах, у которых все коды выглядят как 4xx или 5xx)
    except requests.exceptions.RequestException as e: # обрабатываем все возможные исключения библиотеки requests при выполнении HTTP-запроса и сохраняем объект исключения в переменную e для дальнейшей обработки или логирования
        raise ConnectionError(f"API недоступен: {e}") # преобразуем техническую ошибку в пользовательское исключение ConnectionError
    try: # начинаем блок try для обработки всех исключений
        data = response.json() # преобразуем текст ответа HTTP-запроса из формата JSON в словарь или список
    except json.JSONDecodeError as e: # обрабатываем исключение, которое возникает при попытке преобразовать строку в формат JSON, когда строка содержит синтаксические ошибки или не является корректным JSON, и сохраняем объект исключения в переменную e для получения подробной информации об ошибке
        raise ValueError(f"Некорректный JSON: {e}") # преобразуем техническую ошибку в пользовательское исключение ValueError
    if "Valute" not in data: # проверяем, отсутствует ли ключ 'Valute' в полученных данных
        raise KeyError("Ключ 'Valute' отсутствует в ответе API") # вызываем исключение KeyError
    result = {} # создаем пустой словарь для хранения результатов
    for code in currency_codes: # перебираем все запрошенные коды валют
        if code not in data["Valute"]: # проверяем, отсутствует ли код запрошенной валюты в данных API
            raise KeyError(f"Валюта '{code}' отсутствует в данных") # вызываем исключение KeyError, если валюта отсутствует
        currency_data = data["Valute"][code] # получаем данные по конкретной валюте
        value = currency_data.get("Value") # извлекаем значение курса валюты по ключу 'Value'
        if not isinstance(value, (int, float)): # проверяем, являеется ли тип данных курса отличным от int или float
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}") # вызываем исключение TypeError
        result[code] = float(value) # преобразуем значение курса к типу float и добавляем в результат
    return result # возвращаем результат
if __name__ == "__main__":
    try: # блок try для обработки всех исключений
        currencies = get_currencies(['USD', 'EUR']) # вызываем функцию для получения заданных курсов
        print(f"Курсы валют: {currencies}") # выводим полученные курсы в консоль
    except ConnectionError as e: # обрабатываем исключение ConnectionError
        print(f"Ошибка соединения: {e}") # выводим тип исключения
    except ValueError as e: # обрабатываем исключение ValueError
        print(f"Ошибка данных: {e}") # выводим тип исключения
    except KeyError as e: # обрабатываем исключение KeyError
        print(f"Ошибка ключа: {e}") # выводим тип исключения
    except Exception as e: # обрабатываем исключение Exception
        print(f"Неизвестная ошибка: {type(e).__name__}: {e}") # выводим тип исключения
```
## **Файл quadratic.py**
```python
import logging # импортируем logging для записи информации о работе программы
import math # импортируем модуль math для вычисления квадратного корня
from typing import Optional, Tuple # импортируем типы данных для аннотаций
# настраиваем базовую конфигурацию логирования: имя файла для записи логов, минимальный уровень логирования, формат записи: "уровень: сообщение"
logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)
def solve_quadratic(a: float, b: float, c: float) -> Optional[Tuple[float, ...]]:
    '''
    Функция solve_quadratic() решает квадратное уравнение ax^2 + bx + c = 0 с полным логированием
    Параметры:
    a -- коэффициент при x^2
    b -- коэффициент при x
    c -- свободный член
    Возвращает:
    None -- если нет действительных корней (D < 0)
    Tuple[float] -- один корень если D = 0 или a = 0
    Tuple[float, float] -- два корня если D > 0
    Исключения:
    ValueError -- a=0 и b=0 (уравнение не имеет смысла)
    TypeError -- некорректный тип коэффициентов
    '''
    logging.info(f"Вызов функции с параметрами: a={a}, b={b}, c={c}") # логируем начало работы функции с переданными параметрами
    for name, value in zip(("a", "b", "c"), (a, b, c)): # проходим по всем трем коэффициентам для проверки их типов
        if not isinstance(value, (int, float)): # проверяем, если хотя бы один коэффициент не является числом типа int или типа float
            logging.error(f"Коэффициент '{name}'='{value}' имеет неверный тип {type(value).__name__}") # логируем ошибку с информацией о некорректном типе
            raise TypeError(f"Коэффициент '{name}' должен быть числом, получено: {type(value)}") # вызываем исключение TypeError
    if a == 0: # проверяем, равен ли коэффициент a нулю
        if b == 0: # проверяем, равен ли коэффициент b нулю
            logging.critical("Оба коэффициента a и b равны нулю") # логируем критическую ошибку
            raise ValueError("Оба коэффициента a и b равны нулю") # вызываем исключение ValueError
        logging.info(f"Линейное уравнение: {b}x + {c} = 0") # логируем информацию о решении линейного уравнения
        x = -c / b # вычисляем корень линейного уравнения
        logging.info(f"Найден корень линейного уравнения: x = {x}") # логируем найденный корень
        return (x,) # возвращаем кортеж с одним корнем
    logging.info(f"Квадратное уравнение: {a}x^2 + {b}x + {c} = 0") # логируем информацию об уравнении
    d = b*b - 4*a*c # вычисляем дискриминант
    logging.debug(f"Дискриминант D = {b}^2 - 4*{a}*{c} = {d}") # логируем отладочную информацию с деталями вычислений (уровень DEBUG)
    if d < 0: # проверяем, является ли дискриминант отрицательным
        logging.warning(f"Дискриминант отрицательный (D={d}). Действительных корней нет") # логируем предупреждение (уровень WARNING)
        return None # возвращаем None (отсутствия корней)
    if d == 0: # проверяем, равен ли дискриминант нулю
        x = -b / (2*a) # вычисляем корень
        logging.info(f"Дискриминант равен нулю. Один корень: x = {x}") # логируем информацию о найденном корне
        return (x,) # возвращаем кортеж с одним корнем
    sqrt_d = math.sqrt(d) # вычисляем квадратный корень из дискриминанта
    x1 = (-b + sqrt_d) / (2*a) # вычисляем первый корень
    x2 = (-b - sqrt_d) / (2*a) # вычисляем второй корень
    logging.info(f"Найдено два корня: x1 = {x1:.2f}, x2 = {x2:.2f}") # логируем информацию о двух корнях с округлением до 2ух знаков после запятой
    return (x1, x2) # возвращаем кортеж с двумя корнями
if __name__ == "__main__":
    result = solve_quadratic(1, 6.2, 8) # вызываем функцию для нахождения корней квадратного уравнения
    print(f"Корни: {result}") # выводим полученные корни уравнения
```
# **4. Фрагменты логов**
## **Logger_stdout**
```
INFO: Вызов функции multiply_x_on_number с аргументами: 5
INFO: Функция multiply_x_on_number успешно завершилась. Результат: 15
```
## **Logger_StringIO**
```
INFO: Вызов функции add_numbers с аргументами: 8, 4
INFO: Функция add_numbers успешно завершилась. Результат: 12
```
## **Logger_logging**
```
INFO: Вызов функции multiply_numbers с аргументами: 9, 8
INFO: Функция multiply_numbers успешно завершилась. Результат: 72
```
## **Logger_exception**
```
INFO: Вызов функции error_function с аргументами:
ERROR: Функция error_function вызвала исключение ValueError: Ошибка
```
## **Quadratic_two_roots**
```
INFO: Вызов функции с параметрами: a=1, b=6.2, c=8
INFO: Квадратное уравнение: 1x^2 + 6.2x + 8 = 0
DEBUG: Дискриминант D = 6.2^2 - 4*1*8 = 6.440000000000001
INFO: Найдено два корня: x1 = -1.83, x2 = -4.37
```
## **Quadratic_no_real_roots**
```
INFO: Вызов функции с параметрами: a=1, b=1, c=1
INFO: Квадратное уравнение: 1x^2 + 1x + 1 = 0
DEBUG: Дискриминант D = 1^2 - 4*1*1 = -3
WARNING: Дискриминант отрицательный (D=-3). Действительных корней нет
```
## **Quadratic_one_root**
```
INFO: Вызов функции с параметрами: a=1, b=2, c=1
INFO: Квадратное уравнение: 1x^2 + 2x + 1 = 0
DEBUG: Дискриминант D = 2^2 - 4*1*1 = 0
INFO: Дискриминант равен нулю. Один корень: x = -1.0
```
## **Quadratic_linear_equation**
```
INFO: Вызов функции с параметрами: a=0, b=2, c=-4
INFO: Линейное уравнение: 2x + -4 = 0
INFO: Найден корень линейного уравнения: x = 2.0
```
## **Quadratic_invalid_type**
```
INFO: Вызов функции с параметрами: a=один, b=2, c=3
ERROR: Коэффициент 'a'='один' имеет неверный тип str
```
## **Quadratic_critical_error**
```
INFO: Вызов функции с параметрами: a=0, b=0, c=5
CRITICAL: Оба коэффициента a и b равны нулю
```
# **5. Тесты**
## **Файл test_logger.py**
```python
import unittest # импортируем unittest для создания и запуска тестов
import io # импортируем io для работы со строковыми потоками ввода-вывода
import sys # импортируем sys для работы с системными потоками ввода-вывода
import logging # импортируем logging для логирования
from logger import logger # импортируем тестируемый декоратор
class TestLogger(unittest.TestCase):
    '''
    Класс тестов декоратора logger
    '''
    def test_logger_with_stdout(self):
        """
        Тестирование декоратора @logger() с использованием sys.stdout
        Проверяет, что декоратор без параметров пишет логи в стандартный вывод
        """
        stdout = sys.stdout # сохраняем оригинальный поток стандартного вывода, чтобы потом можно было восстановить его после временного перенаправления вывода в другой поток
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        sys.stdout = stream # перенаправляем sys.stdout в наш stream
        try: # начинаем блок try для обработки всех исключений
            @logger # применяем декоратор к тестовой функции
            def multiply_x_on_number(x): # создаем тестовую функцию multiply_x_on_number
                return x * 3 # возвращаем результат тестовой функции
            result = multiply_x_on_number(5) # вызываем декорированную функцию
            logs = stream.getvalue()
            self.assertEqual(result, 15) # проверяем, что функция возвращает правильный результат
            self.assertIn("INFO: Вызов функции multiply_x_on_number", logs)
            self.assertIn("с аргументами: 5", logs)
            self.assertIn("INFO: Функция multiply_x_on_number успешно завершилась", logs)
            self.assertIn("Результат: 15", logs)
        finally: # выполняем следующий блок кода даже если появилось исключение
            sys.stdout = stdout  # восстанавливаем stdout даже при провале теста
    def test_logger_with_stringio(self):
        """
        Тестирование декоратора @logger() с явным указанием потока вывода StringIO
        Проверяет, что декоратор с параметром handle=stream пишет логи в указанный поток StringIO
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        @logger(handle=stream) # применяем декоратор к тестовой функции
        def add_numbers(a, b): # создаем тестовую функцию add_numbers
            return a + b # возвращаем результат тестовой функции
        result = add_numbers(8, 4) # вызываем декорированную функцию
        logs = stream.getvalue() # извлекаем все, что было записано в stream
        self.assertEqual(result, 12) # проверяем, что функция возвращает правильный результат
        self.assertIn("INFO: Вызов функции add_numbers", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 8, 4", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция add_numbers успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn("Результат: 12", logs) # проверяем, что в логах зафиксирован результат выполнения
    def test_logger_with_logging(self):
        """
        Тестирование декоратора @logger() с использованием модуля logging
        Проверяет, что декоратор может работать с объектами logging.Logger и правильно форматирует сообщения
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        test_logger = logging.getLogger("test_logger") # создаем объект логгера в модуле logging и настраиваем его
        test_logger.setLevel(logging.INFO) # устанавливаем уровень логирования INFO
        test_logger.handlers.clear() # очищаем все предыдущие обработчики (чтобы не дублировался вывод)
        handler = logging.StreamHandler(stream) # создаем обработчик, который направляет логи в stream
        formatter = logging.Formatter("%(levelname)s: %(message)s") # настраиваем формат вывода (уровень: сообщение)
        handler.setFormatter(formatter) # устанавливаем formatter для обработчика, который определяет как будут выглядеть логируемые сообщения
        test_logger.addHandler(handler) # добавляем обработчик к логгеру
        @logger(handle=test_logger) # применяем декоратор к тестовой функции
        def multiply_numbers(a, b): # создаем тестовую функцию multiply_numbers
            return a * b # возвращаем результат тестовой функции
        result = multiply_numbers(9, 8) # вызываем декорированную функцию
        logs = stream.getvalue() # извлекаем все, что было записано в stream
        self.assertEqual(result, 72) # проверяем, что функция возвращает правильный результат
        self.assertIn("INFO: Вызов функции multiply_numbers", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 9, 8", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция multiply_numbers успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn("Результат: 72", logs) # проверяем, что в логах зафиксирован результат выполнения
    def test_logger_exception_handling(self):
        """
        Тестирование логирования исключений
        Проверяет, что декоратор корректно логирует ошибки и пробрасывает исключения
        """
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        @logger(handle=stream) # применяем декоратор к тестовой функции
        def error_function(): # создаем тестовую функцию error_function
            raise ValueError("Ошибка") # выбрасываем исключение
        with self.assertRaises(ValueError) as error_message: # проверяем, что функция вызывает ValueError, и сохраняем контекст исключения в error_message
            error_function() # вызываем функцию error_function, выбрасывающую исключение
        logs = stream.getvalue() # извлекаем все, что было записано в stream
        self.assertRegex(logs, r"ERROR") # проверяем, что в логах есть строка ERROR
        self.assertEqual(str(error_message.exception), "Ошибка") # проверяем, что сообщение исключения соответствует ожидаемому
    def test_logger_with_different_arguments(self):
        """Тестирование логирования разных типов аргументов"""
        stream = io.StringIO() # создаем StringIO объект, который позволяет работать со строкой как с файловым объектом
        @logger(handle=stream) # применяем декоратор к тестовой функции
        def return_different_arguments(a, b=10, *args, **kwargs): # создаем тестовую функцию test_logger_with_different_arguments
            return f"a={a}, b={b}, args={args}, kwargs={kwargs}" # возвращаем результат тестовой функции
        return_different_arguments(1, 'hello', 3, 4, x=5, y=[6, 7], z={'s': 5, 'n': 30})
        logs = stream.getvalue() # проверяем, что функция возвращает правильный результат
        # проверяем, что repr() корректно обрабатывает разные типы
        self.assertIn("'hello'", logs)  # это -- строка
        self.assertIn("[6, 7]", logs)  # это -- список
        self.assertIn("{'s': 5, 'n': 30}", logs)  # это -- словарь
        # проверяем корректность логов
        self.assertIn("INFO: Вызов функции return_different_arguments", logs) # проверяем, что в логах есть сообщение о вызове функции с префиксом INFO
        self.assertIn("с аргументами: 1, 'hello', 3, 4, x=5, y=[6, 7], z={'s': 5, 'n': 30}", logs) # проверяем, что в логах зафиксированы переданные аргументы
        self.assertIn("INFO: Функция return_different_arguments успешно завершилась.", logs) # проверяем, что в логах есть сообщение об успешном завершении функции с префиксом INFO
        self.assertIn('Результат: "a=1, b=hello, args=(3, 4), kwargs={\'x\': 5, \'y\': [6, 7], \'z\': {\'s\': 5, \'n\': 30}}"', logs) # проверяем, что в логах зафиксирован результат выполнения
if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()
```
## **Файл test_currencies.py**
```python
import unittest # импортируем unittest для создания и запуска тестов
from unittest.mock import patch, Mock # импортируем patch и Mock из unittest.mock для мокирования объектов
import requests # импортируем библиотеку requests для тестирования сетевых ошибок
from currencies import get_currencies # импортируем тестируемую функцию get_currencies из файла currencies
class TestFunctionGetCurrencies(unittest.TestCase):
    '''
    Класс тестов для функции get_currencies()
    '''
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_success(self, mock_get):
        '''
        Тестируем случай, когда функция успешно возвращает курсы валют
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # задаем возвращаемое значение для метода json()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25, "Nominal": 1},
                "EUR": {"Value": 101.70, "Nominal": 1}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        result = get_currencies(['USD', 'EUR']) # вызываем тестируемую функцию get_currencies с аргументами
        self.assertEqual(result, {'USD': 93.25, 'EUR': 101.70}) # проверяем, что функция возвращает правильный результат
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_missing_currency(self, mock_get):
        '''
        Тестируем случай, когда запрашиваемая валюта не существует
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # создаем данные только с USD, без EUR
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        with self.assertRaises(KeyError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение KeyError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD', 'XYZ']) # вызываем функцию, один из кодов валют которой не существует
        self.assertIn("Валюта 'XYZ' отсутствует в данных", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_invalid_json(self, mock_get):
        '''
        Тестируем случай, когда JSON некорректен
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        mock_response.json.side_effect = ValueError("Некорректный JSON") # настраиваем side_effect чтобы метод json() вызывал исключение
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        with self.assertRaises(ValueError) as context: # проверяем, что внутри блока кода будет вызвано исключение ValueError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        self.assertIn("Некорректный JSON", str(context.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_missing_valute_key(self, mock_get):
        '''
        Тестируем случай, отсутствует ключ 'Valute'
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        mock_response.json.return_value = {"SomeOtherKey": {}} # устанавливаем мок-объекта mock_response, который имитирует отсутствие обязательного ключа "Valute"
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        with self.assertRaises(KeyError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение KeyError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        self.assertIn("Ключ 'Valute' отсутствует", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_connection_error(self, mock_get):
        '''
        Тестируем случай, когда происходит ошибка соединения
        '''
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed") # настраиваем side_effect чтобы requests.get вызывал исключение
        with self.assertRaises(ConnectionError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение ConnectionError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        self.assertIn("API недоступен", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    @patch('currencies.requests.get') # декоратор patch заменяет реальный requests.get на mock объект во время теста
    def test_get_currencies_invalid_value_type(self, mock_get):
        '''
        Тестируем случай, когда значение курса имеет неверный тип
        '''
        mock_response = Mock() # создаем mock объект для имитации HTTP-ответа
        mock_response.status_code = 200 # устанавливаем код статуса 200 (успех)
        # задаем возвращаемое значение для метода json(), но вместо числа другой тип (строка)
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": "not_a_number"}
            }
        }
        mock_get.return_value = mock_response # настраиваем mock_get, чтобы он возвращал mock_response
        with self.assertRaises(TypeError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение TypeError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            get_currencies(['USD']) # вызываем функцию с корректным кодом валюты
        self.assertIn("неверный тип", str(error_message.exception).lower()) # проверяем, что сообщение об ошибке содержит нужный текст
if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()
```
## **Файл test_quadratic.py**
```python
import unittest # импортируем unittest для создания и запуска тестов
from quadratic import solve_quadratic # импортируем тестируемую функцию solve_quadratic из файла quadratic
class TestSolveQuadratic(unittest.TestCase):
    '''Класс тестов для функции solve_quadratic()'''
    def test_two_roots(self):
        '''
        Тестируем случай, когда уравнения имеет два корня
        '''
        roots = solve_quadratic(1, -3, 2) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        self.assertIsNotNone(roots)# проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 2) # проверяем, что возвращаемых корней два
        self.assertAlmostEqual(roots[0], 2.0) # проверяем, что первый корень должен быть 2.0 + небольшая погрешность
        self.assertAlmostEqual(roots[1], 1.0) # проверяем, что второй корень должен быть 1.0 + небольшая погрешность
    def test_one_root(self):
        '''
        Тестируем случай, когда уравнения имеет один корень
        '''
        roots = solve_quadratic(1, 2, 1) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        self.assertIsNotNone(roots) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots[0], -1.0) # проверяем, что корень должен быть -1.0 + небольшая погрешность
    def test_no_real_roots(self):
        '''
        Тестируем случай, когда уравнения не имеет действительных корней
        '''
        roots = solve_quadratic(1, 1, 1) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        self.assertIsNone(roots) # проверяем, что функция вернула None
    def test_linear_equation(self):
        '''
        Тестируем случай, когда уравнения линейно
        '''
        roots = solve_quadratic(0, 2, -4) # вызываем функцию solve_quadratic с коэффициентами для уравнения
        self.assertIsNotNone(roots) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots[0], 2.0) # проверяем, что корень должен быть 2.0 + небольшая погрешность
    def test_invalid_type(self):
        '''
        Тестируем случай, когда в уравнении содержится неккоректный тип данных
        '''
        with self.assertRaises(TypeError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение TypeError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            solve_quadratic("abc", 2, 3) # вызываем функцию с некорректным (строковым) типом данных
        self.assertIn("Коэффициент 'a' должен быть числом", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    def test_a_and_b_zero(self):
        '''
        Тестируем случай, когда в уравнении a=0 и b=0
        '''
        with self.assertRaises(ValueError) as error_message: # проверяем, что внутри блока кода будет вызвано исключение ValueError, и сохраняем его в переменную error_message для последующей проверки деталей исключения
            solve_quadratic(0, 0, 1) # вызываем функцию, где a=0 и b=0
        self.assertIn("Оба коэффициента a и b равны нулю", str(error_message.exception)) # проверяем, что сообщение об ошибке содержит нужный текст
    def test_extreme_numbers(self):
        '''
        Тестируем случай, когда коэффициенты очень большие/малые
        '''
        roots_small = solve_quadratic(1e-10, 2e-10, 1e-10) # вызываем функцию solve_quadratic с очень малыми коэффициентами для уравнения
        self.assertIsNotNone(roots_small) # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots_small), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots_small[0], -1.0, places=6) # проверяем, что корень должен быть -1.0 + небольшая погрешность
        roots_large = solve_quadratic(1e10, 2e10, 1e10) # вызываем функцию solve_quadratic с очень большими коэффициентами для уравнения
        self.assertIsNotNone(roots_large)  # проверяем, что функция вернула не None (должен быть хотя бы один корень)
        self.assertEqual(len(roots_large), 1) # проверяем, что возвращаемый корень один
        self.assertAlmostEqual(roots_large[0], -1.0, places=6) # проверяем, что корень должен быть -1.0 + небольшая погрешность
if __name__ == '__main__': # запуск всех тестов в классе
    unittest.main()
```
# **6. Вывод**
В ходе лабораторной работы №7 я научилась создавать гибкие параметризуемые декораторы, разделять бизнес-логику и сквозную функциональность, корректно обрабатывать исключения при работе с внешними API и вести логирование в разные типы потоков. Эти навыки позволят мне в будущем разрабатывать более надежные, поддерживаемые и профессиональные приложения, где важно контролировать выполнение кода, обрабатывать ошибки и вести детальное логирование для отладки и мониторинга.
