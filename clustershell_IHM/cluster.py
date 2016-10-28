#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from ClusterShell.Task import task_self, NodeSet

import sys,os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


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
                print("Avortement %s: le service %s n'est pas activé ou installé" % (NodeSet.fromlist(nodelist),serv_split[m]))
                clustershell_IHM.listWidget.addItem("Avortement %s: le service %s n'est pas activé ou installé" % (NodeSet.fromlist(nodelist),serv_split[m]))


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
            print "nodeset: %s" % str(nodeset)
            print "nodes: %s" % nodes
            if(str(nodeset)!=nodes):
                print("OK %s: %s" % (name_split[n],nodeset))
                clustershell_IHM.listWidget.addItem("OK %s: %s" % (name_split[n],nodeset))
            if(str(nodeset)==nodes):
                print("OK %s: %s" % (name_split[n],nodes))
                clustershell_IHM.listWidget.addItem("OK %s: %s" % (name_split[n],nodes))
            #if(out==output):
            #    print("OK")
            #    clustershell_IHM.listWidget.addItem("OK")


