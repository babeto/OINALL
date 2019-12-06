import os
import subprocess

from Schedule.Machine import Machine
from Schedule.Config import Config
from WMIHelper import WMIHelper
from Schedule.Helper.CMDHelper import CMDHelper
from Schedule.Helper.LogHelper import LogHelper
from Schedule.Helper.PowerShellHelper import PowerShellHelper

class VirtualMachine(Machine):
    """description of class"""
    def __init__(self):
        super().__init__()
        self.userName = r'.\administrator'
        self.password = r'User@123'
        self.fullyQualifiedDomainName = None
        self.domainName = None
        self.machineName = None
        self.ip = None
        self.vmid=None
        self.hostName=None

    def setCredential(self):
        if self.domainName == None:
            self.userName = r'.\administrator'
            self.password = r'User@123'
        elif self.domainName == 'redmond' or self.domainName == 'fareast':
            self.userName = r'.\administrator'
            self.password = r'User@123'
        else:
            self.userName = ('\\').join([self.domainName,'administrator'])
            self.password = r'User@123'

    def getvmid():
        return self.vmid
    def getUser():
        return self.user
    def getHostName():
        return self.hostName


    def get_ip(self):
        if self.ip == None or CMDHelper.testconnection(self.ip) == False:
            print('try to get ip by powershell...')
            LogHelper.append("get {0} ip by powershell".format(self.machineName))
            self.ip = PowerShellHelper.getvmip(self.hostName, r'.\administrator', r'User@123', self.machineName)
            LogHelper.append("get {0} ip {1} by powershell".format(self.machineName, self.ip))
            if self.ip == None:
                return None

        return self.ip

    def set_credential(self):
        print(Config.account)
        for account in Config.account:
            print(account)
            if self.domainName == None:
                username = ('\\').join(['.', account['user']])
                password = account['password']
            elif self.domainName == 'redmond' or self.domainName == 'fareast':
                username = ('\\').join(['.', 'administrator'])
                password = 'User@123'
            else:
                username = ('\\').join([self.domainName, account['user']])
                password = account['password']
            if WMIHelper.accountverify(self.ip, username, password):
                self.userName = username
                self.password = password
                return True
        return False


    def getOSLang(self):
        self.osLang = super().getOSLang(self.ip, self.userName, self.password)
        return self.osLang

    def getRebootStatus(self):
        self.rebootRequired = WMIHelper.getRebootReg(self.ip, self.userName, self.password)
        return self.rebootRequired


    def getInstalledUpdate(self):
        if self.get_ip() == None:
            LogHelper.append("get update error ip/username/password not right {0}:{1} using {2}:{3} ".format(self.machineName, self.ip, self.userName, self.password))
            return None
        """
        if self.set_credential() == False:
            LogHelper.append("get update error ip/username/password not right {0}:{1} using {2}:{3} ".format(self.machineName, self.ip, self.userName, self.password))
            return None
        """
        cre = self.set_credential()
        self.getOSLang()
        LogHelper.append("try to get  {0}:{1} update using {2}:{3}".format(self.machineName, self.ip, self.userName, self.password))
        return super(VirtualMachine, self).getInstalledUpdate(self.ip, self.userName, self.password, self.osLang)

    def testconnection(self):
        log = CMDHelper.testconnection(self.ip)
        LogHelper.append("vm test ip connection {0}:{1} is {2}".format(self.machineName, self.ip, log))



    def invokeWUInstall(self):
        if self.get_ip() == None:
            LogHelper.append("invoke wuinstall error ip/username/password not right {0}:{1} using {2}:{3} ".format(self.machineName, self.ip, self.userName, self.password))
            return None
        """
        if self.set_credential() == False:
            LogHelper.append("get update error ip/username/password not right {0}:{1} using {2}:{3} ".format(self.machineName, self.ip, self.userName, self.password))
            return None
        """
        cre = self.set_credential()
        self.getOSLang()
        LogHelper.append("try to invoke wuinstall  {0}:{1} update using {2}:{3}".format(self.machineName, self.ip, self.userName, self.password))
        return super(VirtualMachine, self).invokeWUInstall(self.ip, self.userName, self.password)


    def getSqlVersion(self):
        self.sqlVersion = WMIHelper.get_sqlversion(self.ip, self.userName, self.password)
        return self.sqlVersion

    def getVSInstalled(self):
        self.vsInstalled = WMIHelper.check_VS(self.ip, self.userName, self.password)
        return self.vsInstalled

class mytest():
    pass