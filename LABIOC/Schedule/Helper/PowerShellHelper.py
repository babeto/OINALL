from Helper.MyJsonHelper import MyJsonHelper
import subprocess

class PowerShellHelper(object):
    """description of class"""
    @staticmethod
    def getvmip(hostname, username, password, vmname):

        args=[r"PowerShell",r".\\PowerShellScripts\\GetVMIP.ps1",r"-MachineName", hostname, r"-Username" , username ,r"-Password", password, r'-VMName', vmname]
        print('trying to get ip by ')
        try:
            p = subprocess.Popen(args,stdout=subprocess.PIPE)
            dt = str(p.stdout.read())
            ip = dt[2:-5]
            if ip == '':
                print('ip not found')
                return None
            else:
                return ip
        except Exception as e:
            print(str(e))
    
    @staticmethod
    def getupdate(machinename, username, password):
        print("scan %s started..."% machinename)
        args=[r"PowerShell",r".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machinename, r"-Username" ,username ,r"-Password", password]
        print(args)
        updateinfo = []
        try:
            p=subprocess.Popen(args,stdout=subprocess.PIPE)
            dt=p.stdout.read()
            # print(dt)
            if dt != None:
                updatelist = MyJsonHelper.parseJson(dt)
            else:
                updatelist = None
            print('%s updates' %machinename)
            for update in updatelist:
                updateinfo.append(update.tojson())
                print(update.updateTitle)
        except Exception as e:
            print(str(e))
        return updateinfo
