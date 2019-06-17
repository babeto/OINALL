
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
sys.path.append(rootPath)
sys.path.append(curPath)




from Machine import Machine
from VirtualMachine import VirtualMachine
from HyperV import HyperV
from WMIHelper import WMIHelper


class PhysicalMachine(Machine):
    """description of class"""
    def __init__(self, machinename):
        super().__init__()
        self.machineName = machinename
        self.hyperv=None
        self.vms=[]

    def checkhyperv(self):
        if WMIHelper.hypervexists(self.machineName, self.userName, self.password):
            self.hyperv = True
            return True
        else:
            self.hyperv = False
            return False

    def getvmip(self,vmname):
        ip=WMIHelper.getvmip(self.machineName,self.userName,self.password,vmname)
        return ip

    def getallvms(self):
        if self.checkhyperv():
            self.vms = WMIHelper.getAllVMsOnHost(self.machineName, self.userName, self.password)
            return self.vms
        else:
            self.vms=[]
            print("hyperv not installed, No VMs")

    def getInstalledUpdate(self):
        print("PhysicalMachine:start get update")
        return super(PhysicalMachine, self).getInstalledUpdate(self.machineName, self.userName, self.password)

    def scanphymachVM(self):
        self.osName = self.getOSName()
        self.installedUpdate = phym.scanInstalledUpdate

    def getOSName(self):
        self.osName = WMIHelper.getMachineOSName(self.machineName, self.userName, self.password)
        return self.osName

if __name__ == '__main__':
    physical = PhysicalMachine('msd-2880384')
    vms = physical.getallvms()
    for vm in vms:
        print(vm.machineName)

