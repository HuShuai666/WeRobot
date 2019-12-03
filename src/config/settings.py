# coding:utf-8
import pymysql

# 测试服务号   通过app_id和app_secret获取access_token
APP_ID = 'wx595cd703e0b81932'
APP_SECRET = '70464ae8a0ea1f0b72c939d4e1d177f3'

# db_config = {
#     'host': '47.92.115.126',
#     'port': 3306,
#     'db': 'stu_system',
#     'user': 'root',
#     'password': 'svLE26eg',
#     'cursorclass': pymysql.cursors.DictCursor,
#     'charset': 'utf8'
# }

test_db_config = {
    'host': '47.105.104.233',
    'port': 3306,
    'db': 'website_backend',
    'user': 'root',
    'password': 'root',
    'cursorclass': pymysql.cursors.DictCursor,
    'charset': 'utf8'
}

REDIS_CONFIG = {
    'host': '47.105.104.233',
    'port': 6379,
    'password': '1q2w3e4r!'
}

micro_service_domain = 'http://127.0.0.1:6060'
