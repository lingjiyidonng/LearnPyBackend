import os

# MySQL数据库连接
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/boba?charset=utf8"

# 数据库追踪关闭
SQLALCHEMY_TRACK_MODIFICATIONS = False

# APPID
appID = ""

# SECRET
SECRET = ""

# 密钥设置
SECRET_KEY = "SecretKey"

# JSON自动排序关闭
JSON_SORT_KEYS = False

# 文件下载地址
UPLOAD_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'uploads'))

# host
HOST = "127.0.0.1:5000"