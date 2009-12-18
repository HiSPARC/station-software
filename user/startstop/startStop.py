import os
import wmi
import win32con
import win32gui
from hslog import *
from ctypes import c_ulong, byref, windll
running=0
stopped=1
exception=2

class StartStop:
	exeName=''
	ShowWindow=win32con.SW_SHOWMINIMIZED
	currentDirectory=''
	command=''
	title=''
	serviceName=''
	wmiObj = None
	
	def __init__(self):
		self.wmiObj = wmi.WMI()
		
	
	def spawnProcess(self):
		startup = self.wmiObj.Win32_ProcessStartup.new(ShowWindow=self.ShowWindow, Title=self.title)
		pid, res = self.wmiObj.Win32_Process.Create(CommandLine=self.command, CurrentDirectory= self.currentDirectory,ProcessStartupInformation=startup)
		if res==0 or res==10:
			result=running
		else:
			raise Exception("Win32_Process.Create exception: error code %d" % res)
			result=exception
		return result
			

	
	def startProcess(self):
		result=stopped
		process = self.wmiObj.Win32_Process(name=self.exeName)
		if process==[]:
			result=self.spawnProcess()
		else:
			result=running
			
		return result
		
		
	def startService(self):
		result=stopped
		service=self.wmiObj.Win32_Service(Name=self.serviceName)
		if service!=[]:
			res = service[0].StartService()
			if res[0]==0 or res[0]==10:
				result=running
				return result
			else:
				raise Exception(" error code %d" % res)
				
		else:
			result=exception
		return result
	
	def killProcess(self):
		try:
			for process in self.wmiObj.Win32_Process(name = self.exeName):
				process.Terminate()
			result=stopped
		except Exception:
			result=exception
		return result
	
	def stopProcess(self):
		result=running
		process=self.wmiObj.Win32_Process(name = self.exeName)
		if process!=[]:
			if self.command !='':
				for iterator in range(1,3):
					if result==running:
						result=self.askStopProcess()
						return result
				result=self.killProcess()
			else:
				result=self.killProcess()
		else:
			result=stopped
		return result
			
	def askStopProcess(self):
		startup = self.wmiObj.Win32_ProcessStartup.new(ShowWindow=win32con.SW_HIDE)
		pid, res=self.wmiObj.Win32_Process.Create(CommandLine=self.command, CurrentDirectory= self.currentDirectory,ProcessStartupInformation=startup)
		if (res==0) or (res==10):
			return stopped
		else:
			return running

	
	def stopService(self):
		result=running
		service=self.wmiObj.Win32_Service(Name=self.serviceName)
		if service!=[]:
			res = service[0].StopService()
			if res[0]==0 or res[0]==10 or res[0]==5:
				result=stopped
				return result
			else:
				raise Exception(": error code %d" % res)
				
		else:
			result=exception
		return result
		
		
class CMDStartStop(StartStop):
	
	def __init__(self):
		self.wmiObj = wmi.WMI()
		
	def startProcess(self):
		w = win32gui.FindWindow(None, self.title)
		result=stopped
		if w==0:
			result=self.spawnProcess()
		else:
			result=running
			
		return result
	def stopProcess(self):
		print "finding window '%s'.." % self.title
		w = win32gui.FindWindow(None, self.title)
		if w!=0:
			result=running
			win32gui.SetWindowText(w, self.title + ' (shutdown in progress...)')
			dword = c_ulong()
			tid = windll.user32.GetWindowThreadProcessId(w, byref(dword))
			pid = dword.value
			
			phandle = windll.kernel32.OpenProcess(2035711, 0, pid)
			
			log("stopping process with pid %d and handle %d..." % (pid, phandle))
			r = windll.kernel32.TerminateProcess(phandle, 0)
			if r:
				log("success")
				result = stopped
			else:
				log("major fail: r =  %d" % r)
				result = exception
			
			
			#for process in self.wmiObj.Win32_Process(name = self.exeName):
			#	print 'processId: %d' %process.ProcessId
			#	if process.Terminate()==0:
			#		result=stopped
		else:
			result=stopped
		return result

		




