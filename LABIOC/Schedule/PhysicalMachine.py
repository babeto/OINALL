import Machine
import VirtualMachine
import HyperV
from Helper.WMIHelper import WMIHelper


class PhysicalMachine(Machine):
    """description of class"""
    def __init__(self, machinename):
        super().__init(machinename)
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

    def scanphymach(self):
        self.osName = self.getOSName()
        self.installedUpdate = phym.scanInstalledUpdate()

