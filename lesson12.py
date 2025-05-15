from abc import ABC,abstractmethod

class Animal(ABC):
    def __init__(self,name):
        self.name=name
    
    @abstractmethod
    def make_sound(self):
        pass
    
    @abstractmethod
    def move(self):
        pass

    def sleep(self):
        print(f"{self.name} is sleeping...")

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name}says woof woof")

    def move(self):
        print(f"{self.name} is really fast")

class Bird(Animal):
    def make_sound(self):
        print(f"{self.name}says ciu ciu")

    def move(self):
        print(f"{self.name} is decently fast")

def describe_animal(Animal):
    Animal.move()
    Animal.make_sound()
    Animal.sleep()

animals=[
    Dog("Buddy"),
    Bird("Blu")
]

for Kafshet in animals:
    print("Animal Information:")
    describe_animal(Kafshet)
