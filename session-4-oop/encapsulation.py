'''
# OOP 4 pillars:
 Encapsulation
 Inheritance
 Polymorphism
 Abstract
'''

# Encapsulation
class BankAccount:
    def __init__(self, account_number, balance):
        # Public attribute
        self.account_number = account_number
        
        # Protected attribute - internal use attribute( not for public)
        self._balance = balance
        
        # private attribute - can be used within this class only
        self.__pin = '1234'
    
    # public method
    def get_balance(self, currency):
        if currency == 'RMB':
            return self._balance * 7
        return self._balance
    
    # Private method
    def __validate_pin(self, pin):
        return self.__pin == pin
    
    def login(self, account_number, pin):
        self.__validate_pin(pin)
        

        
        
account_1 = BankAccount(123, 999)

print(account_1.account_number)
print(account_1._balance)
# print(account_1.__pin)
account_1.login(123, '123')

# setter & getter
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
        
    # Getter
    @property    
    def celsius(self):
        return self._celsius
    
    # Getter
    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32
    
    @celsius.setter
    def celsius(self, value):
        if value < -273:
            raise ValueError('Cannot be lower than absolute zero')
    
        self._celsius = value
        
    @fahrenheit.setter    
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9
    

temp_1 = Temperature(30)

print(temp_1.celsius)
print(temp_1.fahrenheit)

temp_1.celsius = 22
print(temp_1.celsius)
print(temp_1.fahrenheit)

temp_1.fahrenheit = 77
print(temp_1.celsius)
print(temp_1.fahrenheit)
