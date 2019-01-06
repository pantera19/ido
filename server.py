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

define("port", default=7878, help="run on the given port", type=int)
define("dev", type=bool, help="dev mode switch", default=True)
define("config", default="./config/ido.ini", help="config file", type=str)


def init_log():
    # init log
    from tornado.log import LogFormatter
    logger = logging.getLogger()
    logger.setLevel('INFO')

    # out log file
    path = os.path.join(os.path.dirname(__file__), "log", 'admin_%s.log' % options.port)
    channel = logging.handlers.TimedRotatingFileHandler(
        filename=path,
        when='midnight',
        interval=1,
        backupCount=options.log_file_num_backups
    )

    channel.setFormatter(LogFormatter(color=False))

    # out stderr
    rf_handler = logging.StreamHandler(sys.stderr)
    rf_handler.setLevel(logging.DEBUG)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(channel)


def main():
    from application import app

    init_log()  # init log
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
