import os
import sys
import json
import time
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
print(sys.path)

from Shedule import Update

class MyJsonHelper(object):
    """description of class"""
    
    @staticmethod
    def parseJson(data):
        installedUpdate=[]
        dic = json.loads(data)
        for iupdate in dic:
            update = Update.Update()
            update.updateTitle=iupdate["Title"]
            update.updateKB=iupdate["HotfixID"]
            timestamp=int(iupdate["Date"][6:-2])/100 #transform minisecond to second
            timearray = time.localtime(timestamp)
            update.installedDate = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
            installedUpdate.append(update)
        return installedUpdate