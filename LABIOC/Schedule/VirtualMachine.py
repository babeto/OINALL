import os
import subprocess

from Schedule.Machine import Machine
from WMIHelper import WMIHelper
from Schedule.Helper.PowerShellHelper import PowerShellHelper

class VirtualMachine(Machine):
    """description of class"""
    def __init__(self):
        super().__init__()
        self.machineName = None
        self.ip = None
        self.vmid=None
        self.hostName=None
        self.userName = r'vlan974\administrator'


    def getvmid():
        return self.vmid
    def getUser():
        return self.user
    def getHostName():
        return self.hostName

    def getInstalledUpdate(self):

        print("scan %s started..."% self.machineName)
        if self.ip == None:
            print('try to get ip')
            self.ip = PowerShellHelper.getvmip(self.hostName, r'.\administrator', r'User@123', self.machineName)
            if self.ip == None:
                return None

        return super(VirtualMachine, self).getInstalledUpdate(self.ip, self.userName, self.password)

class mytest():
    pass