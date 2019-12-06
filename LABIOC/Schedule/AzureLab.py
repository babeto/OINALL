import os
import sys
import subprocess
import re
import json


curpath = os.path.abspath(os.getcwd())
sys.path.append(curpath)

print(sys.path)

from AzureMachine import AzureMachine
from DB import DB

class AzureLab(object):
    """description of class"""


    DB.clear(location = '', type ='azm')
    AzureMachines = []
    args = [r'Powershell',r'.\\PowerShellScripts\\GetAzureVM.ps1']

    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    dt = p.stdout.read()

    dt = dt.decode(encoding='utf-8')

    print(dt)

    regex = r'[[](.*?)[]]'

    dt_check = re.search(regex, dt, re.DOTALL)

    dt = dt_check.group()
    allmachines = json.loads(dt)
    print(type(allmachines))
    
    for obj in allmachines:
        azm = AzureMachine()
        print(obj)
        
        azm.machineName = obj["Name"]
        azm.resourceID = obj["ResourceId"]
        azm.resourceName = obj["ResourceName"]
        azm.resourceGroupName = obj["ResourceGroupName"]
        Tags = obj["Tags"]
        if Tags != None:
            try:
                azm.role = Tags["Role"]
            except Exception as e:
                pass
            try:
                azm.owner = Tags["Owner"]
            except Exception as e:
                pass
        AzureMachines.append(azm)
    

    for azm in AzureMachines:
        DB.save(azm,'azm','')
