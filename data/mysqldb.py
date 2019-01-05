# -*- coding:utf8 -*-

import torndb
import config

mysql_write = torndb.Connection(**config.mysql_write)
mysql_read = torndb.Connection(**config.mysql_read)
