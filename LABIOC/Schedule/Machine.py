import os
import subprocess

#from Schedule.HyperV import HyperV
from Schedule.Update import Update
from WMIHelper import WMIHelper
from Schedule.Helper.LogHelper import LogHelper
from Schedule.Helper.MyJsonHelper import MyJsonHelper
from Schedule.Helper.PowerShellHelper import PowerShellHelper

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
        print("enable PS on %s..." % machinename)
        print(machinename,username,password)
        updatelist = []
        try:
            WMIHelper.enableps(machinename, username, password)
            updatelist = PowerShellHelper.getupdate(machinename, username, password)
        except Exception as e:
            print(str(e))
        return updatelist
        
        """
        try:

        except Exception as e:
            print(e)
            LogHelper.append(' '.join([r'Machine.getInstalledUpdate error:', str(e)]))
        """