import re

class IPHelper(object):
    """description of class"""

    @classmethod
    def available(IPHelper,ip):
        regex = r'(10\.)(([0,1]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){2}([0,1]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])'
        if re.match(regex, ip):
            return True
        else:
            return False

if __name__ == '__main__':
    print(IPHelper.available('10.177.45.32'))
    print(IPHelper.available('10.156.213.2'))
    print(IPHelper.available('10.52.136.122'))
    print(IPHelper.available('10.5.156.212'))
    print(IPHelper.available('10.05.156.212'))
    print(IPHelper.available('10.005.6.02'))
    print(IPHelper.available('10.05.06.02'))
    print(IPHelper.available('10.9.9.0'))