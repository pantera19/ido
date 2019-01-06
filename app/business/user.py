# -*- coding:utf8 -*-

from bass_access import BaseAccess

import datetime, time
import os
import urllib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

_table = 'ido.user'


class user_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

    ''' api '''

    def reg(self, open_id, union_id, nickname, sex, avatar, country, province, city):
        params = locals()
        params.pop('self')

        flag, id = self._insert(params)

        return flag, id

    def get_detail_by_openid(self, open_id):
        return self._get(conditions=dict(open_id=open_id))

    ''' admin '''

    def update_status(self, id, status=0):
        flag = self._update_status(id, status)

        return flag

    def get_detail(self, id):
        return self._get(conditions=dict(id=id))

    def get_list(self, page=1, page_size=20):
        start = (page - 1) * page_size

        conditions = dict()
        order = dict(status='desc', id='asc')
        limit = (start, page_size)

        rows = self._list(['*'], conditions, limit, order)

        return rows

    def get_count(self):
        return self._count()

    def avatarUrl2loacl(self, url):
        folder = str(datetime.datetime.now().date())
        fn = 'user_%s.jpg' % int(time.time())
        dirs = './static/upload/%s' % folder
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        urllib.urlretrieve(url, filename=dirs + '/%s' % fn)

        return '/upload/%s/%s' % (folder, fn)
