'''
Demonstrates basic file I/O operations in Python:
- Opening files with different modes (read, write, append)
- Reading using read(), readline(), readlines()
- Writing to files
- Using context managers (with statement)
'''

# Sample string to append/write
string = "Good luck learning"

# 1. Open existing file for reading
# 'r' mode opens for reading (default). File must exist.
f = open("file.txt", "r")

# readline(): reads a single line (up to newline) and returns it as a string
f1 = f.readline()
print("Read first line:", f1, type(f1))

# It's good practice to close files when done
f.close()

# 2. Append to file using 'a' mode
# 'a' mode opens for appending; writes go to end of file
with open("file.txt", "a") as f:
    f.write("\n" + string)  # write string on a new line

# Immediately read entire file to verify append
with open("file.txt", "r") as f:
    content = f.read()       # read() reads whole file as one string
    print("\nFull file content after append:\n", content)

# 3. Write to a new file using 'w' mode
# 'w' mode opens for writing (overwrites existing file or creates new)
with open("myfile.txt", "w") as f:
    word = "Its clean syntax makes it beginner-friendly."
    f.write(word)

# Read back what was written
txt = open("myfile.txt", "r")
print("\nContent of myfile.txt:", txt.read())
txt.close()

# Note on other methods:
# - f.readlines(): returns a list of all lines in the file
# - f.read(n): reads up to n characters
# - f.readline(): successive calls move file pointer forward
# Always use 'with' for safer file handling (auto-close on exit)
