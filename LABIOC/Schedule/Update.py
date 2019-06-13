
class Update(object):
    """description of class"""
    def __init__(self):
        self.updateTitle=None
        self.updateKB=None
        self.installedDate=None

    def tojson(self):
        updatedict = {'updateTitle':self.updateTitle,'updateKB':self.updateKB,'installedDate':self.installedDate}
        return updatedict