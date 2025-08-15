# Mall Admin - 商城管理系统

## 项目简介
`mall_admin` 是一个用 Python 开发的商城管理系统，支持用户管理、商品管理、订单管理等功能。项目设计为模块化，易于扩展和迭代，可从命令行版本逐步升级到 Web 版本。  

主要功能：
- 用户管理：注册、登录、余额管理
- 商品管理：添加、删除、修改商品信息，库存管理
- 订单管理：购物车、下单、订单查询、订单状态管理
- 数据持久化：支持 JSON 文件存储，可升级为数据库
- 可迭代扩展：报表、优惠活动、Web 前端等功能可逐步增加

---

## 项目目录结构
```plaintext
mall_admin/ # 主包
│
├── init.py # 包初始化
├── main.py # 程序入口
├── users.py # 用户管理模块
├── products.py # 商品管理模块
├── orders.py # 订单管理模块
├── reports.py # 数据报表模块（可选扩展）
├── utils.py # 工具函数模块
│
data/ # 数据存储目录
├── users.json # 用户信息数据文件
├── products.json # 商品信息数据文件
├── orders.json # 订单信息数据文件
│
README.md # 项目说明文档
requirements.txt # 依赖库清单（可选）
```


## 使用说明
1. 克隆项目到本地：`git clone <项目地址>`  
2. 安装依赖（如果有）：`pip install -r requirements.txt`  
3. 运行命令行商城系统：`python mall_admin/main.py`  

## 后续迭代方向
增加管理员与普通用户权限区分、商品分类与搜索功能、订单状态管理（付款、发货、完成）、报表导出与统计分析、Web 界面（Flask / Django）、优惠活动、积分系统、评价系统等。
