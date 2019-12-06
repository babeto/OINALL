
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
sys.path.append(rootPath)
sys.path.append(curPath)

from Schedule.Config import Config
from Machine import Machine
from VirtualMachine import VirtualMachine
from HyperV import HyperV
from WMIHelper import WMIHelper


class PhysicalMachine(Machine):
    """description of class"""
    def __init__(self, *machinename):
        super().__init__()
        self.userName = r'.\administrator'
        self.password = r'User@123'
        self.owner = r'Lab'
        if machinename != ():
            self.machineName = machinename[0]
            self.set_credential()
            self.osName = self.getOSName()
            self.osVersion = self.getOSVersion()
            self.osLang = self.getOSLang()
        else:
            self.machineName = None
            self.osName = None
            self.osVersion = None
            self.osLang = None

        self.hyperv=None
        self.vms=[]

    def checkhyperv(self):
        if WMIHelper.hypervexists(self.machineName, self.userName, self.password):
            self.hyperv = True
            print("yesssssssssssssssssssss")
            return True
        else:
            self.hyperv = False
            return False


    def set_credential(self):
        print(Config.account)
        for account in Config.account:
            print(account)
            username = account['user']
            password = account['password']

            if WMIHelper.accountverify(self.machineName, username, password):
                self.userName = username
                self.password = password
                return True
        return False


    def getvmip(self,vmname):
        ip=WMIHelper.getvmip(self.machineName,self.userName,self.password,vmname)
        return ip

    def getallvms(self):
        if self.checkhyperv():
            self.vms = WMIHelper.getAllVMsOnHost(self.machineName, self.userName, self.password)
        else:
            self.vms=[]
            print("hyperv not installed, No VMs")
        return self.vms

    def getInstalledUpdate(self):
        print("PhysicalMachine:start get update")
        self.set_credential()
        self.osName = self.getOSName()
        self.osVersion = self.getOSVersion()
        self.osLang = self.getOSLang()
        return super(PhysicalMachine, self).getInstalledUpdate(self.machineName, self.userName, self.password, self.osLang)
    
    def invokeWUInstall(self):
        print("PhysicalMachine:start invoke install")
        self.set_credential()
        self.osName = self.getOSName()
        self.osVersion = self.getOSVersion()
        self.osLang = self.getOSLang()
        return super(PhysicalMachine, self).invokeWUInstall(self.machineName, self.userName, self.password)

    def getOSName(self):
        self.osName = WMIHelper.getMachineProperty(self.machineName, self.userName, self.password, 'OSName')
        return self.osName

    def getOSVersion(self):
        self.osVersion = WMIHelper.getMachineProperty(self.machineName, self.userName, self.password, 'Version')
        return self.osVersion

    def getOSLang(self):
        return super().getOSLang(self.machineName, self.userName, self.password)

    def getRebootStatus(self):
        self.rebootRequired = WMIHelper.getRebootReg(self.machineName, self.userName, self.password)
        return self.rebootRequired


    def getSqlVersion(self):
        self.sqlVersion = WMIHelper.get_sqlversion(self.machineName, self.userName, self.password)
        return self.sqlVersion

    def getVSInstalled(self):
        self.vsInstalled = WMIHelper.check_VS(self.machineName, self.userName, self.password)
        return self.vsInstalled

if __name__ == '__main__':
    """
    physical = PhysicalMachine('CMSE-5665903')
    vms = physical.getallvms()
    for vm in vms:
        print(vm.machineName)
        print(vm.ip)
    """
    physical = PhysicalMachine('MSD-1531344')
    physical.invokeWUInstall()
