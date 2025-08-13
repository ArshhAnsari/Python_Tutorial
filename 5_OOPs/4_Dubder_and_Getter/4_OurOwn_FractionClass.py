"""
This script demonstrates the use of Object-Oriented Programming (OOP) concepts in Python by 
implementing a custom Fraction class. 
"""

# Making our own Fraction variable using a Fraction class
class Fraction:
    # constructor
    def __init__(self,x,y):
        self.numerator = x
        self.denominator = y
    # string representation
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    # addition
    def __add__(self,other):
        
            new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
            new_denominator = self.denominator * other.denominator
            return f"Fraction of {self} + {other} = {new_numerator}/{new_denominator}"
    # subtraction
    def __sub__(self,other):
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return f"Fraction of {self} - {other} = {new_numerator}/{new_denominator}"
    # division
    def __truediv__(self,other):
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return f"Fraction of {self} / {other} = {new_numerator}/{new_denominator}"

# Creating Fraction objects
fr1 = Fraction(1, 2)
fr2 = Fraction(1, 3)
# print(fr1.denominator)
print(fr1)
print(fr2)
print(fr1 + fr2)
print(fr1 - fr2)
print(fr1 / fr2)
