class Currency:
    def __init__(self, id: str, char_code: str, name: str, value: float, nominal: int, num_code: str = ""):
        self._id = None
        self._char_code = None
        self._name = None
        self._value = None
        self._nominal = None
        self._num_code = None
        
        self.id = id
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal
        self.num_code = num_code  # Добавляем инициализацию num_code
    
    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ID должен быть строкой")
        self._id = value
    
    @property
    def num_code(self) -> str:
        return self._num_code
    
    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Цифровой код должен быть строкой")
        self._num_code = value
    
    @property
    def char_code(self) -> str:
        return self._char_code
    
    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Символьный код должен быть строкой")
        self._char_code = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")
        self._name = value
    
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
    
    @property
    def nominal(self) -> int:
        return self._nominal
    
    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Номинал должен быть целым числом")
        if value <= 0:
            raise ValueError("Номинал должен быть положительным числом")
        self._nominal = value
    
    def get_value_per_unit(self) -> float:
        return self.value / self.nominal
    
    def __repr__(self):
        return f"Currency(id='{self.id}', char_code='{self.char_code}', name='{self.name}', value={self.value}, nominal={self.nominal})"