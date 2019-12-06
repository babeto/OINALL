import os
import sys
import subprocess

curpath = os.path.abspath(os.getcwd())
sys.path.append(curpath)
print(sys.path)

from Machine import Machine
from Config import Config
from WMIHelper import WMIHelper
from Helper.CMDHelper import CMDHelper
from Helper.LogHelper import LogHelper
from Helper.PowerShellHelper import PowerShellHelper

class AzureMachine(Machine):
    """description of class"""
    def __init__(self):
        super().__init__()
        self.userName = r'administrator'
        self.password = r'User@123'
        self.fullyQualifiedDomainName = None
        self.domainName = None
        self.machineName = None
        self.ip = None
        self.hostName = None
        self.resourceID = None
        self.location = None
        self.resourceName = None
        self.resourceGroupName = None
        self.role = None
        self.owner = None

    def set_credential(self):
        print(Config.account)
        for account in Config.account:
            print(account)
            if self.domainName == None:
                username = ('\\').join(['.', account['user']])
                password = account['password']
            elif self.domainName == 'redmond' or self.domainName == 'fareast':
                username = ('\\').join(['.', 'administraor'])
                password = 'User@123'
            else:
                username = ('\\').join([self.domainName, account['user']])
                password = account['password']
            if WMIHelper.accountverify(self.ip, username, password):
                self.userName = username
                self.password = password
                return True
        return False