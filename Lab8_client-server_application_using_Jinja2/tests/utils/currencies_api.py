import requests # импортируем библиотеку requests для выполнения HTTP-запросов
import json # импортируем модуль json для работы с JSON-форматом
import xml.etree.ElementTree as ET # импортируем модуль xml.etree.ElementTree для работы с XML-документами под псевдонимом ET
from typing import Dict, List, Optional # импортируем типы данных для аннотаций

def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Dict[str, float]:
    '''
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
    '''
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


def get_currencies_full_info(currency_codes: Optional[List[str]] = None) -> Dict[str, Dict]:
    '''
    Получает полную информацию о валютах
    
    Параметры:
        currency_codes -- список символьных кодов валют или None для всех валют
        
    Возвращает:
        Dict[str, Dict] -- словарь с данными о валютах
    '''
    try: # начинаем блок try для обработки всех исключений
        if currency_codes: # проверяем, были ли переданы конкретные коды валют
            currency_values = get_currencies(currency_codes) # получаем значения курсов для указанных валют
        else: # в противном случае
            currency_codes = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'CAD', 'SGD'] # получаем все, указанные тут
            try: # начинаем блок try для обработки всех исключений
                currency_values = get_currencies(currency_codes) # пробуем получить все указанные валюты
            except KeyError: # обрабатываем случай, когда некоторые валюты отсутствуют в API
                currency_values = get_currencies(['USD', 'EUR']) # получаем только доступные
        
        xml_url = "https://www.cbr.ru/scripts/XML_daily.asp" # URL XML API Центрального банка России
        response = requests.get(xml_url, timeout=10) # выполняем GET-запрос к XML API
        response.raise_for_status() # проверяем статус ответа
        
        root = ET.fromstring(response.content) # парсим XML-ответ в дерево элементов
        currencies_full_info = {} # создаем пустой словарь для хранения полной информации о валютах
        
        for valute in root.findall('Valute'): # перебираем все элементы Valute в XML-документе
            char_code = valute.find('CharCode').text # извлекаем символьный код валюты
            name = valute.find('Name').text # извлекаем название валюты
            nominal = int(valute.find('Nominal').text) # извлекаем номинал и преобразуем в целое число
            valute_id = valute.get('ID') # извлекаем ID валюты из атрибутов элемента
            
            if currency_codes and char_code not in currency_codes: # проверяем, нужно ли фильтровать по кодам валют
                continue # пропускаем валюту, если она не в списке запрошенных

            value = currency_values.get(char_code) # пытаемся получить значение курса из JSON API
            if value is None: # проверяем, отсутствует ли значение в JSON API
                xml_value = valute.find('Value').text # извлекаем значение курса из XML
                value = float(xml_value.replace(',', '.')) # заменяем запятую на точку и преобразуем в float
            
            currencies_full_info[char_code] = { # создаем запись в словаре с полной информацией
                'id': valute_id, # уникальный идентификатор валюты
                'char_code': char_code, # символьный код валюты
                'name': name, # название валюты
                'value': value, # значение курса
                'nominal': nominal # номинал валюты
            }
        
        return currencies_full_info # возвращаем словарь с полной информацией о валютах
        
    except Exception as e: # обрабатываем любые исключения
        return get_test_currencies(currency_codes) # возвращаем тестовые данные


def get_test_currencies(currency_codes: Optional[List[str]] = None) -> Dict[str, Dict]:
    '''
    Возвращает тестовые данные о валютах
    
    Параметры:
        currency_codes -- список символьных кодов валют или None для всех тестовых валют
        
    Возвращает:
        Dict[str, Dict] -- словарь с тестовыми данными о валютах
        '''
    # создаем словарь с тестовыми данными о валютах
    test_data = {
        'USD': {
            'id': 'R01235',
            'num_code': '840',
            'char_code': 'USD',
            'name': 'Доллар США',
            'value': 75.5,
            'nominal': 1
        },
        'EUR': {
            'id': 'R01239',
            'num_code': '978',
            'char_code': 'EUR',
            'name': 'Евро',
            'value': 85.3,
            'nominal': 1
        },
        'GBP': {
            'id': 'R01035',
            'num_code': '826',
            'char_code': 'GBP',
            'name': 'Фунт стерлингов',
            'value': 95.2,
            'nominal': 1
        },
        'JPY': {
            'id': 'R01820',
            'num_code': '392',
            'char_code': 'JPY',
            'name': 'Японская йена',
            'value': 0.65,
            'nominal': 100
        },
        'CNY': {
            'id': 'R01375',
            'num_code': '156',
            'char_code': 'CNY',
            'name': 'Китайский юань',
            'value': 11.8,
            'nominal': 10
        }
    }
    
    if currency_codes: # проверяем, были ли переданы конкретные коды валют
        return {code: test_data[code] for code in currency_codes if code in test_data} # используем генератор словаря для фильтрации данных
    
    return test_data # возвращаем все тестовые данные


if __name__ == "__main__":
    try: # блок try для обработки всех исключений
        currencies = get_currencies(['USD', 'EUR']) # вызываем функцию для получения заданных курсов
        print(f"Курсы валют: {currencies}") # выводим полученные курсы в консоль
        
        full_info = get_currencies_full_info(['USD', 'EUR']) # получаем полную информацию о долларе и евро
        print(f"\nПолная информация: {full_info}")
    except ConnectionError as e: # обрабатываем исключение ConnectionError
        print(f"Ошибка соединения: {e}") # выводим тип исключения
    except ValueError as e: # обрабатываем исключение ValueError
        print(f"Ошибка данных: {e}") # выводим тип исключения
    except KeyError as e: # обрабатываем исключение KeyError
        print(f"Ошибка ключа: {e}") # выводим тип исключения
    except Exception as e: # обрабатываем исключение Exception
        print(f"Неизвестная ошибка: {type(e).__name__}: {e}") # выводим тип исключения