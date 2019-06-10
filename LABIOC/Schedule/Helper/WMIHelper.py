import os
import sys

rootPath = os.path.abspath(os.path.join(os.getcwd(),"../.."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)

from Schedule.VirtualMachine import VirtualMachine

from win32com.client import GetObject
import wmi
from Schedule.Helper.LogHelper import LogHelper

class WMIHelper(object):
    """description of class"""

    @staticmethod
    def executeWMIQuery(machineName, username, password, namespace, wql):
        remoteWmi = wmi.WMI(computer=machineName,user=username,password=password,namespace=namespace)
        return remoteWmi.query(wql)
    
    @staticmethod
    def getMachineOSName(machinename,username,password):
        try:
            namespace = r"root\cimv2"
            wql = "select Caption from Win32_OperatingSystem"
            dt = WMIHelper.executeWMIQuery(machinename,username,password,namespace,wql)
            for wmiobj in dt:
                return wmiobj.Caption
        except Exception as e:
            LogHelper.append(str(e))

    @staticmethod
    def getHostVMNameAndID(hostname, hostosname, username, password):
        try:
            virtualnamespace = WMIHelper.getVirtualizationNamespace(hostosname)
        except Exception as e:
            LogHelper.append(str(e))

    @staticmethod
    def getVirtualizationNamespace(osName):
        if(osName.find('2008')>0):
            return r"root\virtualization"
        else:
            return r"root\virtualization\v2";

    @staticmethod
    def getAllVMsOnHost(hostname, username, password):
        osname = WMIHelper.getMachineOSName(hostname,username,password)
        virtualnamespace = WMIHelper.getVirtualizationNamespace(osname)
        wql = "SELECT Name, Elementname FROM Msvm_ComputerSystem where EnabledState=2 and Caption='Virtual Machine'"
        vms = []
        try:
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            vm = VirtualMachine()
            for idt in dt:
                vm.VMID = idt.Name
                print(vm.VMID)
                vm.machineName = idt.ElementName
                print(vm.machineName)
                vm.hostName = hostname
                print(vm.hostName)
                vms.append(vm)
            return vms
        except Exception as e:
            LogHelper.append(str(e))


    """propertyName:
    FullyQualifiedDomainName, OSName, OSVersion, OSMajorVersion, OSMinorVersion, OSBuildNumber, OSPlatformId, 
    ServicePackMajor, ServicePackMinor, SuiteMask, ProductType, OSVendor, OSSignature, OSEditionId, ProcessorArchitecture, 
    IntegrationServicesVersion, NetworkAddressIPv4, NetworkAddressIPv6, RDPAddressIPv4, RDPAddressIPv6
    """
    @staticmethod
    def getVMPropertyValue(hostname, username, password, vmname, vmid, property):
        try:
            print('getvmproperty')
            osname = WMIHelper.getMachineOSName(hostname,username,password)
            print(osname)
            virtualnamespace = WMIHelper.getVirtualizationNamespace(osname)
            print(virtualnamespace)
            wql = "SELECT GuestIntrinsicExchangeItems FROM Msvm_KvpExchangeComponent where SystemName='%s'" % vmid;
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            for idt in dt:
                print(idt)
                propertyxml = idt.GuestIntrinsicExchangeItems
        except Exception as e:
            LogHelper.append(str(e))

    @staticmethod
    def getVMID(hostname, hostosname, vmname):
        virtualnamespace = WMIHelper.getVirtualizationNamespace(hostosname)

if __name__ == "__main__":
    print('start..')
    WMIHelper.getVMPropertyValue('CMSE-5665903', '.\Administrator', 'User@123', 'DW-Bench9-S1', '017345F8-F255-46E4-9A5C-855B430FC72E', 'RDPAddressIPv4')
