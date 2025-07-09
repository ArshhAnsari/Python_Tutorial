# Can you multiple context managers in a single "with" statement 

with (
    open("file1.txt", "r") as f1,
    open("file2.txt", "w") as f2
):
    f2.write(f1.read()) # write content of f1 to f2