import sys
import time
import logging
from threading import Lock

from Observer import Observer
from NagiosResult import NagiosResult
from StorageManager import StorageManager

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

TIME_DIFF_INI = '../../persistent/configuration/HisparcII.ini'

logging.getLogger('hsmonitor.check')

class Check:
    def __init__(self):
        self.nagiosResult = NagiosResult()
        self.nagiosResult.status_code = UNKNOWN

    def check(self, sched, config):
        pass

    def parse_range(self, prange):
        """Make a tuple from a range string. 'min:max' -> (min, max)"""
        try:
            a = prange.split(':')
            mina = float(a[0])
            maxa = float(a[1])
            return (mina, maxa)
        except:
            logger.critical('Wrong arguments given! %s' % (prange,))
            sys.exit(CRITICAL)


class TriggerRate(Check):
    def __init__(self, interpreter):
        Check.__init__(self)
        self.nagiosResult.serviceName = "TriggerRate"
        self.interpreter = interpreter

    def check(self, sched, config):
        while True:
            try:
                warnRange = config['triggerrate_warn']
                warn = self.parse_range(warnRange)
                critRange = config['triggerrate_crit']
                crit = self.parse_range(critRange)
            except:
                logger.critical('Unable to read config.ini in %s' % 
                                self.nagiosResult.serviceName)
                self.nagiosResult.status_code = CRITICAL

            wmin, wmax = warn
            cmin, cmax = crit

            self.triggerRateValues = self.interpreter.getTriggerRate()
            self.lastupdate = self.triggerRateValues.date
            self.trate = self.triggerRateValues.triggerRate

            if self.trate <= cmin or self.trate >= cmax:
                self.nagiosResult.status_code = CRITICAL
            elif self.trate <= wmin or self.trate >= wmax:
                self.nagiosResult.status_code = WARNING
            else:
                self.nagiosResult.status_code = OK

            if self.lastupdate:
                t = time.strptime(str(self.lastupdate), '%Y-%m-%d %H:%M:%S')

                # Timestamp is in GPS time.  Naively treat it as a local
                # timestamp, then subtract the LabVIEW-determined offset
                # between pc clock time (local time) and GPS time.

                # Read offset from file
                with open(TIME_DIFF_INI) as f:
                    d = {}
                    for line in f:
                        key, value = line.split('=')
                        d[key] = value

                # Naively calculate timestamp and adjust for pc / gps offset
                t = time.mktime(t)
                try:
                    t += int(d['time_difference'])
                except TypeError:
                    # Offset is not yet determined
                    pass
                except ValueError:
                    # Offset may be to large
                    pass
                # Calculate time difference between trigger and 'now'
                dt = time.time() - t
            else:
                # Never updated, make dt very large
                dt = 1e6

            # If last update was significantly longer than time between monitor
            # upload checks, detector is probably stalled
            interval = int(config['triggerrate_interval'])
            if abs(dt) > (2 * interval):
                self.nagiosResult.description = ("No recent triggers. "
                                                 "Trigger rate: %.2f. Last "
                                                 "update: %d seconds ago" %
                                                 (self.trate, dt))
                self.nagiosResult.status_code = CRITICAL
            else:
                self.nagiosResult.description = ("Trigger rate: %.2f. Last "
                                                 "update: %d seconds ago" %
                                                 (self.trate, dt))
            yield (self.nagiosResult)


class StorageSize(Check):
    def __init__(self, storageManager):
        Check.__init__(self)
        self.nagiosResult.serviceName = "StorageSize"
        self.storageManager = storageManager

    def check(self, sched, config):
        """Check the buffer size.

        The acceptable range is between the warn and crit range.
        cmin <= wmin <= OK >= wmax >= cmax.

        """
        if StorageManager.storagesize is None:
                self.storageManager.getNumEvents()

        while True:
            try:
                warnRange = config['storagesize_warn']
                warn = self.parse_range(warnRange)
                critRange = config['storagesize_crit']
                crit = self.parse_range(critRange)
            except:
                logger.critical('Unable to read config.ini %s' % 
                                self.nagiosResult.serviceName)
                self.nagiosResult.status_code = CRITICAL

            wmin, wmax = warn
            cmin, cmax = crit

            self.storageSize = StorageManager.storagesize

            if self.storageSize < cmin or self.storageSize > cmax:
                self.nagiosResult.status_code = CRITICAL
            elif self.storageSize < wmin or self.storageSize > wmax:
                self.nagiosResult.status_code = WARNING
            else:
                self.nagiosResult.status_code = OK

            if not self.storageSize:
                self.storageSize = 0

            self.nagiosResult.description = ("Storage size: %d events" %
                                             self.storageSize)

            yield (self.nagiosResult)


class EventRate(Check, Observer):
    def __init__(self):
        Check.__init__(self)
        self.nagiosResult.serviceName = "EventRate"
        self.eventCount = 0
        self.oldCountTime = 0
        self.eventRate = 0
        self.lock = Lock()

    # Add number of events
    def notify(self, count):
        self.lock.acquire()
        self.eventCount = self.eventCount + count
        self.lock.release()

    def check(self, sched, config):
        isCritical = config['eventrate_crit']

        while True:
            if self.oldCountTime == 0:
                self.oldCountTime = time.time()
            else:
                self.timeDifference = time.time() - self.oldCountTime
                self.oldCountTime = time.time()
                self.lock.acquire()
                self.eventRate = (float(self.eventCount) /
                                  float(self.timeDifference))
                self.eventCount = 0
                self.lock.release()

                if self.eventRate < isCritical:
                    self.nagiosResult.status_code = OK
                else:
                    self.nagiosResult.status_code = CRITICAL
                self.nagiosResult.description = ("Event rate for a period of "
                                                 "%.2f seconds is %.2f" %
                                                 (self.timeDifference,
                                                  self.eventRate))
            yield (self.nagiosResult)


class StorageGrowth(Check):
    def __init__(self, storageManager):
        Check.__init__(self)
        self.nagiosResult.serviceName = "StorageGrowth"
        self.newStorageSize = 0
        self.oldStorageSize = 0
        self.storageGrowth = 0
        self.storageManager = storageManager

    def check(self, sched, config):
        self.interval = config['storagegrowth_interval']
        while True:
            try:
                warn = float(config['storagegrowth_warn'])
                crit = float(config['storagegrowth_crit'])
            except:
                logger.critical('Unable to read config.ini in %s' % 
                                self.nagiosResult.serviceName)
                self.nagiosResult.status_code = CRITICAL

            self.newStorageSize = StorageManager.storagesize
            self.storageGrowth = ((self.newStorageSize - self.oldStorageSize) /
                                  float(self.interval))
            self.oldStorageSize = self.newStorageSize
            if self.storageGrowth < warn:
                self.nagiosResult.status_code = OK
            elif self.storageGrowth < crit:
                self.nagiosResult.status_code = WARNING
            else:
                self.nagiosResult.status_code = CRITICAL
            self.nagiosResult.description = ("Storage growth: %f Hz" %
                                             self.storageGrowth)
            yield (self.nagiosResult)
