import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LABIOC.settings")
django.setup()

import subprocess


from LA import models
"""
from LA.models import SHVirtualMachine
from LA.models import REDHost
from LA.models import REDVirtualMachine
"""
#class Machine(object):
#class Machine(object):
#    """description of class"""

Scan = ".\\shedule\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1"
GetIP = ".\\sheduleTask\\PowerShellScripts\\GetVMIP.ps1"

def getVM(machineobj):
    pass
def getVMIP(machineobj):
    pass
def enablePSRemote(machineobj):
    pass

def executePSScript(psscript):
    pass
def getupdate(machineobj):
    try:
        args=[r"PowerShell",r".\\schedule\\PowerShellScripts\\ScanAllInstalledHotfixes.ps1",r"-MachineName", machineobj,r"-Username", r".\administrator",r"-Password", r"User@123"]
        print(args)
        p=subprocess.Popen(args,stdout=subprocess.PIPE)
        dt=p.stdout.read()
        return dt
    except Exception as e:
        print(e)
if __name__ == "__main__":
    dt=getupdate('10.10.64.103')
    print(dt)