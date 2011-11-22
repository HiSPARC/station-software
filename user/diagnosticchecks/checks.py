import subprocess
import wmi
from socket import *
import time
import win32service
import win32serviceutil
import win32com.client
import os
import ConfigParser
import MySQLdb
import win32gui
from ctypes import c_ulong, byref, windll

CONFIG_INI = "/user/hsmonitor/data/config.ini"

OK = 0
WARNING = 1
CRITICAL = 2

localhost = gethostbyname("127.0.0.1") 

def checkBufferdb(warn=None, crit=None):
    if warn:
        wmin, wmax = warn
    if crit:
        cmin, cmax = crit
    
    config = ConfigParser.ConfigParser()

    try:
        config.read(CONFIG_INI)
        host = config.get('BufferDB', 'Host')
        user = config.get('BufferDB', 'Username')
        pwd = config.get('BufferDB', 'Password')
        db = config.get('BufferDB', 'DB')    
    except:
        print 'Could not read config.ini file!'
        return CRITICAL
    
    try:
        dbcon = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db)
    except MySQLdb.OperationalError, (errid, errmsg):
        print '%s (Error %d)' % (errmsg, errid)
        return CRITICAL

    cursor = dbcon.cursor()
    cursor.execute("SHOW TABLE STATUS LIKE 'message'")
    idx = [x[0] for x in cursor.description].index('Rows')
    num_events = cursor.fetchone()[idx]
    dbcon.close()
    print 'Buffer DB contains %d events' % num_events

    if crit:
        if not cmin <= num_events <= cmax:
            return CRITICAL
    if warn:
        if not wmin <= num_events <= wmax:
            return WARNING
    return OK

def check_lvusage(warn, crit):
    """
    Check the memory using Labview and also immediately give the cpu time.

    """
    w = wmi.WMI()
    wmin, wmax = warn
    cmin, cmax = crit
    LABVIEW_CAPTIONS = ['hisparcdaq.exe', 'HISPAR~1.EXE']

    for p in w.Win32_Process():
        if p.Name in LABVIEW_CAPTIONS:
            mem = float(p.WorkingSetSize) / (1024 * 1024.0)
            cpu = (float(p.UserModeTime) + float(p.KernelModeTime)) / 10000000.0
            
            print 'Memory usage: %.1f Mb' % mem
            print 'CPU time: %.2fs' % cpu
            
            if mem < cmin or mem > cmax:
                return CRITICAL
            elif mem < wmin or mem > wmax:
                return WARNING
            else:
                return OK

    # The process is not running.
    print 'Labview is not running'
    return CRITICAL
