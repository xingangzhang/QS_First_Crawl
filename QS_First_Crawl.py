# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: QS_First_Crawl.py
@time: 2017/12/15 17:43
"""
from spider.QSCrawl import QSCrawl
if __name__ == "__main__":
    print "qs run"
    spider = QSCrawl()
    spider.initUrls()
    spider.start()
    print "qs exit"