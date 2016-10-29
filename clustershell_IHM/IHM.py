#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from ClusterShell.Task import task_self, NodeSet
from cluster import clustershell,fichier,typeservice

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import sys

import clustershell_IHM,configuration_IHM


#class typeservice:
#    def __init__(self,nom,action,noeuds,dependance=""):
#        self.nom=nom
#        self.action=action
#        self.noeuds=noeuds
#        self.dependance=dependance

class clustershell_IHM(QtGui.QMainWindow, clustershell_IHM.Ui_MainWindow):
    list_service=[]
    def __init__(self, parent=None):
        super(clustershell_IHM, self).__init__(parent)
        self.setupUi(self)
        #self.label.setText("test")
        self.progressBar.hide()
    def main(self):
        self.show()

class configuration_IHM(QtGui.QWidget, configuration_IHM.Ui_Form):
    def __init__(self, parent=None):
        super(configuration_IHM, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.addItem("start")
        self.comboBox.addItem("stop")
        self.comboBox.addItem("restart")
        self.comboBox.addItem("reload")
    def main(self):
        self.show()





if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    clustershell_IHM = clustershell_IHM()
    configuration_IHM = configuration_IHM()

    #actions boutons
    @pyqtSlot()
    def config():
        configuration_IHM.lineEdit.clear()
        configuration_IHM.lineEdit_2.clear()
        configuration_IHM.lineEdit_3.clear()
        configuration_IHM.main()

    def on_click_add_service():
        ok=0        
        if(configuration_IHM.lineEdit.text()!=""):
            name=configuration_IHM.lineEdit.text()
            dependance=configuration_IHM.lineEdit_3.text()
            action=configuration_IHM.comboBox.currentText()
            if(configuration_IHM.lineEdit_2.text()!=""):
                try:
                    noeuds=configuration_IHM.lineEdit_2.text()
                    nodeset=NodeSet(str(noeuds))
                    ok=1
                except:
                    noeuds=""
                    QMessageBox.about(configuration_IHM,"Erreur","Syntaxe noeuds incorrect")
                if( ok==1 and name!="" and noeuds!="" and dependance!=""):
                    configuration_IHM.listWidget.addItem("%d: %s %s ON %s (depend %s)"%(configuration_IHM.listWidget.count()+1,name,action,noeuds,dependance))
                    clustershell_IHM.list_service.append(typeservice(name,action,noeuds,dependance))
                    print("c'est cool")
                if(ok==1 and name!="" and noeuds!="" and dependance==""):
                    configuration_IHM.listWidget.addItem("%d: %s %s ON %s"%(configuration_IHM.listWidget.count()+1,name,action,noeuds))
                    clustershell_IHM.list_service.append(typeservice(name,action,noeuds))
            else:
                QMessageBox.about(configuration_IHM,"Erreur","Attribut noeuds manquant")
        else:
            QMessageBox.about(configuration_IHM,"Erreur","Attribut service manquant")


    def on_click_delete_service():
        service_number=configuration_IHM.listWidget.currentRow()
        configuration_IHM.listWidget.takeItem(service_number)
        del clustershell_IHM.list_service[configuration_IHM.listWidget.currentRow()]


    def close():
        clustershell_IHM.label.setText("%d action(s)" % configuration_IHM.listWidget.count())
        if(configuration_IHM.listWidget.count()==0):
            clustershell_IHM.pushButton_2.setEnabled(False)
        else:
            clustershell_IHM.pushButton_2.setEnabled(True)
        configuration_IHM.close()

    def importer():
        if(fichier(clustershell_IHM,configuration_IHM)):
            print("OKKKKKKKKKKKKKKKKKK")
            print(clustershell_IHM.list_service[0])



    def lancer():
        clustershell_IHM.listWidget.clear()
        clustershell_IHM.progressBar.reset()
        clustershell_IHM.progressBar.update()
        clustershell_IHM.progressBar.show()
        for i in range(0,len(clustershell_IHM.list_service)):
            nom=clustershell_IHM.list_service[i].nom
            action=clustershell_IHM.list_service[i].action
            noeuds=clustershell_IHM.list_service[i].noeuds
            dependance=clustershell_IHM.list_service[i].dependance
            if(clustershell_IHM.list_service[i].dependance==""):
                #clustershell_IHM.listWidget.insertItem(clustershell_IHM.listWidget.count()+1,"%s %s ON %s" % (nom,action,noeuds))
                clustershell_IHM.listWidget.addItem("%s %s ON %s *********************************" % (nom,action,noeuds))
                print("%s %s ON %s *********************************" % (nom,action,noeuds))
            else:
                clustershell_IHM.listWidget.addItem("%s %s ON %s (depend: %s) ********************" % (nom,action,noeuds,dependance))
                print("%s %s ON %s (depend: %s) ********************" % (nom,action,noeuds,dependance))


            clustershell(clustershell_IHM,clustershell_IHM.list_service,i)
            clustershell_IHM.progressBar.setValue((100/(len(clustershell_IHM.list_service))*(i+1)))
            clustershell_IHM.progressBar.update()
        clustershell_IHM.progressBar.setValue(100)
        clustershell_IHM.progressBar.update()




    #signaux
    clustershell_IHM.pushButton.clicked.connect(config)
    clustershell_IHM.pushButton_2.clicked.connect(lancer)

    configuration_IHM.pushButton.clicked.connect(on_click_add_service)
    configuration_IHM.pushButton_2.clicked.connect(on_click_delete_service)
    configuration_IHM.pushButton_3.clicked.connect(close)
    configuration_IHM.pushButton_4.clicked.connect(importer)


    clustershell_IHM.main()
    app.exec_()


