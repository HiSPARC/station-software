"""Start the HiSPARC user executables:

These applications are started:
LabVIEW DAQ, LabVIEW Weather, LabVIEW Lightning, MySQL, HiSPARC Monitor, HiSPARC Updater

"""

import time
import os
import glob
import win32con
import ConfigParser
import logging

import startstop_logger
from startStop import StartStop, CMDStartStop, status, RUNNING, DISABLED

logger = logging.getLogger('startstop.startuser')


def start():
    logger.info("Starting User-Mode applications...")

    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
        logger.critical("FATAL: environment variable HISPARC_ROOT not set!")
        return

    configFile = os.path.join(HS_ROOT, "persistent/configuration/config.ini")
    config = ConfigParser.ConfigParser()
    config.read(configFile)

    try:
        logger.info("Starting MySQL...")
        datapath = os.path.join(HS_ROOT, "persistent/data/mysql")
        binlogs = glob.glob(os.path.join(datapath, "mysql-bin.*"))
        if binlogs:
            logger.info("Removing stale MySQL binary logs...")
            for f in binlogs:
                os.remove(f)

        binary = "mysqld.exe"
        # Were the extra quotes in the path string required?
        program = os.path.join(HS_ROOT, "user/mysql/bin", binary)

        handler = StartStop()
        handler.exeName = binary
        # Check if MySQL is already running
        res = handler.probeProcess()
        if res == RUNNING:
            delay_monitor = 0
        else:
            delay_monitor = 10
            handler.ShowWindow = win32con.SW_HIDE
            handler.command = program
            handler.currentDirectory = HS_ROOT
            handler.title = "MySQL server"

            res = handler.startProcess()
            if res == RUNNING:
                time.sleep(5)
                # check run-status again
                res = handler.probeProcess()
        logger.info("Status: %s", status(res))
    except:
        logger.exception("An exception was generated while starting MySQL")

    try:
        logger.info("Starting HiSPARC Detector...")
        if config.getboolean("Detector", "Enabled"):
            handler = StartStop()
            handler.exeName = "HiSPARC DAQ.exe"
            handler.currentDirectory = os.path.join(HS_ROOT, "user/hisparcdaq")
            handler.command = os.path.join(HS_ROOT,
                                           "user/hisparcdaq/HiSPARC DAQ.exe")
            res = handler.startProcess()
        else:
            res = DISABLED
        logger.info("Status: %s", status(res))
    except:
        logger.exception("An exception was generated while starting "
                         "HiSPARC Detector")

    try:
        logger.info("Starting HiSPARC Weather...")
        if config.getboolean("Weather", "Enabled"):
            handler = StartStop()
            handler.exeName = "HiSPARC Weather Station.exe"
            handler.currentDirectory = os.path.join(HS_ROOT,
                                                    "user/hisparcweather")
            handler.command = os.path.join(HS_ROOT, "user/hisparcweather",
                                           "HiSPARC Weather Station.exe")
            result = handler.startProcess()
        else:
            result = DISABLED
        logger.info("Status: %s", status(result))
    except:
        logger.exception("An exception was generated while starting "
                         "HiSPARC Weather")

    try:
        logger.info("Starting HiSPARC Lightning...")
        if config.getboolean("Lightning", "Enabled"):
            handler = StartStop()
            handler.exeName = "HiSPARC Lightning Detector.exe"
            handler.currentDirectory = os.path.join(HS_ROOT,
                                                    "user/hisparclightning")
            handler.command = os.path.join(HS_ROOT, "user/hisparclightning",
                                           "HiSPARC Lightning Detector.exe")
            result = handler.startProcess()
        else:
            result = DISABLED
        logger.info("Status: %s", status(result))
    except:
        logger.exception("An exception was generated while starting "
                         "HiSPARC Lightning")

    # Pause to let MySQL start completely if it was not already running
    time.sleep(delay_monitor)

    cmd = '%s/user/startstop/runmanually.bat "{name}" "{path}" {cmd}' % HS_ROOT

    try:
        logger.info("Starting HiSPARC Monitor...")
        handler = CMDStartStop()
        handler.windowName = "HiSPARC Monitor"
        handler.title = "Start HiSPARC Monitor"
        handler.currentDirectory = os.path.join(HS_ROOT, "user/hsmonitor")
        handler.command = cmd.format(name=handler.windowName,
                                     path=r"\user\hsmonitor",
                                     cmd="HsMonitor.py")
        result = handler.startProcess()
        logger.info("Status: %s", status(result))
    except:
        logger.exception("An exception was generated while starting "
                         "HiSPARC Monitor")

    try:
        logger.info("Starting HiSPARC Updater...")
        handler = CMDStartStop()
        handler.windowName = "HiSPARC Updater"
        handler.title = "Start HiSPARC Updater"
        handler.currentDirectory = os.path.join(HS_ROOT, "user/updater")
        handler.command = cmd.format(name=handler.windowName,
                                     path=r"\user\updater",
                                     cmd="Update.py")
        result = handler.startProcess()
        logger.info("Status: %s", status(result))
    except:
        logger.exception("An exception was generated while starting the "
                         "HiSPARC Updater")


if __name__ == "__main__":
    startstop_logger.setup()
    start()
