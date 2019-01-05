# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# import logging
# import errno
# from base_handler import base_handler
# from app.business.user import user_bll
#
#
# class user_handler(base_handler):
#     def __init__(self, application, request, **kwargs):
#         base_handler.__init__(self, application, request, *kwargs)
#         self.ub = user_bll(self.dc)
#
#     @base_handler.decorator_arguments(code=[None, str, True])
#     def login(self, **args):
#         # 注册
#
#         print(args['code'])
#         return 1
