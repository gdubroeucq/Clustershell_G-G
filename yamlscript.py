#!/usr/bin/env python
#coding: utf8

import yaml,sys,os
from ClusterShell.Task import task_self, NodeSet



def main():

    if(len(sys.argv)<2):
        print("/!\\ fichier.yaml en argument requis /!\\")
    else: 
        if(os.path.isfile(sys.argv[1])==True):   # vérifie l'existence du fichier yaml
            fichier = sys.argv[1]
            with open(fichier,'r') as stream:
                try:
                    doc=yaml.load(stream)
                    print("------------")                              #####################
                    print("nombre de service: %d" % len(doc))          #                   #
                    print(type(doc))                                   # Section debugging #
                    print(doc)                                         #                   #
                    print("------------")                              ##################### 
                    service=[]
                    if(isinstance(doc,dict)==True and len(doc.keys())!=0): # vérification de la structure du fichier YAML
                        print(len(doc.keys()))
                        print("D'après le fichier \"%s\", les services concernés sont:" % sys.argv[1])
                        compt=0
                        service=[]
                        for cle in reversed(doc.keys()):    #remet les clés dans le bon ordre
                            print("   %d: %s" % (compt,cle))
                            compt += 1
                            service.append(cle)
                        rep=""

                        print("\n")
                        while(rep !='y' and rep !='n'):
                            rep = raw_input("Confirmer (y/n) : ")
                        if(rep=='y'):
                            print '\n'
                            for i in range(0,len(service)):  # vérification des attributs de chaque service
                                name=service[i]
                                if(doc.get(name).has_key("state")==False):   
                                    print("/!\\ attribut \"state\" manquant pour %d: %s /!\\" % (i,name))
                                    sys.exit()

                                if not(doc.get(name).get("state") in ['start','stop','status','reload']):
                                    print("/!\\ attribut \"state\" doit être [start/stop/status/reload] pour %d: %s /!\\" % (i,name)) 
                                    sys.exit()

                                if(doc.get(name).has_key("nodes")==False or doc.get(name).get("nodes")==None):
                                    print("/!\\ attribut \"nodes\" manquant pour %d: %s /!\\" % (i,name))
                                    sys.exit()
                                try:               # vérifie les erreurs de syntaxe pour les nodes
                                    nodeset=NodeSet(doc.get(name).get("nodes"))
                                except:
                                    print("/!\\ Problème avec la syntaxe des noeuds \"%s\" pour %d: %s /!\\" % (doc.get(name).get("nodes"),i,name))
                                    print("\n")
                                    sys.exit()
                            for i in range(0,len(service)): # Une fois la vérification terminée, on effectue les actions
                                task = task_self()
                                name=service[i]
                                state=doc.get(name).get("state")
                                nodes=doc.get(name).get("nodes")
                                cli="service %s %s in %s" % (name,state,nodes)     
                                task.shell(cli, nodes=nodes) 
                                task.run()
                                print("- name: %s     state: %s         nodes: %s" % (name,state,nodes))
                                for output, nodelist in task.iter_buffers():
                                    print '--> %s: %s' % (NodeSet.fromlist(nodelist), output) 
                                    print '\n'
                            print '\n'
                            

                    else:
                        print("/!\\ Erreur syntaxe dans \"%s\" /!\\" % sys.argv[1])
            
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            print("\"%s\" n'existe pas" % sys.argv[1])






if __name__ == '__main__':
    main()
