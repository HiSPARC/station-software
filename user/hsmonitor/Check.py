import sys
import time
import calendar
import logging
from threading import Lock

from Observer import Observer
from NagiosResult import NagiosResult
from StorageManager import StorageManager
from EConfigParser import EConfigParser

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

TIME_DIFF_INI = '../../persistent/configuration/HiSPARC.ini'

logger = logging.getLogger('hsmonitor.check')


class Check(object):
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
        super(TriggerRate, self).__init__()
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
                # Timestamp is in GPS time.  Naively treat it as a local
                # timestamp, then subtract the LabVIEW-determined offset
                # between pc clock time (UTC time) and GPS time.

                # Read offset from DAQ config.
                # This offset is (DAQ GPS time - PC clock time).
                # (the number of seconds GPS time is ahead of the PC clock)
                # Note: this offset changed sign between v3 and v4 of the DAQ
                dt_config = EConfigParser()
                dt_config.read(TIME_DIFF_INI)
                offset = dt_config.ifgetint('HiSPARC', 'time_difference', 1e6)

                # calculate event (trigger) time and transform to local PC time
                t_trigger = calendar.timegm(self.lastupdate.timetuple())
                t_trigger -= offset

                # Calculate time difference between current and trigger time
                dt = time.time() - t_trigger
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
        super(StorageSize, self).__init__()
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
        super(EventRate, self).__init__()
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
        super(StorageGrowth, self).__init__()
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
