# OOP - Object oriented programing
# VS Procedural oriented programing

'''
1. Class - Blueprint / Template
2. Instance - Actual object from Class
3. Attributes - data / properties of a class
4. Methods - Bahavior (What it can do as a function)
'''

######
class Dog: # use PascalCase for class name
    # Class attribute
    species = "Mammal"
    count = 0
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        Dog.count += 1
        
    # instance method
    def bark(self):
        print(f"{self.name} says woof!")
        
    def eat(self, food):
        print(f"{self.name} is eating {food}")
        
    @classmethod
    def from_birth_year(cls, name, birth_year):
        age = 2025 - birth_year
        return cls(name, age)
        
    #static method - class method
    @staticmethod
    def is_valid_age(age):
        return 0 < age < 30

        

dog_1 = Dog("Buddy", 2)
dog_2 = Dog("Max", 5)
print(dog_1.name, dog_2.age)
print(dog_1 is dog_2)

# Not Recommend
dog_1.color = 'black'
print(dog_1.color)
print(dog_1.species)

print(Dog.species)

dog_1.bark()

dog_1.eat('Bone')

print(Dog.is_valid_age(25))

dog_3 = Dog.from_birth_year('Blackie', 2020)
print(dog_3.age)


    



