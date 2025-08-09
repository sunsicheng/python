
# 个数可变的位置参数
def  fun1(*parm):
    print(type(parm))           # 可变参数的形式是<class 'tuple'>
    for  element in parm:
        print(element)


fun1('hello','world','spark')
lst=['hello','world','spark']
fun1(lst)    # 列表会当做一个整体传进可变参数， 输出 ['hello', 'world', 'spark']
fun1(*lst)  #  加入* 会解包，一个一个传进去



#个数可变的关键字参数

def fun2(**parm2):
    print(type(parm2))
    for k,v in parm2.items():
        print(f'参数的k={k},v={v}')

aaa=dict()

fun2(name='郭靖',age=18)   #fun2('name'='郭靖','age'='18')  参数不用加引号，否则会报错

dic={'name':'郭靖','age':18}
fun2(**dic)






