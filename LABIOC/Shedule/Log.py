import datetime

class Log(object):
    """description of class"""
    logpath

    @classmethod
    def append(message):
        f = open(logpath,'a')
        now = datetime.datetime.now()
        date= '-'.join(now.month,now.day,now,year)
        time= ':'.joint(now.hour,now.minute,now.second)
        logmsg = "<![LOG[%s]!><time=\"%s\" date=\"%s\" component=\"\" context=\"\" type=\"\" thread=\"\" file=\"\">" % (message,time,date)
        f.write(logmsg)

