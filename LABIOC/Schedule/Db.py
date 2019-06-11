
from Schedule.PhysicalMachine import PhysicalMachine
from Schedule.LogHelper import LogHelper

import os
import sys
import django

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
sys.path.append(rootPath)
sys.path.append(curPath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LABIOC.settings")
django.setup()

from LA.models import SHHost
from LA.models import SHVirtualMachine
from LA.models import REDHost
from LA.models import REDVirtualMachine

class DB(object):
    """description of class"""
    

    @classmethod
    def updateSHPhyMach(DB,phymachinfo):
        try:
            for phym in phymachinfo:
            shhost = SHHost.objects.get(host_name = phym.machineName)
            shhost.vms = phym.vms
            shhost.os = phym.osName
            shhost.installedupdate = phym.installedUpdate
            shhost.save()
        except Exception as e:
            LogHelper.append(' '.join(r'DB.updateSHPhyMachin error:', str(e)))

    @classmethod
    def getSHPhyMachName(DB):
        all_sh_host = SHHost.objects.all()
        phymachinfo = []
        for host in all_sh_host:
            phyname = host.get('host_name')
            phymachinfo.append(phyname)
        return phymachinfo

    @classmethod
    def updateSHVM(DB,virmachinfo):
        try:
            for vm in virmachinfo:
                shvm = SHVirtualMachine.objects.get(vm_name = vn.machineName)
                shvm.ip = vm.ip
                shvm.installedupdate = vm.installedUpdate
                shvm.save()
        except Exception as e:
            LogHelper.append(' '.join(r'DB.updateSHVM error:', str(e)))

    @classmethod
    def getSHVM(DB):
        pass

        @classmethod
    def updateREDPhyMach(DB):
        pass

    @classmethod
    def getREDPhyMach(DB):
        pass


    @classmethod
    def updateREDVM(DB):
        pass

    @classmethod
    def getREDVM(DB):
        pass

if __name__ == "__main__":
    """
    dt=getupdate('cmse-4198321')
    print(dt)
    """
    ip = getVMIP('CMSE-5665903','.\\administrator','User@123','valvin1810EC1')
    print(ip)
    dt=getupdate('CMSE-4198321')
    print(dt)
    updateList = MyJsonHelper.parseJson(dt)
    for i in updateList:
        print(i.updateTitle)
        print(i.updateKB)
        print(i.installedDate)