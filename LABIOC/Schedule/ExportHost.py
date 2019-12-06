
from PhysicalMachine import PhysicalMachine
from DB import DB
import re

class ExportHost(object):
    """description of class"""

    file = 'exportedhost.txt'

    @classmethod
    def exporthost(ExportHost):
        f = open(ExportHost.file, 'w')
        f.seek(0,0)
        j = 0

        hmlist = DB.getlist('hm','sh','full')
        for host in hmlist:
            j += 1
            tag = re.search('\d+', host.machineName)
            print(host.machineName + ' ' + host.owner + ' ' + tag.group() + '\n')
            f.write(host.machineName + ' ' + host.owner + ' ' + tag.group() + '\n')


if __name__ == '__main__':

    ExportHost.exporthost()

