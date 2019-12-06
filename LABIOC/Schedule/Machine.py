import os
import sys
import subprocess

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
sys.path.append(rootPath)
sys.path.append(curPath)

#from Schedule.HyperV import HyperV
from Schedule.Update import Update
from WMIHelper import WMIHelper
from Schedule.Helper.LogHelper import LogHelper
from Schedule.Helper.PowerShellHelper import PowerShellHelper

class Machine(object):
    """description of class"""
    def __init__(self):
        self.systemName = None
        self.userName = None
        self.password = None
        self.osName = None
        self.osVersion = None
        self.osLang = None
        self.location = None
        self.rebootRequired = None
        self.installedUpdate = None
        self.lastCU = None
        self.scancompletetime = None
        self.compliant = None
        self.ip = None
        self.status = None
        self.msg = None
        self.sqlVersion = None
        self.vsInstalled = None

    def getMachineName(self):
        return self.machineName

    def getRebootRequired(self):
        return self.rebootRequired

    def getSystemName(self):
        return self.systemName

    def getOSLang(self, machinename, username, password):
        langID = WMIHelper.getMachineProperty(self.machineName, self.userName, self.password, 'OSLanguage')
        LogHelper.append(" {0} Local:{1}".format(machinename, langID))
        if langID == 1033:
            self.osLang = 'enu'
        elif langID == 2052:
            self.osLang = 'chs'
        elif langID == 1031:
            self.osLang = 'deu'

        return self.osLang

    def getRebootStatus(self, machinename, username, password):
        self.rebootRequired = WMIHelper.getRebootReg(machinename, username, password)
        return self.rebootRequired

    def reboot(self):
        WMIHelper.rebootMachine(self.machineName, self.userName, self.password)

    def getInstalledUpdate(self, machinename, username, password, lang='enu'):
        print("check PS Remoting on %s..." % machinename)
        if PowerShellHelper.testpsremoting(machinename, username, password) == True:
            pass
        else:
            if WMIHelper.enableps(machinename, username, password) == False:
                LogHelper.append("EnablePSRemoting failed {0}".format(machinename))
        print("get update on %s..." % machinename)
        updatelist = []
        try:
            LogHelper.append("Powershell: getUpdate for{0} {1} with {2}:{3}".format(self.machineName, machinename, username, password))
            updatelist = PowerShellHelper.getupdate(machinename, username, password, lang)
        except Exception as e:
            print(str(e))
            LogHelper.append("Powershell: getUpdate failed for{0} {1} with {2}:{3}".format(self.machineName, machinename, username, password))
        return updatelist

    def invokeWUInstall(self, machinename, username, password):
        print("check PS Remoting on %s..." % machinename)
        if PowerShellHelper.testpsremoting(machinename, username, password) == True:
            pass
        else:
            if WMIHelper.enableps(machinename, username, password) == False:
                LogHelper.append("EnablePSRemoting failed {0}".format(machinename))
        print("invokeWUInstall on %s..." % machinename)
        ret = ''
        try:
            ret = PowerShellHelper.invoke_wuinstall(machinename, username, password)
        except Exception as e:
            LogHelper.append(str(e))
            LogHelper.append("Powershell: invoke wuinstall failed for {0} {1} with {2}:{3}".format(self.machineName, machinename, username, password))
        return ret


    def getSqlVersion(self, machinename, username, password, lang='enu'):
        self.sqlVersion = WMIHelper.get_sqlversion(machinename, username, password)
        return self.sqlVersion

    def getVSInstalled(self, machinename, username, password, lang='enu'):
        self.VSInstalled = WMIHelper.check_VS(machinename, username, password)
        return self.VSInstalled


if __name__ == "__main__":
    vm = Machine()
    #vm.getInstalledUpdate('10.177.44.128', r' DW-Bench10\administrator', r'User@123')

    #vm.getInstalledUpdate('10.177.45.38', r'4013131dom\administrator', r'Elvis1')
    vm.getInstalledUpdate('10.177.45.7', r'R61156518DOM\administrator', r'Elvis1')