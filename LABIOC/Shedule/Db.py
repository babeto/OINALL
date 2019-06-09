import sys, os, django


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
print(rootPath)
sys.path.append(rootPath)
sys.path.append(curPath)
#os.chdir(rootPath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LABIOC.settings")
django.setup()


from Helper import JsonHelper
import Update
import subprocess

from LA.models import SHHost
"""
from LA.models import SHVirtualMachine
from LA.models import REDHost
from LA.models import REDVirtualMachine
"""
#class Machine(object):
#class Machine(object):
#    """description of class"""

Scan = ".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1"
GetIP = ".\\PowerShellScripts\\GetVMIP.ps1"

def getVMIP(machineobj,username,password,vmobj):
    args=[r"powershell",r"PowerShellScripts\\GetVMIP.ps1",r"-MachineName",machineobj, r"-Username",username,r"-Password", password, r"-VMName",vmobj]
    try:
        p=subprocess.Popen(args,stdout=subprocess.PIPE)
        dt=p.stdout.read()
        return dt
    except Exception as e:
        print(e)
        return e

def enablePSRemote(machineobj,username,password):
    pass

def executePSScript(psscript,username,password):
    pass
def getupdate(machineobj):
    args=[r"PowerShell",r".\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machineobj,r"-Username", r".\administrator",r"-Password", r"User@123"]
    try:
        p=subprocess.Popen(args,stdout=subprocess.PIPE)
        dt=p.stdout.read()
        return dt
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    """
    dt=getupdate('cmse-4198321')
    print(dt)
    """

    ip = getVMIP('CMSE-5665903','.\\administrator','User@123','valvin1810EC1')
    print(ip)
    dt=getupdate(ip)
    print(dt)
    updateList = JsonHelper.parseJson(dt)
    print(updateList)