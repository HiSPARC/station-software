#########################################################################################
#
# HiSPARC service check included in Windows Task scheduler
# Code checks at runtime whether all HiSPARC User processes and Admin services are
# running. Reboot the HiSPARC pc when one or more HiSPARC process(es) or service(s) is
# (are) not running.
# Called from:  - /user/startstop/runmanually.bat
#
# tkooij@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Apr 2019: - Check HiSPARC Status created as scheduled task as of installer 9.15.2
#
#########################################################################################

import os
import sys
import logging
import wmi
import ConfigParser
import startstop_logger

from startStop import (StartStop, CMDStartStop, RUNNING, STOPPED, DISABLED,
                       EXCEPTION, NOT_INSTALLED)

# Check is carried out once per day (02:00 UTC) and logged in startstop logfile
logger = logging.getLogger('startstop.checkstatus')

status_dict = {RUNNING: 'RUNNING', STOPPED: 'STOPPED', EXCEPTION: 'EXCEPTION',
               DISABLED: 'DISABLED', NOT_INSTALLED: 'NOT INSTALLED'}

def schedule_reboot():
    # Schedule a (forced) reboot of the station PC by calling "shutdown"
    os.system("shutdown /r /f")

def check_app(name, exe_name=None, window_name=None, service_name=None):

    # Check if a program or service is running:
    #   param name:         common name for the process,
    #   param exe_name:     executable name of the process,
    #   param window_name:  title of the process,
    #   param service_name: name of the service.
    try:
        if exe_name is not None:
            handler = StartStop()
            handler.exeName = exe_name
            res = handler.probeProcess()
        elif window_name is not None:
            handler = CMDStartStop()
            handler.windowName = window_name
            res = handler.probeProcess()
        elif service_name is not None:
            handler = StartStop()
            handler.serviceName = service_name
            res = handler.probeService()
        else:
            raise Exception("exe_name, window_name, or service_name should be "
                            "given.")
    except Exception as e:
        res = EXCEPTION
    if res != RUNNING:
        # Program or service not running or not recognised so reboot
        logger.critical("Process %s has status %s. Schedule reboot!" %
                     (name, status_dict.get(res, 'UNKNOWN')))
        schedule_reboot()
        sys.exit(1)

def detect_monitor_and_updater():
    # The monitor and updater are python.exe processes.
    # Unfortunately we cannot check the Window Titles for processes
    # running as a different user.
    # Poor man's solution: Count the number of python.exe processes.
    # If the number >= 3 assume we have monitor and updater (and this
    # script) running.
    wmi_obj = wmi.WMI()
    res = wmi_obj.win32_Process(name='python.exe')
    if len(res) >= 3:
        logger.debug("Found python.exe processes for Monitor and Updater.")
    else:
        logger.critical("Found only %d python.exe processes. Schedule reboot!" %
                        len(res))
        schedule_reboot()
        sys.exit(1)

def check():
    # Check if HiSPARC scheduled User programs and Admin services are active
    logger.debug("Check status of all User processes and Admin services.")
    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
        logger.critical("FATAL: environment variable HISPARC_ROOT not set!")
        return
    # Check individual programs selected in config file and processes
    config_file = os.path.join(HS_ROOT, "persistent/configuration/config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    # Get status programs
    check_app("MySQL", exe_name="mysqld.exe")
    if config.getboolean("DAQ", "Enabled"):
        check_app("HiSPARC DAQ", exe_name="HiSPARC DAQ.exe")
    if config.getboolean("Weather", "Enabled"):
        check_app("HiSPARC Weather", exe_name="HiSPARC Weather Station.exe")
    if config.getboolean("Lightning", "Enabled"):
        check_app("HiSPARC Lightning", exe_name="HiSPARC Lightning Detector.exe")
    #Poor man's check on Monitor and Updater (Python) programs
    detect_monitor_and_updater()
    # Get status services
    check_app("TightVNC", service_name="tvnserver")
    check_app("Nagios", service_name="nscp")
    check_app("OpenVPN", service_name="OpenVPNService")
    # All are running...
    logger.info("HiSPARC user processes and admin services are running. No action required.")

if __name__ == "__main__":
    startstop_logger.setup()
    check()
