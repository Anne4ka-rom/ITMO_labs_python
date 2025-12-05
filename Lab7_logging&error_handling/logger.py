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