# -*- coding:utf8 -*-

import logging
import xmltodict
import time
import random
import string

import base64
import json

from Crypto.Cipher import AES
import requests
import hashlib
import urllib3

import config
from data.redisdb import redis_db

urllib3.disable_warnings()


class wechat(object):

    def __init__(self, app_id, app_secret, mch_id, mch_key):
        self.app_id = app_id
        self.app_secret = app_secret
        self.mch_id = mch_id
        self.mch_key = mch_key
        self.redis_db = redis_db

    def exchange_code_for_session_key(self, code):
        req_params = {
            "appid": self.app_id,
            "secret": self.app_secret,
            "js_code": code,
            "grant_type": 'authorization_code'
        }
        req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                                  params=req_params, timeout=3, verify=False)

        ret = req_result.json()
        return ret

    def get_wx_access_token(self, app_id, app_secret, key='wx:access_token'):

        rds = self.redis_db

        if not rds.exists(key):
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
            params = {'appid': app_id, 'secret': app_secret}

            data = requests.get(url, params)
            html = data.json()

            if html.get('access_token'):
                rds.set(key, html['access_token'])
                rds.expire(key, 7180)

        return rds.get(key)

    def decrypt(self, encryptedData, iv, sessionKey):
        # base64 decode
        sessionKey = base64.b64decode(sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.app_id:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    # -----------微信支付
    # 生成nonce_str
    def generate_randomStr(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 32))

    # 生成签名
    def getSign(self, param):
        # 计算签名
        stringA = '&'.join(["{0}={1}".format(k, param.get(k)) for k in sorted(param)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.mch_key)
        sign = hashlib.md5(stringSignTemp).hexdigest()

        return sign

    def getxml(self, kwargs):

        kwargs['sign'] = self.getSign(kwargs)

        # 生成xml
        xml = ''
        for key, value in kwargs.items():
            if key == 'sign':

                xml += '<{0}>{1}</{0}>'.format(key, value)
            else:
                xml += '<{0}><![CDATA[{1}]]></{0}>'.format(key, value)

        xml = '<xml>{0}</xml>'.format(xml)

        # print(xml)
        return xml

    def get_generate_bill_xml(self, out_trade_no, fee, openid):
        nonce_str = self.generate_randomStr()

        import collections
        dic = collections.OrderedDict()
        dic['appid'] = self.app_id
        dic['body'] = '卡尺改装-活动报名费'
        dic['mch_id'] = self.mch_id
        dic['notify_url'] = 'https://api.cars04.com/cars04/event/wx_notify'
        dic['nonce_str'] = nonce_str
        dic['out_trade_no'] = out_trade_no
        dic['openid'] = openid
        dic['spbill_create_ip'] = '47.15.75.2'
        dic['total_fee'] = fee
        dic['trade_type'] = 'JSAPI'

        xml = self.getxml(dic)

        resp = requests.post("https://api.mch.weixin.qq.com/pay/unifiedorder", data=xml.encode('utf-8'),
                             headers={'Content-Type': 'application/xml'})
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xmlresp = xmltodict.parse(msg)

        return xmlresp

    def generate_bill(self, out_trade_no, fee, openid):

        xmlresp = self.get_generate_bill_xml(out_trade_no, fee, openid)

        if xmlresp['xml']['return_code'] == 'SUCCESS':
            if xmlresp['xml']['result_code'] == 'SUCCESS':

                timestamp = str(int(time.time()))
                data = dict(appId=self.app_id,
                            nonceStr=self.generate_randomStr(),
                            package="prepay_id=" + xmlresp['xml']['prepay_id'],
                            signType="MD5",
                            timeStamp=timestamp)

                data['paySign'] = self.getSign(data)
                data['orderid'] = out_trade_no  # 付款后操作的订单
                data['prepay_id'] = xmlresp['xml']['prepay_id']
                # 签名后返回给前端做支付参数
                return data
            else:
                msg = xmlresp['xml']['err_code_des']
                return msg
        else:
            msg = xmlresp['xml']['return_msg']
            return msg

    def close_bill(self, out_trade_no):
        nonce_str = self.generate_randomStr()

        import collections
        dic = collections.OrderedDict()
        dic['appid'] = self.app_id
        dic['mch_id'] = self.mch_id
        dic['nonce_str'] = nonce_str
        dic['out_trade_no'] = out_trade_no

        xml = self.getxml(dic)

        resp = requests.post("https://api.mch.weixin.qq.com/pay/closeorder", data=xml.encode('utf-8'),
                             headers={'Content-Type': 'application/xml'})
        msg = resp.text.encode('ISO-8859-1').decode('utf-8')
        xmlresp = xmltodict.parse(msg)

        return True

    def check_wx_notify_url_data(self, str_xml):
        '''校验微信回调 url 数据 是否安全'''
        xmlresp = xmltodict.parse(str_xml)

        if xmlresp['xml']['return_code'] == 'SUCCESS':
            if xmlresp['xml']['result_code'] == 'SUCCESS':
                if xmlresp['xml']['appid'] == self.app_id and xmlresp['xml']['mch_id'] == self.mch_id:
                    return dict(code=1, order_id=xmlresp['xml']['out_trade_no'])
                else:
                    return dict(code=0, msg='FORBIDDEN')
            else:
                msg = xmlresp['xml']['err_code_des']
                logging.error(msg)
                return dict(code=0, msg=msg)
        else:
            msg = xmlresp['xml']['return_msg']
            logging.error(msg)
            return dict(code=0, msg=msg)


wx = wechat(**config.minip)
