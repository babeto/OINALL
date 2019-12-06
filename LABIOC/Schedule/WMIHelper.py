import os
import sys
import time
import xml.dom.minidom as minidom
# need add this when test ,not in threading
sys.coinit_flags = 0
# support multiple threads of win32com
import pythoncom
import re
import traceback
from pprint import pprint


rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)

from Schedule.Helper.CMDHelper import CMDHelper
from Schedule.Helper.XMLHelper import XMLHelper
from Schedule.Helper.IPHelper import IPHelper


from win32com.client import GetObject
import wmi
import winreg
from Schedule.Helper.LogHelper import LogHelper

class WMIHelper(object):
    """description of class"""

    @staticmethod
    def executeWMIQuery(machinename, username, password, namespace, wql):
        result = None
        try:
            print(machinename)
            print(namespace)
            print(wql)
            pythoncom.CoInitialize()
            remotewmi = wmi.WMI(computer=machinename,user=username,password=password,namespace=namespace)
            result = remotewmi.query(wql)
        except Exception as e:
            print(str(e))
            LogHelper.append(' '.join([r'executeWMIQuery error:', str(e)]))
        finally:
            #pythoncom.CoUninitialize()
            return result
    
    @staticmethod
    def hypervexists(machinename, username, password):
        osname = WMIHelper.getMachineProperty(machinename, username, password, 'OSName')
        print(osname)
        namespace = WMIHelper.getVirtualizationNamespace(osname)
        result = None
        pythoncom.CoInitialize()
        try:
            remotewmi = wmi.WMI(computer=machinename,user=username,password=password,namespace=namespace)
            result = True
        except Exception as e:
            LogHelper.append(' '.join([r'hyperv namespace test error:', str(e)]))
            result = False
        finally:
            pythoncom.CoUninitialize()
            return result


    @staticmethod
    def getMachineProperty(machinename,username,password, property):
        result = None
        try:
            namespace = r"root\cimv2"
            if property == 'OSName':
                wql = "select Caption from Win32_OperatingSystem"
                print(wql)
                print(machinename)
                print(username)
                print(password)
                dt = WMIHelper.executeWMIQuery(machinename,username,password,namespace,wql)
                for wmiobj in dt:
                    result = wmiobj.Caption
            elif property == 'Version':
                wql = "select Version from Win32_OperatingSystem"
                dt = WMIHelper.executeWMIQuery(machinename,username,password,namespace,wql)
                for wmiobj in dt:
                    result = wmiobj.Version
            elif property ==  'OSLanguage':
                wql = "select OSLanguage from Win32_OperatingSystem"
                dt = WMIHelper.executeWMIQuery(machinename,username,password,namespace,wql)
                for wmiobj in dt:
                    result = wmiobj.OSLanguage
        except Exception as e:
            LogHelper.append(' '.join([r'getMachineOSName error:', str(e)]))

        return result


    @staticmethod
    def getVirtualizationNamespace(osName):
        if(osName.find('2008')>0):
            return r"root\virtualization"
        else:
            return r"root\virtualization\v2";

    @staticmethod
    def getAllVMsOnHost(hostname, username, password):
        osname = WMIHelper.getMachineProperty(hostname,username,password, 'OSName')
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
        # initialize VM properties
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
                            if IPHelper.available(ip):
                                vms[index].ip = ip
                                break
                    except Exception as e:
                        LogHelper.append(' '.join([r'getAllVMsOnHost get ip error:', str(e)]))
                        print(str(e))
                    try:
                        print("trying get OS Name...")
                        vms[index].osName = property_dict.get('OSName')
                        
                        vms[index].osVersion = property_dict.get('OSVersion')
                    except Exception as e:
                        print("get os name error")
                        LogHelper.append(' '.join([r'getAllVMsOnHost get OS Name error:', str(e)]))
                    try:
                        print("trying get domain name...")
                        vms[index].fullyQualifiedDomainName = property_dict.get('FullyQualifiedDomainName')
                        vms[index].domainName = vms[index].fullyQualifiedDomainName.split('.')[1]
                    except Exception as e:
                        print("get OS domain name error")
                        LogHelper.append(' '.join([r'getAllVMsOnHost get domain name error:', str(e)]))
                    try:
                        print("trying get OSVersion...")
                        vms[index].osVersion = property_dict.get('OSVersion')
                    except Exception as e:
                        print("get os Version error")
                        LogHelper.append(' '.join([r'getAllVMsOnHost get osversion error:', str(e)]))
        except Exception as e:
            LogHelper.append(' '.join([r'getAllVMsOnHost Initialize VM property error:', str(e)]))
        for vm in vms:
            print(vm.machineName)
            print(vm.vmid)
            print(vm.ip)
            print(vm.osName)
            print(vm.osVersion)
            print(vm.domainName)

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
            osname = WMIHelper.getMachineProperty(hostname,username,password, 'OSName')
            print(osname)
            virtualnamespace = WMIHelper.getVirtualizationNamespace(osname)
            print(virtualnamespace)
            wql = "SELECT GuestIntrinsicExchangeItems FROM Msvm_KvpExchangeComponent where SystemName='%s'" % vmid;
            dt = WMIHelper.executeWMIQuery(hostname,username,password,virtualnamespace,wql)
            property_dict = {}
            for idt in dt:
                #print(idt)
                propertyxml = idt.GuestIntrinsicExchangeItems
                #print(propertyxml)
                for eachpro in propertyxml:
                    #print(eachpro)
                    eachprodict = XMLHelper.parsexmltodict(eachpro)
                    property_dict.update(eachprodict)
                print(property_dict)
        except Exception as e:
            LogHelper.append(' '.join([r'getVMPropertyValue error:', str(e)]))
        #print(property)
        #print(property_dict.get(property))
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
        osname = WMIHelper.getMachineProperty(hostname,username,password, 'OSName')
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
        #pythoncom.CoInitialize()
        try:
            conn=wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2")
            cmd_call = r"cmd /c Powershell -Command \"Disable-PSRemoting\""
            id, value = conn.Win32_Process.Create(CommandLine=cmd_call)
            print(id,value)
        except Exception as e:
            print("disalbe WinRm failed")
            LogHelper.append("Disable Winrm failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            pass
            #pythoncom.CoUninitialize()

    @staticmethod
    def enableps(machinename, username, password):
        result = None
        conn = None
        pythoncom.CoInitialize()
        try:
            LogHelper.append("try to enable ps on {0} with {1}:{2}".format(machinename, username, password))
            conn=wmi.WMI(computer=machinename, user=username, password = password, namespace=r'root\cimv2')
        except Exception as e:
            print(str(e))
            LogHelper.append(str(conn))
            LogHelper.append("connect wmi failed on {0} with {1}:{2}".format(machinename, username, password))
            conn == None
            result == False
        if conn != None:
            """
            try:
                ## this need to be change, a service running can't be regarded as PS enabled
                svcs = conn.Win32_Service()
                for svc in svcs:
                    if svc.Name == 'WinRM' and svc.State == 'Running':
                        result = True
                        LogHelper.append("winrm service is running on {0} with {1}:{2}".format(machinename, username, password))
                        break
            except Exception as e:
                print(str(e))
                LogHelper.append("check winrm service failed on {0} with {1}:{2}".format(machinename, username, password))
            if result != True:
            """
            """
            try:
                cmd_call = "cmd /c PowerShell -Command \"Set-WSManQuickConfig -Force\""
                print(cmd_call)
                id, value = conn.Win32_Process.Create(CommandLine=cmd_call)
                print(id,value)
                watcher = conn.watch_for(notification_type="Deletion",
                    wmi_class="Win32_Process",
                    delay_secs=1,
                    ProcessId=id)
                LogHelper.append("waiting Set-WSManQuickConfig process {0} complete on {1}".format(id, machinename))
                try:
                    LogHelper.append("waiting 300 seconds Set-WSManQuickConfig process {0} complete on {1}".format(id, machinename))
                    error_log = watcher(timeout_ms=300000)
                    LogHelper.append(error_log)
                except wmi.x_wmi_timed_out:
                    pythoncom.PumpWaitingMessages()
                    LogHelper.append("timout out Set-WSManQuickConfig process {0} complete on {1} {2}".format(id, machinename, error_log))
                time.sleep(10)
            except Exception as e:
                print(str(e))
                LogHelper.append("Set-WSManQuickConfig failed on {0} with {1}:{2}".format(machinename, username, password))
            """
            try:
                cmd_call = "cmd /c PowerShell -Command \"Enable-PSRemoting -Force\""
                print(cmd_call)
                id, value = conn.Win32_Process.Create(CommandLine=cmd_call)
                print(id,value)
                watcher = conn.watch_for(notification_type="Deletion",
                    wmi_class="Win32_Process",
                    delay_secs=1,
                    ProcessId=id)
                LogHelper.append("waiting EnablePS process {0} complete on {1}".format(id, machinename))
                try:
                    LogHelper.append("waiting 300 seconds EnablePS process {0} complete on {1}".format(id, machinename))
                    error_log = watcher(timeout_ms=300000)
                    LogHelper.append(error_log)
                except wmi.x_wmi_timed_out:
                    pythoncom.PumpWaitingMessages()
                    LogHelper.append("timout out EnablePS process {0} complete on {1} {2}".format(id, machinename, error_log))

                time.sleep(30)
                LogHelper.append("enable ps succeed on {0} with {1}:{2}".format(machinename, username, password))
                result = True
            except Exception as e:
                print(str(e))
                LogHelper.append("enable PSRemoting failed on {0} with {1}:{2}".format(machinename, username, password))
                result = False

        pythoncom.CoUninitialize()
        return result


    @staticmethod
    def accountverify(machinename, username, password):
        pythoncom.CoInitialize()
        try:
            conn=wmi.WMI(computer=machinename, user=username, password = password, namespace=r'root\cimv2')
            LogHelper.append("accountverify succeed {0} with {1}:{2}".format(machinename, username, password))
            result = True
        except Exception as e:
            LogHelper.append("accountverify failed {0} with {1}:{2} {3}".format(machinename, username, password, str(e)))
            result = False
        finally:
            pythoncom.CoUninitialize()

        return result

    @staticmethod
    def getRebootReg(machinename, username, password):
        pythoncom.CoInitialize()
        try:
            r = wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2").StdRegProv
            HKLM = 0x80000002
            result, names = r.EnumKey(
                hDefKey=HKLM,
                sSubKeyName=r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update"
                )
            for key in names:
                print(key)
                if key == 'RebootRequired':
                    LogHelper.append("Reboot registry found {0}".format(key))
                    return True
            LogHelper.append("No registry found {0}".format(names))
            LogHelper.append("No registry found {0} with {1}:{2}".format(machinename,username,password))
            return False
        except Exception as e:
            print("check registry failed")
            LogHelper.append("Get registry failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            pythoncom.CoUninitialize()

    
    @staticmethod
    def getRegValue(machinename, username, password, regkey, regvalue):
        pythoncom.CoInitialize()
        try:
            r = wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2").StdRegProv
            HKLM = 0x80000002
            result, valuenames, types = r.EnumValues(
                hDefKey=HKLM,
                sSubKeyName=regkey
                )
            for valuename in valuenames:
                if valuename == regvalue:
                    LogHelper.append("Registry value found {0}".format(valuename))
                    result, value = r.GetStringValue(
                        hDefKey=HKLM,
                        sSubKeyName=regkey,
                        sValueName=regvalue)
                    return value
            LogHelper.append("No registry value found {0}".format(names))
            LogHelper.append("No registry value found {0} with {1}:{2}".format(machinename,username,password))
        except Exception as e:
            print("check registry failed")
            LogHelper.append("Get registry failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            #pythoncom.CoUninitialize()
            pass

    @staticmethod
    def enumRegValue(machinename, username, password, regkey):
        regkeyvalue = {}
        print(regkey)
        pythoncom.CoInitialize()
        try:
            r = wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2").StdRegProv
            print(regkey)
            pprint(r.__dict__)
            HKLM = 0x80000002
            result, valuenames, types = r.EnumValues(
                hDefKey=HKLM,
                sSubKeyName=regkey
                )
            print(valuenames)
            for valuename in valuenames:
                LogHelper.append("Registry value found {0}".format(valuename))
                result, value = r.GetStringValue(
                        hDefKey=HKLM,
                        sSubKeyName=regkey,
                        sValueName=valuename)
                regkeyvalue[valuename] = value
            print(regkeyvalue)
            return regkeyvalue
        except Exception as e:
            traceback.print_exc()
            print("check registry failed")
            LogHelper.append("Get registry failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            #pythoncom.CoUninitialize()
            pass

    @staticmethod
    def enum_namespace(machinename, username, password, namespace):
        pythoncom.CoInitialize()
        namespaces = None
        print(namespace)
        try:
            r = wmi.WMI(computer=machinename, user=username, password = password, namespace=namespace)
            wql = "SELECT * FROM __NAMESPACE"
            namespaces = r.query(wql)
            print(namespaces)
        except Exception as e:
            print("get namespace failed")
            LogHelper.append("Get wmi namespaces failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            #pythoncom.CoUninitialize()
            pass
        print(namespaces)
        return namespaces
            

    @staticmethod
    def get_sqlversion(machinename, username, password):
        rootnamespace = r'root\Microsoft\SqlServer'
        relativenamespace = None
        try:
            namespaces = WMIHelper.enum_namespace(machinename, username, password,rootnamespace)
            print(namespaces)
            for namespace in namespaces:
                print(namespace.Name)
                name_check = re.match(r'ComputerManagement[\d\d]?', namespace.Name)
                print(name_check)
                if name_check is None:
                    pass
                else:
                    relativenamespace = namespace.Name
                    fullnamespace = rootnamespace + '\\' + namespace.Name
                    print(fullnamespace)
                    wql = "SELECT PropertyStrValue FROM SqlServiceAdvancedProperty WHERE PropertyName='FILEVERSION' AND ServiceName='MSSQLSERVER'"
                    results = WMIHelper.executeWMIQuery(machinename,username,password,fullnamespace,wql)
                    for result in results:
                        patch_version = result.PropertyStrValue
                        return patch_version

        except Exception as e:
            print("get wmi sqlversion failed")
            LogHelper.append("Get wmi sqlversion failed {0} with {1}:{2}".format(machinename,username,password))
            pass

        try:
            rootreg = r'SOFTWARE\Microsoft\Microsoft SQL Server'
            instancenamekey = r'SOFTWARE\Microsoft\Microsoft SQL Server\Instance Names\SQL'
            reginstance = WMIHelper.enumRegValue(machinename, username, password, instancenamekey)
            for key in reginstance:
                instancekey = reginstance[key]
                print(instancekey)
            relativekey = instancekey + r'\Setup'
            print(relativekey)
            regvalue = 'PatchLevel'
            """
            if relativenamespace == 'ComputerManagement10':
                relativekey = r'\100\Tools\Setup'
            elif relativenamespace == 'ComputerManagement11':
                relativekey = r'\110\Tools\Setup'
            elif relativenamespace == 'ComputerManagement12':
                relativekey = r'\120\Tools\Setup'
            elif relativenamespace == 'ComputerManagement13':
                relativekey = r'\130\Tools\Setup'
            elif relativenamespace == 'ComputerManagement14':
                relativekey = r'\140\Tools\Setup'
            """
            regkey = rootreg + '\\' + relativekey
            patch_version = WMIHelper.getRegValue(machinename, username, password, regkey, regvalue)
            return patch_version
        except Exception as e:
            print("get reg sqlversion failed")
            LogHelper.append("Get reg sqlversion failed {0} with {1}:{2}".format(machinename,username,password))

    @staticmethod
    def check_VS(machinename, username, password):
        #pythoncom.CoInitialize()
        try:
            r = wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2").StdRegProv
            HKLM = 0x80000002
            HKCR = 0X80000000
            result, names = r.EnumKey(
                hDefKey=HKCR,
                sSubKeyName=r''
                )
            for key in names:
                key_check = re.match(r'VisualStudio.DTE.(\d|\d\d).(\d|\d\d)', key)
                if key_check is not None:
                    version = key_check.group()[17:]
                    print(version)
                    vsdevreg = r'SOFTWARE\Wow6432Node\Microsoft\DevDiv\vs\Servicing' + '\\' + version + '\\' + 'devenv'
                    try: 
                        result, names = r.EnumKey(
                            hDefKey=HKLM,
                            sSubKeyName=vsdevreg
                            )
                        for key in names:
                            return version
                    except Exception as e:
                        print("check vsdevreg registry failed")
                        LogHelper.append("Get vsdevreg registry failed {0} with {1}:{2}".format(machinename,username,password))
            #LogHelper.append("No registry found {0}".format(names))
            LogHelper.append("No VisualStudio.DTE registry found {0} with {1}:{2}".format(machinename,username,password))
            return False
        except Exception as e:
            print("check registry failed")
            LogHelper.append("Get registry failed {0} with {1}:{2}".format(machinename,username,password))
            return False
        finally:
            #pythoncom.CoUninitialize()
            pass

    # Reboot a remote machine
    # To do something this drastic to a remote system, the WMI script must take RemoteShutdown privileges, which means that you must specify them in the connection moniker. The WMI constructor allows you to pass in an exact moniker, or to specify the parts of it that you need. Use help on wmi.WMI.__init__ to find out more.
    # other_machine = "machine name of your choice"
    @staticmethod
    def rebootMachine(machinename, username, password):
        pythoncom.CoInitialize()
        try:
            conn = wmi.WMI(computer=machinename, user=username, password = password, namespace=r"root\cimv2")
            conn=wmi.WMI(computer=machinename,privileges=["RemoteShutdown"])
            os = conn.Win32_OperatingSystem (Primary=1)[0]
            os.Reboot ()
        except Exception as e:
            print("Reboot failed")
            LogHelper.append("reboot failed {0} with {1}:{2}".format(machinename,username,password))
        finally:
            pythoncom.CoUninitialize()


if __name__ == "__main__":
    print('start..')
    #WMIHelper.getvmip('CMSE-5665903', '.\Administrator', 'User@123', 'DW-Bench5-DC')
    #osname = WMIHelper.getMachineProperty('MSD-2880384', '.\Administrator', 'User@123', 'OSName')
    #print(osname)
    #WMIHelper.getvmip('SCCMEXTBLD-25', '.\Administrator', 'User@123', 'CMSE_SCUP_BUILD')
    #WMIHelper.getAllVMsOnHost('CMSE-5665903', '.\Administrator', 'User@123')
    #WMIHelper.enableps('novashafs01', '.\\administrator','User@123')
    #WMIHelper.disableps('novashafs01', '.\\administrator','User@123')
    #osname = WMIHelper.getVMPropertyValue('CMSE-5665903', '.\Administrator', 'User@123', 'DW-Bench4-CL1', '381c5a29-1c79-4278-b9b9-3a91ba02bc88', 'OSName')
    #print(osname)
    #namespaces = WMIHelper.enum_namespace('CMSE-5665903', '.\Administrator', 'User@123', 'root\\Microsoft\\SqlServer')
    #for name in namespaces:
    #    print(name.Name)
    patch = WMIHelper.get_sqlversion('10.177.45.49',r'.\Administrator', r'User@123')
    print(patch)
    patch = WMIHelper.check_VS('10.177.44.46',r'.\Administrator', r'User@123')
    print(patch)