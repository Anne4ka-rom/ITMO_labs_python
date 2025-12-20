import requests # импортируем requests для выполнения HTTP-запросов к API Центрального банка России
import json # импортируем json для работы с JSON-данными и обработки JSON-ошибок
from typing import Dict, List # импортируем типы Dict и List из модуля typing для аннотаций типов


def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, Dict]:
    '''
    Функция get_currencies() выполняет запрос к указанному API Центрального банка России,
    получает полную информацию о запрошенных валютах и возвращает их в виде словаря
    
    Параметры:
    currency_codes -- список кодов валют для получения
    url -- URL API ЦБ РФ
    
    Возвращает:
    Dict[str, Dict] -- словарь, где ключи -- коды валют, значения -- словари с полной информацией о валюте
    
    Исключения:
    ConnectionError -- проблемы с сетевым соединением или HTTP-ошибка
    ValueError -- некорректный JSON в ответе или пустой список кодов
    KeyError -- отсутствие ключа 'Valute' или запрошенной валюты в данных
    TypeError -- неверный тип данных курса валюты
    '''
    if not currency_codes: # проверяем, не является ли список кодов валют пустым
        raise ValueError("Список кодов валют не может быть пустым") # вызываем исключение ValueError с сообщением о пустом списке
    
    try: # начинаем блок try для обработки сетевых ошибок и ошибок HTTP
        response = requests.get(url, timeout=10) # выполняем HTTP GET-запрос к указанному URL с таймаутом 10 секунд
        response.raise_for_status() # проверяем статус ответа, вызываем исключение для кодов ошибок -- 4xx, 5xx
    except requests.exceptions.RequestException as e: # перехватываем любые исключения, связанные с запросами
        raise ConnectionError(f"API недоступен: {e}") # преобразуем исключение requests в ConnectionError с информативным сообщением
    
    try: # начинаем блок try для обработки ошибок парсинга JSON
        data = response.json() # преобразуем содержимое ответа из JSON в словарь Python
    except json.JSONDecodeError as e: # перехватываем исключение при некорректном JSON
        raise ValueError(f"Некорректный JSON: {e}") # преобразуем исключение в ValueError с сообщением об ошибке
    
    if "Valute" not in data: # проверяем, отсутствует ли полученный словарь ключ 'Valute'
        raise KeyError("Ключ 'Valute' отсутствует в ответе API") # вызываем исключение KeyError, если ключ отсутствует
    
    result = {} # создаём пустой словарь для хранения результата
    for code in currency_codes: # проходим по каждому коду валюты из входного списка
        if code not in data["Valute"]: # проверяем, отсутствует ли текущий код валюты в данных API
            raise KeyError(f"Валюта '{code}' отсутствует в данных") # вызываем исключение KeyError
        
        currency_data = data["Valute"][code] # получаем данные о конкретной валюте по её коду
        value = currency_data.get("Value") # получаем значение курса валюты с использованием метода get для безопасного доступа
        
        if not isinstance(value, (int, float)): # проверяем, является ли значение курса чем-то, кроме числом типа int или float
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}") # вызываем исключение TypeError для неверного типа
        
        num_code = currency_data.get('NumCode', '') # извлекаем цифровой код валюты или пустую строку, если ключ отсутствует
        
        result[code] = { # добавляем информацию о валюте в словарь результата
            'id': currency_data.get('ID', ''), # получаем ID валюты или пустую строку по умолчанию
            'char_code': code, # сохраняем буквенный код валюты
            'num_code': str(num_code), # преобразуем цифровой код в строку
            'name': currency_data.get('Name', ''), # получаем название валюты или пустую строку по умолчанию
            'value': float(value), # преобразуем значение курса в тип float для единообразия
            'nominal': int(currency_data.get('Nominal', 1)) # получаем номинал валюты, преобразуем в int, по умолчанию 1
        }
    
    return result # возвращаем словарь с информацией о всех запрошенных валютах


if __name__ == "__main__":
    try: # начинаем блок try для обработки исключений при тестовом запуске
        currencies = get_currencies(['USD', 'EUR']) # вызываем функцию get_currencies для получения данных о USD и EUR
        print(f"Курсы валют: {currencies}") # выводим словарь с курсами валют
        
        print("\nПодробная информация:") # выводим заголовок для подробной информации
        for code, info in currencies.items(): # проходим по всем валютам в словаре
            print(f"{code}: {info['name']} - {info['value']} руб. (номинал: {info['nominal']})") # выводим подробную информацию о каждой валюте
            
    except ConnectionError as e: # перехватываем исключение ConnectionError
        print(f"Ошибка соединения: {e}") # выводим сообщение об ошибке соединения
    except ValueError as e: # перехватываем исключение ValueError
        print(f"Ошибка данных: {e}") # выводим сообщение об ошибке данных
    except KeyError as e: # перехватываем исключение KeyError
        print(f"Ошибка ключа: {e}") # выводим сообщение об ошибке ключа
    except Exception as e: # перехватываем любые другие исключения
        print(f"Неизвестная ошибка: {type(e).__name__}: {e}") # выводим тип и сообщение неизвестного исключения