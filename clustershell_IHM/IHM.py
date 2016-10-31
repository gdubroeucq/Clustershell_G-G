#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

from ClusterShell.Task import task_self, NodeSet
from cluster import clustershell,fichier,typeservice,recap_cluster,fichier2,check_service2,check_attribut2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import sys,datetime,os,yaml


import clustershell_IHM,configuration_IHM,etatnoeud_IHM,check_noeud
from ClusterShell.Task import task_self, NodeSet


class clustershell_IHM(QtGui.QMainWindow, clustershell_IHM.Ui_MainWindow):
    list_service=[]
    list_recap=[]
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

class etatnoeud_IHM(QtGui.QWidget, etatnoeud_IHM.Ui_Form):
    sortie = []
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


    #actions boutons
    @pyqtSlot()
    def config():
        configuration_IHM.lineEdit.clear()
        configuration_IHM.lineEdit_2.clear()
        configuration_IHM.lineEdit_3.clear()
        configuration_IHM.pushButton_2.setEnabled(False)
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
        configuration_IHM.pushButton_2.setEnabled(False)


    def on_click_ouvre_etat():
        etatnoeud_IHM.main()

    def check_etat_noeud():

        etatnoeud_IHM.listWidget.clear()
        etatnoeud_IHM.listWidget_2.clear()
        etatnoeud_IHM.listWidget_3.clear()

        i = 1
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Erreur")
        noeuds = etatnoeud_IHM.lineEdit.text()
        if (noeuds!=""):
            try:
                nodeset = NodeSet(str(noeuds))
                print nodeset
                for node in nodeset:
                    cli = "echo Hello"
                    taske = task_self()
                    taske.shell(cli, nodes=node)
                    taske.run()

                    for output, nodelist in task_self().iter_buffers():
                        if(output=="Hello"):

                            etatnoeud_IHM.listWidget.insertItem(i,"%s" % (NodeSet.fromlist(nodelist)))
                            i = i + 1

                        else:
                            etatnoeud_IHM.listWidget_2.insertItem(i,"%s" % (NodeSet.fromlist(nodelist)))
                            i = i + 1
                            etatnoeud_IHM.sortie.append(output)
                            print "output: %s" % output

            except:
                msg.setText("Oups ! Probleme")
                msg.exec_()

        else:
            msg.setText("Veuillez rentrer un ou plusieur noeuds")
            msg.setDetailedText("node1,node2\nnode[1-5]\nnode1,node[5-6]\netc...")
            msg.exec_()

    def close_window_etat():
        etatnoeud_IHM.close()

    def open_file_browsers():
        fichier2(etatnoeud_IHM)


    def on_item_clicked():
        index = etatnoeud_IHM.listWidget_2.currentRow()
        print "index: %s" % index
        etatnoeud_IHM.listWidget_3.clear()
        etatnoeud_IHM.listWidget_3.insertItem(1,str(etatnoeud_IHM.sortie[index]))

    def close():
        clustershell_IHM.label.setText("%d action(s)" % configuration_IHM.listWidget.count())
        if(configuration_IHM.listWidget.count()==0):
            clustershell_IHM.pushButton_2.setEnabled(False)
        else:
            clustershell_IHM.pushButton_2.setEnabled(True)
        configuration_IHM.close()

    def importer():
        fichier(clustershell_IHM,configuration_IHM)

    def lancer():
        del(clustershell_IHM.list_recap[:])
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

    def resultat():
        print("")
        if(len(clustershell_IHM.list_recap)>0):
            for b in clustershell_IHM.list_recap:
                if(b.resultat==1):
                    print("OK: [%s] %s: %s" % (b.nom,b.nom_split,b.noeuds))
                else:
                    if(b.type==1):
                        print("FAIL: [%s] %s: %s DEPENDANCE FAIL" % (b.nom,b.nom_split,b.noeuds))
                        print("Output: %s" % b.output)
                    elif(b.type==2):
                        print("FAIL: [%s] %s: %s SERVICE FAIL" % (b.nom,b.nom_split,b.noeuds))
                        print("Output: %s" % b.output)
                print("")
        date=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print type(date)
        if(len(clustershell_IHM.list_recap)>0):
            with open("log_%s" % date,'w') as fich:
                for b in clustershell_IHM.list_recap:
                    if(b.resultat==1):
                        print("OK: [%s] %s: %s" % (b.nom,b.nom_split,b.noeuds))
                        fich.write("OK: [%s] %s: %s\n" % (b.nom,b.nom_split,b.noeuds))
                    else:
                        if(b.type==1):
                            print("FAIL: [%s] %s: %s DEPENDANCE FAIL" % (b.nom,b.nom_split,b.noeuds))
                            print("Output: %s" % b.output)
                            fich.write("FAIL: [%s] %s: %s DEPENDANCE FAIL\n" % (b.nom,b.nom_split,b.noeuds))
                            fich.write("Output: %s\n" % b.output)
                        elif(b.type==2):
                            print("FAIL: [%s] %s: %s SERVICE FAIL" % (b.nom,b.nom_split,b.noeuds))
                            print("Output: %s" % b.output)
                            fich.write("FAIL: [%s] %s: %s SERVICE FAIL\n" % (b.nom,b.nom_split,b.noeuds))
                            fich.write("Output: %s\n" % b.output)
                    print("")
                    fich.write("\n")


    def item_selected():
        configuration_IHM.pushButton_2.setEnabled(True)

    #signaux
    clustershell_IHM.pushButton.clicked.connect(config)
    clustershell_IHM.pushButton_2.clicked.connect(lancer)
    clustershell_IHM.pushButton_3.clicked.connect(resultat)
    clustershell_IHM.pushButton_4.clicked.connect(on_click_ouvre_etat)

    configuration_IHM.pushButton.clicked.connect(on_click_add_service)
    configuration_IHM.pushButton_2.clicked.connect(on_click_delete_service)
    configuration_IHM.pushButton_3.clicked.connect(close)
    configuration_IHM.pushButton_4.clicked.connect(importer)
    configuration_IHM.listWidget.itemClicked.connect(item_selected)

    etatnoeud_IHM.pushButton_2.clicked.connect(close_window_etat)
    etatnoeud_IHM.pushButton_3.clicked.connect(open_file_browsers)
    etatnoeud_IHM.pushButton.clicked.connect(check_etat_noeud)
    etatnoeud_IHM.listWidget_2.currentItemChanged.connect(on_item_clicked)


    clustershell_IHM.main()
    app.exec_()


