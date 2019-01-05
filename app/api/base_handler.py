# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
#
# import logging
# import tornado.web
# from tornado.util import ObjectDict
#
# from app.api import errors
# from util.token import token_manager
#
#
# # from modules.user_bll import user_bll
#
#
# class base_handler(tornado.web.RequestHandler):
#
#     def __init__(self, application, request, **kwargs):
#         super(base_handler, self).__init__(application, request, **kwargs)
#         self.set_header('Content-Type', 'text/json')
#
#         self.user = None
#
#         headers = self.request.headers
#
#         self.dc = application.DB
#         self.application = application
#
#         # 刷新token时间
#         # self.refresh_token()
#         #
#         # self.init_bll()
#
#     #
#     # def init_bll(self):
#     #     pass
#     #
#     # def refresh_token(self):
#     #     # 刷新token时间
#     #     token = self.header('token')
#     #     if token:
#     #         at = self.header('atype')
#     #         ub = user_bll(self.dc)
#     #         ub.check_token(token, at, True)
#     #
#     def post(self, method, *kwargs):
#         print(method)
#         print(kwargs)
#         return self.send_error(200)
#
#     #
#     # def get(self, method, *kwargs):
#     #     user = self.current_user
#     #     self.uid = ''
#     #     if user:
#     #         self.uid = user['id']
#     #         self.uname = user['name']
#     #         self.user = user
#     #
#     #     try:
#     #         ret = eval('self.%s(*kwargs)' % method)
#     #     except Exception as e:
#     #         import traceback
#     #         msg = '%s %s' % (e, traceback.format_exc())
#     #         ret = Errors.copy_item(Errors.PARAM_ERROR)
#     #         ret['error'] = '%s' % msg
#     #         logging.error(msg)
#     #
#     #     if ret != None:
#     #         ct = self.para('ct', 'text/json')
#     #         self.set_header('Content-Type', ct)
#     #
#     #         cb = self.para('callback', '')
#     #         ret = json.dumps(ret, default=self.default_json_decoder)
#     #         if cb:
#     #             ret = '%s(%s)' % (cb, ret)
#     #         return self.write(ret)
#
#     def put(self, method, *kwargs):
#         return self.write_error(405)
#
#     def delete(self, method, *kwargs):
#         return self.send_error(405)
#
#     @staticmethod
#     def decorator_arguments(*dargs, **dkargs):
#         def wrapper(func):
#             def _wrapper(*args, **kargs):
#                 nkargs = dict()
#                 for k, v in dkargs.items():
#                     val = args[0].get_argument(k, v[0])
#
#                     if v[2]:
#                         if not val:
#                             return
#                             # return Errors.copy_item(Errors.PARAM_ERROR)
#                     try:
#                         nkargs[k] = v[1](val)
#                     except Exception as e:
#                         logging.error('params error=======%s', e)
#                         return
#                         # return Errors.copy_item(Errors.PARAM_ERROR)
#                 kargs.update(nkargs)
#                 return func(*args, **kargs)
#
#             return _wrapper
#
#         return wrapper
#     #
#     # def header(self, paraName, default=None):
#     #     # 获取header内容
#     #     return self.request.headers.get(paraName, default)
#     #
#
#     # @staticmethod
#     # def author(func):
#     #     # 鉴权
#     #     def __decorator(*args, **kargs):
#     #         a = args[0]
#     #         user = a.get_current_user()
#     #
#     #         if not user:
#     #             result = Errors.copy_item(Errors.UNLOGIN_ERROR)
#     #         else:
#     #             a.current_user = user
#     #             a.uid = user.id
#     #             result = func(*args, **kargs)
#     #
#     #         return result
#     #
#     #     return __decorator
#     #
#     # def get_current_user(self):
#     #     token = self.header('token')
#     #     auth_type = self.header('atype')
#     #
#     #     ub = user_bll(self.dc)
#     #     user = ub.get_by_token(token, auth_type)
#     #
#     #     return ObjectDict(user) if user else None
