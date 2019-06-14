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
            print("start scan %s ..." %phyname)
            phym = PhysicalMachine(phyname)
            phym.osName = phym.getOSName()
            print(" OS of {0} is {1}".format(phyname, phym.osName))
            phym.installedUpdate = phym.getInstalledUpdate()
            phymachinfo.append(phym)
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
        DB.saveSHPhyMach(Lab.phymachinfo)

    @classmethod
    def savevmsinfo(Lab):
        DB.saveSHVM(Lab.vmsinfo)

if __name__ == "__main__":
    print("start...")
    Lab.physicalmachines = ['MSD-2880384']
    print(Lab.physicalmachines)
    print("physical machines getted...")
    #Lab.scanphysicalmachines()
    print("scan completed")
    #Lab.savephysicalinfo()
    print("save completed")
    Lab.scanallvms()
    Lab.savevmsinfo()