# Syntax : lambda arguments : expression

x = lambda a : a + 10
print(x(5))

square=lambda x : x*x
print(square(5))

sum = lambda a,b,c : a+b+c
print(sum(1,2,3))


# Join method 
str1 = "Arsh"
str2 = "Ansari"
lst = ["Arsh","Ansari"]
str3 = " ".join([str1,str2])
print(" ".join(lst))
print(str3)