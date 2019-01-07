# coding:utf-8


from app.admin.admin import login, logout, change_password, dashboard
from app.admin.gift import gift_list, gift_detail
from app.admin.event import event_list, event_detail
from app.admin.event_option import event_option_list, event_option_detail
from app.admin.user import user_list

from app.admin.img import img_upload, img_delete

urls = [
    # 管理
    [r'/admin', dashboard],

    [r'/admin/login$', login],
    [r'/admin/logout$', logout],
    [r'/admin/change_password$', change_password],

    [r'/admin/gifts', gift_list],
    [r'/admin/gift', gift_detail],

    [r'/admin/events', event_list],
    [r'/admin/event', event_detail],

    [r'/admin/event/options', event_option_list],
    [r'/admin/event/option', event_option_detail],

    [r'/admin/users', user_list],
    [r'/admin/upload', img_upload],
    [r'/admin/img/del', img_delete],
]

from app.api.user import user_handler as user
from app.api.event import event_handler as event
from app.api.address import address_handler as address

api_url = [
    [r"/api/user/(.*)", user],
    [r"/api/event/(.*)", event],
    [r"/api/address/(.*)", address]
]

urls.extend(api_url)
