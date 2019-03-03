# -*- coding:utf8 -*-

from bass_access import BaseAccess
from collections import defaultdict

from app.business.event import event_bll
from app.business.event_option import event_option_bll
from app.business.gift import gift_bll
from app.business.user import user_bll
from app.business.address import address_bll
from PIL import Image, ImageDraw, ImageFont
import os
from StringIO import StringIO
from urllib2 import urlopen
import io


_table = 'ido.donation_record'


class donation_record_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)
        self.event = event_bll()
        self.event_option = event_option_bll()
        self.gift = gift_bll()
        self.user = user_bll()
        self.address = address_bll()

    def get_all(self, user_id):
        conditions = dict(status=1, user_id=user_id)
        order = dict(id='desc')
        rows = self._list(['*'], conditions, order=order)

        for row in rows:
            row['price'] /= float(100)
            row['event'] = self.event.get_detail(row['event_id'])

        return rows

    def get_all_by_event_id(self, event_id, page=1, page_size=20):
        start = (page - 1) * page_size

        conditions = dict(status=1)

        if event_id > 0:
            conditions['event_id'] = event_id

        order = dict(id='desc')
        limit = (start, page_size)
        rows = self._list(['order_number'], conditions, limit, order)

        _rows = []
        for row in rows:
            _rows.append(self.get_detail_by_order_number(row['order_number'], all=True))
        return _rows

    def get_count_by_event_id(self, event_id):

        conditions = dict(status=1)

        if event_id > 0:
            conditions['event_id'] = event_id
        count = self._count(conditions)
        return count

    def get_pic_by_order_number(self, order_number):

        def get_top_cover(cover):
            c = cover.split('/')

            cover = os.path.join(os.path.dirname(__file__), "../../static/upload/" + c[-2], c[-1])

            ima = Image.open(cover).convert("RGBA")
            ima = ima.resize((405, 325))

            return ima

        def get_logo():
            cover_c = os.path.join(os.path.dirname(__file__), "../../static/upload", 'ido_logo.png')
            # 头像
            ima = Image.open(cover_c).convert("RGBA")
            ima = ima.resize((100, 100))

            return ima

        def get_cover(cover):
            c = cover.split('/')

            cover = os.path.join(os.path.dirname(__file__), "../../static/upload/" + c[-2], c[-1])
            cover_c = os.path.join(os.path.dirname(__file__), "../../static/upload", 'ido_user_c.png')

            # 圆圈
            cir_ima = Image.open(cover_c).convert("RGBA")
            cir_ima = cir_ima.resize((161, 161))

            # 头像
            ima = Image.open(cover).convert("RGBA")
            ima = ima.resize((159, 159))

            r, g, b, a = cir_ima.split()
            ima.paste(cir_ima, (-1, -1), mask=a)

            # 剪裁至圆形
            size = ima.size

            r2 = min(size[0], size[1])
            if size[0] != size[1]:
                ima = ima.resize((r2, r2), Image.ANTIALIAS)

            circle = Image.new('L', (r2, r2), 0)

            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, r2, r2), fill=255)
            alpha = Image.new('L', (r2, r2), 255)
            alpha.paste(circle, (0, 0))

            ima.putalpha(alpha)
            x = 80
            code_image = ima.resize((x, x))
            return code_image

        def get_bg(name, theme, order_number):

            bg_url = os.path.join(os.path.dirname(__file__), "../../static/upload", 'ido_bg.png')
            bg_image = Image.open(bg_url)

            font_url = os.path.join(os.path.dirname(__file__), "../../static/upload", 'PingFang.ttc')
            font1 = ImageFont.truetype(font_url, 26)
            font2 = ImageFont.truetype(font_url, 16)
            font3 = ImageFont.truetype(font_url, 14)

            color1, color2 = '#333', '#969696'

            draw = ImageDraw.Draw(bg_image)

            draw.text((55, 475), unicode('我是 %s' % name), font=font1, fill=color1)
            draw.text((55, 510), u'付出，是我热爱生活的方式', font=font1, fill=color1)
            draw.text((55, 555), unicode('#%s#' % theme), font=font2, fill=color2)
            draw.text((55, 582), u'捐款单号： %s' % order_number, font=font2, fill=color2)
            draw.text((175, 687), u'长按识别二维码', font=font3, fill=color2)
            draw.text((175, 715), u'为梦想助力', font=font3, fill=color2)

            return bg_image

        def drawLine(im, width, height):
            '''
            在图片上绘制矩形图
            :param im: 图片
            :param width: 矩形宽占比
            :param height: 矩形高占比
            :return:
            '''
            draw = ImageDraw.Draw(im)
            image_width = im.size[0]
            image_height = im.size[1]
            line_width = im.size[0] * width
            line_height = im.size[1] * height

            draw.line(
                ((image_width - line_width) / 2, (image_height - line_height) / 2,
                 (image_width + line_width) / 2, (image_height - line_height) / 2),
                fill=(253, 182, 197))
            draw.line(
                ((image_width - line_width) / 2, (image_height - line_height) / 2 - 1,
                 (image_width + line_width) / 2, (image_height - line_height) / 2 - 1),
                fill=(253, 182, 197))

            draw.line(
                ((image_width - line_width) / 2, (image_height - line_height) / 2,
                 (image_width - line_width) / 2, (image_height + line_height) / 2),
                fill=(253, 182, 197))

            draw.line(
                ((image_width - line_width) / 2 - 1, (image_height - line_height) / 2 - 1,
                 (image_width - line_width) / 2 - 1, (image_height + line_height) / 2 + 1),
                fill=(253, 182, 197))

            draw.line(
                ((image_width + line_width) / 2, (image_height - line_height) / 2,
                 (image_width + line_width) / 2, (image_height + line_height) / 2),
                fill=(253, 182, 197))

            draw.line(
                ((image_width + line_width) / 2 + 1, (image_height - line_height) / 2 - 1,
                 (image_width + line_width) / 2 + 1, (image_height + line_height) / 2 + 1),
                fill=(253, 182, 197))

            draw.line(
                ((image_width - line_width) / 2, (image_height + line_height) / 2,
                 (image_width + line_width) / 2, (image_height + line_height) / 2),
                fill=(253, 182, 197))
            draw.line(
                ((image_width - line_width) / 2, (image_height + line_height) / 2 + 1,
                 (image_width + line_width) / 2, (image_height + line_height) / 2 + 1),
                fill=(253, 182, 197))
            del draw

        cert = self.get_detail_by_order_number(order_number, all=True)

        # order_number 单号
        if cert:
            if cert.event:
                theme = cert.event['theme']  # 主题
            if cert.user:
                nickname = cert.user['nickname']
                user_cover = cert.user['avatar']

            cert_pic = cert['cert_pic']

        bg_cover = get_bg(nickname, theme, order_number)
        cover = get_cover(user_cover)
        sr, g, b, a = cover.split()
        bg_cover.paste(cover, (55, 375), mask=a)

        logo = get_logo()
        sr, g, b, a = logo.split()
        bg_cover.paste(logo, (350, 655), mask=a)

        top_cover = get_top_cover(cert_pic)
        sr, g, b, a = top_cover.split()
        bg_cover.paste(top_cover, (45, 45), mask=a)

        drawLine(bg_cover, 0.9, 0.95)

        dirs = './static/certificate'
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        file = open(dirs + "/certificate_%s.jpg" % order_number, 'w+')  # 以写方式打开一个文件

        stream = StringIO()
        bg_cover.save(stream, 'PNG')
        data = stream.getvalue()


        file.write(data)
        file.close()

        pic = 'http://localhost:7878/static/certificate/certificate_%s.jpg' % order_number

        return pic

    def get_detail_by_order_number(self, order_number, status=-1, all=False):
        conditions = dict(order_number=order_number)
        if status != -1:
            conditions['status'] = status
        row = self._get(['*'], conditions)

        if row and all:
            row['user'] = self.user.get_detail(row['user_id'])
            row['price'] /= float(100)
            row['event'] = self.event.get_detail(row['event_id'])

            if row['event_option_id'] == 0:
                event_options = self.event_option.get_list(row['event_id'])
                prices = [int(eo['price'] * 100) for eo in event_options]
                idx = index_number(prices, row['price'] * 100)
                row['event_option'] = event_options[idx]
            else:
                row['event_option'] = self.event_option.get_detail(row['event_option_id'])

            row['gift'] = self.gift.get_detail(row['event_option']['gift_id'])

            row['address'] = None
            if row['gift']:
                row['address'] = self.address.get_detail_by_user_id(row['user_id'])

        return row

    def get_amount(self):
        conditions = dict(status=1)
        times = self._count(conditions)
        amount_ret = self.sql('select sum(price) as amount from ido.donation_record where status=1')
        amount = amount_ret[0]['amount'] / 100
        return amount, times

    def get_amount_by_user_id(self, user_id):
        conditions = dict(status=1, user_id=user_id)

        rows = self._list(['*'], conditions)

        amount = 0
        times_di = defaultdict(int)
        for row in rows:
            amount += row['price']
            times_di[row['event_id']] += 1

        if len(rows) > 0:
            amount /= float(100)
        times = len(times_di)
        return amount, times

    def add(self, user_id, event_id, event_option_id, gift_id, address_id, order_number, price, pay_order, pay_status,
            pay_data, pay_notify_data, status=0):
        params = locals()
        params.pop('self')

        pic = self.event.rand_pic(event_id)
        params['cert_pic'] = pic

        flag, id = self._insert(params)

        return flag, id

    def update_status(self, id, status=0):
        flag = self._update_status(id, status)

        return flag


def index_number(li, defaultnumber):
    select = defaultnumber - li[0]

    index = 0
    for i in range(1, len(li) - 1):
        select2 = defaultnumber - li[i]
        if abs(select) > abs(select2):
            select = select2
            index = i
    return index
