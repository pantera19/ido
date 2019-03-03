#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from base_handler import base_handler
from app.business.donation_record import donation_record_bll

import errors
import time


class donation_record_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.donation_record = donation_record_bll()

    @base_handler.author
    @base_handler.decorator_arguments(
        order_number=[0, int, True]
    )
    def info(self, **args):
        order_number = args['order_number']
        donation_record = self.donation_record.get_detail_by_order_number(order_number, 1, True)
        return self.write_json(donation_record)

    @base_handler.author
    def list(self):
        donation_records = self.donation_record.get_all(self.user_id)
        return self.write_json(donation_records)

    @base_handler.author
    @base_handler.decorator_arguments(
        order_number=[0, int, True]
    )
    def pic(self, **args):
        order_number = args['order_number']
        cert = self.donation_record.get_pic_by_order_number(order_number)

        return self.write_json(cert)

    def get_amount(self):
        amount, times = self.donation_record.get_amount()
        return self.write_json({'amount': amount, 'times': times})
