from .author import Author # импортируем класс Author из файла author.py
from .app import App # импортируем класс App из файла app.py
from .user import User # импортируем класс User из файла user.py
from .currency import Currency # импортируем класс Currency из файла currency.py
from .user_currency import UserCurrency # импортируем класс UserCurrency из файла user_currency.py

__all__ = ['Author', 'App', 'User', 'Currency', 'UserCurrency'] # определяем список __all__, который указывает, какие имена будут экспортированы при использовании "from models import *"