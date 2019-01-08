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
        id=[0, int, True],
        name=['', str, True],
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
        args['user_id'] = self.user_id
        if args['id'] == 0:
            args.pop('id')
            flag, id = self.address.add(**args)
        else:
            flag = self.address.update(**args)

        return self.write_json(flag)

    @base_handler.author
    @base_handler.decorator_arguments(id=[0, int, True])
    def info(self, **args):
        '''
            根据id 获取用户地址
        '''
        address = self.address.get_detail(args['id'])

        if address:
            if address['user_id'] == self.user_id:
                return self.write_json(address)
            else:
                return self.write_json(errors.error_not_allowed)
        else:
            return self.write_json(None)

    @base_handler.author
    def list(self):
        '''
            获取用户 地址列表
        '''
        address = self.address.get_list_by_user_id(self.user_id)

        return self.write_json(address)
