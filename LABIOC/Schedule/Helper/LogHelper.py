import datetime

class LogHelper(object):
    """description of class"""
    logpath = r"C:\repos\OINALL\LABIOC\Schedule\sch.log"

    @classmethod
    def append(LogHelper,message):
        f = open(LogHelper.logpath,'a')
        now = datetime.datetime.now()
        year = '%04d' %now.year
        month = '%02d' %now.month
        day = '%02d' %now.day
        hour = '%02d' %now.hour
        minute = '%02d' %now.minute
        second = '%02d' %now.second
        date = '-'.join(LogHelper.tostr([month, day, year]))
        time = ':'.join([hour,minute, second])
        time = ''.join([time, r'.000+000'])
        logmsg ="<![LOG[%s]LOG]!><time=\"%s\" date=\"%s\" component=\"\" context=\"\" type=\"\" thread=\"\" file=\"\"> \n" % (message,time,date)
        f.writelines(logmsg)


    @classmethod
    def tostr(LogHelper, numlist):
        strlist = [str(i) for i in numlist]
        return strlist

    @classmethod
    def formatlogdtime(datetime):
        pass