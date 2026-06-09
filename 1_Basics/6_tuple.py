# 1. Nature of Tuples: Immutable, ordered sequence
# Once created, tuple elements cannot be changed, added, or removed.
# Tuples can be used as dictionary keys and in situations where immutability is desired.

# Create a tuple
fruits = ("Apple", "Banana", "Cherry")
print("Initial tuple:", fruits)
print("Type:", type(fruits))

# Accessing elements (indexing)
print("First item:", fruits[0])
print("Last item:", fruits[-1])

# Slicing
print("First two items:", fruits[:2])

# Unpacking
# Unpacking: the tuple on the right (fruits) is an ordered iterable.
# The assignment on the left (a, b, c) is a sequence of target variables.
# Python matches items by position: first item -> a, second -> b, third -> c.
# If the number of variables doesn't match the number of items, Python raises a ValueError.
a, b, c = fruits  # a gets fruits[0], b gets fruits[1], c gets fruits[2]
print(f"Unpacked values: a={a}, b={b}, c={c}")

# Example showing positional mapping explicitly:
# fruits = ("Apple", "Banana", "Cherry")
# a -> "Apple"  (fruits[0])
# b -> "Banana" (fruits[1])
# c -> "Cherry" (fruits[2])

# Extended unpacking: capture remaining items with *rest
# (works if there are more items than variables)
# a, *rest = fruits  # a="Apple", rest=["Banana","Cherry"]

# 2. Common tuple methods
# count(value): number of occurrences of value
tups = (1, 2, 3, 2, 2, 4)
print("\nTuple for methods:", tups)
print("Count of 2:", tups.count(2))

# index(value[, start[, end]]): first index of value
print("Index of first 2:", tups.index(2))
# specifying range
print("Index of 2 between idx2-5:", tups.index(2, 2, 5))

# 3. Tuple operations
# concatenation
t1 = (1, 2)
t2 = (3, 4)
t3 = t1 + t2
print("\nConcatenated tuple:", t3)

# repetition
print("Repeated tuple:", ("Hi",) * 3)

# 4. Converting between tuple and list
to_list = list(fruits)
print("List from tuple:", to_list)
# modify list, then back to tuple
to_list.append("Durian")
new_tuple = tuple(to_list)
print("New tuple after modification:", new_tuple)

# Note: Trying to assign to an index raises an error (immutability)
# fruits[0] = "Mango"

