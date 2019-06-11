import os
import sys
import xml.dom.minidom as minidom
# test ip
import subprocess
import re


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
                print(propertyxml)
                property_dict = {}
                for eachpro in propertyxml:
                    print(eachpro)
                    eachprodict = WMIHelper.parsexmltodict(eachpro)
                    property_dict.update(eachprodict)
                print(property_dict)
        except Exception as e:
            LogHelper.append(str(e))
        return property_dict[property]


    @staticmethod
    def testconnection(ip):
        p = subprocess.Popen(["ping.exe ", ip],stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
        out = p.stdout.read()
        # out maybe different on locliazed os, need decode like print(out.decode('gbk')), so just check TTL
        regex = re.compile("TTL=(\d+)", re.IGNORECASE)
        ttllist = regex.findall(str(out))
        if ttllist:
            return True
        else:
            return False


    @staticmethod
    def getvmip(hostname,username,password,vmname):
        vmid = WMIHelper.getvmid(hostname, username, password,vmname)
        ips = WMIHelper.getVMPropertyValue(hostname, username, password, vmname, vmid, 'RDPAddressIPv4')
        iparray = ips.split(';')
        for ip in iparray:
            if WMIHelper.testconnection(ip):
                return ip
        return None

    @staticmethod
    def getvmid(hostname, username,password, vmname):
        osname = WMIHelper.getMachineOSName(hostname,username,password)
        virtualnamespace = WMIHelper.getVirtualizationNamespace(osname)
        wql = "SELECT Name FROM Msvm_ComputerSystem where EnabledState=2 and Caption='Virtual Machine' and Elementname ='%s" %vmname
        try:
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            for idt in dt:
                vmid = idt.Name
                return vmid
        except Exception as e:
            LogHelper.append(str(e))

    @staticmethod
    def parsexmltodict(xmldt):
        dom = minidom.parseString(xmldt)
        eroot = dom.documentElement
        itemlist = eroot.getElementsByTagName('PROPERTY')
        for item in itemlist:
            print(item)
            if item.getAttribute('NAME') == 'Data':
                elements = item.getElementsByTagName('VALUE')
                try:
                    value = elements[0].firstChild.nodeValue
                except Exception as e:
                    value = None
                    LogHelper.append(str(e))
                continue

            if item.getAttribute('NAME') == 'Name':
                elements = item.getElementsByTagName('VALUE')
                try:
                    key = elements[0].firstChild.nodeValue
                    print(key)
                except Exception as e:
                    key = None
                    LogHelper.append(str(e))
                continue

        dtdict = {key:value}
        return dtdict



if __name__ == "__main__":
    print('start..')
    WMIHelper.getVMPropertyValue('CMSE-5665903', '.\Administrator', 'User@123', 'DW-Bench9-S1', '017345F8-F255-46E4-9A5C-855B430FC72E', 'RDPAddressIPv4')
