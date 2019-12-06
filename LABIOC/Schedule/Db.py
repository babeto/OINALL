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

from Schedule.PhysicalMachine import PhysicalMachine
from Schedule.VirtualMachine import VirtualMachine
from Schedule.Helper.LogHelper import LogHelper

from LA.models import SHHost
from LA.models import SHVirtualMachine
from LA.models import REDHost
from LA.models import REDVirtualMachine
from LA.models import AzureVirtualMachine
from django.db.models import Q

class DB(object):
    """description of class"""

    @classmethod
    def save(DB, machine, type, location):
        if type == 'hm':
            if location == 'sh':
                hmobj = SHHost
            elif location == 'red':
                hmobj = REDHost
            try:
                hm = hmobj.objects.get(machine_name=machine.machineName)
                hm.ip = machine.ip
                hm.installedupdate = machine.installedUpdate
                hm.os = machine.osName
                hm.osversion = machine.osVersion
                hm.oslang = machine.osLang
                hm.rebootrequired = machine.rebootRequired
                hm.lastscantime = machine.scancompletetime
                hm.compliant = machine.compliant
                hm.vms = machine.vms
                hm.status = machine.status
                hm.msg = machine.msg
                hm.sqlversion = machine.sqlVersion
                hm.vsinstalled = machine.vsInstalled
                hm.save()
            except hmobj.DoesNotExist:
                hmobj.objects.create(
                    machine_name=machine.machineName,
                    owner = machine.owner,
                    ip=machine.ip, 
                    installedupdate=machine.installedUpdate, 
                    os=machine.osName, 
                    osversion=machine.osVersion, 
                    oslang = machine.osLang,
                    rebootrequired = machine.rebootRequired,
                    lastscantime = machine.scancompletetime,
                    vms = machine.vms,
                    status = machine.status,
                    msg = machine.msg,
                    sqlversion = machine.sqlVersion,
                    vsinstalled = machine.vsInstalled)
            except Exception as e:
                print('DB.save error: host not found or save failed')
                LogHelper.append('DB.save error: host {0} not found or save failed'.format(machine.machineName))
        elif type == 'vm':
            if location == 'sh':
                vmobj = SHVirtualMachine
                hm = SHHost.objects.get(machine_name = machine.hostName)
            elif location == 'red':
                vmobj = REDVirtualMachine
                hm = REDHost.objects.get(machine_name = machine.hostName)
            try:
                vm = vmobj.objects.get(vmid = machine.vmid)
                vm.ip = machine.ip
                vm.installedupdate = machine.installedUpdate
                vm.os = machine.osName
                vm.osversion = machine.osVersion
                vm.oslang = machine.osLang
                vm.rebootrequired = machine.rebootRequired
                vm.fullyqualifieddomainname = machine.fullyQualifiedDomainName
                vm.domainname = machine.domainName
                vm.lastscantime = machine.scancompletetime
                vm.loc_host = hm
                vm.status = machine.status
                vm.msg = machine.msg
                vm.sqlversion = machine.sqlVersion
                vm.vsinstalled = machine.vsInstalled
                vm.save()
            except vmobj.DoesNotExist:
                vmobj.objects.create(machine_name=machine.machineName,
                    vmid=machine.vmid,ip=machine.ip, 
                    installedupdate=machine.installedUpdate, 
                    os=machine.osName, 
                    osversion=machine.osVersion, 
                    oslang = machine.osLang,
                    rebootrequired = machine.rebootRequired,
                    fullyqualifieddomainname = machine.fullyQualifiedDomainName,
                    domainname = machine.domainName,
                    lastscantime=machine.scancompletetime,
                    loc_host=hm,
                    status = machine.status,
                    msg = machine.msg,
                    sqlversion = machine.sqlVersion,
                    vsinstalled = machine.vsInstalled)
            except Exception as e:
                print(str(e))
                LogHelper.append('update or create vm object failed')
        
        elif type == 'azm':
            try:
                azm = AzureVirtualMachine.objects.get(machine_name=machine.machineName)
                azm.ip = machine.ip
                azm.installedupdate = machine.installedUpdate
                azm.os = machine.osName
                azm.osversion = machine.osVersion
                azm.oslang = machine.osLang
                azm.rebootrequired = machine.rebootRequired
                azm.lastscantime = machine.scancompletetime
                azm.status = machine.status
                azm.msg = machine.msg
                azm.resourceid = machine.resourceID
                azm.location = machine.location
                azm.resourcename = machine.resourceName
                azm.resourcegroupname = machine.resourceGroupName
                azm.role = machine.role
                azm.owner = machine.owner
                azm.save()
            except AzureVirtualMachine.DoesNotExist:
                AzureVirtualMachine.objects.create(
                    machine_name=machine.machineName,
                    ip=machine.ip, 
                    installedupdate=machine.installedUpdate, 
                    os=machine.osName, 
                    osversion=machine.osVersion, 
                    oslang = machine.osLang,
                    rebootrequired = machine.rebootRequired,
                    lastscantime = machine.scancompletetime,
                    status = machine.status,
                    msg = machine.msg,
                    resourceid = machine.resourceID,
                    location = machine.location,
                    resourcename = machine.resourceName,
                    resourcegroupname = machine.resourceGroupName,
                    role = machine.role,
                    owner = machine.owner)
            except Exception as e:
                print('DB.save error: Azure Machine not found or save failed')
                LogHelper.append('DB.save error: Azure Machine not found or save failed')
    
    # delete VMs from table in case vm removed, but record is still there
    @classmethod
    def clear(DB, location, type='vm'):
        if type == 'vm':
            if location == 'sh':
                vmobj = SHVirtualMachine.objects.all()
            elif location == 'red':
                vmobj = REDVirtualMachine.objects.all()
        elif type == 'azm':
                vmobj = AzureVirtualMachine.objects.all()
        
        vmobj.delete()


    @classmethod
    def updateProperty(DB, machine, type, location, property):
        if type == 'hm':
            if location == 'sh':
                hmobj = SHHost
            elif location == 'red':
                hmobj = REDHost
            try:
                hm = hmobj.objects.get(machine_name=machine.machineName)
                if property == 'compliant':
                    hm.compliant = machine.compliant
                if property == 'lastcu':
                    hm.lastcu = machine.lastCU
                hm.save()
            except hmobj.DoesNotExist:
                print('DB.updateproperty error: host not found or save failed')
                LogHelper.append('DB.updateproperty error: host not found or save failed')
        elif type == 'vm':
            if location == 'sh':
                vmobj = SHVirtualMachine
            elif location == 'red':
                vmobj = REDVirtualMachine
            try:
                vm = vmobj.objects.get(vmid = machine.vmid)
                if property == 'compliant':
                    vm.compliant = machine.compliant
                if property == 'lastcu':
                    vm.lastcu = machine.lastCU
                vm.save()
            except Exception as e:
                print(str(e))
                LogHelper.append('update property error: update or create vm object failed')


    @classmethod
    def getlist(DB, type, location, scope):
        machinelist = []
        if type == 'hm':
            if location == 'sh':
                hmobj = SHHost
            elif location == 'red':
                hmobj = REDHost
            if scope == 'full':
                hms = hmobj.objects.filter(obsolete = False)
            elif scope == 'delta':
                hms = hmobj.objects.filter(Q(obsolete=False)&~Q(compliant=True))

            for hm in hms:
                machine = PhysicalMachine()
                #print(hm.machine_name)
                machine.machineName = hm.machine_name
                machine.owner = hm.owner
                machine.osName = hm.os
                machine.osVersion = hm.osversion
                machine.osLang = hm.oslang
                machine.installedUpdate = hm.installedupdate
                machine.lastCU = hm.lastcu
                machine.rebootRequired = hm.rebootrequired
                machine.compliant = hm.compliant
                machine.vms = hm.vms
                machinelist.append(machine)
            return machinelist

        elif type == 'vm':
            vmobj = None
            if location == 'sh':
                print('hello shanghai')
                vmobj = SHVirtualMachine
            elif location == 'red':
                print('hello redmond')
                vmobj = REDVirtualMachine
            if scope == 'full':
                vms = vmobj.objects.all()
            elif scope == 'delta':
                vms = vmobj.objects.filter(~Q(compliant=True))
            machinelist = []
            for vm in vms:
                machine = VirtualMachine()
                machine.machineName = vm.machine_name
                machine.domainName = vm.domainname
                machine.vmid = vm.vmid
                machine.osName = vm.os
                machine.osVersion = vm.osversion
                machine.osLang = vm.oslang
                machine.installedUpdate = vm.installedupdate
                machine.lastCU = vm.lastcu
                machine.rebootRequired = vm.rebootrequired
                machine.compliant = vm.compliant
                hm = vm.loc_host
                machine.hostName = hm.machine_name
                machinelist.append(machine)

            return machinelist



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