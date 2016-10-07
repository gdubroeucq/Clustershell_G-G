#!/usr/bin/python

# Too low-level (libssh2), too buggy (paramiko), too complicated
# (both), too poor in features (no use of the agent, for instance)

# Here is the right solution today:

import subprocess
import sys
from ClusterShell.NodeSet import NodeSet

COMMAND="uname -a"

nodeset = NodeSet("node[2-3]")
numbernode_ok = 0
total_node = nodeset.__len__()
for node in nodeset:
	ssh = subprocess.Popen(["ssh", "%s" % node, COMMAND],
			shell=False,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	if result == []:
		error = ssh.stderr.readlines()
		print >>sys.stderr, "ERREUR: Le noeud %s n'est pas accessible" % node
	else:
		numbernode_ok = numbernode_ok + 1 

if numbernode_ok == total_node:
	print "Tous les noeuds sont disponibles"
