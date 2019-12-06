import os
import sys
import json
import time
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
print(sys.path)

from Schedule.Update import Update #import Update class from Update file

class OutputHelper(object):
    """description of class"""
    
    @staticmethod
    def parseJson(data):
        installedUpdate = []
        #print(data)
        dic = json.loads(data)
        #print(dic)
        #print(type(dic))
        if (type(dic) == list):
            for iupdate in dic:
                update = Update()
                update.updateTitle = iupdate["Title"]
                update.updateKB = iupdate["HotfixID"]
                timestamp = int(iupdate["Date"][6:-2])/1000 #transform minisecond to second
                timearray = time.localtime(timestamp)
                update.installedDate = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
                installedUpdate.append(update)
        else:
            update = Update()
            update.updateTitle = dic["Title"]
            update.updateKB = dic["HotfixID"]
            timestamp = int(dic["Date"][6:-2])/1000 #transform minisecond to second
            timearray = time.localtime(timestamp)
            update.installedDate = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
            installedUpdate.append(update)
        # for u in installedUpdate:
        #   print(u.updateTitle)
        return installedUpdate