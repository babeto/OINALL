import os
import sys

rootPath = os.path.abspath(os.path.join(os.getcwd(),"../.."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)


import traceback
import re

from Schedule.WMIHelper import WMIHelper 
from Schedule.Helper.OutputHelper import OutputHelper
from Schedule.Helper.LogHelper import LogHelper
import subprocess
import json

class PowerShellHelper(object):
    """description of class"""

    @staticmethod
    def testpsremoting(machinename, username, password):
        args=[r"PowerShell",r".\\PowerShellScripts\\TestPSRemoting.ps1",r"-MachineName", machinename, r"-Username" , username ,r"-Password", password]
        print(args)
        print('Powershell TestPSRemoting for {0}'.format(machinename))
        try:
            p = subprocess.Popen(args,stdout=subprocess.PIPE)
            dt = p.stdout.read()
            dt = dt.decode(encoding='utf-8')
            dt = int(dt)
            if(dt == 1):
                return True
        except Exception as e:
            print("Powershell TestPSRemoting Exception " + str(e))
            LogHelper.append("Powershell TestPSRemoting exception for {0}".format(machinename))
        return False



    @staticmethod
    def getvmip(hostname, username, password, vmname):
        vmname = '\''+ vmname + '\''
        args=[r"PowerShell",r".\\PowerShellScripts\\GetVMIP.ps1",r"-MachineName", hostname, r"-Username" , username ,r"-Password", password, r'-VMName', vmname]
        print(args)
        print('Powershell getvmip for {0} on {1}'.format(vmname, hostname))
        try:
            p = subprocess.Popen(args,stdout=subprocess.PIPE)
            dt = p.stdout.read()
            LogHelper.append(dt)
            dt = dt.decode(encoding='utf-8')
            ip = dt.strip()
            if ip == '':
                print('ip not found')
                return None
            else:
                return ip
        except Exception as e:
            print("powershell getvmip exception " + str(e))
            LogHelper.append("getvmip failed for {0}".format(vmname))
            return None
    
    @staticmethod
    def getupdate(machinename, username, password, lang='enu'):
        print("scan %s started..."% machinename)
        #LogHelper.append("Powershell:try to scan {0} with account {1}:{2}".format(machinename, username, password))
        args=[r"PowerShell",r".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machinename, r"-Username" ,username ,r"-Password", password]
        print(args)
        updateinfo = []
        try:
            p=subprocess.Popen(args,stdout=subprocess.PIPE)
            dt=p.stdout.read()
            #print(dt)
            # this is a byte string start with b', contains data with different encoding like gbk
            # windows-1250, will be handled in OutputHelper
            if lang == 'enu':
                dt = dt.decode('utf-8', errors = 'ignore')
            elif lang == 'chs':
                dt = dt.decode('gbk', errors = 'ignore')
            elif lang == 'deu':
                dt = dt.decode('windows-1250', errors = 'ignore')
            #print(dt)
            if dt != None:
                updatelist = OutputHelper.parseJson(dt)
            else:
                updatelist = None
            print('%s updates' %machinename)
            for update in updatelist:
                updateinfo.append(update.todict())
                #print(update.updateTitle)
        except Exception as e:
            print(traceback.print_exc())
            LogHelper.append("Powershell: getUpdate failed for{0} with {1}:{2}".format(machinename, username, password))
        return json.dumps(updateinfo)

    @staticmethod
    def invoke_wuinstall(machinename, username, password):
        args=[r'Powershell', r'.\\PowerShellScripts\\ScheduleWUJob.ps1', r'-MachineName', machinename, r'-Username', username, r'-Password', password]
        print(args)
        try:
            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            dt=p.stdout.read()
            LogHelper.append(dt)
        except Exception as e:
            traceback.print_exc()
            LogHelper.append("Powershell: Shedule WUJob failed for{0} with {1}:{2}".format(machinename, username, password))
        return dt
        




if __name__ == '__main__':
    ip = PowerShellHelper.getvmip('CMSE-5665903', r'.\administrator', r'User@123', 'DW-Bench5-DC')
    print(ip)
    #WMIHelper.enableps('MSD-2880384', 'Administrator', r'user@123')
    #update = PowerShellHelper.getupdate('CMSE-5665903', r'.\Administrator', r'User@123')
    #print(update)

    #update = PowerShellHelper.getupdate('CMSE-5665903', r'.\Administrator', r'User@123')
    #print(update)
    #Y = PowerShellHelper.testpsremoting('CMSE-5665903', r'.\Administrator', r'User@123')
    #print(Y)
