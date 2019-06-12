import os
import sys

rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)


from PhysicalMachine import PhysicalMachine
from VirtualMachine import VirtualMachine
from DB import DB

class Lab(object):
    """description of class"""

    physicalmachines = []

    phymachinfo = []

    vmsinfo = []


    @classmethod
    def getallphysicalmachines(Lab):
        Lab.physicalmachines = DB.readHostList()
        return Lab.physicalmachines

    @classmethod
    def scanphysicalmachines(Lab):
        phymachinfo = []
        for phyname in Lab.physicalmachines:
            phym = PhysicalMachine(phyname)
            phym.osName = phym.getOSName()
            phym.vms = phym.getallvms()
            phym.installedUpdate = phym.getInstalledUpdate()
            phymachinfo.append(phmy)
        Lab.phymachinfo = phymachinfo
        return Lab.phymachinfo

    @classmethod
    def scanallvms(Lab):
        for phyname in Lab.physicalmachines:
            phym = PhysicalMachine(phyname)
            vms = phym.getallvms()
            for index, vm in enumerate(vms):
                vms[index].installedUpdate = vm.getInstalledUpdate()
        Lab.vmsinfo = vms
        return Lab.vmsinfo

    @classmethod
    def savephysicalinfo(Lab):
        for phym in Lab.phymachinfo:
            DB.saveSHPhyMach(phym)

    @classmethod
    def savevmsinfo(Lab):
        for vm in Lab.vmsinfo:
            DB.saveSHVM(vm)

if '__name__' == '__main__':
    Lab.getallphysicalmachines
    Lab.scanphysicalmachines
    Lab.savephysicalinfo