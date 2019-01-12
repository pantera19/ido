# -*- coding:utf8 -*-

import tornado

from app.handler.base import BaseHandler
from app.business.agreement import agreement_bll


class agreement_detail(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.agreement = agreement_bll()

    @tornado.web.authenticated
    def get(self):
        agreement = self.agreement.get_detail()

        self.render('agreement/detail.html', agreement=agreement)

    @tornado.web.authenticated
    def post(self):
        summary = self.get_argument('summary', '')

        ret = self.agreement.update(summary)
        print(ret)
        self.write_json(ret)
