# coding:utf-8

import os

from url import urls
import tornado.web
from tornado.options import options

app = tornado.web.Application(
    handlers=urls,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=options.dev,
    login_url='/admin/login',
    cookie_secret='0Ekg[(bQKM9{VnwnQI9;F@u`}Wt8Pn&R'
)
