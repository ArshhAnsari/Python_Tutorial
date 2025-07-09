'''
A simple demonstration of Python's built-in data types and naming rules.
'''

# Integer
my_int = 4  # whole numbers
# print("Value:",my_int," ,Type:",type(my_int))
# When you prefix a string with f, like f"...", it lets you embed expressions (like variables or even calculations) directly inside curly braces {} within the string.
print(f"Value: {my_int}, Type: {type(my_int)}")

# String (sequence of characters)
greeting = 'Hello, World!'
print(f"Value: {greeting}, Type: {type(greeting)}")

# Character (in Python, a one-character string)
letter = 'c'
print(f"Value: {letter}, Type: {type(letter)}")

# Float (decimal numbers)
my_float = 4.250
print(f"Value: {my_float}, Type: {type(my_float)}")

# Boolean (True or False)
is_active = False
print(f"Value: {is_active}, Type: {type(is_active)}")

# NoneType (represents absence of a value)
data = None
print(f"Value: {data}, Type: {type(data)}")

# -------------------------------------------
# Variable naming rules:
# Valid examples:
name = 'Alice'
_name = 'Bob'
name1 = 'Carol'
# Invalid examples (will cause SyntaxError if uncommented):
# 1name = 'Not allowed'
# @name = 'Not allowed'
# hy-phen = 5

# Note:
# 1) Variable names must start with a letter or underscore, followed by letters, digits, or underscores.
# 2) They are case-sensitive ('myVar' != 'myvar').
# 3) Avoid using Python reserved keywords (e.g., 'class', 'def', 'if').
