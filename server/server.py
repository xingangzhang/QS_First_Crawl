# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: server.py
@time: 2017/12/18 18:30
"""
import web
import sys
from db.QSDataHelper import qs
import json

urls = (
    '/(.*)', 'select'
)


class select(object):

    def GET(self, name):
        inputs = web.input()
        print inputs
        json_result = json.dumps(qs.get_a_item(), ensure_ascii=False)
        return json_result


if __name__ == "__main__":
    # sys.argv.append('0.0.0.0:8000')
    app = web.application(urls, globals())
    app.run()
