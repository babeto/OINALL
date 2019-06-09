from win32com.client import GetObject
import wmi


class WMIHelper(object):
    """description of class"""

    @classmethod
    def executeWMIQuery(machineName, Username, Password, Namespace, Wql):
        remoteWmi = wmi.WMI(computer='machineName',user='Username',Password='Passord',namespace='Namespace')
        return remoteWmi.query(Wql)

    @classmethod
    def getVMIP(machineName, Username, Password, VMName):
        pass