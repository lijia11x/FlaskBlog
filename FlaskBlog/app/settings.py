# -*- coding:utf-8 -*-
from datetime import timedelta
from redis import Redis
from dbutils.pooled_db import PooledDB, SharedDBConnection
import pymysql
import os

# class Config(object):
#     DEBUG = True
#     SECRET_KEY = 'asdwqadads12314'
#     # Session声明周期
#     PERMANENT_SESSION_LIFETIME = timedelta(minutes=2)
#     # 正常session只会在一级修改的时候save session，只有把每次请求的刷新设置为True才会在更改二级及以后的session时生效
#     # 否则不生效的情况为在一个视图中修改的session，在其他视图获取session是未被修改的
#     SESSION_REFRESH_EACH_REQUEST = True
#     SESSION_TYPE = 'redis'
#     SESSION_REDIS = Redis(host='120.26.103.203', port=6379)
#     PYMSQL_POOL = PooledDB(
#         creator=pymysql,  # 使用链接数据库的模块
#         maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
#         mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
#         maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
#         maxshared=3,
#         # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
#         blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
#         maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
#         setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
#         ping=0,
#         # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
#         host='120.26.103.203',
#         port=3306,
#         user='root',
#         password='123456',
#         database='usr_info',
#         charset='utf8'
#     )
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@120.26.103.203:3306/app?charset=utf8"
#
#


class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = '123abcdljx'   # os.environ.get('you-will-never-guess')
    MAIL_SERVER = 'smtp.qq.com'  # os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '604055488@qq.com' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'egibrmfzjxasbddc' #os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = "[Claus's Blog]"
    MAIL_SENDER = 'lijianxin <604055488@qq.com>'
    DEFAULT_NAME = 'lijianxin'
    DEFAULT_AUTHOR = 'Claus Lee'

# class ProductionConfig(Config):
#     DATABASE_URI = 'mysql://user@localhost/foo'


# class DevelopmentConfig(Config):
#     DEBUG = True

#
# class TestingConfig(Config):
#     TESTING = True