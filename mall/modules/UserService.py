from mall.entity.DataBase import DataBase as db
from mall.entity.User import User


class UserService:

    def __init__(self):
        pass

    # 用户登录
    def login(self, userName, password):
        if userName is None or '' == userName:
            raise ValueError('用户名不能为空')
        elif userName in db.pwInfo.keys():
            if password == db.pwInfo.get(userName):
                print('恭喜你，登陆成功！！！')
            else:
                print('密码错误，请重新输入密码！！！')
        else:
            print('用户名不存在！！')

    ## 新增用户

    def addUser(self, user):
        if user.name in db.userInfo:
            raise ValueError('当前用户已经存在，无法添加')
        else:
            db.userInfo.append(user.name)

    ## 删除用户
    def delUser(self, user):
        if user.name in db.userInfo:
            print(f'当前用户{user.name}已经存在,无法删除')

    ## 修改用户密码
    def updataUserPW(self, user):
        if user.name in db.pwInfo:
            db.pwInfo[user.name] = user.passwd

    ## 查询订单信息
    def showOrders(self, userName):
        pass

    def showUsers(self):
        for user in db.userInfo:
            print(f'{user}')


if __name__ == '__main__':
    userService = UserService()
    userService.login('cindy', 'flink123')
    ## 打印当前所有用户
    userService.showUsers()
    print('')
    ##创建一个用户
    jquery = User(1010, 'jquery', 26, 1000, '江西', '132132', 'pw1001')
    userService.addUser(jquery)
    userService.showUsers()
