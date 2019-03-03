# -*- coding:utf8 -*-

import tornado
import math

from app.handler.base import BaseHandler
from app.business.event import event_bll


class event_list(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.event = event_bll()

    @tornado.web.authenticated
    def get(self):
        page, page_size = self.get_page()
        events = self.event.get_list(page, page_size)
        count = self.event.get_count()

        self.render('event/event_list.html', events=events, page=page, page_size=page_size,
                    page_count=int(math.ceil(count / float(page_size))))

    @tornado.web.authenticated
    def post(self):
        '''删除'''
        id = self.get_argument('id', '')
        status = int(self.get_argument('status', '0'))

        return self.write_json(self.event.update_status(id, status))


class event_detail(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.event = event_bll()

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', '')
        event = self.event.get_detail(id)

        self.render('event/event_detail.html', event=event)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument('id', '')

        name = self.get_argument('name', '')
        cover = self.get_argument('cover', '')
        summary = self.get_argument('summary', '')
        theme = self.get_argument('theme', '')
        pay_cover = self.get_argument('pay_cover', '')
        cart_cover = self.get_argument('cart_cover', '')

        if id:
            ret, id = self.event.update(id, name, cover, summary, theme, pay_cover, cart_cover)
        else:
            ret, id = self.event.add(name, cover, summary, theme, pay_cover, cart_cover)

        self.write_json(ret)
