import os
from Schedule.HyperV import HyperV
from Schedule.Update import Update

class Machine(object):
    """description of class"""
    def __init__(self):
        self.machineName=None
        self.systemName=None
        self.osName=None
        self.ip=None
        self.location=None
        self.rebootRequired=None
        self.installedUpdate=None

    def getMachineName():
        return self.machineName
    def getOSName():
        return self.osName
    def getInstalledUpdate():
        return self.installedUpdate
    def getRebootRequired():
        return self.rebootRequired
    def getSystemName():
        return self.systemName
