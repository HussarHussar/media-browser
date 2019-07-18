#! /usr/bin/python3
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QMainWindow, QStyleFactory, QPushButton, QSlider,
                             QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
                             QDialog, QGroupBox, QTabWidget,
                             QListWidgetItem, QGridLayout, QTextEdit,
                             QListWidget, QScrollArea)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal)
from PyQt5.QtGui import QIcon
import sys, requests, youtube_dl, subprocess
from resources import contentdata

class MediaBrowser(QMainWindow):

    def __init__(self, parent=None):
        super(MediaBrowser, self).__init__(parent)
        self.makeItems()
        self.setWindowTitle('Media Browser')
        self.resize(600, 400)
        return

    def makeItems(self):
        #More things should be added here in UX branch
        self.vids = []
        self.makeTabs()
        self.config = Configs(self)
        return

    def makeTabs(self):
        self.tabWidget = QTabWidget()
        self.tab1 = QGridLayout()
        self.tab2 = QHBoxLayout()
        self.tab3 = QVBoxLayout()
        self.tab2.addWidget(QLabel("hello world"))
        self.tab3.addWidget(QLabel("coming soon..."))

        self.makeSearchView()

        a = QWidget()
        a.setLayout(self.tab1)
        b = QWidget()
        b.setLayout(self.tab2)
        c = QWidget()
        c.setLayout(self.tab3)
        self.tabWidget.addTab(a, 'Search')
        self.tabWidget.addTab(b, 'Channels')
        self.tabWidget.addTab(c, 'Videos') #Split into 'playing' and 'Downloading' lists
        self.setCentralWidget(self.tabWidget)
        return

    def makeSearchView(self):
        #Setup navigator
        self.navigator = QListWidget()
        self.navigator.setMaximumWidth(100)
        QListWidgetItem('Youtube', self.navigator)
        self.searchResults = QScrollArea()
        self.tab1.addWidget(self.searchResults, 2, 1)

        #Should be determined with configs. All views should be created and the same time and chosen from QStackedWidget according to config. https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
        self.makeYtView()
        self.tab1.addWidget(self.navigator, 2,0)
        return

    def makeYtView(self):
        topLayout = QHBoxLayout()
        self.searchBox = QLineEdit()
        topLayout.addWidget(self.searchBox)
        searchButton = QPushButton('Search')
        topLayout.addWidget(searchButton)

        #a = QWidget()
        #a.setLayout(topLayout)
        self.tab1.addLayout(topLayout, 1, 0, 1, 2)
        topLayout.setAlignment(Qt.AlignTop)

        self.yt = contentdata.YtInf(self)
        searchButton.clicked.connect(self.yt.getPage)
        self.searchBox.setFocus()
        self.searchBox.returnPressed.connect(self.yt.getPage)
        return

    def makeResults(self, blocks):
        resultLayout = QVBoxLayout()
        w = QWidget()
        n = 0

        for b in blocks:
            bl = QHBoxLayout()
            element = QWidget()
            pb = PButton(self, b.link)
            db = DButton(self, b.link)

            if len(b.title) > self.config.titleMaxSize:
                m = self.config.titleMaxSize - 5
                b.title = b.title[0:m] + '...'

            bl.addWidget(QLabel(b.title))
            bl.addWidget(db)
            bl.addWidget(pb)
            element.setLayout(bl)
            resultLayout.addWidget(element)
            n = n + 1
            print(n)

        w.setLayout(resultLayout)
        #s.setAlignment(Qt.AlignTop)
        self.searchResults.setWidget(w)
        #s.setMaximumSize(600, 400)
        return

    def playVideo(self, link):
        print('playing video...')
        vid = VidWorker()
        self.vids.append(vid)
        vid.load(link)
        vid.start()
        return

class VidWorker(QThread):
    writing = pyqtSignal(str)

    def __init__(self):
        super(VidWorker, self).__init__()
        return

    def load(self, link):
        self.link = link
        return

    def run(self):
        subprocess.run(['mpv', self.link])
        print('Done')
        self.quit()
        return

class PButton(QPushButton):

    def __init__(self, v, link):
        super().__init__('')
        self.link = link
        self.v = v
        self.setIcon(QIcon.fromTheme('media-playback-start'))
        self.setFixedWidth(30)
        self.clicked.connect(self.play)
        return

    def play(self):
        self.v.playVideo(self.link)
        return

class DButton(QPushButton):

    def __init__(self, v, link):
        super().__init__('')
        self.link = link
        self.setIcon(QIcon.fromTheme('document-save'))
        self.setFixedWidth(30)
        self.clicked.connect(self.download)
        return

    def download(self):
        return

class Configs:
    #This class should be more refined later
    #With reading and writing from a config file

    def __init__(self, v):
        #Max title size should not be lower than 6
        self.titleMaxSize = 60
        return


#class netMessenger(QObject):
#    #This class is used as a messenger to carry actions for the QThread
#    #instance spawned by interfaces
#   Could be used again later for playing videos asyncronously instead of
#   spawning a new thread for every video
#
#    done = pyqtSignal()
#
#    def __init__(self):
#        super(netMessenger, self).__init__()
#        return
#
#    def load(self, location, x):
#        self.location = location
#        self.x = x
#        return
#
#    def go(self):
#        r = requests.get(self.location)
#        self.x(r.text)
#        return
#
if __name__ == '__main__':
    app = QApplication([])
    view = MediaBrowser()
    view.show()
    sys.exit(app.exec_())
