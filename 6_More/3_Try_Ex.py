### Try-Except
# try:
#     a=int(input("Enter a number: "))
#     # print(f"You have entered {a}")

# except Exception as e:
#     print(e)

### Exception Raising
# a=int(input("Enter a number: "))
# b=int(input("Enter another number: "))

# if b==0:
#     raise ValueError("Heeyyy bhai, You Cannot divide by zero")

# print(f"{a} / {b} = {a/b}")


### Try-Except-Else
try:
    a=int(input("Enter a number: "))
    

except Exception as e:
    print(e)

else:
    print(f"You have entered {a}")