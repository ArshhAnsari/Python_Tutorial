# # Operators in Python:

# # Arithmetic Operators
# print("# Arithmetic Operators")
# print(f"5 + 3 = {5 + 3}")
# print(f"5 - 3 = {5 - 3}")
# print(f"5 * 3 = {5 * 3}")
# print(f"5 / 2 = {5 / 2}")
# print(f"5 // 2 = {5 // 2}")
# print(f"5 % 2 = {5 % 2}")
# print(f"2 ** 3 = {2 ** 3}\n")

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
# y = x
# z = [1, 2, 3]
# print("# Identity Operators")
# print(f"x is y → {x is y} (same object)")
# print(f"x is z → {x is z} (different objects with same contents)")
# print(f"x == z → {x == z} (equal contents)\n")

# # Operator Precedence
# print("# Operator Precedence")
# expr1 = 2 + 3 * 4
# expr2 = (2 + 3) * 4
# print(f"2 + 3 * 4 = {expr1}  # multiplication before addition")
# print(f"(2 + 3) * 4 = {expr2}  # parentheses change order")
