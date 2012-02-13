import time
import sys
import re
import os
from threading import Lock

MODE_PRINT = 1
MODE_FILE = 2
MODE_BOTH = MODE_PRINT | MODE_FILE

logMode = MODE_FILE

lock = Lock()

# severity support is not implemented yet
# but the constants are here so the interface is ready

SEVERITY_NORMAL = 1
SEVERITY_CRITICAL = 2

# "private" function that extracts current application name by taking the
# directory of the initially invoked .py file.


def getCurrentAppName():
    mo = re.search('\\\\([^\\\\]*)$', sys.path[0])
    return mo.group(1)

# Sends a message to screen, to a file, or both, depending on the logMode.
# The optional severity parameter is not implemented yet, but you are still
# recommended to pass SEVERITY_CRITICAL in case you are logging an error that
# cannot be recovered from without user intervention.


def log(message, severity=SEVERITY_NORMAL):
    global logMode
    lock.acquire()

    if logMode & MODE_PRINT:
        print message

    if logMode & MODE_FILE:
        # make directory if it does not exist yet
        logDirname = "/persistent/logs/%s" % getCurrentAppName()
        if not os.access(logDirname, os.F_OK):
            os.makedirs(logDirname)

        # compute filename
        logFilename = time.strftime('%d-%m-%Y', time.localtime())
        logFilename = '%s/%s.log' % (logDirname, logFilename)

        # write log message
        line = "%s - %s\n" % (time.strftime('%H:%M:%S', time.localtime()),
                              message)
        fp = open(logFilename, 'a')
        fp.write(line)
        fp.close()
    lock.release()


def setLogMode(mode):
    global logMode
    lock.acquire()
    if not mode in [MODE_PRINT, MODE_FILE, MODE_BOTH]:
        raise Exception("incorrect log mode!")
    logMode = mode
    lock.release()
