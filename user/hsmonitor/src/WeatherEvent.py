#!/usr/bin/env python

import datetime
import time
import base64
from Event import Event
import EventExportValues

# A Weather event class.
# Makes all data handling easy
class WeatherEvent(Event):
	def __init__(self, message):		
		# invoke constructor of parent class
		Event.__init__(self)	
		self.message = message[1]		
	
	def parseMessage(self):		
		tmp = self.message.split("\t")
		t = time.strptime(tmp[-1].strip(), "%Y-%m-%d %H:%M:%S")
		self.datetime = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5])
		self.nanoseconds = 0 # Weather is not acurate enough
		self.second = self.datetime.second
		self.minute = self.datetime.minute
		self.hour = self.datetime.hour
		self.day = self.datetime.day
		self.month = self.datetime.month
		self.year = self.datetime.year
		self.tempInside = float(tmp[0])
		self.tempOutside = float(tmp[1])
		self.humidityInside = float(tmp[2])
		self.humidityOutside = float(tmp[3])
		self.barrometer = float(tmp[4])
		self.windDir = float(tmp[5])
		self.WindSpeed = float(tmp[6])
		self.solarRad = float(tmp[7])
		self.UV = float(tmp[8])
		self.ET = float(tmp[9])
		self.rainRate = float(tmp[10])
		self.heatIndex = float(tmp[11])
		self.dewPoint = float(tmp[12])
		self.windChill = float(tmp[13])
		
		# get all event data necessary for an upload.
		self.export_values = EventExportValues.export_values[self.uploadCode]	
		return self.getEventData()
		
	#--------------------------End of __init__--------------------------#	
	
	def __getattribute__(self, name):
		return object.__getattribute__(self, name)

	def __getattr__(self, name):
		if name == "date":
			return self.datetime.date().isoformat()
		elif name == "time":
			return self.datetime.time().isoformat()
		else:
			raise AttributeError, name
	
	def getEventData(self):		
		"""	Get all event data necessary for an upload.
			This function parses the export_values variable declared in the EventExportValues
			and figures out what data to collect for an
			upload to the eventwarehouse. It returns a list of
			dictionaries, one for each data element.
		"""	
		
		eventdata = []
		for value in self.export_values:
			eventdata.append({
				"calculated":value[0], # Calculated data
				"data_uploadcode":value[1], # data_uploadcode
				"data": base64.b64encode(self.__getattribute__(value[2])) # data
			})
			
		return eventdata	

	#--------------------------End of getEventData--------------------------#			
