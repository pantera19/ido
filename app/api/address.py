#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_handler import base_handler
from app.business.address import address_bll

import errors


class address_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.address = address_bll()

    @base_handler.author
    @base_handler.decorator_arguments(
        name=['', str, True],
        sex=[0, int, True],
        phone=['', str, True],
        country=['', str, True],
        province=['', str, True],
        city=['', str, True],
        street=['', str, True]
    )
    def add(self, **args):
        '''
            新增 & 修改 地址信息
        '''

        address = self.address.get_detail_by_user_id(self.user_id)

        if address:
            args['id'] = address['id']
            flag = self.address.update(**args)
        else:
            args['user_id'] = self.user_id
            flag, id = self.address.add(**args)

        return self.write_json(flag)

    @base_handler.author
    def info(self):
        '''
            根据id 获取用户地址
        '''
        address = self.address.get_detail_by_user_id(self.user_id)

        if address:

            return self.write_json(address)
        else:
            return self.write_json(None)
