# coding=utf-8

import json
from tornado.util import ObjectDict
from data.mysqldb import mysql_read, mysql_write
from data.redisdb import redis_db
import MySQLdb


class BaseAccess(object):
    '''access的基类'''

    def __init__(self, table):
        '''
        构造函数
        '''
        self.mysql_read = mysql_read
        self.mysql_write = mysql_write
        self.redis_db = redis_db

        self.table = table

    # public
    def get_list(self, page=1, page_size=20):
        start = (page - 1) * page_size

        conditions = dict()
        order = dict(id='desc')
        limit = (start, page_size)

        return self._list(['*'], conditions, limit, order)

    # mysql

    def _get(self, field=['*'], conditions=None, order=None, in_=None, between=None, like=None):
        sql, params = self._select_sql(field, conditions, (0, 1), order, in_, between, like)
        return self.mysql_read.get(sql, *params)

    def _list(self, field=['*'], conditions=None, limit=None, order=None, in_=None, between=None, like=None):
        sql, params = self._select_sql(field, conditions, limit, order, in_, between, like)
        return self.mysql_read.query(sql, *params)

    def _count(self, conditions=None, order=None, in_=None, between=None, like=None):
        sql, params = self._select_sql(['count(0) as rows_count'], conditions, None, order, in_, between, like)

        return self.mysql_read.query(sql, *params)[0]['rows_count']

    def _select_sql(self, field=['*'], conditions=None, limit=None, order=None, in_=None, between=None, like=None):
        '''
        :param field_:
            field_name : string : default: [*] : [id,name,summary]
        :param conditions_:
            conditions : dict : {'id':1,'name':'pantera','summary':'this is a summary'}
        :param limit :
            limit : tuple : (0,100)
        :param order:
            order : dict :  {'id': 'asc','name':'desc'}
        :param in_:
            in_ : dict : {'id':[1,2,3]}
        :return: string,list : sql,params
        '''
        sql = []
        params = []
        sql.append('select %s' % ",".join(field))
        sql.append('from %s ' % self.table)

        if conditions or in_ or between or like:
            sql.append('where')

            if conditions:
                s, p = self._dict_2_str_and(conditions)
                sql.append(s)
                params.extend(p)
            if in_:
                s, p = self._dict_2_in(in_)
                sql.append(self._joint(sql) + s)
                params.extend(p)
            if between:
                s, p = self._dict_2_between(between)
                sql.append(self._joint(sql) + s)
                params.extend(p)
            if like:
                s, p = self._dict_2_like(like)
                sql.append(self._joint(sql) + s)
                params.extend(p)

        if order:
            s, p = self._dict_2_str_blank(order)
            sql.append(('order by %s ' % s) % tuple(p))

        if limit:
            sql.append('limit %s,%s')
            params.extend(list(limit))

        return ' '.join(sql), params

    def _insert(self, field_value):
        '''
        :param table:
            table_name : string
        :param field_value:
            key-field_value : dict : {'id':1,'name':'pantera','summary':'this is a summary'}
        :return:
            sql,params
        '''

        sql, params = [], []

        sql.append('insert into %s set' % self.table)
        s, p = self._dict_2_str(field_value)
        sql.append(s)
        params.extend(p)

        id = self.mysql_write.execute_lastrowid(' '.join(sql), *params)

        return True, id

    def _update(self, value, conditions=None):
        '''
        :param value: dict
        :param conditions: dict
        :return:
        '''

        id = conditions.get('id')
        sql, params = self._update_sql(value, conditions)
        self.mysql_write.execute_rowcount(sql, *params)

        return True, id

    def _update_status(self, id, status):
        sql, params = self._update_sql(dict(status=status), dict(id=id))

        self.mysql_write.execute_rowcount(sql, *params)

        return True

    def _update_sql(self, value, conditions=None):
        '''
        :param value: dict
        :param conditions: dict
        :return:
        '''

        sql, params = [], []

        sql.append('update %s set' % self.table)

        s, p = self._dict_2_str(value)
        sql.append(s)
        params.extend(p)

        if conditions:
            s, p = self._dict_2_str_and(conditions)
            sql.extend(['where', s])
            params.extend(p)

        return ' '.join(sql), params

    def _exists(self, conditions=None, in_=None, between=None, like=None):
        sql, params = self._select_sql(['count(0) as rows_count'], conditions, None, in_, between, like)

        return self.mysql_read.query(sql, *params)[0]['rows_count'] > 0

    def sql(self, sql, params=None):
        '''
        执行sql语句

        :param sql: sql语句
        :param params: 参数
        :return: 根据sql语句返回结果
        '''

        if params:
            return self.mysql_read.query(sql, *params)
        else:
            return self.mysql_read.query(sql)

    def _safe(self, s):
        return MySQLdb.escape_string(s)

    def _dict_2_str(self, dictin, eq='=', sep=','):
        '''
        :param dictin: dict : {'id':1,'name'='pantera'}
        :param eq: string : dict to 'key eq value' : id=1
        :param sep: string : dict to ' a sep b sep c ' : id=1,name='pantera'

        :return: string : id=1,name='pantera'
        '''

        tmps = []
        params = []
        for k, v in dictin.items():
            if v != None:
                tmp = " %s%s%s" % (str(k), eq, '%s')
                tmps.append(tmp)
                params.append(v)

        return sep.join(tmps), params

    def _dict_2_str_and(self, dictin):
        '''
        :return: string : id=1 and name='pantera'
        '''
        return self._dict_2_str(dictin, eq='=', sep=' and ')

    def _dict_2_str_blank(self, dictin):
        '''
        :return: string : id asc, name desc
        '''
        return self._dict_2_str(dictin, eq=' ', sep=',')

    def _dict_2_in(self, dictin):
        tmps = []
        params = []
        for k, v in dictin.items():
            tmp = '%s in (%s)'
            format_strings = ','.join(['%s'] * len(v))
            sql = tmp % (k, format_strings)
            tmps.append(sql)
            params.extend(v)

        return ' and '.join(tmps), params

    def _dict_2_between(self, dictin):
        tmps = []
        params = []
        for k, v in dictin.items():
            tmp = '%s between %s'
            format_strings = '%s and %s'
            sql = tmp % (k, format_strings)
            tmps.append(sql)
            params.extend(v)

        return ' and '.join(tmps), params

    def _dict_2_like(self, dictin):
        tmps = []
        params = []
        for k, v in dictin.items():
            tmp = '%s like %s'
            sql = tmp % (k, '%s')
            tmps.append(sql)
            params.append(v)

        return ' and '.join(tmps), params

    def _joint(self, list):
        for sl in list:
            if "%s" in sl:
                return 'and '

        return ''

    def get_wh(self, img_url):
        import urllib2
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

        img_url
        img_url += '?x-oss-process=image/info'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

        request = urllib2.Request(img_url, headers=headers)
        response = urllib2.urlopen(request)

        t = json.loads(response.read())
        return ObjectDict(t)
