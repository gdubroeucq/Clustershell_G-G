#!/usr/bin/env python

import sys
from ClusterShell.Task import task_self, NodeSet



def main():


    task = task_self()
    task.shell("date", nodes="node[2-3]")
    task.run()

    for output, nodelist in task.iter_buffers():
        print '%s: %s' % (NodeSet.fromlist(nodelist), output)

    





if __name__ == '__main__':
    main()



