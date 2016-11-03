#!/usr/bin/env python
#coding: utf8
#
# Script.yaml:
#              ---
#               - service1,[service2,...]:
#                   state: [start,stop,restart,reload] 
#                   nodes: node1,[node2,...]
#                   depend: service
# Exemple:                 
#              ---
#               - cron,nginx: 
#                   state: restart
#                   nodes: node[50-100]
#               - proxmox:
#                   state: stop
#                   nodes: node[1-10]
#                   depend: vsphere
#
# ./yamlscript example.yaml [-force]
# -force: Bypass la confirmation humaine, utile si on veut automatiser par exemple 
# Il est fortement conseiller de tester son fichier de configuration une fois avant de l'automatiser.

import yaml,sys,os
from ClusterShell.Task import task_self, NodeSet
from supply import has_colours,printout,getTerminalSize

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def debug(doc):
    print("------------")                              #####################
    print("nombre de service: %d" % len(doc))          #                   #
    print(type(doc))                                   # Section debugging #
    print(doc)                                         #                   #
    print(doc[0])
    print(len(doc))
    print(doc[0].keys()[0])
    print(doc[0].get(doc[0].keys()[0]).get("state"))
    print(len(doc))
    print("------------")                              ##################### 
    return() 


def check_service(doc):
    if(isinstance(doc,list)==True and len(doc)>=1): # vérification de la structure du fichier YAML
        print("D'après le fichier \"%s\", les services concernés sont:" % sys.argv[1])
        return(True)
    else:
        print("/!\\ Erreur syntaxe dans \"%s\" /!\\" % sys.argv[1]) 
        return(False)
 
def check_attribut(doc,service):
    for i in range(0,len(service)):  # vérification des attributs de chaque service
        name=service[i]
        if(doc[i].get(name).has_key("state")==False):
            print("/!\\ attribut \"state\" manquant pour %d: %s /!\\" % (i,name))
            return(False) 
        if not(doc[i].get(name).get("state") in ['start','stop','status','reload','restart']):
            print("/!\\ attribut \"state\" doit être [start/stop/status/reload] pour %d: %s /!\\" % (i,name)) 
            return(False)
        if(doc[i].get(name).has_key("nodes")==False or doc[i].get(name).get("nodes")==None): 
            print("/!\\ attribut \"nodes\" manquant pour %d: %s /!\\" % (i,name))
            return(False)
        try:               # vérifie les erreurs de syntaxe pour les nodes
            nodeset=NodeSet(doc[i].get(name).get("nodes"))
        except:
            print("/!\\ Problème avec la syntaxe de \"%s\" pour %d: %s /!\\" % (doc[i].get(name).get("nodes"),i,name))
            print("\n")
            return(False) 
    return(True) 

def check_depend(doc,name,i):
    if(doc[i].get(name).get("depend")!=None):
        serv=doc[i].get(name).get("depend")
        serv_split=serv.split(",")
        taske = task_self()
        nodes=doc[i].get(name).get("nodes")
       # out=""
       # output=""
        result=[]
        for m in range(0,len(serv_split)):
            out=""
            output=""
            cli="service %s start" % serv_split[m]
            taske.shell(cli, nodes=nodes)
            taske.run()
            for output, nodelist in taske.iter_buffers():
                result.append(serv_split[m])
                error_nodes=NodeSet.fromlist(nodelist)
    else:
        return(True,0,0)
    if(len(result)==0):
        return(True,0,0)
    else:
        return(False,result,error_nodes)
                    

def add_key(doc):  # remet les services dans le bon ordre
        service=[]
        compt=0
        for i in range(0,len(doc)):
            print("   %s: %s" % (compt,doc[i].keys()[0]))
            compt +=1
            service.append(doc[i].keys()[0])
        print("")
        return(service)

def clustershell(doc,service):  # Commandes distribuées
    recap=[]
    for i in range(0,len(service)): 
        task = task_self()
        name=service[i]
        name_split=service[i].split(",")
        state=doc[i].get(name).get("state")
        nodes=doc[i].get(name).get("nodes")
        x,y=getTerminalSize()
        string="TASK: [%s]" % name
        star= '*' * (x-len(string))
        print("%s %s" % (string,star))
        test_depend,result,error_nodes=check_depend(doc,name,i)
        if(test_depend==True):
            for n in range(0,len(name_split)):
                out=""
                output=""
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
                print("")
        else:
            space=' ' * (15-len(name))
            printout("%s%s:  state=%s    nodes=%s\n" % (name,space,state,nodes), YELLOW)
            printout("Error depend %s: le(s) service(s) %s n'est(sont) pas activé(s) ou installé(s)\n" % (error_nodes,result), RED)
            print("")
            for yop in range(0,len(name_split)):
                recap.append(0)
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
                    doc=yaml.safe_load(stream)
                   #debug(doc) # information (optionnel)
                    if(check_service(doc)): # Contrôle les services
                        service=add_key(doc) # Met les services en état
                        passe=0
                        for r in sys.argv:
                            if(r=="-force"):
                                passe=1
                        if(passe==0):     
                            while(rep !='y' and rep !='n'):
                                rep = raw_input("Confirmer (y/n) : ")
                            if(rep=='y'):
                                print ""
                                if(check_attribut(doc,service)): # Contrôle les attributs des services
                                    recapitulatif=clustershell(doc,service)  
                                    recap(service,recapitulatif)
                                print ""
                        else:
                            if(check_attribut(doc,service)):
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
