# -*- coding:utf8 -*-

from bass_access import BaseAccess
from app.business.gift import gift_bll

_table = 'ido.event_option'


class event_option_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)
        self.gift = gift_bll()

    def add(self, event_id, price, gift_id, status=1):
        params = locals()
        params.pop('self')

        flag, id = self._insert(params)

        return flag, id

    def update(self, id, event_id, price, gift_id):
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

    def get_list(self, event_id, page=1, page_size=20):
        start = (page - 1) * page_size

        conditions = dict(event_id=event_id)
        order = dict(status='desc', price='asc')
        limit = (start, page_size)

        rows = self._list(['*'], conditions, limit, order)

        for row in rows:
            row['gift'] = self.gift.get_detail(row['gift_id'])

        return rows

    def get_count(self, event_id):
        conditions = dict(event_id=event_id)
        return self._count(conditions)
