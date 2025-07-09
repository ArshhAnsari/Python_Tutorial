n:int=5

name:str='Arsh Ansari'

def sum(a:int,b:int)->int:
    return a+b

print(sum(1,2))

from typing import List,Union,Dict

numbers:List[int]=[1,2,3,4,5]
print(numbers)

Dictionary:Dict[str,int]={'a':1,'b':2}
print(Dictionary)

int_char: Union[int,str]=1
print(int_char)

Employee:List[Union[str,int]]=['Arsh',1]
print(Employee)
