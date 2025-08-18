# Magic/dunder methods - special methods that have double underscores
# dunder methods are called automatically when you do something special with an object
class Age_Name:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __len__(self):
        return 'The length of {} is {}, and the length of age {} is {}'.format(self.name, len(self.name), self.age, len(str(self.age)))
    
    def __str__(self):
        # The __str__ method returns a string representation of the object 
        # commonly used for displaying the object in a human-readable format 
        return f"Name: {self.name}, Age: {self.age}"
    def __repr__(self):
        # The __repr__ method returns a string representation of the object
        return f"Age_Name('{self.name}', {self.age})"
    


str1=Age_Name("Arsh",20)
str2=Age_Name("Ankush",21)

print("It prints the debug representation of the object:",str1.__repr__()) # this will call the __repr__ method automatically
print("It prints the string representation of the object",str2) # this will call the __str__ method automatically

print(str1.__len__()) 
print(str2.__len__())