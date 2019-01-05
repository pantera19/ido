# -*- coding:utf8 -*-

from bass_access import BaseAccess

_table = 'ido.user'


class user_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

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
