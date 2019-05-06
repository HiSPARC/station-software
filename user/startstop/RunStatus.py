#########################################################################################
#
# HiSPARC menu option
# Code checks at runtime whether all HiSPARC User processes and Admin services are
# running. Result is printed in CMD window.
# Called from:  - /user/startstop/runmanually.bat
#
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Mar 2019: - Replaced 'Detector' by 'DAQ'
#
#########################################################################################

import os
import ConfigParser

from startStop import StartStop, CMDStartStop, status, EXCEPTION, DISABLED

def pStdout(name, result):

    # User initiated check results are ('pretty') printed in CMD window
    info = "%(name)-20s: %(status)s" % {"name": name, "status": status(result)}
    print info

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
    except:
        res = EXCEPTION
    pStdout(name, res)

def check():

    # Check if HiSPARC scheduled User programs and Admin services are active
    HS_ROOT = "%s" % os.getenv("HISPARC_ROOT")
    if HS_ROOT == "":
        print "FATAL: environment variable HISPARC_ROOT not set!"
        return
    # Check individual programs (selected in config file)/processes
    config_file = os.path.join(HS_ROOT, "persistent/configuration/config.ini")
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    # Get status programs
    print "Checking User-Mode applications..."
    check_app("MySQL", exe_name="mysqld.exe")
    if config.getboolean("DAQ", "Enabled"):
        check_app("HiSPARC DAQ", exe_name="HiSPARC DAQ.exe")
    else:
        pStdout("HiSPARC DAQ", DISABLED)
    if config.getboolean("Weather", "Enabled"):
        check_app("HiSPARC Weather", exe_name="HiSPARC Weather Station.exe")
    else:
        pStdout("HiSPARC Weather", DISABLED)
    if config.getboolean("Lightning", "Enabled"):
        check_app("HiSPARC Lightning", exe_name="HiSPARC Lightning Detector.exe")
    else:
        pStdout("HiSPARC Lightning", DISABLED)
    check_app("HiSPARC Monitor", window_name="HiSPARC Monitor")
    check_app("HiSPARC Updater", window_name="HiSPARC Updater")
    print
    # Get status services
    print "Checking Admin-Mode services..."
    check_app("TightVNC", service_name="tvnserver")
    check_app("Nagios", service_name="nscp")
    check_app("OpenVPN", service_name="OpenVPNService")

if __name__ == "__main__":
    check()
