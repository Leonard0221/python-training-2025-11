# Magic methods
# Python calls some special methods of a class when you do some operation
# the method name starts with __
class Dog:

    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"{self.name} is {self.age} years old"
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age
    

    
        
dog_1 = Dog('max', 5)
dog_2 = Dog('max', 5)

print(dog_1 == dog_2)

class ShoppingCart:
    def __init__(self, items):
        self.items = items
        
    def __len__(self):
        return len(self.items)
    
    @property
    def length(self):
        return len(self.items)
    
cart1 = ShoppingCart(['computer', 'basketball', 'shampoo'])
print(len(cart1))
print(cart1.length)

