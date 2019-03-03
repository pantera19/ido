#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from base_handler import base_handler
from app.business.event import event_bll
from app.business.event_option import event_option_bll
from app.business.donation_record import donation_record_bll
from app.business.gift import gift_bll
from app.business.user import user_bll

from util.wechat import wx

import errors
import time


class event_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.event = event_bll()
        self.event_option = event_option_bll()
        self.donation_record = donation_record_bll()
        self.gift = gift_bll()
        self.user = user_bll()

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

        events = self.event.get_all()
        return self.write_json(events)

    @base_handler.author
    @base_handler.decorator_arguments(
        event_id=[0, int, True],
        event_option_id=[0, int, True],
        other_price=[0, float, True],
    )
    def pay(self, **args):
        event_id = args['event_id']
        event_option_id = args['event_option_id']
        price = args['other_price']
        gift_id = 0
        address_id = 0
        order_number = int(time.time())
        if event_option_id > 0:
            event_option = self.event_option.get_detail(event_option_id)
            # 选项是否存在
            if event_option is None:
                return self.write_json(errors.error_params)
            else:
                # 选项状态是否 可用
                if event_option['status'] == 0:
                    return self.write_json(errors.error_params)
                else:
                    price = event_option['price']
                    gift = self.gift.get_detail(event_option['gift_id'])
                    if gift and gift['status'] == 0:
                        return self.write_json(errors.error_params)

                    gift_id = event_option['gift_id']

        pay_data = wx.generate_bill(order_number, int(float(price) * 100), self.user.open_id)

        if pay_data:
            if price * 100 < 1:
                return self.write_json(errors.error_pay_error)

            flag, id = self.donation_record.add(self.user_id, args['event_id'], args['event_option_id'], gift_id,
                                                address_id,
                                                order_number, price * 100, pay_data['prepay_id'], 0,
                                                json.dumps(pay_data), '')
            if flag:
                pay_data['order_id'] = order_number
                return self.write_json(pay_data)
            else:
                return self.write_json(errors.error_pay_error)
        else:
            return self.write_json(errors.error_pay_error)

    @base_handler.author
    @base_handler.decorator_arguments(
        order_number=[None, str, True]
    )
    def pay_done(self, **args):
        dr = self.donation_record.get_detail_by_order_number(args['order_number'])
        if self.user_id == dr['user_id']:
            self.donation_record.update_status(dr['id'], 1)
            return self.write_json(args['order_number'])
        else:
            return self.write_json(errors.error_not_allowed)
