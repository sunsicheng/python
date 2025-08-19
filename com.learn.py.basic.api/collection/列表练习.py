# 从键盘录入 5 个商品信息（1001 手机）添加到商品列表中，展示商品信息，提示用户选择商品，用户选中的商品添加到购物车中（购物车中的商品要逆序），用户选中的商品不存在需要有相应提示，当用户输入“q”时循环结束，显示购物车中的商品。


print('*'*10)
list1 = [1, 2, 3, 4, 5]
list2 = ["a", "b", "c", "d", "e"]
tuple_list = [(i, j) for i in list1 for j in list2]
print(tuple_list)
print('*'*10)

list1 = [100, 200, 300, 400, 500]
print(list1)  # 取全部元素
print(list1[:])  # 复制整个列表
print(list1[2:4])  # 取索引从2开始到4(不包含)的元素
print(list1[2:])  # 取索引从2开始到末尾的元素
print(list1[:2])  # 取索引从0开始到2(不包含)的元素
print(list1[2:-1])  # 取索引从2开始到-1(不包含)的元素
print(list1[::-1])  # 倒序取元素

print('*'*10)
list1 = [1, 2, 3, 4, 5]
list2 = ["a", "b", "c", "d", "e"]
tuple_list = [(i, j) for i in list1 for j in list2]
print(tuple_list)


# 1001 iphone,1002 ipad,1003 airpods,1004 macbookpro,1005 华为

str = input("请输入商品信息:")
product_lst = str.split(',')  # 字符串split后返回的就是列表
# print(product_lst,type(product_lst))

for item in product_lst:
    print(item)

car_lst = []
while True:
    flag = False  # 如果需要再循环里面加上判断，则可以flag
    product = input("请选择商品:")
    if product != 'q':
        for item in product_lst:
            temp = item[5:]
            if temp == product:
                flag = True
                car_lst.append(product)
            else:
                continue
        if flag != True:
            print("当前商品不存在")
    else:
        break;

car_lst.reverse()

print(car_lst)
