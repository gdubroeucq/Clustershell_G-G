#!/usr/bin/env python
# utilisation:
# ./script.py noeuds service1 commande service2 commande ...

import glob
import os
import sys
from ClusterShell.Task import task_self, NodeSet

def ouvrirfichier():

  path = '/etc/clustershell/'
  try:
      os.path.exists(path)
  except IOError:
      print 'Repertoire introuvable'

      try:
          fichier = open(path,"r")
          try:
  	      print 'Verification des fichiers de configuration...'
 	  finally:
	      fichier.close()
      except IOError:
          print 'Fichier de configuration introuvable'


#def main():
#
#    argument = []
#    for arg in sys.argv:
#        argument.append(arg)
#
#    #print(len(argument))
#    if len(argument) < 4:
#	print "Veuillez rentrer tous les parametres"
#
#    elif len(argument) > 4:
#	print "Oups trop de parametres !"
#    else: 
#    	for i in range(2,len(argument)):
#        	if i%2 == 0:    # pour chaque chiffre pair
#	            if(argument[i+1] == 'start' or 'stop' or 'status' or 'restart'):
#        	        task = task_self()
#	                cli="service %s %s"% (argument[i], argument[i+1])
#	                task.shell(cli, nodes=argument[1])
#	                task.run() 
#        for output, nodelist in task.iter_buffers():
#	        print '\n'
#	        print '%s: %s' % (NodeSet.fromlist(nodelist), output)

if __name__ == '__main__':
#    main()
	ouvrirfichier()


