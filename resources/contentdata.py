#!/usr/bin/python3

from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import requests

class YtInf():
#The interface for youtube navigation.
#It takes the QMainWindow class as a parameter in order to interact with the browser.

    def __init__(self, v):
        self.v = v
        return

    def getPage(self):
        s = 'https://www.youtube.com/results?search_query='
        search = self.v.searchBox.text()
      #  m = netMessenger()
      #  m.load(s+search, self.v.browser.setHtml)
      #  m.moveToThread(self.v.thread)
      #  m.go()
        self.v.t = NetWorker()
        self.v.t.writing.connect(self.pullData)
        self.v.t.load(s+search)
        self.v.t.start()
        return

    def updateBrowser(self, s):
        a = s.partition('<title>')[1] + s.partition('<title>')[2]
        print(a)
        self.v.browser.setHtml(a)
        return

#This will need to be async.
    def pullData(self, text):
        soup = BeautifulSoup(text)
        ids = []
        titles = []
        blocks = []
        s = soup.find_all(self.findTags)
        for tag in s:
            ids.append(tag.get('data-context-item-id'))
            titles.append(self.findTitle(tag))

        n = 0
        for i in ids:
            blocks.append(self.buildBlock(i, titles[n]))
            n = n + 1

        self.pushData(blocks)
        return

    def pushData(self, blocks):
        self.v.makeResults(blocks)
        return

#findTags updates the global ids and titles (calling findTitle), then returns
#all div tags which contained the ids
    def findTags(self, tag):
        if tag.name == 'div' and tag.has_attr('data-context-item-id'):
            id_ = str(tag.get('data-context-item-id'))
            print('found ' + (id_))
            return True
        return False

    def buildBlock(self, i, title):
        b = ContentBlock(i, title)
        return b

    def findTitle(self, tag):
        t = tag.find_all(self.a_has_title)
        t = str(t[0].get('title'))
        print('found title ' + t)
        return t

    def a_has_title(self, tag):
        return tag.name == 'a' and tag.has_attr('title')

class NetWorker(QThread):
    writing = pyqtSignal(str)

    def __init__(self):
        super(NetWorker, self).__init__()
        return

    def load(self, location):
        self.location = location
        return

    def run(self):
        r = requests.get(self.location)
        self.writing.emit(r.text)
        self.quit()
        return

class ContentBlock():

    def __init__(self, i, title):
        self.i = str(i)
        self.title = str(title)
        self.link = 'https://www.youtube.com/watch?v=' + i
        self.img_link = 'https://i.ytimg.com/vi/' + i + '/hqdefault.jpg'
        return
    description = ''
    image = 0
    title = ''
