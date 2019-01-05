# -*- coding:utf8 -*-

import datetime, time
import tornado
import os

from app.handler.base import BaseHandler


class img_upload(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)

    @tornado.web.authenticated
    def post(self):
        '''上传'''
        file_metas = self.request.files.get('file_data', None)

        if file_metas is None:
            file_metas = self.request.files.get('file', None)
        if file_metas:
            folder = str(datetime.datetime.now().date())
            file_name = int(time.time())
            o_file_name = self.request.files.get('filename', None)
            ext = o_file_name.split('.')[1] if o_file_name else 'jpg'
            fn = '%s.%s' % (file_name, ext)
            dirs = './static/upload/%s' % folder
            if not os.path.exists(dirs):
                os.makedirs(dirs)

            img_file = file_metas[0]["body"]  # 取列表的第一个元素
            file = open(dirs + "/%s" % fn, 'w+')  # 以写方式打开一个文件
            file.write(img_file)
            file.close()

        return self.write_json('/upload/%s/%s' % (folder, fn))


class img_delete(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)

    @tornado.web.authenticated
    def post(self):
        '''上传'''

        return self.write_json(1)
