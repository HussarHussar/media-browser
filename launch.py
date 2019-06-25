#! /usr/bin/python3
from PyQt5.QtWidgets import (QApplication, QLabel, QCheckBox, QRadioButton,
                             QMainWindow, QStyleFactory, QPushButton, QSlider,
                             QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextBrowser, QDialog, QGroupBox, QTabWidget,
                             QTextEdit)
from PyQt5.QtCore import Qt
import sys, urllib.request, requests

class DracoView(QMainWindow):

    def __init__(self, parent=None):
        super(DracoView, self).__init__(parent)
        self.makeTabs()
        self.setWindowTitle('Draco')
        return

    def makeTabs(self):
        self.tabWidget = QTabWidget()
        self.tab1 = QVBoxLayout()
        self.tab2 = QHBoxLayout()
        self.tab2.addWidget(QLabel("hello world"))

        self.makeSearchView()

        a = QWidget()
        a.setLayout(self.tab1)
        b = QWidget()
        b.setLayout(self.tab2)
        self.tabWidget.addTab(a, 'Search')
        self.tabWidget.addTab(b, 'Channels')
        self.setCentralWidget(self.tabWidget)
        return

    def makeSearchView(self):
        topLayout = QHBoxLayout()
        self.searchBox = QLineEdit()
        topLayout.addWidget(self.searchBox)
        searchbutton = QPushButton('Search')
        topLayout.addWidget(searchbutton)
        topLayout.setAlignment(Qt.AlignTop)

        a = QWidget()
        a.setLayout(topLayout)
        self.browser = QTextBrowser()

        self.tab1.addWidget(a)
        self.tab1.addWidget(self.browser)

        self.yt = YtInf(self)
        searchbutton.clicked.connect(self.yt.ytSearch)
        return

class YtInf:
#The interface for youtube navigation.
#It takes the QMainWindow class as a parameter in order to interact with the browser.

    def __init__(self, v):
        self.v = v
        return

    def ytSearch(self):
        s = 'https://www.youtube.com/results?search_query='
        s = s + self.v.searchBox.text()

        req = urllib.request.Request(s)
        response = urllib.request.urlopen(req)
        print(type(response))
        self.v.browser.setHtml(response.read().decode())

        return

if __name__ == '__main__':
    app = QApplication([])
    view = DracoView()
    view.show()
    sys.exit(app.exec_())
