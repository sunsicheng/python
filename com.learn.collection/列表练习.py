# 从键盘录入 5 个商品信息（1001 手机）添加到商品列表中，展示商品信息，提示用户选择商品，用户选中的商品添加到购物车中（购物车中的商品要逆序），用户选中的商品不存在需要有相应提示，当用户输入“q”时循环结束，显示购物车中的商品。


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
