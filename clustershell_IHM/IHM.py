#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/python2.7

from PyQt4 import QtGui, QtCore
import sys

import clustershell_IHM

class clustershell_IHM(QtGui.QMainWindow, clustershell_IHM.Ui_MainWindow):
    def __init__(self, parent=None):
        super(clustershell_IHM, self).__init__(parent)
        self.setupUi(self)

    def main(self):
        self.show()

if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    clustershell_IHM = clustershell_IHM()
    clustershell_IHM.main()
    app.exec_()
