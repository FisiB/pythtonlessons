from abc import ABC,abstractmethod

class Person(ABC):
    def __init__(self,name,age,weight,height,):
        self.name=name
        self.age=age
        self.weight=weight
        self.height=height
       
    @abstractmethod
    def calculate_bmi(self,age,weight,height,bmi):
        self.bmi=bmi
        bmi=weight/(height)**2
        pass
    
    @abstractmethod
    def get_bmi_category(self,age,bmi):
        pass

    def print_info(self):
        print(f"{self.name} has these")

class Adult(Person):
    def calculate_bmi(self):
        return self.weight/self.height**2
    
    def get_bmi_category(self):
        bmi= self.calculate_bmi()
        if bmi < 18.5:
            print("You are Underweight for an Adult")
        elif  bmi>=18.5 and bmi<24.9 :
            print("You are Normal weight for an Adult")
        elif  bmi>=24.9 and bmi<29.9 :
            print("You are Overweight for an Adult")
        else:
            print("You are Obese for an Adult")

class Child(Person):
    def calculate_bmi(self):
        return self.weight/self.height**2*1.3
    
    def get_bmi_category(self):
        bmi= self.calculate_bmi()
        if bmi < 14:
            print("You are Underweight for a Child")
        elif  bmi>=14 and bmi<18 :
            print("You are Normal weight for a Child")
        elif  bmi>=18 and bmi<24 :
            print("You are Overweight for a Child")
        else:
            print("You are Obese for a Child")


           