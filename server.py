#!/usr/bin/env python
# coding:utf-8
import os
import logging
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from ConfigParser import ConfigParser

define("port", default=7878, help="run on the given port", type=int)
define("dev", type=bool, help="dev mode switch", default=True)
define("config", default="./config/ido.ini", help="config file", type=str)


def init_log():
    # 初始化日志
    from tornado.log import LogFormatter
    logger = logging.getLogger()
    logger.setLevel('INFO')
    path = os.path.join(os.path.dirname(__file__), "log", 'admin_%s.log' % options.port)
    channel = logging.handlers.TimedRotatingFileHandler(
        filename=path,
        when='midnight',
        interval=1,
        backupCount=options.log_file_num_backups
    )

    channel.setFormatter(LogFormatter(color=False))
    logger.addHandler(channel)


def main():
    from application import app

    init_log()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
