"""
This is the main process of the HiSPARC monitor.
This process creates other objects and threads.
"""

__author__="thevinh"
__date__ ="$16-sep-2009"

import os, sys, cmd
sys.path.append("..\..\pythonshared")
import hslog
from EConfigParser import EConfigParser
import BufferListener
from Interpreter import Interpreter
from CheckScheduler import CheckScheduler
from StorageManager import StorageManager
from Uploader import Uploader

# Default configuration file path
CONFIG_INI_PATH1 = '..\data\config.ini'
CONFIG_INI_PATH2 = '../../../persistent/configuration/config.ini'

# HsMonitor class
class HsMonitor:
	def __init__(self):		
		# setup the log mode
		hslog.setLogMode(hslog.MODE_PRINT)

		# read the configuration file
		try:
			self.cfg = EConfigParser()
			self.cfg.read([CONFIG_INI_PATH1, CONFIG_INI_PATH2])
		except:
			hslog.log("Cannot open the config file!")
			return
		else:
			hslog.log("Initilize variables")			
			
			#list of all the threads
			self.hsThreads = []		
		# Assume one server (eventwarehouse)
		# if the local is also specified it will be added
		self.numServers = 1
			
	#--------------------------End of __init__--------------------------#
	
	def startAll(self):		
		try:
			# create StorageManager and interpreter for bufferlistener
			sm = StorageManager()
			it = Interpreter(sm)
	
			# buffer listener
			buffLis = self.createBufferListener(it)
			
			if buffLis.conn:
				self.hsThreads.append(buffLis)
		
			# check scheduler
			# get the nagios configuration section from config file 
			nagiosConf = self.cfg.itemsdict('NagiosPush')	
			checkSched = self.createCheckScheduler(it, nagiosConf)
			eventrate = checkSched.getEventRate()
			sm.addObserver(eventrate)
			self.hsThreads.append(checkSched)
		
			# Uploader central
			up = self.createUploader(0, "Upload-eventwarehouse", nagiosConf)
			self.hsThreads.append(up)
			sm.addObserver(up)
			up.setNumServer(self.numServers)

			# try local server
			try:
				up2 = self.createUploader(1, "Upload-local", nagiosConf)
				self.hsThreads.append(up2)
				sm.addObserver(up2)
				self.numServers+=1
				up.setNumServer(self.numServers)
				up2.setNumServer(self.numServers)
			except Exception, msg:
				hslog.log("Error while parsing local server: %s" %(msg,))
				hslog.log("Will not upload to local server!")
		
			# Start all threads
			for t in self.hsThreads:
				t.start()
		
		except Exception, msg:
			hslog.log("Error: %s" % (msg,))
			exit(1)
			
	#--------------------------End of startAll--------------------------#
	
	def stopAll(self):
		# stop all threads
		for thread in self.hsThreads:
			thread.stop()
	
	def createBufferListener(self, interpreter):
		# get the information from configuration file		
		bufferdb = {}		
		bufferdb['host'] = self.cfg.ifgetstr('BufferDB', 'Host', 'localhost')		
		bufferdb['db'] = self.cfg.ifgetstr('BufferDB', 'DB', 'buffer')
		bufferdb['user'] = self.cfg.ifgetstr('BufferDB', 'Username', "buffer")
		bufferdb['password'] = self.cfg.ifgetstr('BufferDB', 'Password', "PLACEHOLDER")
		bufferdb['poll_interval'] = self.cfg.ifgetfloat('BufferDB', 'Poll_Interval', 1.0)
		bufferdb['poll_limit'] = self.cfg.ifgetint('BufferDB', 'Poll_Limit', 100)
		bufferdb['keep_buffer_data'] = self.cfg.ifgetint('BufferDB', 'KeepBufferData', 0)

		# create an instance of BufferListener class
		buffLis = BufferListener.BufferListener(bufferdb, interpreter)	
					
		return buffLis
		
	#--------------------------End of createBufferListener--------------------------#

	def createCheckScheduler(self, interpreter, nagiosConf):		
		
		checkSched = CheckScheduler(nagiosConf, interpreter)		
		
		return checkSched
	
	#--------------------------End of createCheckScheduler--------------------------#

	def createUploader(self, serverID, section_name, nagiosConf):
		stationID = self.cfg.get("Station", "Nummer")
		url = self.cfg.get(section_name, "URL")
		passw = self.cfg.get("Station", "Password")
		minbs = self.cfg.ifgetint(section_name, "MinBatchSize", 50)
		maxbs = self.cfg.ifgetint(section_name, "MaxBatchSize", 50)
		if (minbs > maxbs):
			hslog.log("warning: maximum batch size must be more than minimum batch size. Setting maximum=minimum.")
			maxbs = minbs
		minwait = self.cfg.ifgetfloat(section_name, "MinWait", 1.0)
		maxwait = self.cfg.ifgetfloat(section_name, "MaxWait", 60.0)

		up = Uploader(serverID, stationID, passw, url, nagiosConf, minwait, maxwait, minbs, maxbs)
		return up
	#--------------------------End of createUploader--------------------------#
	
# main function
def main():
	# create a HiSparc monitor object
	hsMonitor = HsMonitor()
	
	# start all threads
	hsMonitor.startAll()
	
	# this to get the keyboard interruption
	c = cmd.Cmd()	
	
	try:
		c.cmdloop()		
	except KeyboardInterrupt:
		 # stop all threads
		 hsMonitor.stopAll()
	
	# wait for all threads to finish
	#for thread in hsMonitor.hsThreads:
	#	thread.join()	
		
#--------------------------Main--------------------------#
if __name__ == '__main__':
	main()
