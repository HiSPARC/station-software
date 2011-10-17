"""
This is the main process of the HiSPARC monitor.
This process creates other objects and threads.

DF: Unfortunately, I think the UML model of this system is not entirely
    correct.  For example, this creates several instances of our
    StorageManager class.  It has its own class, that's good, but I
    think it should also have just one instance.  At the moment, there
    are three instances: the HsMonitor one, which doubles as an instance
    for the BufferListener and which contains the observers, and one for
    each uploader, which handle the actual data storage.  As a result of
    this, we have four (!) instances of a numServers variable, which
    *all* need to have the exact same value and thus need to be updated
    when there is a change in the number of uploaders.
"""

__author__ = "thevinh"
__date__ = "$16-sep-2009"

import os, sys
import re
import time
import hslog
from EConfigParser import EConfigParser
import BufferListener
from Interpreter import Interpreter
from CheckScheduler import CheckScheduler
from StorageManager import StorageManager
from Uploader import Uploader
from UserExceptions import ThreadCrashError

# Default configuration file path
CONFIG_INI_PATH1 = '../data/config.ini'
CONFIG_INI_PATH2 = '../../../persistent/configuration/config.ini'

# HsMonitor class
class HsMonitor:
    def __init__(self):
        # setup the log mode
        hslog.setLogMode(hslog.MODE_BOTH)

        # read the configuration file
        try:
            self.cfg = EConfigParser()
            self.cfg.read([CONFIG_INI_PATH1, CONFIG_INI_PATH2])
        except:
            hslog.log("Cannot open the config file!")
            return
        else:
            hslog.log("Initialize variables")

            #list of all the threads
            self.hsThreads = []
        # Assume one server (datastore)
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
            m = re.search('([a-z0-9]+).zip', self.cfg.get('Station', 'Certificate'))
            nagiosConf['machine_name'] = m.group(1)
            checkSched = self.createCheckScheduler(it, nagiosConf)
            eventrate = checkSched.getEventRate()
            sm.addObserver(eventrate)
            self.hsThreads.append(checkSched)

            # Uploader central
            up = self.createUploader(0, "Upload-datastore", nagiosConf)
            self.hsThreads.append(up)
            sm.addObserver(up)
            up.setNumServer(self.numServers)

            # try local server
            try:
                up2 = self.createUploader(1, "Upload-local", nagiosConf)
                self.hsThreads.append(up2)
                sm.addObserver(up2)
                self.numServers += 1
                up.setNumServer(self.numServers)
                up2.setNumServer(self.numServers)
            except Exception, msg:
                hslog.log("Error while parsing local server: %s" %(msg,))
                hslog.log("Will not upload to local server!")

            # Set number of servers for our own StorageManager
            sm.setNumServer(self.numServers)
            sm.clearOldUploadedEvents()

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

    # Periodically check for crashed threads, and restart them if
    # necessary
    try:
        while True:
            time.sleep(10)
            for t in hsMonitor.hsThreads:
                if not t.is_alive():
                    hslog.log("Thread %s died, restarting" % t.name)
                    t.init_restart()
                    t.start()
                    hslog.log("Thread %s restarted." % t.name)
    except ThreadCrashError, exc:
        hslog.log(exc)
        hslog.log("Thread %s keeps crashing, shutting down." % t.name)
    except KeyboardInterrupt:
        hslog.log("Interrupted by keyboard, closing down.")

    # Close down everything
    hsMonitor.stopAll()
    # wait for all threads to finish
    for thread in hsMonitor.hsThreads:
        thread.join()
#--------------------------Main--------------------------#
if __name__ == '__main__':
    main()
