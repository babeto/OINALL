
from Schedule.Machine import Machine

class VirtualMachine(Machine):
    """description of class"""
    def __init__(self):
        super().__init__()
        self.machineName = None
        self.ip = None
        self.vmid=None
        self.hostName=None
        self.user=None
        self.password=None

    def getvmid():
        return self.vmid
    def getUser():
        return self.user
    def getHostName():
        return self.hostName

    def getInstalledUpdate(self):
        if self.ip == None:
            return None
        else:
            return super(VirtualMachine, self).getInstalledUpdate(self.ip, self.userName, self.password)

class mytest():
    pass