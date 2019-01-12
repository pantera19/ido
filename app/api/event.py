#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_handler import base_handler
from app.business.event import event_bll


class event_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.event = event_bll()

    @base_handler.decorator_arguments(
        id=[None, int, True],
    )
    def info(self, **args):
        '''
            获取单个活动信息
        '''

        event = self.event.get_detail(args['id'])
        return self.write_json(event)

    def list(self):
        '''
            注册 & 登录
        '''

        events = self.event.get_all()
        return self.write_json(events)
