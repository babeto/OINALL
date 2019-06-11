import Machine
import VirtualMachine
import HyperV
from Helper.WMIHelper import WMIHelper


class PhysicalMachine(Machine):
    """description of class"""
    def __init__(self):
        self.owner=None
        self.hyperv=None
        self.VMs=None

    def hypervInstalled():
        pass

    def getvmip(self,vmname):
        ip=WMIHelper.getvmip(self.machineName,self.userName,self.password,vmname)
        return ip

