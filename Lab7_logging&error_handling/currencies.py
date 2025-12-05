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