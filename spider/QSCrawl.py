# coding:utf-8

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: QSCrawl.py
@time: 2017/12/11 14:12
"""
# !/usr/bin/python
# -*-coding:utf-8-*-

"""
@author: smartgang

@contact: zhangxingang92@qq.com

@file: qs_crawl.py

@time: 2017/11/30 17:29
"""
import urllib
import urllib2
import re
import hashlib
from db.QSDataHelper import QSDataHelper


class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}| {6}')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n  ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class QSCrawl:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False
        self.dbhelper = QSDataHelper()
        self.dbhelper.create()
        self.dbindex = 0
        self.tool = Tool()

    def getPage(self, pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/page' + '/' +str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, why:
            if hasattr(why, "reason"):
                print u"连接糗事百科失败,错误原因", why.reason
                return None

    def getPageItem(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        # print pageCode
        if not pageCode:
            print u"页面加载失败......"
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?' +
                             '<div.*?class="articleGender.*?>(.*?)</div>.*?' +
                             '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?</div>.*?</a>.*?' +
                             '(.*?)<div class="stats.*?>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search("img", item[3])
            if not haveImg:
                pageStories.append([item[0].strip(), item[1].strip(), self.tool.replace(item[2].strip()), ''])
            else:
                pattern = re.compile('<img src="(.*?)".*?>', re.S)
                img = re.findall(pattern, item[3])
                pageStories.append([item[0].strip(), item[1].strip(), self.tool.replace(item[2].strip()), img[0]])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItem(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            self.loadPage()
            self.dbindex += 1
            hashcode = hashlib.md5(story[2].encode('utf-8')).hexdigest()
            data = [(self.dbindex, hashcode, story[0], story[2], story[3])]
            self.dbhelper.insert(data)

    def start(self):
        # print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        newPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                newPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, newPage)

if __name__ == '__main__':
    spider = QSCrawl()
    spider.start()
