import sys
sys.path.append("../src")
from StorageManager import StorageManager
from Observer import Observer
import unittest
from cPickle import loads

class Event:
    def __init__(self, datetime):
        self.datetime = datetime

observer_calls = 0

class Obs(Observer):
    def notify(self, count):
	    global observer_calls
	    observer_calls += count

class TestStorageManager(unittest.TestCase):

    def setUp(self):
        # create a few dummy events
        self.e1 = Event(0)
        self.e2 = Event(4)
        self.e3 = Event(5)
        self.e4 = Event(6)

	self.elist = [self.e1,self.e2,self.e3,self.e4]
        # add bogus information to an event
        self.e1.data = "hello world"
        self.e2.data = "snd message"
        self.e3.data = "non-funny message"
        self.e4.data = "whatever"
        
        # setup storagemanager
        self.sm = StorageManager()
	self.sm.setNumServer(2)
	self.sm.openConnection()

    def tearDown(self):
	global observer_calls
        # remove all events to get back in virgin state
        self.sm.clear()
	observer_calls  = 0

    def testAddOnebyOne(self):
        num = self.sm.getNumEvents()
        self.sm.addEvent(self.e1)
        num1 = self.sm.getNumEvents()
        self.sm.addEvent(self.e2)
        num2 = self.sm.getNumEvents()
        self.sm.addEvent(self.e3)
        num3 = self.sm.getNumEvents()
        self.sm.addEvent(self.e4)
        num4 = self.sm.getNumEvents()
	
	# test the numbers
        self.assertEqual(num1, num+1)
        self.assertEqual(num2, num+2)
        self.assertEqual(num3, num+3)
        self.assertEqual(num4, num+4)

    def testAddMultiple(self):
	num = self.sm.getNumEvents()
	self.sm.addEvents(self.elist)
	num4 = self.sm.getNumEvents()
        self.assertEqual(num+4, num4)

    def testGetOneByOne(self):
	# this test also sets the status so that you get a new event each time
        self.sm.addEvent(self.e1)
        self.sm.addEvent(self.e2)
        self.sm.addEvent(self.e3)
        self.sm.addEvent(self.e4)

	self.assertEqual(4, self.sm.getNumEventsServer(0))
	
	(e1,id1) = self.sm.getEvent(0)
	self.assertEqual(self.e1.data, e1)
	self.sm.setUploaded(0, [id1])
	self.assertEqual(3, self.sm.getNumEventsServer(0))

	(e2,id2) = self.sm.getEvent(0)
	self.assertEqual(self.e2.data, e2)
	self.sm.setUploaded(0, [id2])
	self.assertEqual(2, self.sm.getNumEventsServer(0))

	(e3,id3) = self.sm.getEvent(0)
	self.assertEqual(self.e3.data, e3)
	self.sm.setUploaded(0, [id3])
	self.assertEqual(1, self.sm.getNumEventsServer(0))

	(e4,id4) = self.sm.getEvent(0)
	self.assertEqual(self.e4.data, e4)
	self.sm.setUploaded(0, [id4])
	self.assertEqual(0, self.sm.getNumEventsServer(0))

    def testUploadStatus(self):
    	# add events
    	self.sm.addEvents(self.elist)
	# get the ids
	(elist, eids) = self.sm.getEvents(0, 4)
	self.assertEqual(4, self.sm.getNumEvents())
	self.assertEqual(4, self.sm.getNumEventsServer(0))
	self.assertEqual(4, self.sm.getNumEventsServer(1))
	# set server 1 uploaded
	self.sm.setUploaded(0, eids)
	self.assertEqual(4, self.sm.getNumEvents())
	self.assertEqual(0, self.sm.getNumEventsServer(0))
	self.assertEqual(4, self.sm.getNumEventsServer(1))
	# set server 2 uploaded
	self.sm.setUploaded(1, eids)
	self.assertEqual(0, self.sm.getNumEvents())
	self.assertEqual(0, self.sm.getNumEventsServer(0))
	self.assertEqual(0, self.sm.getNumEventsServer(1))

    def testUploadStatusWrongID(self):
	self.sm.addEvents(self.elist)
	self.sm.setUploaded(1, [-1,-4,999999999999])
	self.assertEqual(4, self.sm.getNumEvents())
	self.assertEqual(4, self.sm.getNumEventsServer(0))
	self.assertEqual(4, self.sm.getNumEventsServer(1))
    
    def testUploadStatusWrongServerID(self):
    	self.sm.addEvents(self.elist)
	(elist, eids) = self.sm.getEvents(0, 4)
	self.sm.setUploaded(11, eids)
	self.assertEqual(4, self.sm.getNumEvents())
	self.assertEqual(4, self.sm.getNumEventsServer(0))
	self.assertEqual(4, self.sm.getNumEventsServer(1))

	# now see if we can still remove it
	self.sm.setUploaded(0, eids)
	self.sm.setUploaded(1, eids)
	self.assertEqual(0, self.sm.getNumEvents())

    def testGetMultiple(self):
        self.sm.addEvents(self.elist)
	(elist, eidlist) = self.sm.getEvents(0,4)
	i=0
	for e in elist:
		self.assertEqual(e, self.elist[i].data)
		i = i + 1

    def testOtherBatchSize(self):
	    self.sm.addEvents(self.elist)

	    (elist, eidlist) = self.sm.getEvents(0,1)
	    self.assertEqual(1, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,2)
	    self.assertEqual(2, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,3)
	    self.assertEqual(3, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,4)
	    self.assertEqual(4, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,5)
	    self.assertEqual(4, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,0)
	    self.assertEqual(0, len(elist))

	    # remove 2 and test again
    	    (elist, eidlist) = self.sm.getEvents(0,5)
	    self.sm.setUploaded(0, [eidlist[0], eidlist[1]])

	    (elist, eidlist) = self.sm.getEvents(0,1)
	    self.assertEqual(1, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,2)
	    self.assertEqual(2, len(elist))
	    (elist, eidlist) = self.sm.getEvents(0,3)
    	    self.assertEqual(2, len(elist))

    def testObserver(self):
	    global observer_calls
	    obs = Obs()
	    self.sm.addObserver(obs)
	    self.sm.addEvent(self.e1)
	    self.assertEqual(1, observer_calls)
	    self.sm.addEvents(self.elist)
	    self.assertEqual(5, observer_calls)

    def testTwoObservers(self):
	    global observer_calls
	    self.sm.addObserver(Obs())
	    self.sm.addObserver(Obs())
	    self.sm.addEvent(self.e1)
	    self.assertEqual(2, observer_calls)
	    self.sm.addEvents(self.elist)
	    self.assertEqual(10, observer_calls)

if __name__ == '__main__':
    unittest.main()
