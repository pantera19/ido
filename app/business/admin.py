# coding=utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from bass_access import BaseAccess

_table = 'ido.admin'


class admin_bll(BaseAccess):
    def __init__(self):
        BaseAccess.__init__(self, _table)

    def add(self, username, password, role=0):
        password = generate_password_hash(password, salt_length=16)

        return self._insert(dict(id=1, username=username, password=password, role=role), cache=False)

    def update(self, id, password, role):
        password = generate_password_hash(password, salt_length=16)
        return self._update(dict(password=password, role=role), dict(id=id), cache=False)

    def is_login(self, user_name, password):
        '''
        首先通过user_name查询用户
        然后用所查询用户的密码与写入密码进行校验

        :param user_name: 用户名
        :param password: 密码
        :return: 验证结果，用户基本信息
        '''

        user = self._get(conditions=dict(status=1, username=user_name))

        ret = None
        if user:
            ret = check_password_hash(user['password'], password)
            user = {'id': user['id'], 'user_name': user['username'], 'role': user['role']}

        return ret, user

    def change_password(self, user_id, old_password, new_password):
        '''
        首先通过user_name查询用户
        然后查询原始密码与用户密码是否校验通过
        如果校验通过，则修改密码为悉尼米啊

        :param user_id: 用户id
        :param old_password: 旧密码
        :param new_password: 新密码
        :return: 是否修改成功
        '''

        user = self._get(conditions=dict(status=1, id=user_id))

        ret = False
        if user:
            if check_password_hash(user['password'], old_password):
                password = generate_password_hash(new_password, salt_length=16)

                self._update(dict(password=password), dict(id=user['id']))
                ret = True

        return ret
