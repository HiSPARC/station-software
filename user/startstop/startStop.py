#########################################################################################
#
# Start, stop and check the necessary processes and services for HiSPARC.
#
# tkooij@nikhef.nl, NIKHEF, Amsterdam
# vaneijk@nikhef.nl, NIKHEF, Amsterdam
#
#########################################################################################
#
# Apr 2019: - probeProcess extended by searching for string, as of installer 9.15.2
#
#########################################################################################

import wmi
import win32con
import win32gui
import logging

from ctypes import c_ulong, byref, windll

logger = logging.getLogger('startstop.startstop')

RUNNING = 0
STOPPED = 1
EXCEPTION = 2
DISABLED = 4
NOT_INSTALLED = 8

def status(result):
    # Translate result code to a readable string
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

    return status


class StartStop(object):
    # A class to start and stop programs on Windows
    exeName = ''
    windowName = ''
    ShowWindow = win32con.SW_SHOWMINIMIZED
    currentDirectory = ''
    command = ''
    title = ''
    serviceName = ''
    wmiObj = None

    def __init__(self):
        self.wmiObj = wmi.WMI()

    def spawnProcess(self):
        startup = self.wmiObj.Win32_ProcessStartup.new(
            ShowWindow=self.ShowWindow, Title=self.title)
        unused_pid, res = self.wmiObj.Win32_Process.Create(
            CommandLine=self.command, CurrentDirectory=self.currentDirectory,
            ProcessStartupInformation=startup)
        if res in [0, 10]:
            result = RUNNING
        else:
            raise Exception("Win32_Process.Create exception: error code %d" %
                            res)
            result = EXCEPTION
        return result

    def startProcess(self):
        result = STOPPED
        process = self.wmiObj.Win32_Process(name=self.exeName)
        if process == []:
            result = self.spawnProcess()
        else:
            result = RUNNING
        return result

    def startService(self):
        result = STOPPED
        service = self.wmiObj.Win32_Service(Name=self.serviceName)
        if service != []:
            res = service[0].StartService()
            if res[0] in [0, 10]:
                result = RUNNING
            else:
                raise Exception("Error code %d" % res)
        else:
            result = EXCEPTION
        return result

    def killProcess(self):
        try:
            for process in self.wmiObj.Win32_Process(name=self.exeName):
                process.Terminate()
            result = STOPPED
        except Exception:
            result = EXCEPTION
        return result

    def stopProcess(self):
        result = RUNNING
        process = self.wmiObj.Win32_Process(name=self.exeName)
        if process != []:
            if self.command != '':
                for _ in range(1, 3):
                    if result == RUNNING:
                        result = self.askStopProcess()
                        return result  # ADL: Should this not be behind if?
                result = self.killProcess()
            else:
                result = self.killProcess()
        else:
            result = STOPPED
        return result

    def askStopProcess(self):
        startup = self.wmiObj.Win32_ProcessStartup.new(
            ShowWindow=win32con.SW_HIDE)
        unused_pid, res = self.wmiObj.Win32_Process.Create(
            CommandLine=self.command, CurrentDirectory=self.currentDirectory,
            ProcessStartupInformation=startup)
        if res in [0, 10]:
            result = STOPPED
        else:
            result = RUNNING
        return result

    def stopService(self):
        result = RUNNING
        service = self.wmiObj.Win32_Service(Name=self.serviceName)
        if service != []:
            res = service[0].StopService()
            if res[0] in [0, 5, 10]:
                result = STOPPED
            else:
                raise Exception("Error code %d" % res)
        else:
            result = EXCEPTION
        return result

    def probeProcess(self):
        # Find process name
        process = self.wmiObj.Win32_Process(name=self.exeName)
        if process != []:
            result = RUNNING
        else:
            result = STOPPED
        return result

    def probeService(self):
        # Find service name
        service = self.wmiObj.Win32_Service(Name=self.serviceName)
        if service != []:
            service = self.wmiObj.Win32_Service(Name=self.serviceName,
                                                State="Running")
            if service != []:
                result = RUNNING
            else:
                result = STOPPED
        else:
            result = NOT_INSTALLED
        return result


class CMDStartStop(StartStop):
    # Start and stop command line processes
    # Set the windowName attribute to the title of the final process. This is
    # used to check if the process is already running, and to find it when it
    # is to be shutdown.
    # Set the title attribute to the same value if the process will remain in
    # its initial window. Otherwise choose a different name.
    def __init__(self):
        self.wmiObj = wmi.WMI()

    def startProcess(self):
        w = win32gui.FindWindow(None, self.windowName)
        result = STOPPED
        if w == 0:
            result = self.spawnProcess()
        else:
            result = RUNNING
        return result

    def stopProcess(self):
        logger.debug("Finding window '%s'.." % self.windowName)
        w = win32gui.FindWindow(None, self.windowName)
        if w != 0:
            result = RUNNING
            win32gui.SetWindowText(w, self.windowName +
                                   ' (shutdown in progress...)')
            dword = c_ulong()
            windll.user32.GetWindowThreadProcessId(w, byref(dword))
            pid = dword.value

            phandle = windll.kernel32.OpenProcess(2035711, 0, pid)

            logger.debug("Stopping process with pid %d and handle %d...",
                         pid, phandle)
            r = windll.kernel32.TerminateProcess(phandle, 0)
            if r:
                logger.debug("success")
                result = STOPPED
            else:
                logger.debug("major fail: r = %d" % r)
                result = EXCEPTION
        else:
            result = STOPPED
        return result

    def probeProcess(self):
        # Find window name
        w = win32gui.FindWindow(None, self.windowName)
        window_name = self.windowName
        if w != 0:
            result = RUNNING
        else:
            def callback(h, extra):
                # Check if name is part of the string
                if window_name in win32gui.GetWindowText(h):
                    extra.append(h)
                return True
            extra = []
            win32gui.EnumWindows(callback, extra)
            if extra: w = extra[0]
            if w !=0:
                result = RUNNING
            else:
                result = STOPPED
        return result
