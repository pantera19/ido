# -*- coding:utf8 -*-

import traceback
import json

from tornado.web import RequestHandler, HTTPError

from app.handler import errors
from util.json2 import dumps

class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)

    def access_control_allow(self):
        # 允许 JS 跨域调用
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                        "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                        "X-File-Name, Cache-Control, Token")
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def post(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def put(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def delete(self, *args, **kwargs):
        raise HTTPError(**errors.status_0)

    def write_error(self, status_code, **kwargs):
        self._status_code = 200

        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            lines = []
            for line in traceback.format_exception(*kwargs["exc_info"]):
                lines.append(line)

            self.write_json(dict(traceback=''.join(lines)), status_code, self._reason)

        else:
            self.write_json(None, status_code, self._reason)

    def write_json(self, data, status_code=200, msg='success.'):
        self.finish(
            dumps({
                'code': status_code,
                'msg': msg,
                'data': data
            }))

    # @tornado.web.authenticated
    def get_current_user(self):
        user = None
        if self.get_secure_cookie("idouser"):
            user = json.loads(self.get_secure_cookie("idouser"))

        return user

    def get_page(self):
        page = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '20'))

        return page, page_size

    @property
    def data(self):
        return self.application.data
