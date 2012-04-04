#
#   StartUserMode.py ------
#   Start the HiSPARC user executables:
#    - MySQL
#    - LabVIEW Detector
#    - LabVIEW Weather
#    - HiSPARC Monitor
#    - HiSPARC Updater
#

import sys
import time
import os
import glob
import win32con
import ConfigParser

from startStop import StartStop, CMDStartStop, status, RUNNING, DISABLED
from hslog     import log, setLogMode, MODE_BOTH

def start():
    setLogMode(MODE_BOTH)
    log("\nStarting User-Mode applications...")

    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
         log("FATAL: environment variable HISPARC_ROOT not set!")
         return

    configFile = "%s/persistent/configuration/config.ini" % HS_ROOT
    config = ConfigParser.ConfigParser()
    config.read(configFile)

    try:
        #start MySQL
        log("Starting MySQL...")
        datapath = "%s/persistent/data/mysql" % HS_ROOT
        binlogs = glob.glob(os.path.join(datapath, "mysql-bin.*"))
        if binlogs:
            log("Removing stale MySQL binary logs...")
            for f in binlogs:
                os.remove(f)

        binary  = "mysqld.exe"
        exeBase = "%s/user/mysql/bin" % HS_ROOT
        program = "\"%(exec)s/%(binary)s\"" % {"exec": exeBase, "binary": binary}

        handler                  = StartStop()
        handler.exeName          = binary
        handler.ShowWindow       = win32con.SW_HIDE
        handler.command          = program
        handler.currentDirectory = HS_ROOT
        handler.title            = "MySQL server"

        res = handler.startProcess()
        if res == RUNNING:
            time.sleep(5)
            # check run-status again
            res = handler.probeProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while starting MySQL: " +
            str(sys.exc_info()[1]))

    try:
        #start LabVIEW detector
        log("Starting LabVIEW detector...")
        if config.getboolean("Detector", "Enabled"):
            handler                  = StartStop()
            handler.exeName          = "hisparcdaq.exe"
            handler.currentDirectory = "%s/user/hisparcdaq" % HS_ROOT
            handler.command          = "%s/user/hisparcdaq/hisparcdaq.exe" % HS_ROOT

            res = handler.startProcess()
        else:
            res = DISABLED
        log("Status: " + status(res))

    except:
        log("An exception was generated while starting LabVIEW detector: " +
            str(sys.exc_info()[1]))

    try:
        #start LabVIEW weather
        log("Starting LabVIEW weather...")
        if config.getboolean("Weather", "Enabled"):
            handler                  = StartStop()
            handler.exeName          = "hisparcweather.exe"
            handler.currentDirectory = "%s/user/hisparcweather" % HS_ROOT
            handler.command          = "%s/user/hisparcweather/hisparcweather.exe" % HS_ROOT

            res = handler.startProcess()
        else:
            res = DISABLED
        log("Status: " + status(res))

    except:
        log("An exception was generated while starting LabVIEW weather: " +
            str(sys.exc_info()[1]))

        # Introduce a 20-second pause to let MySQL start completely
        time.sleep(20)

    try:
        #start HSMonitor
        log("Starting HSMonitor...")
        handler = CMDStartStop()
        handler.exeName          = "python.exe"
        handler.title            = "HISPARC MONITOR: hsmonitor"
        handler.currentDirectory = "%s/user/hsmonitor" % HS_ROOT
        handler.command          = "%s/user/python/python.exe HsMonitor.py" % HS_ROOT

        res = handler.startProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while starting HSMonitor: " +
            str(sys.exc_info()[1]))

    try:
        #start updater
        log("Starting Updater...")
        handler = CMDStartStop()
        handler.exeName          = "python.exe"
        handler.title            = "HISPARC Updater: updater"
        handler.currentDirectory = "%s/user/updater" % HS_ROOT
        handler.command          = "%s/user/python/python.exe Update.py" % HS_ROOT

        res = handler.startProcess()
        log("Status: " + status(res))

    except:
        log("An exception was generated while starting the Updater: " +
            str(sys.exc_info()[1]))

start()
