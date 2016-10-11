#!/usr/bin/env python
#coding: utf8

import yaml,sys,os



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
                    if(len(doc)!=0 and isinstance(doc,list)==True):
                        for i in range(0,len(doc)):
                            service.append(doc[i].keys()[0]) 
                        print("D'après votre fichier \"%s\", les services concernés sont:" % sys.argv[1])
                        compt=0
                        for n in service:
                            print("   %d: %s" % (compt,n))
                            compt += 1
                        rep=""
                        print("\n")
                        while(rep !='y' and rep !='n'):
                            rep = raw_input("Confirmer (y/n) : ")
                        if(rep=='y'):
                            #Suite du code ici 
                            print("ok")
                         

                    else:
                        print("Erreur syntaxe YAML")
            
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            print("\"%s\" n'existe pas" % sys.argv[1])






if __name__ == '__main__':
    main()
