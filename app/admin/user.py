# -*- coding:utf8 -*-

import tornado
import math

from app.handler.base import BaseHandler
from app.business.user import user_bll


class user_list(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.user = user_bll()

    @tornado.web.authenticated
    def get(self):
        page, page_size = self.get_page()
        users = self.user.get_list(page, page_size)
        count = self.user.get_count()

        self.render('user/user_list.html', users=users, page=page, page_size=page_size,
                    page_count=int(math.ceil(count / float(page_size))))

    @tornado.web.authenticated
    def post(self):
        '''删除'''
        id = self.get_argument('id', '')
        status = int(self.get_argument('status', '0'))

        return self.write_json(self.user.update_status(id, status))

