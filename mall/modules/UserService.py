from mall.entity.DataBase import DataBase
class UserService:

    def __init__(self):
        pass
    

    # 用户登录
    def login(self, userName, password):
        if userName is None or '' == userName:
            raise ValueError('用户名不能为空')
        elif userName in DataBase.userList.keys():
            if password == DataBase.userList.get(userName):
                print('恭喜你，登陆成功！！！')
            else:
                print('密码错误，请重新输入密码！！！')
        else:
            print('用户名不存在！！')

    def showOrders(self, userName):
        pass


if __name__ == '__main__':
    user = UserService()
    user.login('hadoop', 'hadoop')
