"""Determine status of the HiSPARC user processes and admin services.

reboot the station pc if a HiSPARC process or service is not running.

"""

import os
import sys
import logging
import ConfigParser

import startstop_logger
from startStop import (StartStop, CMDStartStop, RUNNING, STOPPED, DISABLED,
                       EXCEPTION, NOT_INSTALLED)


logger = logging.getLogger('startstop.checkstatus')

status_dict = {RUNNING: 'RUNNING', STOPPED: 'STOPPED', EXCEPTION: 'EXCEPTION',
               DISABLED: 'DISABLED', NOT_INSTALLED: 'NOT INSTALLED'}


def schedule_reboot():
    """schedule a (forced) reboot of the station PC by calling `shutdown`"""
    os.system("shutdown /r /f /t 600")


def check_app(name, exe_name=None, window_name=None, service_name=None):
    """Check if a program or service is running

    :param name: common name for the process.
    :param exe_name: executable name of the process.
    :param window_name: title of the process.
    :param service_name: name of the service.

    """

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
        logger.critical("Process %s has status %s. Schedule reboot!" %
                        (name, status_dict.get(res, 'UNKNOWN')))
        schedule_reboot()
        sys.exit(1)


def check():
    """Check if the expected User and Admin processes are active"""

    logger.debug("Checking status of all processes and services.")

    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
        logger.critical("FATAL: environment variable HISPARC_ROOT not set!")
        return

    config_file = os.path.join(HS_ROOT, "persistent/configuration/config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    check_app("MySQL", exe_name="mysqld.exe")
    if config.getboolean("Detector", "Enabled"):
        check_app("HiSPARC Detector", exe_name="HiSPARC DAQ.exe")
    if config.getboolean("Weather", "Enabled"):
        check_app("HiSPARC Weather", exe_name="HiSPARC Weather Station.exe")
    if config.getboolean("Lightning", "Enabled"):
        check_app("HiSPARC Lightning", exe_name="HiSPARC Lightning Detector.exe")
    check_app("HiSPARC Monitor", window_name="HiSPARC Monitor")
    check_app("HiSPARC Updater", window_name="HiSPARC Updater")

    check_app("TightVNC", service_name="tvnserver")
    check_app("Nagios", service_name="nscp")
    check_app("OpenVPN", service_name="OpenVPNService")

    logger.info("All processes and services are running. No action required.")


if __name__ == "__main__":
    startstop_logger.setup()
    check()
