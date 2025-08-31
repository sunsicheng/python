


##   因为 全局sum是数值类型，不可修改，所以在栈里面创建了一个新的对象
# sum=0
# def add(a,b):
#     sum=a+b
#     print(f'内部sum的地址{id(sum)=},sum的值{sum=}')  #  内部sum的地址id(sum)=140704048584392,sum的值sum=30
#     return sum
#
# add(10,20)
# print(f'外部sum的地址{id(sum)=},sum的值{sum=}')    ##  内部sum的地址id(sum)=140704048584392,sum的值sum=30


## 探索 ： 如果是可修改的对象，是不是不会变


lst=['1','2','3','4','5','6']

def modify(n):
    lst.pop(n)
    print(f'内部lst的地址{id(lst)=},sum的值{lst=}')


modify(3)
print(f'外部lst的地址{id(lst)=},sum的值{lst=}')