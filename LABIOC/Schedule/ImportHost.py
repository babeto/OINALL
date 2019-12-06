
from PhysicalMachine import PhysicalMachine
from DB import DB
import re

class ImportHost(object):
    """description of class"""

    file = 'machinelist.txt'

    @classmethod
    def importhost(ImportHost):
        f = open(ImportHost.file)
        f.seek(0,0)
        j = 0 
        for each_line in f:
            
            hostarray = each_line.split('\t')
            hostname = hostarray[0]
            hm = PhysicalMachine()
            hm.machineName = hostname
            try:
                hm.owner = r'Lab'
                print(hm.owner)
            except Exception as e:
                print('owner of {0} not set'.format(hostname))
            if hm.owner == None:
                hm.owner = r'Lab'
            hmlist = DB.getlist('hm','sh','full')
            i = 0
            for host in hmlist:
                i += 1
                if host.machineName == hostname:
                    break
                elif i == len(hmlist):
                    DB.save(hm, 'hm', 'sh')
                    j += 1
                    print("{0}, {1}".format(j, hostname))


if __name__ == '__main__':

    ImportHost.importhost()

