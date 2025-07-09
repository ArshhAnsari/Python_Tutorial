
# Strings are immutable: once created, their content cannot be changed in place.
'''
In Python, strings are immutable, which means once a string object is created, you cannot change its individual characters in place. 
Any attempt to do so will raise an error:

text = "hello"
text[0] = "H"
# TypeError: 'str' object does not support item assignment

How .replace() works despite immutability
The string method .replace(old, new) does not modify the original string. Instead, it:

Scans the original string for every occurrence of the substring old.

Builds and returns a brand-new string where each old is substituted by new.

Leaves the original string unchanged.

Example:
text = "banana"
new_text = text.replace("a", "o")

print(text)      # banana   ← original is intact
print(new_text)  # bonono   ← this is a new string object

text remains "banana".
new_text is a different string with the replacements.
'''
text = "strings"

# 1. Basic properties and slicing
print("# Basic Properties and Slicing")
print(f"Full text: '{text}' (length {len(text)})")
print(f"First two chars: {text[0:2]}")        # indices 0 and 1
print(f"First four chars: {text[:4]}")         # start at 0, up to index 3
print(f"From index 2 onward: {text[2:]}")     # from index 2 to end
print(f"Every 2nd char from idx1 to 5: {text[1:6:2]}")  # start=1,end=5,step=2


# 2. Common string methods (case-sensitive)
print("\n# String Methods")
print(f"Capitalized: {text.capitalize()}")  # first char uppercase, rest lowercase
print(f"Uppercase: {text.upper()}")        # all chars uppercase
print(f"Lowercase: {text.lower()}")        # all chars lowercase
print(f"Endswith 'ng': {text.endswith('ng')}")  # True if suffix matches
print(f"Startswith 's': {text.startswith('s')}")  # True if prefix matches
print(f"Count 's': {text.count('s')}")      # number of occurrences
print(f"Contains 'Str': {"Str" in text}")                       # True if substring found

# 3. Escape sequences in strings
print("\n# Escape Sequences")
escaped = "The \tuniverse is \nvery very \"vast\""
# \t: tab, \n: newline, \" : literal double-quote
print(escaped)

# 4. String concatenation
print("\n# String Concatenation")
greeting = "Hello"
name = "Bob"
print(f"{greeting}, {name}")

# Imutability
print("\n# How Strings Are Immutabile")
Name="Arsh Ansari"
print(f"Name = {Name}\nIf we try to modify it: {Name.replace('Arsh','Mohd Arsh')}")
print(f"It will not change: {Name}\n")
Name=Name.replace('Arsh','Mohd Arsh')
print(f"Assigning a new value however: Name = {Name} will change.\n")
