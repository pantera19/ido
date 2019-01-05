# -*- coding:utf8 -*-

import tornado
import math

from util.json2 import dumps

from app.handler.base import BaseHandler
from app.business.admin import admin_bll

COOKIE_KEY = 'idouser'


class login(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.admin = admin_bll()

    def get(self):
        self.render('admin/login.html')

    def post(self):
        user_name = self.get_argument('username', '')
        password = self.get_argument('password', '')

        flag, user = self.admin.is_login(user_name, password)
        if flag:

            self.set_secure_cookie(COOKIE_KEY, dumps(user))
            self.write_json(True)
        else:
            self.write_json(False)


class logout(BaseHandler):
    def get(self):
        self.clear_cookie(COOKIE_KEY)
        self.redirect('/admin/login')


class change_password(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.admin = admin_bll()

    @tornado.web.authenticated
    def get(self):
        self.render('admin/change_password.html')

    @tornado.web.authenticated
    def post(self):
        old_password = self.get_argument('old_password', '')
        password = self.get_argument('password', '')

        ret = self.admin.change_password(self.current_user['id'], old_password, password)

        return self.write_json(ret)


class dashboard(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('admin/dashboard.html')
