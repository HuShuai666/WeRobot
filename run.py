import sys

from werobot.contrib.tornado import make_handler
from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.netutil
import tornado.process
from src.robot import robot


# if __name__ == '__main__':
#     port = 7080
#     if len(sys.argv) > 1:
#         port = sys.argv[1]
#     robot.run(server='tornado', host='0.0.0.0', port=port)
define('port', default=6060, type=int)

application = tornado.web.Application([
    (r'/weixin/', make_handler(robot)),

])

if __name__ == '__main__':
    # port = 6060
    # if len(sys.argv) > 1:
    #     port = sys.argv[1]
    # sockets = tornado.netutil.bind_sockets(int(port))
    # tornado.process.fork_processes(5)
    # http_server = tornado.httpserver.HTTPServer(application)
    # # application.listen(port)
    # http_server.add_sockets(sockets)
    # tornado.ioloop.IOLoop.instance().start()
    parse_command_line()
    app = application
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
