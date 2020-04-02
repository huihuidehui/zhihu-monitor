#!/usr/bin/env python
# encoding: utf-8

# 数据库链接地址
# SQLALCHEMY_DATABASE_URI = "sqlite:///./dbdir/test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
# mysql数据库示例
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://usename:password@host:port/databasename?charset=encode"
# 例如
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://kanhui:123456@mysql01:3306/monitor?charset=utf8mb4"
# 用于表单加密
SECRET_KEY = "123456"

BCRYPT_LEVEL = 13

# token过期时间
TOKEN_EXPIRATION_TIME = 12000  # 单位是秒

# 默认分页页数，每页的大小
DEFAULTPAGE = 1
DEFAULTSIZE = 5

# 定时爬虫的时间设置
HOUR = 9
MINUTE = 53
# 代理池ip, 默认不开启，如果需要代理池的或可以在文件 /crawler_data.py 58行进行修改
# IPS = [
#             '1.119.129.2:8080',
            # '115.174.66.148',
            # '113.200.214.164'
        # ]