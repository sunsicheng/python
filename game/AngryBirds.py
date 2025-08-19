class Birds:
    """"小鸟基类"""

    def __init__(self, name, color, skill_description):
        self.name = name
        self.color = color
        self.skill_description = skill_description

    # 类方法
    @classmethod
    def fly(self):
        pass

    @classmethod
    def call(self):
        pass

    @classmethod
    def use_skill(self):
        pass


class RedBirds(Birds):

    def fly(self):
        print(f'{self.name}飞翔展示{self.color}的火焰')

    def call(self):
        print(f'{self.name}唧唧叫')


class YellowBirds(Birds):
    def fly(self):
        print(f'{self.name}飞翔的时候展示{self.color}的火焰')

    def call(self):
        print(f'{self.name}呱呱叫')


class BlueBirds(Birds):
    def fly(self):
        print(f'{self.name}飞翔的时候展示{self.color}的火焰')

    def call(self):
        print(f'{self.name}嘿嘿叫')


class Obstacle:
    def __init__(self, name, strength):
        # 障碍物名称
        self.name = name
        # 障碍物血量
        self.strength = strength

    def be_attacked(self, bird):
        # 调用父类方法
        bird.use_skill()

        # 根据鸟的类型，定义伤害
        if isinstance(bird, RedBirds):
            damageValue = 100
        elif isinstance(bird, YellowBirds):
            damageValue = 60
        elif isinstance(bird, BlueBirds):
            damageValue = 20
        else:
            damageValue = 10

        self.strength -= damageValue

        if self.strength<=0:
            print(f'{self.name}被{bird.name}摧毁啦~~~~~')
        else:
            print(f'{self.name}正在被{bird.name}攻击，还剩下{self.strength}的血量')




if __name__ == '__main__':
    yellow=YellowBirds('黄鹂','黄色','吟诗')
    red=RedBirds('凤凰','红色','四大神兽之一')
    blue=BlueBirds('老鹰','蓝色','鹰击长空')


    #创建障碍物
    stone=Obstacle('石头',200)
    tree=Obstacle('木头',100)


    ##模拟共计过程

    stone.be_attacked(yellow)
    stone.be_attacked(blue)