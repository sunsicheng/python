
## 数据集基本信息类
class DataBase:

    ## 当前系统所有的用户信息
    userInfo=['hadoop','cindy','july','spark']

    ## 模拟数据库中存储的用户名->密码
    pwInfo = {'hadoop1': 'hadoop', 'cindy': 'flink123', 'july': 'paimon123', 'spark': 'spark456'}

    ## 模拟数据库中用户的订单信息
    orderDict={
        'hadoop': ['ord1001','ord1003','ord1005','ord1006'],
        'flink': ['ord1002','ord1004'],
        'paimon': ['ord1007','ord1010','ord1012','ord1018'],
        'spark':['ord1008','ord1009','ord1011','ord1014']
    }



