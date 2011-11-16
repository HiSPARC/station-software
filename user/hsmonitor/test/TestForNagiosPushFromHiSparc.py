#TODO insert default values for configuration file
"""A test for the main process of the HiSPARC monitor.

This process creates other objects and threads.

"""

__author__="thevinh"
__date__ ="$16-sep-2009"

import os, sys, cmd
sys.path.append("../src")
import hslog
from EConfigParser import EConfigParser
import BufferListener
from Interpreter import Interpreter
from CheckScheduler import CheckScheduler
from StorageManager import StorageManager
from Uploader import Uploader

# Default configuration file path
CONFIG_INI_PATH1 = '../data/config.ini'
CONFIG_INI_PATH2 = '../../../persistent/configuration/config.ini'

NUMSERVERS = 2 # TODO

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

    def createBufferListener(self, interpreter):
        # get the information from configuration file
        bufferdb = {}
        bufferdb['host'] = self.cfg.get('BufferDB', 'Host')
        bufferdb['db'] = self.cfg.get('BufferDB', 'DB')
        bufferdb['user'] = self.cfg.get('BufferDB', 'Username')
        bufferdb['password'] = self.cfg.get('BufferDB', 'Password')
        bufferdb['poll_interval'] = self.cfg.get('BufferDB', 'Poll_Interval')
        bufferdb['poll_limit'] = self.cfg.get('BufferDB', 'Poll_Limit')
        bufferdb['keep_buffer_data'] = self.cfg.get('BufferDB', 'KeepBufferData')

        # create an instance of BufferListener class
        buffLis = BufferListener.BufferListener(bufferdb, interpreter)

        if not buffLis:
            hslog.log("Cannot connect to the buffer database!")
            return None
        # TODO better error handling

        return buffLis

    def createCheckScheduler(self, interpreter):
        # get the nagios configuration section from config file
        nagiosConf = self.cfg.itemsdict('NagiosPush')
        checkSched = CheckScheduler(nagiosConf, interpreter)
        return checkSched

    def createUploader(self, serverID, section_name, numServers):
        # TODO create default values if parameter doesn't exist
        stationID = self.cfg.get("Station", "StationID")
        url = self.cfg.get(section_name, "URL")
        passw = self.cfg.get(section_name, "Password")
        minbs = self.cfg.ifgetint(section_name, "MinBatchSize", 50)
        maxbs = self.cfg.ifgetint(section_name, "MaxBatchSize", 50)
        if (minbs > maxbs):
            raise Exception("Minimum batch size must be less than maximum batch size")
        minwait = self.cfg.ifgetfloat(section_name, "MinWait", 1.0)
        maxwait = self.cfg.ifgetfloat(section_name, "MaxWait", 60.0)
        up = Uploader(serverID, numServers, stationID, passw, url,
                      minwait, maxwait, minbs, maxbs)
        return up

def main():
    # create a HiSparc monitor object
    hsMonitor = HsMonitor()

##    # start all threads
##    hsMonitor.startAll()
##
##    # this to get the keyboard interruption
##    c = cmd.Cmd()
##
##    try:
##        c.cmdloop()
##    except KeyboardInterrupt:
##         # stop all threads
##         hsMonitor.stopAll()

    # wait for all threads to finish
    #for thread in hsMonitor.hsThreads:
    #    thread.join()

    # DBG: test the nagios push
    # buffLis = hsMonitor.createBufferListener()
    # buffLis.test()

    # DBG: test the nagios push
    sm = StorageManager()
    it = Interpreter(sm)
    checkSched = hsMonitor.createCheckScheduler(it)
    checkSched.run()

if __name__ == '__main__':
    main()
