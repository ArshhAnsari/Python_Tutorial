# Dictionary is a collection of key-value pairs, where the keys are unique and immutable, and the values can be of any type.
# Dictionary is a mutable data type, meaning its elements can be changed after creation.
# Immutability of keys ensures consistent hashing and lookup performance.

# Create a dictionary of student marks
marks = {
    "Rohan": 90,
    "Arsh": 80,
    "Mohd Arsh": 70,
    "Rohit": 60
}
print("Initial dict:", marks)
print("Type:", type(marks))

# 2. Accessing and updating values
print("\nAccess 'Rohan':", marks["Rohan"])     # direct indexing (KeyError if missing)
print("Get 'Rohit':", marks.get("Rohit"))        # safer (returns None or default if missing)
print("Get missing 'Alice':", marks.get("Alice", "Not Found"))

# Update existing key and add a new key
marks["Rohit"] = 50                              # assignment by index
marks.update({"Mohd Arsh": 100, "Alice": 85}) # update multiple at once
print("After updates:", marks)

# 3. Removing entries
removed = marks.pop("Arsh")                      # removes key, returns its value
print(f"Popped 'Arsh' -> {removed}, dict now: {marks}")
last_item = marks.popitem()                       # removes and returns the last inserted (key, value)
print(f"Popitem() -> {last_item}, dict now: {marks}")

# 4. Viewing keys, values, and items
print("\nKeys:", list(marks.keys()))
print("Values:", list(marks.values()))
print("Items:", list(marks.items()))

# 5. Checking membership
print("Is 'Rohan' in dict?", "Rohan" in marks)
print("Is 100 a value?", 100 in marks.values())

# 6. Other useful methods
# setdefault(): get value or set default if key missing
default_score = marks.setdefault("Bob", 75)
print(f"setdefault('Bob',75) -> {default_score}, dict now: {marks}")

# clear(): remove all items
# marks.clear()
# print("After clear():", marks)

# copy(): shallow copy of dict
marks_copy = marks.copy()
print("\nCopied dict:", marks_copy)

# merging two dicts (Python 3.9+)
merge_dict={"Alice":85}
marks.update(merge_dict)
print("After merge:", marks)
