train_info = {
    'G1026':['北京南-天津南', '18:06', '18:39', '36'],
    'G1068': ['北京南-天津南', '18:06', '18:39', '36'],
    'G2018': ['北京-天津北', '18:06', '18:39', '36'],
    'G168':['北京南-天津', '18:06', '18:39', '36']
}


print('车次   出发站-到达站     出发时间    到达时间    耗时')

for key in train_info.keys():
    print(key,end='  ')
    for value in train_info.get(key):
        for e in value:
            print(e,end='')
    print()

# train_no = input('请输入要购买的车次')
# train_person=input("请输入乘车人，如果是多个乘车人请使用逗号分隔:")
# train_info.get('G1026')
# print(f'您已购买了${train_no}  ,{}')