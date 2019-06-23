#! /usr/bin/python3
from PyQt5.QtWidgets import (QApplication, QLabel, QCheckBox, QRadioButton,
QStyleFactory, QPushButton, QSlider, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QGroupBox, QTabWidget)

import sys

class DracoView(QDialog):

    def __init__(self, parent=None):
        super(DracoView, self).__init__(parent)
        self.makeTabs()
        self.setWindowTitle('Draco')
        return

    def makeTabs(self):
        self.tabWidget = QTabWidget()
        self.tab1 = QVBoxLayout()
        self.makeSearchView()
        self.tab2 = QHBoxLayout()
        self.tab2.addWidget(QLabel("hello world"))

        a = QWidget()
        a.setLayout(self.tab1)
        b = QWidget()
        b.setLayout(self.tab2)
        self.tabWidget.addTab(a, 'Search')
        self.tabWidget.addTab(b, 'Channels')
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)
        self.setLayout(self.mainLayout)
        return

    def makeSearchView(self):
        topLayout = QHBoxLayout()
        a = QLineEdit()
        topLayout.addWidget(a)
        topLayout.addWidget(QPushButton('Search'))

        b = QWidget()
        b.setLayout(topLayout)
        self.tab1.addWidget(b)
        return

    def ytSearch():

        return

if __name__ == '__main__':
    app = QApplication([])
    view = DracoView()
    view.show()
    sys.exit(app.exec_())
