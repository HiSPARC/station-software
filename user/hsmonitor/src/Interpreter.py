""" 
	Process HiSPARC messages from a buffer.
    This module processes binary messages from a HiSPARC station buffer and creates Events from them. 
	The Events are passed on to the StorageManager. 
"""

__author__="thevinh"
__date__ ="$16-sep-2009"

import time
import hslog
from CIC import CIC
from ERR import ERR
from CFG import CFG
from CMP import CMP
from WeatherEvent import WeatherEvent
from StorageManager import *

# create a dictionary to store all type_codes of events
event_type_codes =  {	'1': 'CIC',
						'2': 'ERR',
						'3': 'CFG',
						'4': 'CMP',
						'16': 'WTR'
					}

class TriggerRateHolder:
	def __init__(self, triggerRate, date):
		self.triggerRate = triggerRate
		self.date = date

class Interpreter:
	# the instantiation operation
	def __init__(self, storageManager):
		# init variables here if needed				
		self.storageManager = storageManager
		self.triggerRate = TriggerRateHolder(0,0)
		
	#--------------------------End of __init__--------------------------#	

	def openStorage(self):
		self.storageManager.openConnection()
	
	def createEvent(self, eventcode, message):
		# create an event corresponding to the eventcode
		if eventcode == 'CIC':
			event = CIC(message)
		elif eventcode == 'ERR':
			event = ERR(message)
		elif eventcode == 'CFG':
			event = CFG(message)
		elif eventcode == 'CMP':
			event = CMP(message)
		elif eventcode == 'WTR':
			event = WeatherEvent(message)
		else:
			hslog.log("Unknown message type %s (%d)" % eventcode, self.type_id)
			return None
			
		event.uploadCode = eventcode
		event.data = event.parseMessage()
		return event

	#--------------------------End of createEvent--------------------------#	
	
	def setTriggerRate(self, triggerRate):
		self.triggerRate = triggerRate

	def getTriggerRate(self):
		return self.triggerRate

	def parseMessages(self, messages):	
		"""
			This function unpacks messages, creates events, retrieves relevant data from the events and
			returns it as an elaborate data object which can be serialized for
			transfer via an HTTP POST request.
		"""
		
		self.eventlist = []
		self.event_ids = []
		self.discard_event_ids = []
		# this variable stores the trigger rate of the recent event
		trigger_rate = TriggerRateHolder(0, 0)
		hslog.log("Interpreter: parsing %d messages" % len(messages))

		firsttime = True
		for message in messages:					
			try:					
				# get the event message code
				eventcode = event_type_codes['%d' % message[0]]								
							
				# create an event object				
				event = self.createEvent(eventcode, message)
				
				# skip processing event if it is None
				if event is None:
					continue
				
				# create the event header
				# new server uses datetime, old uses date and time
				# for compatibility, include both
				header = {
					'eventtype_uploadcode': event.uploadCode,
					'datetime': event.datetime,            
					'date': event.datetime.date().isoformat(),
					'time': event.datetime.time().isoformat(),
					'nanoseconds': event.nanoseconds,
				}			
				
				# store the trigger rate variable, only for the newest event
				if eventcode == 'CIC' and firsttime:
					firsttime = False
					trigger_rate.triggerRate = event.eventrate
					trigger_rate.date = event.datetime				
				
			except Exception, (errormsg):
				# add parsed event_id into the list of event_ids
				self.discard_event_ids.append(message[2])				
				hslog.log("Event exception (discarding event): %s" % errormsg)								
			else:
				# add parsed event into the list of events
				self.eventlist.append({'header': header, 'datalist': event.data})			
				# add parsed event_id into the list of event_ids			
				self.event_ids.append(message[2])
			
		# set the trigger rate in Storage Manager
		if trigger_rate.triggerRate != 0:			
			self.setTriggerRate(trigger_rate)		
			
		# add all parsed events into the Storage		
		res = self.storageManager.addEvents(self.eventlist)
		# clear the event id list if events cannot be stored in Storage DB
		if res != True:
			self.event_ids = []						
			return self.discard_event_ids		

		return self.event_ids

	#--------------------------End of parseMessages--------------------------#

