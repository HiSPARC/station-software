#
#   CheckUserMode.py ------
#   Determine status of the HiSPARC user processes and admin services.
#

import os
import win32con
import ConfigParser

from startStop import StartStop, CMDStartStop, RUNNING, STOPPED, EXCEPTION, DISABLED, NOT_INSTALLED
from hslog     import log, setLogMode, MODE_BOTH

def pStdout(app, result):

    if result == RUNNING:
        status = "running"
    elif result == STOPPED:
        status = "stopped"
    elif result == EXCEPTION:
        status = "exception"
    elif result == DISABLED:
        status = "disabled"
    elif result == NOT_INSTALLED:
        status = "not installed"
    else:
        status = "unknown (%d)" % result

    info = "%(app)-20s: %(stat)s" %{"app": app, "stat": status}
    log(info)

def check():
    setLogMode(MODE_BOTH)
    log("\nChecking User-Mode applications...\n")

    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
         log("FATAL: environment variable HISPARC_ROOT not set!")
         return

    configFile = "%s/persistent/configuration/config.ini" % HS_ROOT
    config = ConfigParser.ConfigParser()
    config.read(configFile)

    try:
        #check MySQL
        app = "MySQL"
        handler         = StartStop()
        handler.exeName = "mysqld.exe"
        res = handler.probeProcess()
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check LabVIEW Detector
        app = "LabVIEW Detector"
        if config.getboolean("Detector", "Enabled"):
            handler         = StartStop()
            handler.exeName = "hisparcdaq.exe"
            res = handler.probeProcess()
        else:
            res = DISABLED
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check LabVIEW Weather
        app = "LabVIEW Weather"
        if config.getboolean("Weather", "Enabled"):
            handler         = StartStop()
            handler.exeName = "hisparcweather.exe"
            res = handler.probeProcess()
        else:
            res = DISABLED
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check HSMonitor
        app = "HSMonitor"
        handler       = CMDStartStop()
        handler.title = "HISPARC MONITOR: hsmonitor"
        res = handler.probeProcess()
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check Updater
        app = "Updater"
        handler       = CMDStartStop()
        handler.title = "HISPARC Updater: updater"
        res = handler.probeProcess()
    except:
        res = EXCEPTION
    pStdout(app, res)

    log("\nChecking Admin-Mode services...\n")

    try:
        #check TightVNC
        app = "TightVNC"
        handler             = StartStop()
        handler.serviceName = "tvnserver"
        res = handler.probeService()
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check NAGIOS
        app = "NAGIOS"
        handler             = StartStop()
        handler.serviceName = "NSClientpp"
        res = handler.probeService()
    except:
        res = EXCEPTION
    pStdout(app, res)

    try:
        #check OpenVPN
        app = "OpenVPN"
        handler             = StartStop()
        handler.serviceName = "OpenVPNService"
        res = handler.probeService()
    except:
        res = EXCEPTION
    pStdout(app, res)

    log("\n")

check()
