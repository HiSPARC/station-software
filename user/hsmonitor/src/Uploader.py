from Observer import Observer
from StorageManager import StorageManager
import sys
from hslog import log
from NagiosPush import NagiosPush
from NagiosResult import NagiosResult
from UserExceptions import ThreadCrashError
from threading import Thread
from threading import Semaphore
from threading import Event
from time import sleep
from cPickle import dumps
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError
import time

# TODO add observer
# use BUI's trick to stop a thread
BATCHSIZE = 100
MINWAIT = 1 # minimum time to wait in seconds after a failed attempt
            # the waiting time will be double for each failed attempt
MAXWAIT = 60 # maximum time to wait in seconds after a failed attempt

# Python >= 2.5 has hashlib
try:
    from hashlib import md5
    def md5_sum(s):
        return md5(s).hexdigest()
except:
    print "ERROR: No hashlib found. Using md5 instead."
    import md5
    def md5_sum(s):
        return md5.new(s).hexdigest()

class Uploader(Observer, Thread):
    def __init__(self, serverID, stationID, password, URL, config, retryAfter = MINWAIT, maxWait = MAXWAIT, minBatchSize = BATCHSIZE, maxBatchSize = BATCHSIZE):
        self.storageManager = StorageManager()
        self.serverID = serverID
        self.stationID = stationID
        self.password = password
        self.URL = URL
        self.nagiosPush = NagiosPush(config)
        self.minBatchSize = minBatchSize
        self.maxBatchSize = maxBatchSize
        self.retryAfter = MINWAIT
        self.maxWait = MAXWAIT

        # lock to protect numEvents
        self.numEventsLock = Semaphore(1)

        # Semaphore to block if the number of events drops below minBatchSize
        self.noEventsSem = Semaphore(0)

        Thread.__init__(self)
        self.stop_event = Event()
        self.isRunning = False

    def setNumServer(self, numServer):
        """ The number of servers need to be set before changing the uploadedto-status of events in the storagemanager"""
        self.storageManager.setNumServer(numServer)

    def stop(self):
        self.stop_event.set()
        # release semaphore
        self.noEventsSem.release()

        crashes = []
        def init_restart(self):
            """Support for restarting crashed threads"""

            if len(self.crashes) > 3 and time.time() - self.crashes[-3] < 60.:
                raise ThreadCrashError("Thread has crashed three times in "
                                       "less than a minute")
            else:
                # FIXME correctly work out that super stuff.  I think that
                # the superclasses should both use super, but ...?
                #super(Uploader, self).__init__()
                Thread.__init__(self)
                self.crashes.append(time.time())

    def notify(self, count=1):
        """Notify the uploader that count events were received."""

        if (self.isRunning):
            shouldRelease = 0
            self.numEventsLock.acquire()

            oldNumEvents = self.numEvents
            self.numEvents += count
            log("Uploader %i: %i events pending" % (self.serverID, self.numEvents))

            # calculate if uploader-thread should be unblocked
            if (self.numEvents >= self.minBatchSize and oldNumEvents < self.minBatchSize):
                shouldRelease = 1

            self.numEventsLock.release()

            if (shouldRelease):
                self.noEventsSem.release()

    def __getNrEventsToUpload(self):
        """This function will return the number of events that the uploader can upload now.
        The result will be between min and max batch size.
        If insufficient events are available this function will block on noEventSem"""

        shouldBlock = False
        res = self.minBatchSize
        self.numEventsLock.acquire()
        res = min(self.numEvents, self.maxBatchSize)
        if (res < self.minBatchSize):
            shouldBlock = True
        self.numEventsLock.release()

        if shouldBlock:
            log("Uploader %i blocks: too few events" % (self.serverID,))
            self.noEventsSem.acquire()
            log("Uploader %i unblocks" % (self.serverID,))
            return self.minBatchSize
        else:
            return res

    def __upload(self, elist):
        """
            Upload a list of events to the database server
        """

            data = dumps(elist)
            checksum = md5_sum(data)

            params = urlencode(
                {
                        'station_id': self.stationID,
                        'password': self.password,
                        'data': data,
                        'checksum': checksum,
            }
            )

        # Open the connection and send our data. Exceptions are catched explicitly
            # to make sure we understand the implications of errors.
            try:
                f = urlopen(self.URL, params, timeout=30)
        except (URLError, HTTPError), msg:
                # For example: connection refused or internal server error
                returncode = str(msg)
            except Exception, msg:
                returncode = 'Uncatched exception occured in function ' \
                             '__upload: %s' % str(msg)
            else:
                returncode = f.read()

            return returncode

    def run(self):
        log("Uploader %i: thread started for %s" % (self.serverID, self.URL))

        # Initialize storage manager
        self.storageManager.openConnection()

        # number of events that have been received
                log("Getting number of events to upload")
        self.numEvents = self.storageManager.getNumEventsServer(self.serverID)
        log("Uploader %i: %i events in storage" % (self.serverID, self.numEvents))

        self.isRunning = True

        nrFailedAttempts = 0
        while not self.stop_event.isSet():
            bsize = self.__getNrEventsToUpload()

            (elist, eidlist) = self.storageManager.getEvents(self.serverID, bsize)
            returncode = self.__upload(elist)
            if returncode == '100':
                log("Uploader %i: %d events uploaded to %s." % (self.serverID, bsize, self.URL))

                nrFailedAttempts = 0

                # record succesfull upload in storagemanager
                self.storageManager.setUploaded(self.serverID, eidlist)
                # reduce counter
                self.numEventsLock.acquire()
                self.numEvents -= bsize
                self.numEventsLock.release()
            else:
                msg = "Error Uploader %i: %s: return code: %s" % (self.serverID, self.URL, returncode)
                msg += "\n"
                msg += "Uploader %i: nr of Failed Attempts: %i" %(self.serverID, nrFailedAttempts)
                log(msg)
                nr = NagiosResult(2, msg, "ServerCheck")
                self.nagiosPush.sendToNagios(nr)

                sleeptime = min(2 ** nrFailedAttempts * self.retryAfter, self.maxWait)
                log("Uploader %i: Sleeping for %f seconds." %(self.serverID, sleeptime))
                sleep(sleeptime)
                nrFailedAttempts += 1
        log("Uploader %i: thread stopped!" % (self.serverID,))