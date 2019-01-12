# -*- coding:utf8 -*-

from bass_access import BaseAccess

_table = 'ido.agreement'


class agreement_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

    ''' admin '''

    def update(self, summary):
        params = locals()
        params.pop('self')

        ret = self.get_detail()
        if ret:
            flag, id = self._update(params, dict(id=ret['id']))
        else:
            flag, id = self._insert(params)

        return flag

    def get_detail(self):
        return self._get(order=dict(id='desc'))
