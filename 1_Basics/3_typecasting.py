'''
Note on typecasting errors:
- When converting a string to a numeric type (`int` or `float`), the string
  must exactly match the literal format of that type.
  * `int("123")` → works, because "123" is an integer literal.
  * `int("31.5")` → raises ValueError, because "31.5" is not a valid integer literal.
  * `float("3.14")` → works, because "3.14" is a valid float literal.
  * Always ensure the string represents the correct literal before casting.
'''

# 1. Numeric Conversions
print("# Numeric Conversions")
# int -> float
a = 10
b = float(a)
print(f"float(10) -> {b}, Type: {type(b)}")

# float -> int (truncates toward zero)
c = 3.99
d = int(c)
print(f"int(3.99) -> {d}, Type: {type(d)}")

# int -> str
e = 123
f = str(e)
print(f"str(123) -> '{f}', Type: {type(f)}")

# str -> int (must be integer literal)
g = "456"
h = int(g)
print(f"int('456') -> {h}, Type: {type(h)}")

# str -> float (must be float literal)
i = "7.89"
j = float(i)
print(f"float('7.89') -> {j}, Type: {type(j)}")

# str -> int via float (two-step)
k = "31.5"
m=int(float(k))
print(f"int(float('31.5')) -> {m}, Type: {type(m)}")

print("\n# Boolean Conversions")
# int -> bool
print(f"bool(0) -> {bool(0)}")
print(f"bool(42) -> {bool(42)}")

# str -> bool (empty vs non-empty)
print(f"bool('') -> {bool('')} ")
print(f"bool('hello') -> {bool('hello')}")