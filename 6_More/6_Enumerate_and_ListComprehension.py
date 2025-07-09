list = [3,56,99,34,17]

# index = 0
# for value in list:
#     print("At index",index, "= value", value)
#     index += 1

# ^^^^ same as ^^^^
print("Enumerate:")
for index, value in enumerate(list):
    print("At index",index, "= value", value)
    # print(value,end=" ")


# squaredList=[]
# for i in list:
#     squaredList.append(i*i)
# print(squaredList)

# ^^^^ same as ^^^^
print("\nList Comprehension:")
squaredList=[i*i for i in list]
print(squaredList)