 # -*- coding:utf-8 -*-  
import os
import sys

import threading
from django.utils import timezone
import time
import pythoncom

lock = threading.Lock()

rootPath = os.path.abspath(os.path.join(os.getcwd(),".."))
sys.path.append(rootPath)
print(rootPath)
print(sys.path)

from PhysicalMachine import PhysicalMachine
from VirtualMachine import VirtualMachine
from DB import DB
from DBEval import DBEval
from Email import Email
from Report import Report

class Lab(object):
    """description of class"""

    physicalmachines = []

    phymachinfo = []

    shphmlist = []

    redphmlist = []

    vmsinfo = []

    machinelist = []

    @classmethod
    def startscan(Lab, type, location, scope='full'):
        Lab.machinelist = []
        if type == 'hm':
            hmlist = DB.getlist(type, location, scope)
            for host in hmlist:
                if(host.osName == None or host.osVersion == None):
                    hm = PhysicalMachine(host.machineName)
                else:
                    hm = host
                Lab.machinelist.append(hm)
        elif type == 'vm':
            if scope == 'delta':
                Lab.machinelist = DB.getlist(type, location, scope)
            elif scope == 'full':
                print('Full scan , clear all VM record before scan')
                DB.clear(location, 'vm')
                print('read host before scan vm')
                hostlist = DB.getlist('hm', location, 'full')
                hmthreads = []
                for host in hostlist:
                    if(host.osName == None or host.osVersion == None):
                        hm = PhysicalMachine(host.machineName)
                    else:
                        hm = host
                    th = threading.Thread(target = Lab.getvms, args=(hm,'hm',))
                    th.start()
                    hmthreads.append(th)
                for th in hmthreads:
                    th.join()
        for m in Lab.machinelist:
            print(m.machineName)
        Lab.scanconcurrent(Lab.machinelist, type, location)


    @classmethod
    def getvms(Lab, machine, type):
        if type != 'hm':
            return None
        vms = machine.getallvms()
        lock.acquire()
        Lab.machinelist.extend(vms)
        lock.release()
        return machine.vms

    @classmethod
    def scansave(Lab, machine, type, location):
        if type == 'hm':
            #Get OS every time in case Server OS is rebuild
            #if(machine.osName == None):
            machine.getOSName()
            machine.getOSVersion()
        #machine.testconnection()
        
        machine.installedUpdate = machine.getInstalledUpdate()
        machine.rebootRequired = machine.getRebootStatus()
        machine.sqlVersion = machine.getSqlVersion()
        machine.vsInstalled = machine.getVSInstalled()
        machine.scancompletetime = timezone.now()
        machine.compliant = False
        DB.save(machine, type, location)
        
    @classmethod
    def scanconcurrent(Lab, machinelist, type, location):
        scanthreads = []
        for machine in machinelist:
            #Lab.scansave(machine, type, location)
            
            print("start scan %s ..." %machine.machineName)
            print(" OS of {0} is {1}".format(machine.machineName,machine.osName))
            th = threading.Thread(target = Lab.scansave,args = (machine, type, location,))
            th.start()
            scanthreads.append(th)
        for th in scanthreads:
            th.join()
            print("scan completed...")




    @classmethod
    def startwuinstall(Lab, type, location, scope='full'):
        if type == 'hm':
            Lab.machinelist = DB.getlist(type, location, scope)
        elif type == 'vm':
            if scope == 'delta':
                Lab.machinelist = DB.getlist(type, location, scope)
            elif scope == 'full':
                print('read host before scan vm')
                hostlist = DB.getlist('hm', location, 'full')
                hmthreads = []
                for host in hostlist:
                    if(host.osName == None or host.osVersion == None):
                        hm = PhysicalMachine(host.machineName)
                    else:
                        hm = host
                    th = threading.Thread(target = Lab.getvms, args=(hm,'hm',))
                    th.start()
                    hmthreads.append(th)
                for th in hmthreads:
                    th.join()
        for m in Lab.machinelist:
            print(m.machineName)
        Lab.wuinstallconcurrent(Lab.machinelist, type, location)



    @classmethod
    def wuinstallconcurrent(Lab, machinelist, type, location):
        scanthreads = []
        for machine in machinelist:
            #Lab.scansave(machine, type, location)
            
            print("start wuinstall %s ..." %machine.machineName)
            print(" OS of {0} is {1}".format(machine.machineName,machine.osName))
            th = threading.Thread(target = Lab.wuinstall,args = (machine, type, location,))
            th.start()
            scanthreads.append(th)
        for th in scanthreads:
            th.join()
            print("wuinstall completed...")

    @classmethod
    def reboot(Lab, type, location, scope='full'):
        Lab.machinelist = DB.getlist(type, location, scope)
        threads =[]
        for m in Lab.machinelist:
            if m.rebootRequired == True and m.machineName != "MSD-2880384" and m.machineName != "HJColllect":
                print(m.machineName)
                th = threading.Thread(target = Lab.machinereboot, args = (m,))
                th.start()
                threads.append(th)
        for th in threads:
            th.join()
    
    @classmethod
    def machinereboot(Lab, machine):
        machine.reboot()

    @classmethod
    def wuinstall(Lab, machine, type, location):
        if type == 'hm':
            if(machine.osName == None):
                 machine.getOSName()
                 machine.getOSVersion()
        #machine.testconnection()
        
        machine.status = machine.invokeWUInstall()

        #DB.save(machine, type, location)

    @classmethod
    def testvm(Lab, host, location, vmname):
        host = PhysicalMachine(host)
        vms = Lab.getvms(host, 'hm')
        for vm in vms:
            if vm.machineName == vmname:
                Lab.scansave(vm, 'vm', location)

    @classmethod
    def testhm(Lab, host, location):
        hm = PhysicalMachine(host)
        Lab.scansave(hm, 'hm', location)


if __name__ == "__main__":
    #print("start...")
    #Lab.testvm('CMSE-5665903','red', 'zhonglWin7-1')
    #Lab.testhm('STBC-1531334', 'sh')
    #DBEval.evalMachines('hm','sh', 'full')
    """
    Lab.reboot("hm",'sh','full')
    Lab.reboot("vm",'sh','full')
    Lab.reboot("hm",'red','full')

    Lab.reboot("vm",'red','full')
    """

    """
    Lab.startscan('hm','sh', 'full')
    DBEval.evalMachines('hm','sh', 'full')

    #Lab.startscan('vm','sh', 'full')
    #DBEval.evalMachines('vm','sh', 'full')
    """
    #Lab.startscan('hm','red', 'full')
    #DBEval.evalMachines('hm','red', 'full')

    #Lab.startscan('vm','red', 'full')
    #DBEval.evalMachines('vm','red','full')


    #Lab.startscan('hm','sh', 'delta')
    #DBEval.evalMachines('hm','sh', 'delta')

    #Lab.startscan('vm','sh', 'delta')
    #DBEval.evalMachines('vm','sh', 'delta')
    
    Lab.startscan('hm','red', 'delta')
    DBEval.evalMachines('hm','red', 'delta')
    
    Lab.startscan('vm','red', 'delta')
    DBEval.evalMachines('vm','red','delta')
    
    """
    Lab.startscan('hm','sh', 'delta')
    DBEval.evalMachines('hm','sh', 'delta')

    Lab.startwuinstall('hm','sh', 'delta')
    #Lab.startwuinstall('vm','sh', 'delta')

    Lab.startwuinstall('hm','red', 'delta')
    Lab.startwuinstall('vm','red', 'delta')
    """

    """
    Lab.startwuinstall('hm','sh', 'full')
    Lab.startwuinstall('vm','sh', 'full')
    Lab.startwuinstall('hm','red', 'full')
    Lab.startwuinstall('vm','red', 'full')
    """
    """
    Lab.startwuinstall('hm','sh', 'full')
    Lab.startwuinstall('vm','sh', 'full')
    Lab.startwuinstall('hm','red', 'full')
    Lab.startwuinstall('vm','red', 'full')
    """

