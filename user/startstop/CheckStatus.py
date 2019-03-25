"""Determine status of the HiSPARC user processes and admin services.
     Reboot the HiSPARC pc if a HiSPARC process or service is not running.
BvE: Replaced "Detector" by "DAQ"

"""

import os
import sys
import ConfigParser

from startStop import StartStop, CMDStartStop, status, RUNNING, EXCEPTION


def schedule_reboot():
    """schedule a (forced) reboot of the station PC by calling `shutdown`"""
    os.system("shutdown /r /f /t 30")


def check_app(name, exe_name=None, window_name=None, service_name=None):
    """Check if a program or service is running

    :param name: common name for the process.
    :param exe_name: executable name of the process.
    :param window_name: title of the process.
    :param service_name: name of the service.

    It appears that sometimes a timeout occurs and the wrong value is
    returned. Timeout or? So we try max 3 times...

    """
    for i in range(2):
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
      except:
        res = EXCEPTION
      finally:
        if res == RUNNING:
        break

    if res != RUNNING:
        schedule_reboot()
        sys.exit(1)


def check():
    """Check if the expected User and Admin processes are active"""

    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")

    config_file = os.path.join(HS_ROOT, "persistent/configuration/config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_file)

    check_app("MySQL", exe_name="mysqld.exe")
    if config.getboolean("DAQ", "Enabled"):
        check_app("HiSPARC DAQ", exe_name="HiSPARC DAQ.exe")
    if config.getboolean("Weather", "Enabled"):
        check_app("HiSPARC Weather", exe_name="HiSPARC Weather Station.exe")
    if config.getboolean("Lightning", "Enabled"):
        check_app("HiSPARC Lightning", exe_name="HiSPARC Lightning Detector.exe")
    check_app("HiSPARC Monitor", window_name="HiSPARC Monitor")
    check_app("HiSPARC Updater", window_name="HiSPARC Updater")
    check_app("TightVNC", service_name="tvnserver")
    check_app("Nagios", service_name="nscp")
    check_app("OpenVPN", service_name="OpenVPNService")


if __name__ == "__main__":
    check()
