#!/usr/bin/env python
#coding: utf8
#
# Script.yaml:
#              ---
#               service1,[service2,...]:
#                  state: [start,stop,restart,reload] 
#                  nodes: node1,[node2,...]
#
# Exemple:                 
#              ---
#               cron,nginx: 
#                  state: restart
#                  nodes: node[50-100]
#
#

import yaml,sys,os
from ClusterShell.Task import task_self, NodeSet
from supply import has_colours,printout,getTerminalSize

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def debug(doc):
    print("------------")                              #####################
    print("nombre de service: %d" % len(doc))          #                   #
    print(type(doc))                                   # Section debugging #
    print(doc)                                         #                   #
    print("------------")                              ##################### 
    return() 


def check_service(doc):
    if(isinstance(doc,dict)==True and len(doc.keys())!=0): # vérification de la structure du fichier YAML
        print(len(doc.keys()))
        print("D'après le fichier \"%s\", les services concernés sont:" % sys.argv[1])
        compt=0
        return(True)
    else:
        print("/!\\ Erreur syntaxe dans \"%s\" /!\\" % sys.argv[1]) 
        return(False)
 
def check_attribut(doc,service):
    for i in range(0,len(service)):  # vérification des attributs de chaque service
        name=service[i]
        if(doc.get(name).has_key("state")==False):   
            print("/!\\ attribut \"state\" manquant pour %d: %s /!\\" % (i,name))
            return(False) 
        if not(doc.get(name).get("state") in ['start','stop','status','reload']):
            print("/!\\ attribut \"state\" doit être [start/stop/status/reload] pour %d: %s /!\\" % (i,name)) 
            return(False)
        if(doc.get(name).has_key("nodes")==False or doc.get(name).get("nodes")==None):
            print("/!\\ attribut \"nodes\" manquant pour %d: %s /!\\" % (i,name))
            return(False)
        try:               # vérifie les erreurs de syntaxe pour les nodes
            nodeset=NodeSet(doc.get(name).get("nodes"))
        except:
            print("/!\\ Problème avec la syntaxe de \"%s\" pour %d: %s /!\\" % (doc.get(name).get("nodes"),i,name))
            print("\n")
            return(False) 
    return(True) 


def reverse_key(doc):  # remet les services dans le bon ordre
        service=[]
        compt=0
        for cle in reversed(doc.keys()):    
            print("   %d: %s" % (compt,cle))
            compt += 1
            service.append(cle)
        print("")
        return(service)

def clustershell(doc,service):  # Commandes distribuées
    out=""
    output=""
    recap=[]
    for i in range(0,len(service)): 
        task = task_self()
        name=service[i]
        name_split=service[i].split(",")
        state=doc.get(name).get("state")
        nodes=doc.get(name).get("nodes")
        x,y=getTerminalSize()
        string="TASK: [%s]" % name
        star= '*' * (x-len(string))
        print("%s %s" % (string,star))
        for n in range(0,len(name_split)):
            cli="service %s %s" % (name_split[n],state)    
            task.shell(cli, nodes=nodes) 
            task.run()
            space=' ' * (15-len(name_split[n]))
            printout("%s%s:  state=%s     nodes=%s\n" % (name_split[n],space,state,nodes), YELLOW)
            for output, nodelist in task.iter_buffers():
                printout('Error: %s: %s\n' % (NodeSet.fromlist(nodelist), output), RED) 
                recap.append(0)
            if(out==output):
                printout("OK\n", GREEN) 
                recap.append(1)
            else:
                out=output
            print("")
    return recap

def recap(service,recap):
    x,y=getTerminalSize()
    recaptext="RECAP"
    stars= '*' * (x-len(recaptext)-1)
    print("%s %s" % (recaptext,stars))
    z=0
    for g in range(0,len(service)):
        name=service[g]
        name_split=service[g].split(",")
        
        for p in range(0,len(name_split)):
            if(recap[z]==1):
                recap_value="[%s]%s" % (name,name_split[p])
                space=' ' * (30-len(recap_value))
                recap_final="%s %s:" % (recap_value,space)
                print(recap_final),
                printout(" ok=1", GREEN)
                print("        failed=0")
            else:
                recap_value="[%s]%s" % (name,name_split[p])
                space=' ' * (30-len(recap_value))
                recap_final="%s %s: ok=0" % (recap_value,space)
                print(recap_final),
                printout("        failed=1\n", RED)
            z=z+1
        print("")
 
def main():

    service=[]
    rep=""

    if(len(sys.argv)>=2):
        if(os.path.isfile(sys.argv[1])==True):   # vérifie l'existence du fichier yaml
            fichier = sys.argv[1]
            with open(fichier,'r') as stream:
                try:
                    print stream
                    doc=yaml.safe_load(stream)
                    debug(doc) # information (optionnel)
                    if(check_service(doc)): # Contrôle les services
                        service=reverse_key(doc) # Met les services dans le bon ordre
                        while(rep !='y' and rep !='n'):
                            rep = raw_input("Confirmer (y/n) : ")
                        if(rep=='y'):
                            print ""
                            if(check_attribut(doc,service)): # Contrôle les attributs des services
                                recapitulatif=clustershell(doc,service)  
                                recap(service,recapitulatif)
                            print ""
                         
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            print("\"%s\" n'existe pas" % sys.argv[1])

    else:   
        print("/!\\ fichier.yaml en argument requis /!\\")


if __name__ == '__main__':
    main()
