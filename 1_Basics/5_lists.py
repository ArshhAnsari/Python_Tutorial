# 1. Nature of Lists: Mutable sequence type
# Lists can be modified in place: elements can be changed, added, or removed.

# Create a list with mixed types
items = ["Apple", 5, 35.5, "Rohan"]
print("Initial list:", items)

# Modify an element by index
items[0] = "Mango"  # change 'Apple' to 'Mango'
print("After assignment at index 0:", items)

# Append a new element to the end
items.append("Pineapple")
print("After append():", items)

# 2. Sorting a homogeneous list
numbers = [5, 64, 23, 56, 1, 10]
print("\nOriginal numbers:", numbers)

# sort() modifies list in place in ascending order
default_sorted = numbers.copy()
default_sorted.sort()
print("After sort():", default_sorted)

# reverse() modifies in place (reverses order)
default_sorted.reverse()
print("After reverse():", default_sorted)

# 3. Insertion and Removal
# insert(index, value): add value before given index
default_sorted.insert(3, 3333)
print("After insert(3, 3333):", default_sorted)

# pop([index]): remove and return element at index (last if omitted)
popped = default_sorted.pop(4)
print(f"pop(4) removed {popped}, list now:", default_sorted)

# remove(value): remove first occurrence of value
default_sorted.remove(5)
print("After remove(5):", default_sorted)

# 4. Other helpful list operations
print("\nLength of list:", len(default_sorted))
print("Contains 10?", 10 in default_sorted)
print("Index of 10:", default_sorted.index(1))
print("Count of 10:", default_sorted.count(10))
print("Concatenate with [100, 200]:", default_sorted + [100, 200])

# Note: since lists are mutable, operations like sort(), reverse(), insert(), pop(), remove()
# change the original list object rather than creating a new one.
