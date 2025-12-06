class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_name: str):
        self._id = None
        self._user_id = None
        self._currency_name = None
        
        self.id = id
        self.user_id = user_id
        self.currency_name = currency_name
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID должен быть целым числом")
        if value <= 0:
            raise ValueError("ID должен быть положительным числом")
        self._id = value
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("ID пользователя должен быть целым числом")
        if value <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")
        self._user_id = value
    
    @property
    def currency_name(self) -> str:
        return self._currency_name
    
    @currency_name.setter
    def currency_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ID валюты должен быть строкой")
        self._currency_name = value
    
    def __repr__(self):
        return f"UserCurrency(id={self.id}, user_id={self.user_id}, currency_name='{self.currency_name}')"