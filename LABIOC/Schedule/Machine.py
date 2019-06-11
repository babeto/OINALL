import os
from Schedule.HyperV import HyperV
from Schedule.Update import Update
from Schedule.Helper.WMIHelper import WMIHelper
from Schedule.Helper.LogHelper import LogHelper
from Schedule.Helper.MyJsonHelper import MyJsonHelper

class Machine(object):
    """description of class"""
    def __init__(self, machinename):
        self.machineName=machinename
        self.systemName=None
        self.osName=None
        self.userName=r'.\administrator'
        self.password=r'User@123'
        self.ip=None
        self.location=None
        self.rebootRequired=None
        self.installedUpdate=None

    def getMachineName(self):
        return self.machineName

    def getRebootRequired(self):
        return self.rebootRequired

    def getSystemName(self):
        return self.systemName

    def getOSName(self):
        try:
            self.osName = WMIHelper.getMachineOSName(machineName, userName, password)
            return self.osName
        except Exception as e:
            LogHelper.append(' '.join(r'Machine.getOSName error:', str(e)))
            
    def getInstalledUpdate(self):
        args=[r"PowerShell",r".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machineobj,r"-Username", r".\administrator",r"-Password", r"User@123"]
        try:
            p=subprocess.Popen(args,stdout=subprocess.PIPE)
            dt=p.stdout.read()
            self.installedUpdate = MyJsonHelper.parseJson(dt)
            return self.installedUpdate
        except Exception as e:
            LogHelper.append(' '.join(r'Machine.getInstalledUpdate error:', str(e)))