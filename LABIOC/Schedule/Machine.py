import os
import subprocess


#from Schedule.HyperV import HyperV
from Schedule.Update import Update
# from Schedule.Helper.WMIHelper import WMIHelper
from Schedule.Helper.LogHelper import LogHelper
from Schedule.Helper.MyJsonHelper import MyJsonHelper

class Machine(object):
    """description of class"""
    def __init__(self):
        self.systemName = None
        self.osName = None
        self.userName = r'.\administrator'
        self.password = r'User@123'
        self.location = None
        self.rebootRequired = None
        self.installedUpdate = None
        self.scancompletetime = None

    def getMachineName(self):
        return self.machineName

    def getRebootRequired(self):
        return self.rebootRequired

    def getSystemName(self):
        return self.systemName
    """
    def getOSName(self):
        try:
            self.osName = WMIHelper.getMachineOSName(machineName, userName, password)
            return self.osName
        except Exception as e:
            LogHelper.append(' '.join(r'Machine.getOSName error:', str(e)))
    """
    def getInstalledUpdate(self, machinename, username, password):
        print("scan %s started..."% machinename)
        args=[r"PowerShell",r".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machinename, r"-Username" ,username ,r"-Password", password]
        print(args)
        updateinfo = []
        try:
            p=subprocess.Popen(args,stdout=subprocess.PIPE)
            dt=p.stdout.read()
            # print(dt)
            if dt != None:
                self.installedUpdate = MyJsonHelper.parseJson(dt)
            else:
                self.installedUpdate = None
            for update in self.installedUpdate:
                updateinfo.append(update.tojson())
                print(update.updateTitle)
        except Exception as e:
            print(str(e))
        return updateinfo
        
        """
        try:

        except Exception as e:
            print(e)
            LogHelper.append(' '.join([r'Machine.getInstalledUpdate error:', str(e)]))
        """