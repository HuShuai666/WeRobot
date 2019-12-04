# coding:utf-8
import pymysql
import tornado
import os
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
    'host': 'localhost',
    'port': 6379,
    'password': '1q2w3e4r!'
}

micro_service_domain = 'http://127.0.0.1:6060'

WSGI_APPLICATION = 'WeRobot.wsgi.application'

# 格式化日志输出格式
# 默认是这种的：[I 160807 09:27:17 web:1971] 200 GET / (::1) 7.00ms
# 格式化成这种的：[2016-08-07 09:38:01 执行文件名:执行函数名:执行行数 日志等级] 内容消息


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


log = dict(
    # template_path=os.path.join(os.path.dirname(__file__), 'templates'),  # 设置模板路径
    log_path=os.path.join(os.path.dirname(__file__), "logs"),
    # static_url_prefix='/myPath/static/', # 设置html中静态文件的引用路径，默认为/static/
    debug=True,
    # xsrf_cookies=True, //开启后werobot无法使用
)