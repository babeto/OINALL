
from PhysicalMachine import PhysicalMachine
from VirtualMachine import VirtualMachine

class Lab(object):
    """description of class"""

    def __init__(self):
        pass

    physicalmachines = []

    @classmethod
    def scanphysicalmachines(Lab):
        phymachinfo = []
        for phyname in Lab.physicalmachines:
            phym = PhysicalMachine(phyname)
            phym.osName = phym.getOSName()
            phym.vms = phym.getallvms()
            phym.installedUpdate = phym.scanInstalledUpdate()
            phymachinfo.append(phmy)
        return phymachinfo

    @classmethod
    def scanallvms(Lab):
        vms = []
        for phyname in Lab.physicalmachines:
            phym = PhysicalMachine(phyname)
            vms = phym.getallvms()
