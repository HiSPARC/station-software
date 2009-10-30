import subprocess
import wmi
from socket import*
import time
import win32service
import win32serviceutil
import win32com.client
import os
import ConfigParser
import MySQLdb
import win32gui
from hslog import *
from ctypes import c_ulong, byref, windll

CONFIG_INI = "\\user\\hsmonitor\\data\\config.ini"

# RETURN VALUES. 
OK = 0
WARNING = 1
CRITICAL = 2


localhost = gethostbyname("127.0.0.1") 


#------------------------------------------------------------------------------
#--------------------------------Check connection------------------------------
#------------------------------------------------------------------------------

def checkConnection():
    
    print 'Checking connection... Please wait...'
    print
    c = wmi.WMI ()

    # execute the code and pipe the result to a string
    test = "ping 4.2.2.2" #Pinging Global DNS Server 
    process = subprocess.Popen(test, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # give it time to respond
    time.sleep(10)
    process.wait()

    #print process.returncode
    if process.returncode == 0 :
        print 'Ping Successful... Internet connection O.K.'
        return OK
        
    else:
        print 'Ping failed... No internet connection'
        print 'Checking the network adapters...'
        print
        
        for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
            print interface.Description
            for ip_address in interface.IPAddress:
                if ip_address == '0.0.0.0':
                    print 'Connection not reachable...'
                else:
                    print ip_address
                    print interface.Caption
        return CRITICAL



#------------------------------------------------------------------------------
#--------------------------------Service checks--------------------------------
#------------------------------------------------------------------------------

def checkTightVNC():
    c = wmi.WMI()
    process=c.Win32_Process(name = "winVNC.exe")
    if process!=[]:
       return OK
    else:
        return CRITICAL
    

def checkNSClient():
    c = wmi.WMI()
    for s in c.Win32_Service():
        # check NSClient++ running
        if s.name == "NSClientpp":
            print s.DisplayName, "is ", s.State
            break
    if s.State == 'Running':
        return OK
    else:
        return CRITICAL

def checkHSMonitor():
	w = win32gui.FindWindow(None, "HISPARC MONITOR: hsmonitor")
	if w!=0:
		return OK
	else:
		return CRITICAL
	
def checkUpdater():
	w = win32gui.FindWindow(None, "HISPARC Updater: updater")
	if w!=0:
		return OK
	else:
		return CRITICAL
		

def checkOpenVPN():
    c = wmi.WMI()
    for s in c.Win32_Service():
        # check OpenVPN running
        if s.name == "OpenVPNService":
            print s.DisplayName, "is ", s.State
            break
    if s.State == 'Running':
        return OK
    else:
        return CRITICAL


def checkMySQLServer():
    c = wmi.WMI()
    process=c.Win32_Process(name = "mysqld.exe")
    if process!=[]:
       return OK
    else:
        return CRITICAL

def checkDAQ():
	c = wmi.WMI()
	process=c.Win32_Process(name = "hisparcdaq.exe")
	if process!=[]:
		return OK
	else:
		return CRITICAL
#----------------------------------------------------------------------------
#-------------------------------Port checks----------------------------------
#----------------------------------------------------------------------------

def checkVPNport():
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((localhost, 1194))
    if(result == 0) :
        print 'VPN Port %d is Open' % (1194,)
        return OK
    else:
        print 'VPN Port %d is not Open' % (1194,)
        return CRITICAL
    s.close()

def checkHTTPport():
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((localhost, 80))
    if(result == 0):
        print 'HTTP Port %d is Open' % (80,)
        return OK
    else:
        print 'HTTP Port %d is not Open' % (80,)
        return CRITICAL
    s.close()
    
def checkMySQLport():
    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((localhost, 3306))
    if(result == 0):
        print 'MySql Port %d is Open' % (3306,)
        return OK
    else:
        print 'MySql Port %d is not Open' % (3306,)
        return CRITICAL
    s.close()



 
#-----------------------------------------------------------------------------
#-----------------------------Firewall check----------------------------------
#-----------------------------------------------------------------------------

def checkFirewall():
    if win32serviceutil.QueryServiceStatus('SharedAccess', None) [1] == 4: #Service is running!
        
        if not groupPolicy():   #If firewall is not controled by the group policy
                                #Check local policy:
            objFirewall = win32com.client.Dispatch("HNetCfg.FwMgr")
            objPolicy = objFirewall.LocalPolicy
            objProfile = objPolicy.GetProfileByType(1)
            if objProfile.FirewallEnabled:
                print "Firewall Enabled"
                return OK
            else:
                print "Firewall Disabled"
                return CRITICAL
        else:
            print 'Firewall is controled by the group policy, \nPlease contact your network administrator!!!'
            return OK

    else:  #Firewall SERVICE is not running!!!
        print 'ACHTUNG, ACHTUNG, ACHTUNG!!! Firewall service is not running!!!'
        return CRITICAL #No firewall
        

def groupPolicy():
    oPipe = os.popen('netsh firewall show state')
    sLine = oPipe.read()
    words = sLine.split()

    ProfileEqDomain = 0
    GroupPolicyVersion = 0

    index = 0
    while 1:
        if words[index] == 'Profile':
            if words[index+2]=='Domain':
                ProfileEqDomain = 1
                index = index + 1
                
        if (words[index] == 'Group' and words[index+1] == 'policy' and words[index+2] == 'version'):
            if words[index+4] <> 'None':
                GroupPolicyVersion = 1
                index = index + 1
            else:
                index = index + 1           
        else:
            index = index + 1
        if index == len(words):
            break

    if (ProfileEqDomain and GroupPolicyVersion):
        return 1 #Firewall Enabled and controled by the group policy!!!
    else:
        return 0 #Firewall is NOT controled by the group policy!!!

#..........................................................................
#Checking Buffer connection
#..........................................................................


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
        pwd  = config.get('BufferDB', 'Password')
        db   = config.get('BufferDB', 'DB')    
    except:
        print 'Could not read config.ini file!'
        return CRITICAL
    
    try:
        dbcon = MySQLdb.connect( host=host,
                                 user=user,
                                 passwd=pwd,
                                 db=db
                                )
    except MySQLdb.OperationalError, (errid, errmsg):
        print '%s (Error %d)' % (errmsg, errid)
        return CRITICAL

    cursor = dbcon.cursor()
    cursor.execute('SELECT COUNT(*) FROM message')
    num_events = cursor.fetchone()[0]
    dbcon.close()
    print 'Buffer DB contains %d events' % num_events

    if crit:
        if not cmin <= num_events <= cmax:
            return CRITICAL
    if warn:
        if not wmin <= num_events <= wmax:
            return WARNING
    return OK

#..........................................................................
#Checking check_lvusage
#..........................................................................
	
def check_lvusage(warn, crit):
    """
	Check the memory using Labview and also immediately give the cpu time. 
    """
    w = wmi.WMI()
    
    wmin, wmax = warn
    cmin, cmax = crit
    LABVIEW_CAPTION = 'hisparcdaq'
	
    for p in w.Win32_Process():
        if p.Name.startswith(LABVIEW_CAPTION):
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

    # Het proces draait niet.
    print 'Labview is not running'
    return CRITICAL
