# 用 list() 得到列表
# 用 tuple() 得到元组
# 用 set() 得到集合（会去重 + 无序）



# list -> set（去重）
lst = [1, 2, 2, 3]
s = set(lst)
print(s)  # {1, 2, 3}

# set -> list
lst2 = list(s)
print(lst2)  # [1, 2, 3]
#  转成 set 会自动去重，且元素顺序会丢失（因为 set 无序）。


# list -> tuple
lst = [1, 2, 3]
t = tuple(lst)
print(t)  # (1, 2, 3)

# tuple -> list
lst2 = list(t)
print(lst2)  # [1, 2, 3]
# 顺序会保留，因为 list 和 tuple 都是有序的。


# set -> tuple
s = {1, 2, 3}
t = tuple(s)
print(t)  # (1, 2, 3)  # 顺序不固定

# tuple -> set
t2 = (1, 2, 2, 3)
s2 = set(t2)
print(s2)  # {1, 2, 3}
# 转成 set 会去重、无序；转成 tuple 会保留当前遍历顺序（但 set 本身是无序的）。
