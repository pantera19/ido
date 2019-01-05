# -*- coding:utf8 -*-

import tornado
import math

from app.handler.base import BaseHandler
from app.business.gift import gift_bll


class gift_list(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.gift = gift_bll()

    @tornado.web.authenticated
    def get(self):
        page, page_size = self.get_page()
        gifts = self.gift.get_list(page, page_size)
        count = self.gift.get_count()

        self.render('gift/gift_list.html', gifts=gifts, page=page, page_size=page_size,
                    page_count=int(math.ceil(count / float(page_size))))

    @tornado.web.authenticated
    def post(self):
        '''删除'''
        id = self.get_argument('id', '')
        status = int(self.get_argument('status', '0'))

        return self.write_json(self.gift.update_status(id, status))


class gift_detail(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.gift = gift_bll()

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', '')
        gift = self.gift.get_detail(id)

        self.render('gift/gift_detail.html', gift=gift)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id', '')

        name = self.get_argument('name', '')

        if id:
            ret, id = self.gift.update(id, name)
        else:
            ret, id = self.gift.add(name)

        self.write_json(ret)
