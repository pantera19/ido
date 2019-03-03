# -*- coding:utf8 -*-

import tornado
import math

import xlwt
import StringIO

from app.handler.base import BaseHandler
from app.business.event import event_bll
from app.business.donation_record import donation_record_bll


class donation_record_list(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.donation_record = donation_record_bll()

    @tornado.web.authenticated
    def get(self):
        event_id = int(self.get_argument('event_id', '0'))

        page, page_size = self.get_page()
        donation_records = self.donation_record.get_all_by_event_id(event_id, page, page_size)
        count = self.donation_record.get_count_by_event_id(event_id)

        self.render('donation_record/donation_record_list.html', donation_records=donation_records, page=page,
                    page_size=page_size, page_count=int(math.ceil(count / float(page_size))), event_id=event_id)

    @tornado.web.authenticated
    def post(self):
        '''删除'''
        id = self.get_argument('id', '')
        status = int(self.get_argument('status', '0'))

        return self.write_json(self.donation_record.update_status(id, status))


class dr_excel(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.event = event_bll()
        self.donation_record = donation_record_bll()

    @tornado.web.authenticated
    def get(self):
        '''
        导出表单
        :return:
        '''

        event_id = 0
        rows = self.donation_record.get_all_by_event_id(event_id, 1, 10000)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=%s.xls' % (u'IDo捐赠活动'))

        title_tall_style = xlwt.easyxf('font:height 540;')  # 设置字体高度
        tall_style = xlwt.easyxf('font:height 460;')  # 设置字体高度

        wb = xlwt.Workbook()
        wb.encoding = 'gbk'
        ws = wb.add_sheet('sheet1')
        ws.write_merge(0, 0, 0, 7, unicode('IDo 捐赠活动'), title_style())

        one = ws.col(0)
        one.width = 256 * 7
        two = ws.col(1)
        two.width = 256 * 35
        thr = ws.col(2)
        thr.width = 256 * 14
        four = ws.col(3)
        four.width = 256 * 21
        four = ws.col(4)
        four.width = 256 * 14
        four = ws.col(5)
        four.width = 256 * 35
        four = ws.col(6)
        four.width = 256 * 35
        four = ws.col(7)
        four.width = 256 * 70

        ws.write(1, 0, u'序号', def_style(True))
        ws.write(1, 1, u'活动名称', def_style(True))
        ws.write(1, 2, u'捐赠档', def_style(True))
        ws.write(1, 3, u'捐赠者昵称', def_style(True))
        ws.write(1, 4, u'捐赠金额(元)', def_style(True))
        ws.write(1, 5, u'捐赠时间', def_style(True))
        ws.write(1, 6, u'回报物', def_style(True))
        ws.write(1, 7, u'邮寄信息', def_style(True))

        row_title = ws.row(0)
        row_title.set_style(title_tall_style)
        row0 = ws.row(1)
        row0.set_style(tall_style)

        i = 2

        for idx, row in enumerate(rows):
            ws.write(i, 0, idx + 1, def_style())
            ws.write(i, 1, row['event']['name'], def_style())
            ws.write(i, 2, row['event_option']['price'], def_style())
            ws.write(i, 3, row['user']['nickname'], def_style())
            ws.write(i, 4, row['price'], def_style())

            ws.write(i, 5, str(row['create_time']), def_style())
            ws.write(i, 6, row['gift']['name'] if row['gift'] else '-', def_style())
            if row['address']:
                addr = row['address']
                ws.write(i, 7, '%s %s,%s-%s-%s-%s ' % (
                    addr['name'], addr['phone'], addr['country'], addr['province'], addr['city'], addr['street']),
                         def_style())
            else:
                ws.write(i, 7, '', def_style())

            i += 1

        sio = StringIO.StringIO()
        wb.save(sio)

        self.write(sio.getvalue())
        self.finish()


def def_style(is_title=False):
    style = xlwt.XFStyle()

    # 设置边框
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    # 设置居中
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_TOP  # 垂直方向

    font = xlwt.Font()

    font.height = 12 * 20
    font.name = u'黑体'
    if is_title:
        font.bold = True
    style.font = font

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    style.alignment = alignment
    style.borders = borders

    return style


def title_style():
    style = xlwt.XFStyle()

    # 设置边框
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    # 设置居中
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_TOP  # 垂直方向

    font = xlwt.Font()
    font.name = u'黑体'

    font.height = 12 * 27
    font.bold = True
    style.font = font

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    style.alignment = alignment
    # style.borders = borders

    return style
