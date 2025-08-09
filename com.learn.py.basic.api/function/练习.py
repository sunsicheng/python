#  1. 求10个元素中的最大值
lst = [1, 6, 75, 4, 34, 7, 99, 12, 66, 39]
max_v = -9999
for elem in lst:
    if elem > max_v:
        max_v = elem

print(max_v)

print('-' * 50)
# 2 输入一个字符串，提取字符串中的数字，并求和
str = input('请输入字符串')
# lst = list(str)

sum = 0
for elem in str:
    if elem.isdigit():
        sum = sum + int(elem)
print(sum)
