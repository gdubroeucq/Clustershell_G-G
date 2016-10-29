#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/python2.7

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
import sys

import clustershell_IHM,configuration_IHM,etatnoeud_IHM,check_noeud
from ClusterShell.Task import task_self, NodeSet

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

class etatnoeud_IHM(QtGui.QWidget, etatnoeud_IHM.Ui_Form):
    def __init__(self, parent=None):
        super(etatnoeud_IHM, self).__init__(parent)
        self.setupUi(self)

    def main(self):
        self.show()



if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    clustershell_IHM = clustershell_IHM()
    configuration_IHM = configuration_IHM()
    etatnoeud_IHM = etatnoeud_IHM()


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

    def on_click_ouvre_etat():
        etatnoeud_IHM.main()

    def check_etat_noeud():
        etatnoeud_IHM.listWidget.clear()

        i = 1
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Erreur")
        noeuds = etatnoeud_IHM.lineEdit.text()
        if (noeuds!=""):
            try:
                nodeset = NodeSet(str(noeuds))
                msg.setWindowTitle("Information des noeuds")
                msg.setText("Voici les résultats:")
                for node in nodeset:
                    cli = "echo Hello"
                    out=""
                    taske = task_self()
                    taske.shell(cli, nodes=node)
                    taske.run()

                    for output, nodelist in task_self().iter_buffers():
                        if(output=="Hello"):
                            etatnoeud_IHM.listWidget.insertItem(i,"%s: OK" % nodelist)
                            i = i + 1
                            print "%s: OK" % nodelist

                        else:
                            etatnoeud_IHM.listWidget.insertItem(i,"%s: %s" % (nodelist,output))
                            i = i + 1
                            print "%s: %s" % (nodelist,output)


            except:
                print("Oups ! Problème de syntaxe")







        else:
            msg.setText("Veuillez rentrer un ou plusieur noeuds")
            msg.setDetailedText("node1,node2\nnode[1-5]\nnode1,node[5-6]\netc...")
            msg.exec_()

    def close_window_etat():
        etatnoeud_IHM.close()

    def open_file_browsers(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        filename = dlg.getOpenFileName(etatnoeud_IHM, 'Ouverture Fichier','/home/', 'File (*.yaml)')
        print filename




    def close():
        configuration_IHM.close()


    #action boutons
    clustershell_IHM.pushButton.clicked.connect(on_click)
    clustershell_IHM.pushButton_3.clicked.connect(on_click_ouvre_etat)
    configuration_IHM.pushButton.clicked.connect(on_click_add_service)
    configuration_IHM.pushButton_2.clicked.connect(on_click_delete_service)
    configuration_IHM.pushButton_3.clicked.connect(close)
    etatnoeud_IHM.pushButton_2.clicked.connect(close_window_etat)
    etatnoeud_IHM.pushButton_3.clicked.connect(open_file_browsers)
    etatnoeud_IHM.pushButton.clicked.connect(check_etat_noeud)


    clustershell_IHM.main()
    app.exec_()


