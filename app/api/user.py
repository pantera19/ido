#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_handler import base_handler
from app.business.user import user_bll
from app.business.donation_record import donation_record_bll

from util.wechat import wx
from util.token import token_manager


class user_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.ub = user_bll()
        self.donation_record_b = donation_record_bll()

    @base_handler.decorator_arguments(
        code=[None, str, True],
        name=['', str, False],
        sex=[0, int, False],
        avatar=['', str, False],
        country=['', str, False],
        province=['', str, False],
        city=['', str, False],
    )
    def login(self, **args):
        '''
            注册 & 登录
        '''
        code = args['code']
        wx_info = wx.exchange_code_for_session_key(code)
        user = self.ub.get_detail_by_openid(wx_info['openid'])
        if user:
            uid = user['id']
        else:
            name = args['name']
            sex = args['sex']
            avatar = self.ub.avatarUrl2loacl(args['avatar'])
            country = args['country']
            province = args['province']
            city = args['city']

            flag, uid = self.ub.reg(wx_info['openid'], wx_info['unionid'], name, sex, avatar, country, province, city)

        user = self.ub.get_detail(uid)
        token = token_manager.create_token(str(uid))
        user['token'] = token
        user.pop('open_id')
        user.pop('union_id')

        return self.write_json(user)

    @base_handler.author
    def get_amount(self):
        amount, times = self.donation_record_b.get_amount_by_user_id(self.user_id)
        return self.write_json({'amount': amount, 'times': times})
