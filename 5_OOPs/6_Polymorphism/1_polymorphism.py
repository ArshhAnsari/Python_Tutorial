'''
Polymorphism : Polymorphism in Python refers to the ability of different objects to respond to the same method or function call in ways specific to their individual types. 
               Polymorphism is a core concept in object-oriented programming (OOP) that allows programmers to use a single interface with different underlying forms.

Types of polymorphism in Python
Python supports several types of polymorphism. Understanding each type will help you leverage polymorphism effectively in your code.

'''

# Method Overriding
'''
Method overriding occurs when a subclass provides a specific implementation of a method that is already defined in its parent class. 
This is one of the most common forms of polymorphism in Python.
'''
class Animal:
    def speak(self):
        raise NotImplementedError("Subclass must implement this method")

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Duck(Animal):
    def speak(self):
        return "Quack!"

# --- Usage ---
# Create a list of different animal objects
animals = [Dog(), Cat(), Duck()]

# We can iterate through them and call the same method 'speak()'
# Python doesn't care what type of animal it is, just that it has a 'speak' method.
print("Polymorphism in action:")
print("1. Method Overriding")
for animal in animals:
    print(f"The animal says: {animal.speak()}")


''' ---------------------------------------- '''

# Duck Typing
'''
Duck typing is a concept related to dynamic typing where the type or class of an object is less important than the methods it defines. 
The name comes from the saying: “If it walks like a duck and quacks like a duck, then it probably is a duck.”
'''
def make_animal_speak(some_object):
    print("Animal speak:",some_object.speak())

print("\n2. Duck Typing")
make_animal_speak(Dog()) # Output: Woof!
make_animal_speak(Cat()) # Output: Meow!
make_animal_speak(Duck()) # Output: Quack!

# In this example, the make_animal_speak() function works with any object that has a speak() method, regardless of its type. This is a typical example of duck typing.

'''---------------------------------------- '''

# Operator Overloading
print("\n3. Operator Overloading: Look at Our Own Fraction Class in 5_OOPs/3_Dubder_and_Getter/4_OurOwn_FractionClass.py")
'''
Operator overloading is a feature in Python that allows the same operator to have different meanings according to the context. 
For instance, the + operator performs arithmetic addition on numbers but concatenation on strings.

Example : 
 "5_OOPs\3_Dubder_and_Getter\4_OurOwn_FractionClass.py"

 In the example, we define a Fraction class that overloads the + operator to add two fractions together.
 '''

''' ---------------------------------------- '''
# Method Overloading
'''
Unlike some other OOP languages, Python doesn’t support traditional function or method overloading, where multiple methods with the same name but different parameters are defined. 
However, Python achieves similar functionality through default parameters and variable-length arguments.
'''
def calculate_area(length, width=None):
  if width is None:
    return length * length
  return length * width

print("\n4. Method Overloading")
# Using the function with different arguments
print("Area of square:", calculate_area(5))      # Output: 25 (square)
print("Area of rectangle:", calculate_area(4, 6))   # Output: 24 (rectangle)
