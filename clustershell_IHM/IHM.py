#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/python2.7

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
import sys

import clustershell_IHM

class clustershell_IHM(QtGui.QMainWindow, clustershell_IHM.Ui_MainWindow):
    def __init__(self, parent=None):
        super(clustershell_IHM, self).__init__(parent)
        self.setupUi(self)
        #self.label.setText("test")

    def main(self):
        self.show()

if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    clustershell_IHM = clustershell_IHM()
    #clustershell_IHM.label.setText("test")
    @pyqtSlot()
    def on_click():
        #print('clicked')
        clustershell_IHM.label.setText("test")



    clustershell_IHM.pushButton.clicked.connect(on_click)
    clustershell_IHM.main()
    app.exec_()

    #Label=QLabel("wesh")
    #Label.show()
