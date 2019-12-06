

class HyperV(object):
    """description of class"""
    def __init__(self):
        self.installed=None
        self.namespace=None

    def getallVMs(machineName):
        pass

    @classmethod
    def getVirtualizationNamespace(osName): 
        if(osName.find('2008')>0):
            return r"root\virtualization"
        else:
            return r"root\virtualization\v2";

    def  getVMProperty(property):
        pass