#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import json

import logging
from tornado.web import RequestHandler, HTTPError
from tornado.util import ObjectDict

from app.api import errors

from data.mysqldb import mysql_read, mysql_write
from data.redisdb import redis_db

from util.token import token_manager
from util.json2 import dumps, default_json_decoder

from app.business.user import user_bll


class base_handler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(base_handler, self).__init__(application, request, **kwargs)
        self.set_header('Content-Type', 'text/json')

        self.user = None

        self.mysql_read = mysql_read
        self.mysql_write = mysql_write
        self.redis_db = redis_db

    def post(self, method, **kwargs):
        user = self.current_user
        self.user_id = ''
        if user:
            self.user_id = user['id']
            self.user_name = user['nickname']
            self.user = user

        try:
            ret = eval('self.%s(*kwargs)' % method)
        except Exception as e:
            import traceback
            msg = '%s %s' % (e, traceback.format_exc())
            ret = errors.error_server_error
            ret['msg'] = '%s' % msg
            logging.error(msg)

        if ret != None:
            ret = json.dumps(ret, default=default_json_decoder)
            return self.write(ret)

        raise HTTPError(**errors.error_not_found)

    def get(self, method, **kwargs):
        return self.post(method, **kwargs)

    def put(self, *args, **kwargs):
        raise HTTPError(**errors.error_not_found)

    def delete(self, *args, **kwargs):
        raise HTTPError(**errors.error_not_found)

    def options(self, *args, **kwargs):
        if self.settings['allow_remote_access']:
            self.write("")

    def write_json(self, data, status_code=200, msg='success.'):
        self.finish(dumps({
            'code': status_code,
            'msg': msg,
            'data': data
        }))

    @staticmethod
    def decorator_arguments(*dargs, **dkargs):
        '''
            参数校验 装饰器
        '''

        def wrapper(func):
            def _wrapper(*args, **kargs):
                nkargs = dict()
                for k, v in dkargs.items():
                    val = args[0].get_argument(k, v[0])

                    if v[2]:
                        if not val:
                            return errors.error_params
                    try:
                        nkargs[k] = v[1](val)
                    except Exception as e:
                        logging.error('params error=======%s', e)
                        return errors.error_params
                kargs.update(nkargs)
                return func(*args, **kargs)

            return _wrapper

        return wrapper

    @staticmethod
    def author(func):
        '''
            鉴权 装饰器
        '''

        def __decorator(*args, **kargs):
            a = args[0]
            user = a.get_current_user()

            if not user:
                result = errors.error_not_logined
            else:
                a.current_user = user
                a.user_id = user.id
                result = func(*args, **kargs)

            return result

        return __decorator

    def get_current_user(self):
        '''
            通过 header 中 token
            获取当前登录用户
        '''
        is_login = False
        if 'token' in self.request.headers:
            token = self.request.headers['token']
            is_login, user_id = token_manager.validate_token(token)

        if is_login:
            ub = user_bll()
            user = ub.get_detail(user_id)
            return ObjectDict(user)
        else:
            return None
