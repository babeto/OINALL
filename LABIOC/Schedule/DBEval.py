from datetime import datetime
from datetime import timedelta
import re
from DB import DB
import json
import threading
import time

class DBEval(object):
    """description of class"""

    win_prefix = "Security Monthly Quality Rollup for Windows"

    win10_prefix = "Cumulative Update for Windows"

    
    langpre = {
               "enu":{"winpre":"Security Monthly Quality Rollup for Windows", 
                      "win10pre":"Cumulative Update for Windows"},
               "deu":{"winpre":"Monatliches Sicherheitsqualit",
                     "win10pre":"Cumulative Update for Windows"},
               "chs":{"winpre":"月度安全质量汇总",
                     "win10pre":"累积更新"},
               "bak":{"winpre":"Monatliches Sicherheitsqualitätsrollup für Windows",
                      "win10pre":"Cumulative Update for Windows"}
               }

    now = datetime.now()
    year = now.year
    month = now.month

    datepre = "%4d-%02d"% (year, month)

    MonthlyTitle = ''

    monthregex = ''

    @classmethod
    def getMonthRegex(DataEval, osVersion, lang='enu'):
        now = datetime.now()
        year = now.year
        month = now.month
        datepre = "%4d-%02d"% (year, month)
        dateregex = DBEval.to_unicode_regex(datepre)
        if DataEval.versionCompare("10.0.0", osVersion) == 1:
            print("win10 below")
            title = DBEval.langpre[lang].get('winpre')
        elif DataEval.versionCompare("10.0.0", osVersion) == -1:
            print("win10 above")
            title = DBEval.langpre[lang].get('win10pre')

        monthpre = r'[' + datepre + r']' + r'[' + title + r']'
        monthregex = DBEval.to_unicode_regex(monthpre)
        DataEval.monthregex = monthregex
        print(monthregex)
        return monthregex
    
    @classmethod
    def getCURegex(DataEval, osVersion, lang='enu'):
        if DataEval.versionCompare("10.0.0", osVersion) == 1:
            print("win10 below")
            title = DBEval.langpre[lang].get('winpre')
        elif DataEval.versionCompare("10.0.0", osVersion) == -1:
            print("win10 above")
            title = DBEval.langpre[lang].get('win10pre')
        cutitle = r'[(20\d\d-(0[1-9])|(1[0,2]))]'+ r'[' + title + r']'
        curegex = DBEval.to_unicode_regex(cutitle)
        return curegex

    @classmethod
    def getTitle(DataEval, osVersion, lang='enu'):
        if DataEval.versionCompare("10.0.0", osVersion) == 1:
            print("win10 below")
            title = DBEval.langpre[lang].get('winpre')
           
        elif DataEval.versionCompare("10.0.0", osVersion) == -1:
            print("win10 above")
            title = DBEval.langpre[lang].get('win10pre')
            
        return title
    
    
    
    @classmethod
    def getTitleRegex(DataEval, osVersion, lang='enu'):
        if DataEval.versionCompare("10.0.0", osVersion) == 1:
            print("win10 below")
            title = DBEval.langpre[lang].get('winpre')
            titleregex = DBEval.to_unicode_regex(title)
        elif DataEval.versionCompare("10.0.0", osVersion) == -1:
            print("win10 above")
            title = DBEval.langpre[lang].get('win10pre')
            titleregex = DBEval.to_unicode_regex(title)
        return titleregex

    @classmethod
    def to_unicode_regex(DBEval, string):
        ret = ''
        for v in string:
            ret = ret + hex(ord(v)).upper().replace('0X', '\\\\\\\\u')

        ret = r'\'' + ret + r'\''

        return ret.encode()


    @classmethod
    def evalMachines(DataEval, type, location, scope='full'):
        print("start evaluation:")
        machinelist = DB.getlist(type, location, scope)
        for machine in machinelist:
            print(machine.machineName)
            osVersion = machine.osVersion
            print(osVersion)
            osLang = machine.osLang
            if osLang == None:
                osLang = 'enu'
            if osVersion is None or osVersion == []:
                continue
            #monthregex = DBEval.getMonthRegex(osVersion, osLang)
            titleregex = DBEval.getTitleRegex(osVersion, osLang)
            title = DBEval.getTitle(osVersion, osLang)
            print(titleregex)
            #curegex = DBEval.getCURegex(osVersion, osLang)
            #machine.compliant = DBEval.evalUpdate(machine.installedUpdate, monthregex)
            cuInstalled = DBEval.evalMonthCU(machine.installedUpdate, title)
            print(machine.rebootRequired)
            if cuInstalled == True and machine.rebootRequired != True:
                machine.compliant = True
            else:
                machine.compliant = False
            machine.lastCU = DBEval.evalProperty(machine.installedUpdate, title, 'lastcu')
            DB.updateProperty(machine, type, location, 'compliant')
            DB.updateProperty(machine, type, location, 'lastcu')
            print(machine.lastCU)


    @classmethod
    def evalProperty(DBEval, updatelist, titleregex, property):
        if updatelist is None or updatelist == "\[\]":
            print("skipped empty update")
        elif property == 'compliant':
            print("try evaluate")
            updates = json.loads(updatelist)
            print(type(updates))
            if (type(updates) == list):
                for update in updates:
                    if update['updateTitle'].find(' '.join([DBEval.datepre, regex])) == 0:
                        return True
            elif type(updates) == dict:
                if updates['updateTitle'].find(' '.join([DBEval.datepre, titleregex]))  >= 0:
                    return True
            else:
                pass
        else:
            print("evaluate last CU...")
            updates = json.loads(updatelist)
            print(type(updates))
            lastCU = ''
            if (type(updates) == list):
                print("will list the updates")
                for update in updates:
                    if DBEval.titlecompare(update['updateTitle'], lastCU, titleregex) == 1:
                        lastCU = update['updateTitle']
            elif type(updates) == dict:
                if DBEval.titlecompare(updates['updateTitle'], lastCU, titleregex) == 1:
                    lastCU = update['updateTitle']
            print('last cu is' + lastCU)
            return lastCU


    @classmethod
    def evalUpdate(DBEval,updatelist,monthregex):
        if updatelist is None or updatelist == "\[\]":
            print("skipped empty update")
        else:
            print("try evaluate")
            updates = json.loads(updatelist)
            print(type(updates))
            monthregex = monthregex.decode('unicode_escape')
            print(monthregex)
            myre = re.compile(monthregex, re.UNICODE)
            if (type(updates) == list):
                for update in updates:
                    update_check = myre.search(update['updateTitle'])
                    if update_check != None:
                        return True
            elif type(updates) == dict:
                update_check = myre.search(updates['updateTitle'])
                if update_check != None:
                        return True
            else:
                pass
        return False
    
    @staticmethod
    def getTuesday(year, month):
        firstweekday = datetime(year, month, 1).weekday()
        if firstweekday <= 1:
            secondtuesday = datetime(year, month, 1) + timedelta(days =  7 - (firstweekday+1) + 2 )
        else:
            secondtuesday = datetime(year, month, 1) + timedelta(days =  14 - (firstweekday+1) + 2 )
        
        return secondtuesday
    
    
    @classmethod
    def evalMonthCU(DBEval,updatelist, title):
        now = datetime.now()
        year = now.year
        month = now.month
        secondtuesday = DBEval.getTuesday(year, month)
        print("Patch Tuesday time {0}".format(secondtuesday))
        print("Today is {0}".format(now))
        if now >=secondtuesday:
            dateregex = r'%4d-%02d' %(year, month)
        else:
            dateregex = r'%4d-%02d' %(year, month-1)
        #titleregex = titleregex.decode('unicode_escape')
        print(dateregex)
        if updatelist is None or updatelist == "\[\]":
            print("skipped empty update")
        else:
            print("try evaluate")
            updates = json.loads(updatelist)
            print(type(updates))
            #myre = re.compile(titleregex, re.UNICODE)
            if (type(updates) == list):
                for update in updates:
                    title_check = re.search(title, update['updateTitle'])
                    date_check = re.match(dateregex, update['updateTitle'])
                    if title_check != None and date_check != None:
                        return True
            elif type(updates) == dict:
                title_check = re.search(title, updates['updateTitle'])
                date_check = re.match(dateregex, updates['updateTitle'])
                if title_check != None and date_check != None:
                    return True
            else:
                pass
        return False

    
    @classmethod
    def titlecompare(DBEval, u1, u2, title):
        
        daterx = r'\[20\d\d\-\(0\[1-9\]\)|\(1\[0,2\]\)\]'
        
        #curx = r'\[\(20\d\d\-\(0\[1-9\]\)|\(1\[0,2\]\)\)\]'+titleregex.decode('unicode_escape')
        #curx = DBEval.getCURegex(DataEval, osVersion, lang)
        #print(curegex)
        #cure = re.compile(curegex, re.UNICODE)
        #datere = re.compile(daterx, re.UNICODE)
        """
        if titlepre == "Cumulative Update for Windows":
            titlerx = r'20\d\d\-(0[1-9])|(1[0,2]) Cumulative Update for Windows'
        else:
            titlerx = r'20\d\d\-(0[1-9])|(1[0,2]) Security Monthly Quality Rollup for Windows'
        """
        #print(curegex)
        #print(u1)
        #print(titleregex)
        #titleregex = titleregex.decode('unicode_escape')
        #myre = re.compile(titleregex, re.UNICODE)
        u1_check = re.search(title, u1)
        u2_check = re.search(title, u2)
        if u1_check is None:
            #print("u1 not a CU......")
            return -1
        elif u2_check is None:
            #print("u2 not a CU......")
            return 1
        else:
            #print("start to get later one CU")
            u1_check = re.match(daterx, u1)
            u2_check = re.match(daterx, u2)
            if u1_check is None or u2_check is None:
                print("title compare: format not right")
                return 0
            compare = DBEval.datecompare(u1_check.group(), u2_check.group())
            if compare == 1:
                return 1
            elif compare == -1:
                return -1
            else:
                return 0



    @classmethod
    def versionCompare(DataEval, v1, v2):
        regex = r'\d+(\.\d+){0,2}'
        v1_check = re.match(regex, v1)
        v2_check = re.match(regex, v2)
        print(v1_check.group())
        print(v2_check.group())
        if v1_check is None or v2_check is None or v1_check.group() != v1 or v2_check.group() != v2:
            print("here")
            return "Version style not correct, it should be like x.x.x"
        v1_list = v1.split('.')
        v2_list = v2.split('.')
        v1_len = len(v1_list)
        v2_len = len(v2_list)
        if v1_len > v2_len:
            for i in range(v1_len - v2_len):
                v2_list.append('0')
        elif v1_len < v2_len:
            for i in range(v2_len - v1_len):
                v2_list.append("0")
        else:
            pass

        for i in range(len(v1_list)):
            if int(v1_list[i]) > int(v2_list[i]):
                return 1
            if int(v1_list[i]) < int(v2_list[i]):
                return -1
        return 0



    @classmethod
    def datecompare(DBEval,d1, d2):
        regex = r'20\d\d\-(0[1-9])|(1[0-2])'
        d1_check = re.match(regex, d1)
        d2_check = re.match(regex, d2)
        if d1_check is None or d1_check is None or d1_check.group() !=d1 or d2_check.group() != d2:
            print("date format not correct")
            return "date format not correct"
        d1_list = d1.split('-')
        d2_list = d2.split('-')
        d1_len = len(d1_list)
        d2_len = len(d2_list)
        if d1_len > d2_len:
            for i in range(d1_len - d2_len):
                d2_list.append(0)
        elif d1_len < d2_len:
            for i in range(d2_len - d1_len):
                d1_list.append(0)
        else:
            pass
        for i in range(d1_len):
            if int(d1_list[i]) > int(d2_list[i]):
                return 1
            if int(d1_list[i]) < int(d2_list[i]):
                return -1
        return 0

    


    @classmethod
    def titlecompareX(DBEval, u1, u2, curegex):
        
        daterx = r'20\d\d\-(0[1-9])|(1[0,2])'
        curegex = r'20\d\d\-(0[1-9])|(1[0,2])'
        #curx = r'\[\(20\d\d\-\(0\[1-9\]\)|\(1\[0,2\]\)\)\]'+titleregex.decode('unicode_escape')
        #curx = DBEval.getCURegex(DataEval, osVersion, lang)
        #print(curegex)
        cure = re.compile(curegex, re.UNICODE)
        #datere = re.compile(daterx, re.UNICODE)
        """
        if titlepre == "Cumulative Update for Windows":
            titlerx = r'20\d\d\-(0[1-9])|(1[0,2]) Cumulative Update for Windows'
        else:
            titlerx = r'20\d\d\-(0[1-9])|(1[0,2]) Security Monthly Quality Rollup for Windows'
        """
        #print(curegex)
        #print(u1)

        u1_check = cure.search(u1)
        u2_check = cure.search(u2)
        if u1_check is None:
            #print("no u1...")
            return -1
        elif u2_check is None:
            #print("no u2......")
            return 1
        else:
            print("start to get later one CU")
            u1_check = re.match(daterx, u1)
            u2_check = re.match(daterx, u2)
            if u1_check is None or u2_check is None:
                print("title compare: format not right")
                return 0
            compare = DBEval.datecompare(u1_check.group(), u2_check.group())
            if compare == 1:
                return 1
            elif compare == -1:
                return -1
            else:
                return 0

if __name__ == '__main__':
    u = DBEval.to_unicode("月度安全质量汇总")
    print(u)
