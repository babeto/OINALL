# test ip
import subprocess
import re

class CMDHelper(object):
    """description of class"""

    @staticmethod
    def testconnection(ip):
        p = subprocess.Popen(["ping.exe ", ip],stdin = subprocess.PIPE,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
        out = p.stdout.read()
        # out maybe different on locliazed os, need decode like print(out.decode('gbk')), so just check TTL
        regex = re.compile("TTL=(\d+)", re.IGNORECASE)
        ttllist = regex.findall(str(out))
        if ttllist:
            return True
        else:
            return False