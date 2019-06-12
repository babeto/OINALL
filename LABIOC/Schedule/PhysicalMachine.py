import Machine
import VirtualMachine
import HyperV
from Helper.WMIHelper import WMIHelper


class PhysicalMachine(Machine):
    """description of class"""
    def __init__(self, machinename):
        super().__init()
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
        self.vms = WMIHelper.getAllVMsOnHost(self.machineName, self.username, self.password)
        return self.vms

    def getInstalledUpdate(self):
        return super(PhysicalMachine, self).getInstalledUpdate(self.machineName, self.userName, self.password)

    def scanphymachVM(self):
        self.osName = self.getOSName()
        self.installedUpdate = phym.scanInstalledUpdate()

