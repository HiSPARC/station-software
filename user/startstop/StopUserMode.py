from startStop import *
from ctypes import c_ulong, byref, windll
from hslog import *

path='%s:' %os.getenv("HISPARC_DRIVE")

def stop():
	setLogMode(MODE_BOTH)
	log('\nStopping User-Mode applications...')
	try:
		#stop LabView
		log('Stopping LabView...')
		labViewHandler=StartStop()
		labViewHandler.exeName='hisparcdaq.exe'
		labViewHandler.currentDirectory="%s\\user\\hisparcdaq" %path
		#labViewHandler.command="%s\\user\\hisparcdaq\\hisparcdaq.exe" %path
		resLabView=labViewHandler.stopProcess()
		if resLabView==0:
			log('Status:running')
		elif resLabView==1:
			log('Status:stopped')
		else:
			log ('An exception was generated!')
	except:
		log('An exception was generated while stopping LabView!')

	try:
		#stop LabView
		log('Stopping LabView Weather...')
		labViewHandler=StartStop()
		labViewHandler.exeName='hisparcweather.exe'
		labViewHandler.currentDirectory="%s\\user\\hisparcweather" %path
		resLabView=labViewHandler.stopProcess()
		if resLabView==0:
			log('Status:running')
		elif resLabView==1:
			log('Status:stopped')
		else:
			log ('An exception was generated!')
	except:
		log('An exception was generated while stopping LabView Weather!')
	
	try:
		#stop mySql
		log('Stopping MySQL...')
		mySqlHandler=StartStop()
		mySqlHandler.exeName='mysqld.exe'
		mySqlHandler.ShowWindow=win32con.SW_HIDE
		#mySqlHandler.command="cmd /c mysqld.exe"
		#FIXME: find command to shut down mysql nicely!
		mySqlHandler.currentDirectory="%s\\user\\mysql\\bin" %path
		resMySql=mySqlHandler.stopProcess()
		if resMySql==0:
			log('Status:running')
		elif resMySql==1:
			log('Status:stopped')
		else:
			log ('An exception was generated!')
	except:
		log('An exception was generated while stopping MySQL!')
	
	try:
		#stop HSMonitor
		log('Stopping HSMonitor...')
		hsMonitorHandler=CMDStartStop()
		hsMonitorHandler.exeName='python.exe'
		hsMonitorHandler.title='HISPARC MONITOR: hsmonitor'
		#hsMonitorHandler.currentDirectory="%s\\user\\hsmonitor" %path
		#hsMonitorHandler.command="cmd.exe /c %s\\user\\python\\python.exe hsmonitor.py" % path
		resHSMonitor=hsMonitorHandler.stopProcess()
		if resHSMonitor==0:
			log('Status:running')
		elif resHSMonitor==1:
			log('Status:stopped')
		else:
			log ('An exception was generated')
	except:
		log('An exception was generated while stopping HSMonitor!')
	
	try:
		
		#stop Updater
		log('Stopping Updater...')
		updaterHandler=CMDStartStop()
		updaterHandler.exeName='python.exe'
		updaterHandler.title='HISPARC Updater: updater'
		#hsMonitorHandler.currentDirectory="%s\\user\\hsmonitor" %path
		#hsMonitorHandler.command="cmd.exe /c %s\\user\\python\\python.exe hsmonitor.py" % path
		resUpdater=updaterHandler.stopProcess()
		if resUpdater==0:
			log('Status:running')
		elif resUpdater==1:
			log('Status:stopped')
		else:
			log ('An exception was generated')
	except:
		log('An exception was generated while stopping the Updater!')
		


stop()
