# -*- coding:utf8 -*-

from bass_access import BaseAccess

_table = 'ido.address'


class address_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

    ''' api '''

    def get_detail_by_user_id(self, user_id):
        conditions = dict(status=1, user_id=user_id)

        rows = self._get(['*'], conditions)

        return rows

    ''' admin '''

    def add(self, user_id, name, sex, phone, country, province, city, street, is_default=0):
        params = locals()
        params.pop('self')

        flag, id = self._insert(params)

        return flag, id

    def update(self, id, name, sex, phone, country, province, city, street, is_default=0):
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

        conditions = dict(status=1)
        order = dict(id='asc')
        limit = None if all else (start, page_size)

        rows = self._list(['*'], conditions, limit, order)

        return rows

    def get_count(self):
        return self._count()
