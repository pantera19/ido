# coding:utf-8

import json

import decimal
import datetime


def default_json_decoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)


def dumps(obj, *args, **kwargs):
    return json.dumps(obj, default=default_json_decoder, *args, **kwargs)
