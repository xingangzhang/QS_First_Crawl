# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: config.py
@time: 2017/12/8 17:21
"""
import os

DB_CONFIG_FILE = os.path.dirname(__file__) + '/data/qs.db'
DB_CONFIG_TABLE = 'QS2'

urllist = [
    {
        'urls': ['https://www.qiushibaike.com/hot/%s' % n for n in ['page/'] + list(range(2, 14))]
    },
    {
        'urls': ['https://www.qiushibaike.com/8hr/%s' % n for n in ['page/'] + list(range(2, 14))]
    }
]

urlhot = 'https://www.qiushibaike.com/hot/'
