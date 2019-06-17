import os
import sys
import xml.dom.minidom as minidom

rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)

from Schedule.Helper.CMDHelper import CMDHelper
from Schedule.Helper.XMLHelper import XMLHelper


from win32com.client import GetObject
import wmi
from Schedule.Helper.LogHelper import LogHelper

class WMIHelper(object):
    """description of class"""

    @staticmethod
    def executeWMIQuery(machinename, username, password, namespace, wql):
        try:
            print(machinename)
            print(namespace)
            print(wql)
            remotewmi = wmi.WMI(computer=machinename,user=username,password=password,namespace=namespace)
            return remotewmi.query(wql)
        except Exception as e:
            LogHelper.append(' '.join([r'executeWMIQuery error:', str(e)]))
    
    @staticmethod
    def hypervexists(machinename, username, password):
        osname = WMIHelper.getMachineOSName(machinename, username, password)
        namespace = WMIHelper.getVirtualizationNamespace(osname)
        try:
            remotewmi = wmi.WMI(computer=machinename,user=username,password=password,namespace=namespace)
            return True
        except Exception as e:
            LogHelper.append(' '.join([r'hyperv namespace test error:', str(e)]))
            return False

    @staticmethod
    def getMachineOSName(machinename,username,password):
        try:
            namespace = r"root\cimv2"
            wql = "select Caption from Win32_OperatingSystem"
            dt = WMIHelper.executeWMIQuery(machinename,username,password,namespace,wql)
            for wmiobj in dt:
                return wmiobj.Caption
        except Exception as e:
            LogHelper.append(' '.join([r'getMachineOSName error:', str(e)]))

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
        # this query only return VMs in running
        # wql = "SELECT Name, Elementname FROM Msvm_ComputerSystem where EnabledState=2 and Caption='Virtual Machine'"
        # this query return all VMs including turned off VMs
        wql = "SELECT Name, Elementname FROM Msvm_ComputerSystem where Caption='Virtual Machine'"        
        vms = []

        try:
            from VirtualMachine import VirtualMachine
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            for idt in dt:
                vm = VirtualMachine()
                vm.vmid = idt.Name
                print(vm.vmid)
                vm.machineName = idt.ElementName
                print(vm.machineName)
                vm.hostName = hostname
                print(vm.hostName)
                vms.append(vm)
        except Exception as e:
            LogHelper.append(' '.join(['getAllVMsOnHost error:', str(e)]))
        print(len(vms))
        try:
            wql = "SELECT SystemName, GuestIntrinsicExchangeItems FROM Msvm_KvpExchangeComponent"
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)

            for idt in dt:
                for index, vm in enumerate(vms):
                    if vm.vmid != idt.SystemName:
                        continue
                        # print(vm.vmid)
                        # print(idt.SystemName)
                    property_dict = {}
                    propertyxml = idt.GuestIntrinsicExchangeItems
                    #print(idt)
                    for eachpro in propertyxml:
                        eachprodict = XMLHelper.parsexmltodict(eachpro)
                        property_dict.update(eachprodict)
                    try:
                        print("trying get IP address...")
                        ips = property_dict.get('RDPAddressIPv4')
                        iparray = ips.split(';')
                        for ip in iparray:
                            if CMDHelper.testconnection(ip):
                                vms[index].ip = ip
                                break
                    except Exception as e:
                        LogHelper.append(' '.join([r'getAllVMsOnHost get ip error:', str(e)]))
                        print(str(e))
                        continue
                    finally:
                        try:
                            print("trying get OS...")
                            vms[index].osName = property_dict.get('OSName')
                        except Exception as e:
                            LogHelper.append(' '.join([r'getAllVMsOnHost get os error:', str(e)]))

        except Exception as e:
            LogHelper.append(' '.join([r'getAllVMsOnHost get ip error:', str(e)]))
        for vm in vms:
            print(vm.machineName)
            print(vm.vmid)
            print(vm.ip)
            print(vm.osName)

        return vms

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
            property_dict = {}
            for idt in dt:
                print(idt)
                propertyxml = idt.GuestIntrinsicExchangeItems
                print(propertyxml)
                for eachpro in propertyxml:
                    print(eachpro)
                    eachprodict = XMLHelper.parsexmltodict(eachpro)
                    property_dict.update(eachprodict)
                print(property_dict)
        except Exception as e:
            LogHelper.append(' '.join([r'getVMPropertyValue error:', str(e)]))
        print(property)
        print(property_dict.get(property))
        return property_dict.get(property)

    @staticmethod
    def getvmip(hostname,username,password,vmname):
        try:
            vmid = WMIHelper.getvmid(hostname, username, password,vmname)
            print(vmid)
            ips = WMIHelper.getVMPropertyValue(hostname, username, password, vmname, vmid, 'RDPAddressIPv4')
            print(ips)
            iparray = ips.split(';')
            for ip in iparray:
                if CMDHelper.testconnection(ip):
                    print(ip)
                    return ip
        except Exception as e:
            LogHelper.append(' '.join([r'getvmip error:', str(e)]))
        return None

    @staticmethod
    def getvmid(hostname, username,password, vmname):
        osname = WMIHelper.getMachineOSName(hostname,username,password)
        virtualnamespace = WMIHelper.getVirtualizationNamespace(osname)
        wql = "SELECT Name FROM Msvm_ComputerSystem where EnabledState=2 and Caption='Virtual Machine' and Elementname ='%s'" %vmname
        print(wql)
        try:
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            for idt in dt:
                vmid = idt.Name
                return vmid
        except Exception as e:
            LogHelper.append(' '.join([r'getvmid error:', str(e)]))

    @staticmethod
    def disableps(machinename, username, password):
        conn=wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2")
        cmd_call = r"cmd /c Powershell -Command \"Disable-PSRemoting\""
        id, value = conn.Win32_Process.Create(CommandLine=cmd_call)
        print(id,value)

    @staticmethod
    def enableps(machinename, username, password):
        try:
            conn=wmi.WMI(computer=machinename, user=username, password = password, namespace=r'root\cimv2')
            cmd_call = r"cmd /c PowerShell -Command \"Enable-PSRemoting -Force\""
            id, value = conn.Win32_Process.Create(CommandLine=cmd_call)
            print(id,value)
            print('enableRePS succeed')
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    print('start..')
    # WMIHelper.getVMPropertyValue('MSD-2880384', '.\Administrator', 'User@123', 'DW-Bench9-S1', '39C9FDA7-AC81-485A-81ED-18C60DAB7EE0', 'RDPAddressIPv4')
    # WMIHelper.getvmip('CMSE-5665903', '.\Administrator', 'User@123', 'DW-Bench9-S1')
    # WMIHelper.getAllVMsOnHost('MSD-2880384', '.\Administrator', 'User@123')
    