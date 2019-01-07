# -*- coding:utf8 -*-

from bass_access import BaseAccess

_table = 'ido.gift'


class gift_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

    def get_all_di(self):
        conditions = dict(status=1)
        order = dict(id='asc')

        rows = self._list(['*'], conditions, order=order)
        di = {row['id']: row for row in rows}
        return di

    def add(self, name):
        params = locals()
        params.pop('self')

        flag, id = self._insert(params)

        return flag, id

    def update(self, id, name):
        params = locals()
        params.pop('self')
        params.pop('id')

        flag = self._update(params, dict(id=id))

        return flag

    def update_status(self, id, status=0):
        flag = self._update_status(id, status)

        return flag

    def get_detail(self, id):
        return self._get(conditions=dict(id=id))

    def get_list(self, page=1, page_size=20, all=False):
        start = (page - 1) * page_size

        conditions = dict()
        order = dict(status='desc', id='asc')
        limit = None if all else (start, page_size)

        rows = self._list(['*'], conditions, limit, order)

        return rows

    def get_count(self):
        return self._count()
