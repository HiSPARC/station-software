"""Upload Events to the datastore

This module retrieves Events from the storage using the StorageManager
and uploads the events in batches to the datastore.

"""

import logging
from time import sleep, time
from cPickle import dumps
import requests
from threading import Thread, Semaphore, Event
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

from Observer import Observer
from StorageManager import StorageManager
from UserExceptions import ThreadCrashError

logger = logging.getLogger('hsmonitor.uploader')

# TODO add observer
# use BUI's trick to stop a thread
BATCHSIZE = 100
# the waiting time will be doubled for each failed attempt
MINWAIT = 1  # minimum time to wait in seconds after a failed attempt
MAXWAIT = 60  # maximum time to wait in seconds after a failed attempt

# requests (connection, read) timeout
# timeout quickly on connections, but wait for response after upload
# a long ReadTimeout prevents duplicate events (see issue #2)
TIMEOUT = (3, 600)


class Uploader(Observer, Thread):
    def __init__(self, serverID, stationID, password, URL,
                 retryAfter=MINWAIT, maxWait=MAXWAIT,
                 minBatchSize=BATCHSIZE, maxBatchSize=BATCHSIZE):
        self.storageManager = StorageManager()
        self.serverID = serverID
        self.stationID = stationID
        self.password = password
        self.URL = URL
        self.minBatchSize = minBatchSize
        self.maxBatchSize = maxBatchSize
        self.retryAfter = MINWAIT
        self.maxWait = MAXWAIT

        # lock to protect numEvents
        self.numEventsLock = Semaphore(1)

        # Semaphore to block if the number of events drops below minBatchSize
        self.noEventsSem = Semaphore(0)

        super(Uploader, self).__init__(name='Uploader')
        self.stop_event = Event()
        self.isRunning = False

    def setNumServer(self, numServer):
        """Sets the number of servers to upload to.

        Need to be set before changing the UploadedTo-status
        of events in the StorageManager.

        """
        self.storageManager.setNumServer(numServer)

    def stop(self):
        self.stop_event.set()
        # release semaphore
        self.noEventsSem.release()

    crashes = []

    def init_restart(self):
        """Support for restarting crashed threads."""

        if len(self.crashes) > 3 and time() - self.crashes[-3] < 60.:
            raise ThreadCrashError("Thread has crashed three times in "
                                   "less than a minute")
        else:
            super(Uploader, self).__init__()
            self.crashes.append(time())

    def notify(self, count=1):
        """Notify the uploader that count events were received."""

        if (self.isRunning):
            shouldRelease = 0
            self.numEventsLock.acquire()

            oldNumEvents = self.numEvents
            self.numEvents += count
            logger.debug('%i: %i events pending.' %
                         (self.serverID, self.numEvents))

            # calculate if uploader-thread should be unblocked
            if (self.numEvents >= self.minBatchSize and
                    oldNumEvents < self.minBatchSize):
                shouldRelease = 1

            self.numEventsLock.release()

            if (shouldRelease):
                self.noEventsSem.release()

    def __getNumEventsToUpload(self):
        """Gives the number of events that the Uploader can upload now.

        The result will be between min and max batch size. If insufficient
        events are available this function will block on noEventSem.

        """

        shouldBlock = False
        self.numEventsLock.acquire()
        res = min(self.numEvents, self.maxBatchSize)
        if (res < self.minBatchSize):
            shouldBlock = True
        self.numEventsLock.release()

        if shouldBlock:
            logger.debug('%i: Blocked: Too few events' % self.serverID)
            self.noEventsSem.acquire()
            logger.debug('%i: Unblocked' % self.serverID)
            return self.minBatchSize
        else:
            return res

    def __upload(self, elist):
        """Upload a list of events to the database server."""

        elist_data = dumps(elist)
        checksum = md5(elist_data).hexdigest()

        data = {
            'station_id': self.stationID,
            'password': self.password,
            'data': elist_data,
            'checksum': checksum
        }

        # Open the connection and send our data. Exceptions are caught
        # explicitly to make sure we understand the implications of errors.
        try:
            r = requests.post(self.URL, data=data, timeout=TIMEOUT)
        except (requests.Timeout, requests.ConnectionError) as exc:
            returncode = ('Connection error in function'
                          '__upload: %s' % str(exc))
        except Exception as exc:
            returncode = ('Uncatched exception occured in function '
                          '__upload: %s' % str(exc))
        else:
            returncode = r.text

        return returncode

    def run(self):
        """Main loop that continously polls for new events and uploads them"""

        logger.info('%i: Thread started for %s.' % (self.serverID, self.URL))

        # Initialize storage manager
        self.storageManager.openConnection()

        # Number of events that have been received
        logger.debug('%i: Getting number of events to upload.' % self.serverID)
        self.numEvents = self.storageManager.getNumEventsServer(self.serverID)
        logger.debug('%i: %i events in storage.' %
                     (self.serverID, self.numEvents))

        self.isRunning = True

        numFailedAttempts = 0
        while not self.stop_event.isSet():
            bsize = self.__getNumEventsToUpload()

            (elist, eidlist) = self.storageManager.getEvents(self.serverID,
                                                             bsize)
            returncode = self.__upload(elist)
            if returncode == '100':
                logger.info('%i: %d events uploaded to %s.' %
                            (self.serverID, bsize, self.URL))

                numFailedAttempts = 0

                # Record successful upload in storagemanager
                self.storageManager.setUploaded(self.serverID, eidlist)
                # Reduce counter
                self.numEventsLock.acquire()
                self.numEvents -= bsize
                self.numEventsLock.release()
            else:
                numFailedAttempts += 1

                msg1 = ("Error Uploader %i: %s: Return code: %s." %
                        (self.serverID, self.URL, returncode))
                logger.error(msg1)
                msg2 = ("Error Uploader %i: %d events attempted to upload, "
                        "number of failed attempts: %i." %
                        (self.serverID, bsize, numFailedAttempts))
                logger.error(msg2)
                sleeptime = min(2 ** numFailedAttempts * self.retryAfter,
                                self.maxWait)
                logger.debug('%i: Sleeping for %f seconds.' %
                             (self.serverID, sleeptime))
                sleep(sleeptime)
        logger.warning('%i: Thread stopped!' % self.servedID)
