# # Operators in Python:

# # Arithmetic Operators
# print("# Arithmetic Operators")
# print(f"5 + 3 = {5 + 3}")
# print(f"5 - 3 = {5 - 3}")
# print(f"5 * 3 = {5 * 3}")
# print(f"5 / 2 = {5 / 2}") # Division always returns a float
# print(f"5 // 2 = {5 // 2}") # Floor division (returns the largest integer less than or equal to the division result) i.e. 5 / 3 = 1.666... but 5 // 3 = 1
# print(f"5 % 2 = {5 % 2}") # Modulus (returns the remainder of the division)
# print(f"2 ** 3 = {2 ** 3}\n") # Exponentiation (2 raised to the power of 3)

# # Assignment Operators
# x = 10
# print("# Assignment Operators")
# print(f"Initial x = {x}")
# x += 5
# print(f"x += 5 → {x}")
# x *= 2
# print(f"x *= 2 → {x}\n")

# # Comparison Operators
# print("# Comparison Operators")
# print(f"5 == 3 → {5 == 3}")
# print(f"5 != 3 → {5 != 3}")
# print(f"5 > 3 → {5 > 3}")
# print(f"5 < 3 → {5 < 3}")
# print(f"5 >= 3 → {5 >= 3}")
# print(f"5 <= 3 → {5 <= 3}\n")

# # Logical Operators
# a = True
# b = False
# """ 
#     The boolean values True and False are treated as 1 and 0 respectively
#     and → True if both operands are True, otherwise False (1 and 1 = 1, but 1 and 0 = 0)
#     or → True if at least one operand is True, otherwise False (1 or 1 = 1, 1 or 0 = 1, but 0 or 0 = 0)
#     not → True if operand is False, False if operand is True (not 1 = 0, not 0 = 1)
#     """
# print("# Logical Operators")
# print(f"True and False → {a and b}")
# print(f"True or False → {a or b}")
# print(f"not True → {not a}\n")

# # Bitwise Operators
# print("# Bitwise Operators (on ints)")
# print(f"5 & 3 → {5 & 3}") # AND
# print(f"5 | 3 → {5 | 3}") # OR
# print(f"5 ^ 3 → {5 ^ 3}") # XOR
# print(f"~5 → {~5}") # NOT
# print(f"2 << 1 → {2 << 1}") # LEFT SHIFT
# print(f"4 >> 1 → {4 >> 1}\n") # RIGHT SHIFT

# # Membership Operators
# seq = [1, 2, 3]
# print("# Membership Operators")
# print(f"2 in [1,2,3] → {2 in seq}")
# print(f"5 not in [1,2,3] → {5 not in seq}\n")

# # Identity Operators
# x = [1, 2, 3]
# y = x # y references the same list object as x (i.e. they both are pointing to the same object in memory)
# z = [1, 2, 3]
# print("# Identity Operators")
# print(f"x is y → {x is y} (same object)")
# print(f"x is z → {x is z} (different objects with same contents)")
# print(f"x == z → {x == z} (equal contents)\n")
# In python y = x does not create a new list, it just creates a new reference to the same list. 
# This is called "aliasing". So when you modify the list through either x or y, it will affect the same list object in memory. 
# So x and y are two variables that point to the same list object in memory. 
# Therefore, x is y evaluates to True because they are the same object. 
# On the other hand, z is a new list with the same contents as x, but it is a different object in memory. 
# Therefore, x is z evaluates to False, but x == z evaluates to True because they have the same contents.

# # Operator Precedence
# print("# Operator Precedence")
# expr1 = 2 + 3 * 4
# expr2 = (2 + 3) * 4
# print(f"2 + 3 * 4 = {expr1}  # multiplication before addition")
# print(f"(2 + 3) * 4 = {expr2}  # parentheses change order")
# (Parentheses) > Exponentiation > Unary operators(+x, -x, !x, ~x) > Multiplication/Division > Addition/Subtraction > Comparison > Logical operators