""" TimedRotatingFileHandler using 3rd-party module to be thread-safe.

The reason for using this is that the default TimedRotatingFileHandler
that Python provides is not thread-safe. The
ConcurrentRotatingFileHandler is thread-safe, but has no support for
timed rotation. The TimedConcurrentRotatingFileHandler should combine
the benefits of both.

"""

import os
import time
import sys
import re
from stat import ST_MTIME
from random import randint
from cloghandler import ConcurrentRotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class TimedConcurrentRotatingFileHandler(ConcurrentRotatingFileHandler,
                                         TimedRotatingFileHandler):
    """Logger with support for threads and rotating files.

    Handler for logging to a set of files, which rotate at a specific
    time. Combining ConcurrentRotatingFileHandler and the
    TimedRotatingFileHandler of the standard library. Interval should be
    given in seconds, and defaults to one day. It has no support for
    encoding. The debug option toggles the debug messages of
    ConcurrentRotatingFileHandler (default: off). It also adds support
    for the use of a customized suffix (default: log).

    """
    def __init__(self, filename, backupCount=0, when='D', interval=1,
                 utc=False, mode='a', delay=False, debug=False, suffix='log'):
        # Call __init__ of ConcurrentRotatingFileHandler
        ConcurrentRotatingFileHandler.__init__(self, filename,
                                               backupCount=backupCount,
                                               mode=mode, debug=debug,
                                               supress_abs_warn=True,
                                               maxBytes=0)
        self.when = when.upper()
        self.utc = utc
        if not suffix:
            suffix = 'log'
        if self.when == 'S':
            self.interval = 1  # one second
            self.suffix = "%Y-%m-%d_%H-%M-%S." + suffix
            self.extMatch = (r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?=." +
                             suffix + ")")
        elif self.when == 'M':
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M." + suffix
            self.extMatch = (r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?=." + suffix +
                             ")")
        elif self.when == 'H':
            self.interval = 60 * 60  # one hour
            self.suffix = "%Y-%m-%d_%H." + suffix
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}(?=." + suffix + ")"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.interval = 60 * 60 * 24  # one day
            self.suffix = "%Y-%m-%d." + suffix
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(?=." + suffix + ")"
        elif self.when.startswith('W'):
            self.interval = 60 * 60 * 24 * 7  # one week
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover "
                                 "from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: "
                                 "%s" % self.when)
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d."+suffix
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(?=."+suffix+")"
        else:
            raise ValueError("Invalid rollover interval specified: %s" %
                             self.when)

        self.extMatch = re.compile(self.extMatch)
        self.interval = self.interval * interval  # multiply by units requested
        if os.path.exists(filename):
            t = os.stat(filename)[ST_MTIME]
        else:
            t = int(time.time())
        self.rolloverAt = self.computeRollover(t)

    def _shouldRollover(self):
        """
        Determine whether a rollover should occur. This is an overwrite
        of the method used by ConcurrentRotatingFileHandler, in order to
        make it use time.
        """
        if(TimedRotatingFileHandler.shouldRollover(self, None)):
            return True
        else:
            self._degrade(False, "Rotation done or not needed at this time")
        return False

    def doRollover(self):
        """
        Do a rollover, an overwrite of the handling of
        ConcurrentRotatingFileHandler
        """
        if self.backupCount <= 0:
            # Don't keep any backups, just overwrite the existing backup file
            # Locking doesn't much matter here; since we are overwriting it
            # anyway
            self.stream.close()
            self._openFile("w")
            return
        self.stream.close()
        try:
            # Attempt to rename logfile to tempname. There is a slight
            # race-condition here, but it seems unavoidable.
            tmpname = None
            while not tmpname or os.path.exists(tmpname):
                tmpname = "%s.rotate.%08d" % (self.baseFilename,
                                              randint(0, 99999999))
            try:
                # Do a rename test to determine if we can successfully
                # rename the log file
                os.rename(self.baseFilename, tmpname)
            except (IOError, OSError):
                exc_value = sys.exc_info()[1]
                self._degrade(True, "rename failed.  File in use?  "
                              "exception=%s", exc_value)
                return

            # get the time that this sequence started at and make it a
            # TimeTuple
            t = self.rolloverAt - self.interval
            if self.utc:
                timeTuple = time.gmtime(t)
            else:
                timeTuple = time.localtime(t)
            dfn = self.baseFilename + "." + time.strftime(self.suffix,
                                                          timeTuple)
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(tmpname, dfn)
            if self.backupCount > 0:
                for s in self.getFilesToDelete():
                    os.remove(s)
            self._degrade(False, "Rotation completed")
        finally:
            self._openFile(self.mode)
        # Calculate next roll over time
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if ((self.when == 'MIDNIGHT' or self.when.startswith('W')) and
                not self.utc):
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    newRolloverAt = newRolloverAt - 3600
                else:
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt
