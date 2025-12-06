import unittest
import sys
import os
from unittest.mock import patch, Mock
import requests

# Добавляем путь к проекту для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.currencies_api import get_currencies, get_currencies_full_info, get_test_currencies


class TestGetCurrencies(unittest.TestCase):
    @patch('utils.currencies_api.requests.get')
    def test_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'])
    
    def test_empty_currency_codes(self):
        with self.assertRaises(ValueError):
            get_currencies([])
            
    @patch('utils.currencies_api.requests.get')
    def test_successful_response(self, mock_get):
        """Проверка успешного получения курсов"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 75.5},
                "EUR": {"Value": 85.3}
            }
        }
        mock_get.return_value = mock_response
        
        result = get_currencies(['USD', 'EUR'])
        
        self.assertEqual(result['USD'], 75.5)
        self.assertEqual(result['EUR'], 85.3)
        mock_get.assert_called_once()
    
    @patch('utils.currencies_api.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Проверка обработки некорректного JSON"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            get_currencies(['USD'])
    
    @patch('utils.currencies_api.requests.get')
    def test_missing_valute_key(self, mock_get):
        """Проверка отсутствия ключа Valute в ответе"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError):
            get_currencies(['USD'])
    
    @patch('utils.currencies_api.requests.get')
    def test_missing_currency_in_data(self, mock_get):
        """Проверка отсутствия запрошенной валюты в данных"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "EUR": {"Value": 85.3}
            }
        }
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError):
            get_currencies(['USD'])
    
    @patch('utils.currencies_api.requests.get')
    def test_invalid_currency_value_type(self, mock_get):
        """Проверка некорректного типа значения курса"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": "не число"}
            }
        }
        mock_get.return_value = mock_response
        
        with self.assertRaises(TypeError):
            get_currencies(['USD'])
    
    @patch('utils.currencies_api.requests.get')
    def test_network_error(self, mock_get):
        """Проверка обработки сетевой ошибки"""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'])


class TestGetCurrenciesFullInfo(unittest.TestCase):
    """Тесты для функции get_currencies_full_info"""
    
    @patch('utils.currencies_api.get_currencies')
    @patch('utils.currencies_api.requests.get')
    def test_successful_full_info(self, mock_get, mock_get_currencies):
        """Проверка успешного получения полной информации"""
        # Мокаем ответы
        mock_get_currencies.return_value = {
            'USD': 75.5,
            'EUR': 85.3
        }
        
        mock_response = Mock()
        mock_response.content = '''<?xml version="1.0" encoding="windows-1251"?>
<ValCurs>
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>75,5000</Value>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>85,3000</Value>
    </Valute>
</ValCurs>'''
        mock_response.raise_for_status = Mock()  # Важно: добавляем метод
        mock_get.return_value = mock_response
        
        result = get_currencies_full_info(['USD', 'EUR'])
        
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['USD']['name'], 'Доллар США')
        self.assertEqual(result['USD']['value'], 75.5)
        self.assertEqual(result['USD']['nominal'], 1)
    
    @patch('utils.currencies_api.get_currencies')
    @patch('utils.currencies_api.requests.get')
    def test_without_currency_codes(self, mock_get, mock_get_currencies):
        """Проверка вызова без указания кодов валют"""
        mock_get_currencies.return_value = {
            'USD': 75.5,
            'EUR': 85.3
        }
        
        mock_response = Mock()
        mock_response.content = b'<ValCurs></ValCurs>'
        mock_response.raise_for_status = Mock()  # Добавляем этот метод
        mock_get.return_value = mock_response
        
        # Должна быть попытка получить популярные валюты
        result = get_currencies_full_info()
        self.assertIsNotNone(result)
    
    def test_get_test_currencies(self):
        """Проверка функции тестовых данных"""
        result = get_test_currencies(['USD', 'EUR'])
        
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['USD']['name'], 'Доллар США')
        self.assertEqual(result['EUR']['name'], 'Евро')


if __name__ == '__main__':
    unittest.main()