import os
import sys
import json
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
print(sys.path)

import Shedule.Update

class JsonHelper(object):
    """description of class"""
    
    @classmethod
    def parseJson(data):
        installedUpdate=[]
        dic = json.loads(data)
        for iupdate in dic:
            update = Update()
            update.updateTitle=iupdate["Title"]
            update.updateKB=iupdate["HotfixID"]
            timestamp=int(iupdate["Date"][7:-3])
            timearray=time.localtime(timestamp)
            update.installedDate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            installedUpdate.append(update)
        return installedUpdate