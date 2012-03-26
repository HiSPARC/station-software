#
#   startStop.py ------
#   Start, stop and check the necessary processes and services for HiSPARC.
#

import wmi
import win32con
import win32gui

from hslog  import log
from ctypes import c_ulong, byref, windll

RUNNING       = 0
STOPPED       = 1
EXCEPTION     = 2
DISABLED      = 4
NOT_INSTALLED = 8

class StartStop:
    exeName = ''
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
            if res[0] == 0 or res[0] == 10:
                result = RUNNING
                return result
            else:
                raise Exception(" error code %d" % res)
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
                for i in range(1, 3):
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
        if res == 0 or res == 10:
            return STOPPED
        else:
            return RUNNING

    def stopService(self):
        result = RUNNING
        service = self.wmiObj.Win32_Service(Name=self.serviceName)
        if service != []:
            res = service[0].StopService()
            if res[0] == 0 or res[0] == 10 or res[0] == 5:
                result = STOPPED
                return result
            else:
                raise Exception(": error code %d" % res)
        else:
            result = EXCEPTION
        
        return result

    def probeProcess(self):
        process = self.wmiObj.Win32_Process(name=self.exeName)
        if process != []:
            result = RUNNING
        else:
            result = STOPPED
        return result

    def probeService(self):
        service = self.wmiObj.Win32_Service(Name=self.serviceName)
        if service != []:
            service = self.wmiObj.Win32_Service(Name=self.serviceName, State="Running")
            if service != []:
                result = RUNNING
            else:
                result = STOPPED
        else:
            result = NOT_INSTALLED
        return result


class CMDStartStop(StartStop):

    def __init__(self):
        self.wmiObj = wmi.WMI()

    def startProcess(self):
        w = win32gui.FindWindow(None, self.title)
        result = STOPPED
        if w == 0:
            result = self.spawnProcess()
        else:
            result = RUNNING
        return result

    def stopProcess(self):
        print "finding window '%s'.." % self.title
        w = win32gui.FindWindow(None, self.title)
        if w != 0:
            result = RUNNING
            win32gui.SetWindowText(w, self.title +
                                   ' (shutdown in progress...)')
            dword = c_ulong()
            tid = windll.user32.GetWindowThreadProcessId(w, byref(dword))
            pid = dword.value

            phandle = windll.kernel32.OpenProcess(2035711, 0, pid)

            log("stopping process with pid %d and handle %d..." %
                (pid, phandle))
            r = windll.kernel32.TerminateProcess(phandle, 0)
            if r:
                log("success")
                result = STOPPED
            else:
                log("major fail: r = %d" % r)
                result = EXCEPTION
            #for process in self.wmiObj.Win32_Process(name = self.exeName):
            #    print 'processId: %d' % process.ProcessId
            #    if process.Terminate() == 0:
            #        result = STOPPED
        else:
            result = STOPPED
        return result

    def probeProcess(self):
        w = win32gui.FindWindow(None, self.title)
        if w != 0:
            result = RUNNING
        else:
            result = STOPPED
        return result
