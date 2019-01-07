# -*- coding:utf8 -*-

from bass_access import BaseAccess
from app.business.event_option import event_option_bll

_table = 'ido.event'


class event_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)
        self.event_option = event_option_bll()

    ''' api '''

    def get_all(self):
        conditions = dict(status=1)
        order = dict(id='desc')

        rows = self._list(['*'], conditions=conditions, order=order)
        options = self.event_option.get_all_di()

        for row in rows:
            row['options'] = options.get(row['id'], [])
            row['cover'] = row['cover'].split(',')

        return rows

    ''' admin '''

    def add(self, name, cover, summary):
        params = locals()
        params.pop('self')

        flag, id = self._insert(params)

        return flag, id

    def update(self, id, name, cover, summary):
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

    def get_list(self, page=1, page_size=20):
        start = (page - 1) * page_size

        conditions = dict()
        order = dict(status='desc', id='asc')
        limit = (start, page_size)

        rows = self._list(['*'], conditions, limit, order)

        return rows

    def get_count(self):
        return self._count()
