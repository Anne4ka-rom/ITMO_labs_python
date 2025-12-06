from .author import Author # импортируем класс Author из модуля author
from .currency import Currency # импортируем класс Currency из модуля currency
from .user import User # импортируем класс User из модуля user
from .user_currency import UserCurrency # импортируем класс UserCurrency из модуля user_currency

__all__ = ['Author', 'Currency', 'User', 'UserCurrency'] # определяем список __all__ экспортируемых имён для использования с 'from models import *'