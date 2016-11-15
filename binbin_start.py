#coding=UTF-8
import os
import urlparse
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import json

from tornado.options import define, options
define("port", default=8100, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[],
        template_path=os.path.join(os.path.dirname(__file__), "src", "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "src", "static"),
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
