#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from ClusterShell.Task import task_self, NodeSet


import sys,os,yaml

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class typeservice:
    def __init__(self,nom,action,noeuds,dependance=""):
        self.nom=nom
        self.action=action
        self.noeuds=noeuds
        self.dependance=dependance

class recap_cluster:
    def __init__(self,nom,nom_split,noeuds,resultat,type=0,output=""):
        self.nom=nom
        self.nom_split=nom_split
        self.noeuds=noeuds
        self.resultat=resultat
        self.type=type
        self.output=output

def check_depend(clustershell_IHM,service,name,j):
    if(service[j].dependance!=""):
        serv=str(service[j].dependance)
        serv_split=serv.split(",")
        taske = task_self()
        nodes=str(service[j].noeuds)
        result=[]
        error_nodes=[]
        for m in range(0,len(serv_split)):
            out=""
            output=""
            cli="service %s start" % serv_split[m]
            taske.shell(cli, nodes=nodes)
            taske.run()
            for output, nodelist in taske.iter_buffers():
                result.append(serv_split[m])
                print("/!\ Avortement /!\ %s: le service %s n'est pas activé ou installé" % (NodeSet.fromlist(nodelist),serv_split[m]))
                clustershell_IHM.listWidget.addItem("Avortement %s: le service %s n'est pas activé ou installé" % (NodeSet.fromlist(nodelist),serv_split[m]))
                dep="Avortement %s: le service %s n'est pas activé ou installé" % (NodeSet.fromlist(nodelist),serv_split[m])
                clustershell_IHM.list_recap.append(recap_cluster(serv,serv_split[m],NodeSet.fromlist(nodelist),0,1,dep))

    else:
        return(True,0)
    if(len(result)==0):
        return(True,0)
    else:
        return(False,result)


def clustershell(clustershell_IHM,service,i):
    task = task_self()
    name=str(service[i].nom)
    name_split=name.split(",")
    state=str(service[i].action)
    nodes=str(service[i].noeuds)
    test_depend,result=check_depend(clustershell_IHM,service,name,i)
    if(test_depend==True):
        for n in range(0,len(name_split)):
            out=""
            output=""
            cli="service %s %s" % (name_split[n],state)
            task.shell(cli, nodes=nodes)
            task.run()
            nodeset= NodeSet(nodes)
            for output, nodelist in task.iter_buffers():
                print("FAIL %s: %s %s" %(name_split[n],NodeSet.fromlist(nodelist), output))
                clustershell_IHM.listWidget.addItem("FAIL %s: %s %s" %(name_split[n],NodeSet.fromlist(nodelist), output))
                nodeset.remove(NodeSet.fromlist(nodelist))
                clustershell_IHM.list_recap.append(recap_cluster(name,name_split[n],NodeSet.fromlist(nodelist),0,2,output))
            if(str(nodeset)!=nodes):
                if(len(nodeset)>0):
                    print("OK %s: %s" % (name_split[n],nodeset))
                    clustershell_IHM.listWidget.addItem("OK %s: %s" % (name_split[n],nodeset))
                    clustershell_IHM.list_recap.append(recap_cluster(name,name_split[n],nodeset,1))
            if(str(nodeset)==nodes):
                print("OK %s: %s" % (name_split[n],nodes))
                clustershell_IHM.listWidget.addItem("OK %s: %s" % (name_split[n],nodes))
                clustershell_IHM.list_recap.append(recap_cluster(name,name_split[n],nodes,1))
            #if(out==output):
            #    print("OK")
            #    clustershell_IHM.listWidget.addItem("OK")

def check_service(doc):
    if(isinstance(doc,list)==True and len(doc)>=1): # vérification de la structure du fichier YAML
        #print("D'après le fichier \"%s\", les services concernés sont:" % sys.argv[1])
        return(True)
    else:
        print("/!\\ Erreur syntaxe dans \"%s\" /!\\" % sys.argv[1])
        return(False)

def add_key(doc):  # remet les services dans le bon ordre
        service=[]
        compt=0
        for i in range(0,len(doc)):
            print("   %s: %s" % (compt,doc[i].keys()[0]))
            compt +=1
            service.append(doc[i].keys()[0])
        print("")
        return(service)

def check_attribut(doc,service,clustershell_IHM,configuration_IHM):
    for i in range(0,len(service)):
        ok=0
        name=service[i]
        if(doc[i].get(name).has_key("state")==False):
            print("/!\\ attribut \"state\" manquant pour %d: %s /!\\" % (i,name))
            QMessageBox.about(configuration_IHM,"Erreur","/!\\ attribut \"state\" manquant pour %d: %s /!\\" % (i+1,name))
            return(False)
        if not(doc[i].get(name).get("state") in ['start','stop','status','reload']):
            print("/!\\ attribut \"state\" doit être [start/stop/status/reload] pour %d: %s /!\\" % (i,name))
            QMessageBox.about(configuration_IHM,"Erreur","/!\\ attribut \"state\" doit être [start/stop/status/reload] pour %d: %s /!\\" % (i+1,name))
            return(False)
        if(doc[i].get(name).has_key("nodes")==False or doc[i].get(name).get("nodes")==None):
            print("/!\\ attribut \"nodes\" manquant pour %d: %s /!\\" % (i,name))
            QMessageBox.about(configuration_IHM,"Erreur","/!\\ attribut \"nodes\" manquant pour %d: %s /!\\" % (i+1,name))
            return(False)
        try:               # vérifie les erreurs de syntaxe pour les node
            nodeset=NodeSet(doc[i].get(name).get("nodes"))
            ok=1
        except:
            QMessageBox.about(configuration_IHM,"Erreur","/!\\ Problème avec la syntaxe de \"%s\" pour %d: %s /!\\" % (doc[i].get(name).get("nodes"),i,name))
            print("/!\\ Problème avec la syntaxe de \"%s\" pour %d: %s /!\\" % (doc[i].get(name).get("nodes"),i+1,name))
            print("\n")
            return(False)

    if(ok==1):
        for i in range(0,len(service)):
            name=service[i]
            action=doc[i].get(name).get("state")
            noeuds=doc[i].get(name).get("nodes")
            if(doc[i].get(name).get("depend")!=None):
                dependance=doc[i].get(name).get("depend")
                print dependance
                configuration_IHM.listWidget.addItem("%d: %s %s ON %s (depend %s)"%(configuration_IHM.listWidget.count()+1,name,action,str(nodeset),dependance))
                clustershell_IHM.list_service.append(typeservice(name,action,noeuds,dependance))
            else:
                configuration_IHM.listWidget.addItem("%d: %s %s ON %s"%(configuration_IHM.listWidget.count()+1,name,action,str(nodeset)))
                clustershell_IHM.list_service.append(typeservice(name,action,noeuds))

    return(True)



def fichier(clustershell_IHM,configuration_IHM):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)

    filename = dlg.getOpenFileName(configuration_IHM, 'Explorateur','/home/', 'File (*.*)')
    with open(filename,'r') as stream:
        try:
            doc=yaml.safe_load(stream)
            if(check_service(doc)):
                service=add_key(doc)
                if(check_attribut(doc,service,clustershell_IHM,configuration_IHM)):
                    return(True)

        except yaml.YAMLError as exc:
            QMessageBox.about(configuration_IHM,"Erreur Fichier YAML","%s" % exc)
            print(exc)
            return(False)


