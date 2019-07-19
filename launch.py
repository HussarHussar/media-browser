#! /usr/bin/python3
from PyQt5.QtWidgets import (QApplication, QLabel,
                             QMainWindow, QStyleFactory, QPushButton, QSlider,
                             QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
                             QDialog, QGroupBox, QTabWidget,
                             QListWidgetItem, QGridLayout, QTextEdit,
                             QListWidget, QScrollArea, QStatusBar, QComboBox,
                             QTextBrowser, QStackedWidget, QToolBar,
                             QProgressBar)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal)
from PyQt5.QtGui import QIcon
import sys, requests, youtube_dl, subprocess
from resources import contentdata

class MediaBrowser(QMainWindow):
    """
    The main window.
    Attributes accessible to all functions are: searchSelector, state

    state: states Stores important properties of the window in a State class.
    state.states is an array of SearchState classes with attributes for
    the current search methods. A SearchState class is created for each search
    method.
    """

    def __init__(self, parent=None):
        super(MediaBrowser, self).__init__(parent)
        self.makeItems()
        self.setWindowTitle('Media Browser')
        self.resize(900, 700)
        return

    def makeItems(self):
        self.statusBar().showMessage('Welcome')
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(QIcon.fromTheme('list-add'), 'URL')

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
        #Later this should also add all of the interfaces listed in the config
        #class by comparing their names to modules in the 'interfaces' folder
        self.state = State()
        yt = contentdata.YtInf(self, 0)
        self.state.addInterface(yt)
        self.state.setSearchFunc(yt.getPage)

        topLayout = QHBoxLayout()
        self.tab1.addLayout(topLayout, 1, 0, 1, 2)
        self.searchSelector = QComboBox()
        self.searchBox = QLineEdit()
        topLayout.addWidget(self.searchSelector)
        topLayout.addWidget(self.searchBox)

        searchButton = QPushButton('Search')
        topLayout.addWidget(searchButton)
        searchButton.clicked.connect(self.state.searchFunc)
        #Setup navigator
        #self.navigator.setMaximumWidth(100)
        self.searchSelector.addItem('Youtube')
        #self.searchResults = QScrollArea()
        self.searchResults = self.makeResultStack()
        self.tab1.addWidget(self.searchResults, 2, 1)

        self.vidInfoPanel = QTextBrowser()
        self.vidInfoPanel.setMaximumWidth(200)
        self.tab1.addWidget(self.vidInfoPanel, 2,0)
        topLayout.setAlignment(Qt.AlignTop)

        #Should be determined with configs. All views should be created and the same time and chosen from QStackedWidget according to config. https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm
        self.makeYtView()
        return

    def makeResultStack(self):
        stack = QStackedWidget()
       # refresh = QPushButton()
       # refresh.setIcon(QIcon.fromTheme('view-refresh'))
       # stack.addWidget(refresh)

        for i in self.state.interfaces:
            s = QScrollArea()
            stack.addWidget(s)
        return stack

    def switchIntf(self):
        """
        This would be called when a different interface is selected to switch
        the current scrollWidget in the results
        """
        return

    def makeYtView(self):
        #a = QWidget()
        #a.setLayout(topLayout)

        self.searchBox.setFocus()
        self.searchBox.returnPressed.connect(self.state.interfaces[0].getPage)
        return

    def startSearch(self):
        """
        Calls the method that the attribute searchFunc of state refers to.
        """
        self.state.searchFunc()
        return

    def makeResults(self, blocks, index):
        resultLayout = QVBoxLayout()
        w = QWidget()

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

        w.setLayout(resultLayout)
        #s.setAlignment(Qt.AlignTop)
        self.searchResults.widget(index).setWidget(w)
        #s.setMaximumSize(600, 400)
        return

    def playVideo(self, link):
        self.statusBar().showMessage('playing video...')
        vid = VidWorker()
        self.vids.append(vid)
        vid.load(link)
        vid.start()
        return

class State:

    def __init__(self):
        self.interfaces = []
        return

    def addInterface(self, inf):
        self.interfaces.append(inf)

    def setSearchFunc(self, s):
        self.searchFunc = s

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

if __name__ == '__main__':
    app = QApplication([])
    view = MediaBrowser()
    view.show()
    sys.exit(app.exec_())
