# 1. For-loop through a list
print("1. For-loop through a list:")
items = [1, 2, 3, 4, 5]
for i in items:
    print(i, end=" ")   # prints 1 2 3 4 5
print("\n")

# 2. For-loop with range()
print("2. For-loop with range(1, 5):")
for i in range(1, 5):   # numbers 1 to 4
    print(i, end=" ")
print("\n")

# 3. While-loop
print("3. While-loop counting to 4:")
j = 1
while j < 5:
    print(j, end=" ")
    j += 1
print("\n")

# 4. Using break and continue
print("4. break and continue example:")
for i in range(10):
    if i == 4:
        continue    # skip when i == 4
    if i == 6:
        break       # stop loop when i == 6
    print(i, end=" ")
print("\n")

# 5. Nested loops for star pattern
print("5. Star pattern with nested loops:")
for i in range(1, 6):        # rows 1 to 5
    for j in range(i):       # stars equal to row number
        print("*", end=" ")
    print()                 # new line after each row

# While loop version 
# i=1
# while i<num:
#     j=1
#     while j<=i:
#         print("*",end=" ")
#         j+=1
#     print()
#     i+=1


# For star pyramid
num=int(input("Enter a number:"))
for i in range(1,num+1):
    print(" "*(num-i),end="")
    for j in range(1,2*i):
        print("*",end="")  
    print()

# for hollow square
for i in range (1,num+1):
    for j in range(1,num+1):
        if (i==1 or j==1) or (i==num or j==num):
            print("*",end=" ")
        else:
            print(" ",end=" ")
    print()
