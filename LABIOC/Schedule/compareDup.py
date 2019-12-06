
from PhysicalMachine import PhysicalMachine
from DB import DB
import re

class ImportHost(object):
    """description of class"""

    file = 'ExportedHost.txt'
    file2 = 'machinelist.txt'

    @classmethod
    def importhost(ImportHost):
        f = open(ImportHost.file)
        f.seek(0,0)
        taglist = []
        for each_line in f:
            
            hostarray = each_line.split()
            hostname = hostarray[0]
            tag = hostarray[2]
            if tag in taglist:
                print(tag)
            else:
                taglist.append(tag)
                
        f2 = open(ImportHost.file2)
        f.seek(0,0)
        taglist2 = []
        for each_line in f2:
            
            hostarray = each_line.split()
            hostname = hostarray[0]
            tag = hostarray[1]
            if tag in taglist2:
                print(tag)
            else:
                taglist2.append(tag)

        for tag in taglist:
            if tag not in taglist2:
                print(tag)

if __name__ == '__main__':

    ImportHost.importhost()

