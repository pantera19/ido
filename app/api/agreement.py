#! /usr/bin/env python
# -*- coding: utf-8 -*-

from base_handler import base_handler
from app.business.agreement import agreement_bll


class agreement_handler(base_handler):
    def __init__(self, application, request, **kwargs):
        base_handler.__init__(self, application, request, *kwargs)
        self.agreement = agreement_bll()

    def info(self):
        agreement = self.agreement.get_detail()
        return self.write_json(agreement)
