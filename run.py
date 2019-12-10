import os
import sys
from werobot.contrib.tornado import make_handler
from tornado.options import define, options
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.netutil
import tornado.process
from config.settings import LogFormatter
from src.robot import robot
import logging
from config import settings

# 这里配置的是日志的路径，配置好后控制台的相应信息就会保存到目标路径中。
options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'logs/log.log')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/weixin/', make_handler(robot)),

        ]
        super(Application, self).__init__(handlers, **settings.log)  # 加载settings配置


define('port', default=6060, type=int)


def main():
    port = 6060
    if len(sys.argv) > 1:
        port = sys.argv[1]

    # 控制台输出请求详情
    options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    sockets = tornado.netutil.bind_sockets(port)
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
