#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_handler import base_handler
from app.business.address import address_bll


class address_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.address = address_bll()

    def list(self):
        '''
            注册 & 登录
        '''
        user_id = 1
        address = []

        return self.write_json(address)
