#!/usr/bin/env python

import yaml



def main():
    with open("example.yaml",'r') as stream:
        try:
            doc=yaml.load(stream)
           # print(doc)
           # print(doc.get("service")["name"])
           # print(doc[1].get("ssh").get("state"))
           #print(doc[1].keys())
            print(doc[1].keys()[0])
            
            #for i in doc[0].keys():
                
           # for cle in doc.keys():
           #     print cle
            
        except yaml.YAMLError as exc:
            print(exc)












if __name__ == '__main__':
    main()
