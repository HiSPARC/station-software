import sqlite3
import sys
import os
from threading import Lock
from cPickle import dumps
from cPickle import loads
import time

from Subject import Subject
import sys
sys.path.append("..\..\pythonshared")
from hslog import log

FILENAME = "../../../persistent/data/hsmonitor/Storage.db"
VACUUMTHRESHOLD = 1000

lock = Lock()

class StorageManager(Subject):
	"""The Storage Manager is used to access the sqlite database called storage. Prior to version 3.3.1 of SQLite you 
	cannot transfer objects of SQLite, e.g. the connection or the cursor, accross threads. Therefore thread needs to use
	its own instance of the storagemanager. Make sure to create the instance within the run()-method and not in the 
	constructor"""
        
        storagesize = None
        lastvacuum = 0
        
        def __init__(self, db_name=FILENAME):
		global lock
		self.db_name = db_name
                self.lock = lock
                Subject.__init__(self)

		if not os.path.exists(self.db_name):
                	self.__create()
	
	def setNumServer(self,numServer):
                """numServer: the number of servers to upload to. The StorageManager needs this information to know when events
                have been uploaded to all servers and can be removed from the storage.
                """
		self.numServer = numServer
		# Compute the all-uploaded mask: the field uploadedTo should contain all 1's for servers that
                # have been uploaded to.
                # For example with 2 servers, allUploadedMask is 0b11 (3).
                self.allUploadedMask = 0
                for i in xrange(0,numServer):
                        self.allUploadedMask |= 1 << i
	
	def openConnection(self):
		"""Opens a connection to the sql-storage. This function must be called before the other functions can be used.
		It must be executed on the same thread on which the other functions are executed: i.e. in the run()-method of 
		a thread
		"""
                try: 
                	self.db = sqlite3.connect(self.db_name)
                except Exception, msg:
			log("StorageManager: Error opening connection: %s" % (str(msg),))
                        raise Exception("Could not connect to sqlite3 database.")
                
        def __create(self):
                """
                Create a new database structure.
                """
		db = sqlite3.connect(self.db_name)
                c = db.cursor()
                c.execute("""
                    CREATE TABLE Event ( 
                        EventID INTEGER PRIMARY KEY AUTOINCREMENT,
                        EventData BLOB,                         
                        UploadedTo Integer,                                                                     
                        DateTime TIMESTAMP
                    );                  
                    """
                )
		db.commit()
                c.close()
        
        def getEventsRawSQL(self, serverID, numEvents):
                """
                Return numEvents that were not yet uploaded to the server identified by serverID
		Return the output from SQL (so with status and id, do you need this?)
                """
                serverbit = 1 << serverID
                self.lock.acquire()
                c = self.db.cursor()
                ssize = StorageManager.storagesize
                if (ssize is not None and ssize < VACUUMTHRESHOLD and
                    time.time() - StorageManager.lastvacuum > 100000):
                        log("Starting VACUUM operation...")
                        c.execute("VACUUM")
                        StorageManager.lastvacuum = time.time()
                        log("VACUUM finished.")
                c.execute("""
                        SELECT * FROM Event WHERE (UploadedTo & ?) == 0 LIMIT ?;
                        """, (serverbit, numEvents))
                res = c.fetchall()
                c.close()
                self.lock.release() 
                return res

	def getEvents(self, serverID, numEvents):
		"""
                Return numEvents that were not yet uploaded to the server identified by serverID
		The result is a tuple: the first element is a list containing the data attribute of the events that were inserted.
		the second element is a list with the corresponding event ids in the storage
                """
		raw_results = self.getEventsRawSQL(serverID, numEvents)
		elist = list()
		eidlist = list()
		for r in raw_results:
			(id, blob, uploadedto, datetime) = r
			elist.append(loads(str(blob)))
			eidlist.append(id)
		return (elist, eidlist)

	def getEvent(self, serverID):
		""" return tuple consisting of (event,id)"""
		raw_results = self.getEventsRawSQL(serverID, 1)
		if len(raw_results) > 0:
			(id, blob, uploadedto, datetime) = raw_results[0]
			return (loads(str(blob)), id)
		else:
			return None

        def addEvents(self, events):
                """
                Insert events in the storage and notifies all observers.
                The parameters events is a list of events. 
		Each event is assumed to have a datetime attribute and a data attribute.
		The data attribute will be pickled and stored.
                The StorageManager is responsible for serializing the events.
                """

		res = True
                n_events = len(events)
                if n_events > 0:
			log("StorageManager: adding %d parsed events into Storage" %(n_events,))
                        self.lock.acquire()
			log("Acquired lock.")
                        t0 = time.time()

                        c = self.db.cursor()
                        query = """INSERT INTO Event (EventData, UploadedTo, DateTime) VALUES (?,0,?)"""
                        try:
                                c.executemany(query, ((dumps(event), event['header']['datetime']) for event in events))
                                self.db.commit()
                                c.close()
                        except sqlite3.OperationalError, msg:
                                res = False # return False so that events are NOT removed from buffer
                                log("StorageManager: Error AddEvents: %s" % (str(msg),))
                                
                        if StorageManager.storagesize is not None:
                                StorageManager.storagesize += n_events

                        self.lock.release()
			log("Events added in %d seconds." % (time.time() - t0))
                        
                        # notify the observers
                        self.update(n_events)

			return res

        def addEvent(self, event):
                le = list()
                le.append(event)
                self.addEvents(le)

        def __IDList2String(self, IDs):
                """ Helper function that transforms a list of integers in a string like "(1,3,4,5)".
                """
                string_ids = []
                for ei in IDs:
                        string_ids.append("%i" % int(ei))
                list_id = "(" +",".join(string_ids) + ")"
                return list_id
        
        def setUploaded(self, serverID, eventIDs):
                """
                record in the UploadedTo-field of the event that the event was uploaded to server identified by serverID.
                If the event is uploaded to all servers, remove the event
                """
                serverbit = 1 << serverID
                self.lock.acquire()
                c = self.db.cursor()

                # First get the UploadedTo status from the db
                query = """SELECT EventID, UploadedTo from Event Where EventID IN %s;""" % self.__IDList2String(eventIDs)
                c.execute(query)

                # Split the result in events whose status needs to be updated and the events that have to be removed
                need_update = []
                need_remove = []
                for row in c:
                        (eid, e_upto) = row
                        # Set serverbit to 1
                        e_upto |= serverbit
                        if e_upto & self.allUploadedMask == self.allUploadedMask:
                                need_remove.append(eid)
                        else:
                                need_update.append(eid)

                # Remove events that have been uploaded to all servers
                n_remove = len(need_remove)
                if n_remove > 0:
                        query = """DELETE from Event WHERE EventID in %s;""" % self.__IDList2String(need_remove)
			log("StorageManager: %d events removed from Storage" % n_remove)
                        c.execute(query)
                        if StorageManager.storagesize is not None:
                                StorageManager.storagesize -= n_remove
                        
                # Update status of events that have not yet been uploaded to all servers
		n_need_update = len(need_update)
                if len(need_update) > 0:
                        query = """UPDATE Event Set UploadedTo = UploadedTo | ? WHERE EventId in %s;""" % self.__IDList2String(need_update)
			log("StorageManager: %d events updated in Storage" % n_need_update)
                        c.execute(query, (serverbit,))

                self.db.commit()
                c.close()
                self.lock.release()

        def getNumEvents(self):
                """ Return the number of events currently in the storage. """
                self.lock.acquire()
                (res,) = self.db.execute("""SELECT COUNT(*) FROM Event;""")
                StorageManager.storagesize, = res
                self.lock.release()
                (numEvents,) = res
		return int(numEvents)

        def getNumEventsServer(self, serverID):
                """ Return the number of events that still need to be uploaded to a server identified by serverID """
                serverbit = 1 << serverID
                
                self.lock.acquire()
                c = self.db.cursor()
                (qres,) = c.execute("""SELECT COUNT(*) FROM Event Where UploadedTo & ? == 0;""", (serverbit,))
                (res,) = qres
                c.close()
                self.lock.release()
                return res

        def clear(self):
                """For testing purposes: remove all events"""
                self.lock.acquire()
                c = self.db.cursor()
                c.execute("""DELETE FROM Event;""")
		self.db.commit()
                c.close()
                self.lock.release()

	def clearOldUploadedEvents(self):
		"""Delete old, already uploaded events

		   Beware: if the number of servers is NOT correctly
		   set, you might accidentally delete events which are
		   only uploaded to the central datastore, because this
		   function is created to delete old events when the
		   local URL is dropped.  Therefore, once that URL has
		   been dropped, it will even delete events which have
		   not yet been uploaded to that URL.

		"""
		self.lock.acquire()
		self.openConnection()
		c = self.db.cursor()

		log("Deleting old events which have already been uploaded to all currently specified servers")
		sql = "SELECT COUNT(*) FROM Event WHERE UploadedTo & ? = ?"
		args = (self.allUploadedMask, self.allUploadedMask)
		c.execute(sql, args)
		log("Deleting %d events." % c.fetchone()[0])

		sql = "DELETE FROM Event WHERE UploadedTo & ? = ?"
		args = (self.allUploadedMask, self.allUploadedMask)
		c.execute(sql, args)
		self.db.commit()

		c.close()
		self.lock.release()
