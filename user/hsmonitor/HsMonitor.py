"""The main HiSPARC monitor process, it creates other objects and threads.

DF: Unfortunately, I think the UML model of this system is not entirely
    correct. For example, this creates several instances of our StorageManager
    class. It has its own class, that's good, but I think it should also have
    just one instance. At the moment, there are three instances: the HsMonitor
    one, which doubles as an instance for the BufferListener and which contains
    the observers, and one for each uploader, which handle the actual data
    storage. As a result of this, we have four (!) instances of a numServers
    variable, which *all* need to have the exact same value and thus need to be
    updated when there is a change in the number of uploaders.

ADL: Check how the HsMonitor is started, what is the 'working directory'?
"""

import re
from time import sleep

from hslog import log, setLogMode, MODE_BOTH
from EConfigParser import EConfigParser
from BufferListener import BufferListener
from Interpreter import Interpreter
from CheckScheduler import CheckScheduler
from StorageManager import StorageManager
from Uploader import Uploader
from UserExceptions import ThreadCrashError

# Default configuration file path
CONFIG_INI_PATH1 = 'data/config.ini'
CONFIG_INI_PATH2 = '../../persistent/configuration/config.ini'


class HsMonitor:
    def __init__(self):
        # Setup the log mode
        setLogMode(MODE_BOTH)

        # Read the configuration file
        try:
            self.cfg = EConfigParser()
            self.cfg.read([CONFIG_INI_PATH1, CONFIG_INI_PATH2])
        except:
            log("HsMonitor: Cannot open the config file!")
            return
        else:
            log("HsMonitor: Initialize variables.")

            # List of all the threads
            self.hsThreads = []
        # Assume one server (datastore)
        # if the local is also specified it will be added
        self.numServers = 1

    def startAll(self):
        """Setup and start all threads."""
        try:
            # Create StorageManager and Interpreter for BufferListener
            storMan = StorageManager()
            interpr = Interpreter(storMan)

            # Create BufferListener
            buffLis = self.createBufferListener(interpr)

            if buffLis.conn:
                self.hsThreads.append(buffLis)

            # Check scheduler
            # Get the nagios configuration section from config file
            nagiosConf = self.cfg.itemsdict('NagiosPush')
            machine = re.search('([a-z0-9]+).zip',
                                self.cfg.get('Station', 'Certificate'))
            nagiosConf['machine_name'] = machine.group(1)
            checkSched = self.createCheckScheduler(interpr, nagiosConf)
            eventRate = checkSched.getEventRate()
            storMan.addObserver(eventRate)
            self.hsThreads.append(checkSched)

            # Uploader central
            up = self.createUploader(0, "Upload-datastore", nagiosConf)
            self.hsThreads.append(up)
            storMan.addObserver(up)
            up.setNumServer(self.numServers)

            # Try local server
            try:
                up2 = self.createUploader(1, "Upload-local", nagiosConf)
                self.hsThreads.append(up2)
                storMan.addObserver(up2)
                self.numServers += 1
                up.setNumServer(self.numServers)
                up2.setNumServer(self.numServers)
            except Exception, msg:
                log("HsMonitor: Error while parsing local server: %s." % msg)
                log("HsMonitor: Will not upload to local server!")

            # Set number of servers for our own StorageManager
            storMan.setNumServer(self.numServers)
            storMan.clearOldUploadedEvents()

            # Start all threads, running their run() function.
            for thread in self.hsThreads:
                thread.start()

        except Exception, msg:
            log("Error HsMonitor: %s" % msg)
            exit(1)

    def stopAll(self):
        """Stops all threads."""
        for thread in self.hsThreads:
            thread.stop()

    def createBufferListener(self, interpreter):
        # Get the information from configuration file
        bufferdb = {}
        bufferdb['host'] = self.cfg.ifgetstr('BufferDB', 'Host', 'localhost')
        bufferdb['db'] = self.cfg.ifgetstr('BufferDB', 'DB', 'buffer')
        bufferdb['user'] = self.cfg.ifgetstr('BufferDB', 'Username', "buffer")
        bufferdb['password'] = self.cfg.ifgetstr('BufferDB', 'Password',
                                                 "PLACEHOLDER")
        bufferdb['poll_interval'] = self.cfg.ifgetfloat('BufferDB',
                                                        'Poll_Interval', 1.0)
        bufferdb['poll_limit'] = self.cfg.ifgetint('BufferDB', 'Poll_Limit',
                                                   100)
        bufferdb['keep_buffer_data'] = self.cfg.ifgetint('BufferDB',
                                                         'KeepBufferData', 0)

        # Create an instance of BufferListener class
        buffLis = BufferListener(bufferdb, interpreter)
        return buffLis

    def createCheckScheduler(self, interpreter, nagiosConf):
        checkSched = CheckScheduler(nagiosConf, interpreter)
        return checkSched

    def createUploader(self, serverID, section_name, nagiosConf):
        stationID = self.cfg.get("Station", "Nummer")
        url = self.cfg.get(section_name, "URL")
        passw = self.cfg.get("Station", "Password")
        minbs = self.cfg.ifgetint(section_name, "MinBatchSize", 50)
        maxbs = self.cfg.ifgetint(section_name, "MaxBatchSize", 50)
        if (minbs > maxbs):
            log("Warning HsMonitor: Maximum batch size must be more than "
                "minimum batch size. Setting maximum=minimum.")
            maxbs = minbs
        minwait = self.cfg.ifgetfloat(section_name, "MinWait", 1.0)
        maxwait = self.cfg.ifgetfloat(section_name, "MaxWait", 60.0)

        up = Uploader(serverID, stationID, passw, url, nagiosConf,
                      minwait, maxwait, minbs, maxbs)
        return up


def main():
    # Create a HiSPARC monitor object
    hsMonitor = HsMonitor()

    # Start all threads
    hsMonitor.startAll()

    # Periodically check for crashed threads, and restart them if necessary
    try:
        while True:
            sleep(10)
            for thread in hsMonitor.hsThreads:
                if not thread.is_alive():
                    log("HsMonitor: Thread %s died, restarting." % thread.name)
                    thread.init_restart()
                    thread.start()
                    log("HsMonitor: Thread %s restarted." % thread.name)
    except ThreadCrashError, exc:
        log(exc)
        log("HsMonitor: Thread %s keeps crashing, shutting down." %
            thread.name)
    except KeyboardInterrupt:
        log("HsMonitor: Interrupted by keyboard, closing down.")

    # Close down everything
    hsMonitor.stopAll()
    # wait for all threads to finish
    for thread in hsMonitor.hsThreads:
        thread.join()

if __name__ == '__main__':
    main()
