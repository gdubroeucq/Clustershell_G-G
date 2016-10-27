#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/python2.7

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
import sys

import clustershell_IHM,configuration_IHM

class clustershell_IHM(QtGui.QMainWindow, clustershell_IHM.Ui_MainWindow):
    def __init__(self, parent=None):
        super(clustershell_IHM, self).__init__(parent)
        self.setupUi(self)
        #self.label.setText("test")

    def main(self):
        self.show()

class configuration_IHM(QtGui.QWidget, configuration_IHM.Ui_Form):
    def __init__(self, parent=None):
        super(configuration_IHM, self).__init__(parent)
        self.setupUi(self)

    def main(self):
        self.comboBox.addItem("start")
        self.comboBox.addItem("stop")
        self.comboBox.addItem("restart")
        self.comboBox.addItem("reload")
        self.show()


if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    clustershell_IHM = clustershell_IHM()
    configuration_IHM = configuration_IHM()

    @pyqtSlot()
    def on_click():
        #clustershell_IHM.label.setText("test")
        clustershell_IHM.listWidget.insertItem(1,"test")
        configuration_IHM.main()

    def on_click_add_service():
        service=configuration_IHM.lineEdit.text()
        noeuds=configuration_IHM.lineEdit_2.text()
        dependance=configuration_IHM.lineEdit_3.text()
        action=configuration_IHM.comboBox.currentText()
        if(service!="" and noeuds!="" and dependance!=""):
            configuration_IHM.listWidget.insertItem(1,"%s %s on %s (depend %s)"%(service,action,noeuds,dependance))
        if(service!="" and noeuds!="" and dependance==""):
            configuration_IHM.listWidget.insertItem(1,"%s %s on %s"%(service,action,noeuds))
        configuration_IHM.main()

    def on_click_delete_service():
        service_number=configuration_IHM.listWidget.currentRow()
        configuration_IHM.listWidget.takeItem(service_number)

    def close():
        configuration_IHM.close()


    #action boutons
    clustershell_IHM.pushButton.clicked.connect(on_click)

    configuration_IHM.pushButton.clicked.connect(on_click_add_service)
    configuration_IHM.pushButton_2.clicked.connect(on_click_delete_service)
    configuration_IHM.pushButton_3.clicked.connect(close)


    clustershell_IHM.main()
    app.exec_()


