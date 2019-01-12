# -*- coding:utf8 -*-

import tornado
import math

from app.handler.base import BaseHandler
from app.business.event_option import event_option_bll
from app.business.gift import gift_bll


class event_option_list(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.event_option = event_option_bll()

    @tornado.web.authenticated
    def get(self):
        event_id = self.get_argument('event_id', '')

        if event_id == '':
            self.redirect('/admin/events')

        page, page_size = self.get_page()
        event_options = self.event_option.get_list(event_id, page, page_size)
        count = self.event_option.get_count(event_id)

        self.render('event_option/event_option_list.html', event_id=event_id, event_options=event_options, page=page,
                    page_size=page_size, page_count=int(math.ceil(count / float(page_size))))

    @tornado.web.authenticated
    def post(self):
        '''删除'''
        id = self.get_argument('id', '')
        status = int(self.get_argument('status', '0'))

        return self.write_json(self.event_option.update_status(id, status))


class event_option_detail(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.event_option = event_option_bll()
        self.gift_bll = gift_bll()

    @tornado.web.authenticated
    def get(self):
        event_id = self.get_argument('event_id', '')
        id = self.get_argument('id', '')
        event_option = self.event_option.get_detail(id)
        gifts = self.gift_bll.get_list(all=True)
        self.render('event_option/event_option_detail.html', event_id=event_id, event_option=event_option, gifts=gifts)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id', '')

        price = self.get_argument('price', '')
        notice = self.get_argument('notice', '')
        event_id = self.get_argument('event_id', '')
        gift_id = self.get_argument('gift_id', '')

        if id:
            ret, id = self.event_option.update(id, event_id, price, notice, gift_id)
        else:
            ret, id = self.event_option.add(event_id, price, notice, gift_id)

        self.write_json(ret)
