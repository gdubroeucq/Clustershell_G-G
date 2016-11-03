#!/usr/bin/env python2.7
#coding: utf8
# utilisation:
# ./script.py noeuds service1 commande service2 commande
# ./script.py node[1-3] cron stop nginx restart

import sys
from ClusterShell.Task import task_self, NodeSet

def main():
    if len(sys.argv) <= 3:
        print "Veuillez entrer des paramètres (./script.py node[1-3] cron stop)"
    else: 
        if((len(sys.argv)%2)==0):
            try:               # vérifie les erreurs de syntaxe pour les nodes
                nodeset=NodeSet(sys.argv[1])
            except:
                print("Erreur: Problème avec la syntaxe \"%s\"" % sys.argv[1])
                return
            for i in range(2,len(sys.argv)):
                if i%2 == 0:    # pour chaque chiffre pair
                    if(sys.argv[i+1] == 'start' or 'stop' or 'status' or 'restart' or 'reload'):
                        task = task_self()
                        cli="service %s %s"% (sys.argv[i], sys.argv[i+1])
                        task.shell(cli, nodes=sys.argv[1])
                        task.run() 
            for output, nodelist in task.iter_buffers():
                print '\n'
                print '%s: %s' % (NodeSet.fromlist(nodelist), output)
        else:
            print("Erreur: Veuillez vérifier le nombre de paramètres")

if __name__ == '__main__':
    main()



