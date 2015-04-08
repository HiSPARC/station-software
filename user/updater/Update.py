import sched
import time
import random
import os
import logging

import checkFiles
from Checker import Checker

from EConfigParser import EConfigParser
from TimedConcurrentLogging import TimedConcurrentRotatingFileHandler


CONFIG_INI = "config.ini"
PERSISTENT_INI = "../../persistent/configuration/config.ini"
ADMINUPDATE_NAME = "adminUpdater"

logger = logging.getLogger('updater')
logging.Formatter.converter = time.gmtime
formatter_file = logging.Formatter('%(asctime)s %(name)s.%(funcName)s.'
                                   '%(levelname)s: %(message)s',
                                   '%Y-%m-%d %H:%M:%S')
formatter_screen = logging.Formatter('%(asctime)s UTC - %(name)s - '
                                     '%(levelname)s: %(message)s',
                                     '%Y-%m-%d %H:%M:%S')

# Logging levels which can be set in the configuration file
LEVELS = {"notset": logging.NOTSET,
          "debug": logging.DEBUG,
          "info": logging.INFO,
          "warning": logging.WARNING,
          "error": logging.ERROR,
          "critical": logging.CRITICAL}


class Updater(object):

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.checker = Checker()
        self.config = EConfigParser()
        self.config.read([CONFIG_INI, PERSISTENT_INI])
        # Time between checks in seconds
        self.timeBetweenChecks = self.config.ifgetint(
            'Update', 'IntervalBetweenChecks', 1800)
        # Start and stop time of the interval in which checks may be
        # performed on a day (in seconds since midnight) e.g. 7200 is 2am
        self.timeStartCheckInterval = self.config.ifgetint(
            'Update', 'CheckerIntervalStartTime', 0)
        self.timeStopCheckInterval = self.config.ifgetint(
            'Update', 'CheckerIntervalStopTime', 24 * 60 * 60)
        # Bool determine if there will be an initial delay
        self.checkerInitialDelay = self.config.get(
            'Update', 'CheckerInitialDelay', 0)

        # Setup the log mode
        log_dirname = '../../persistent/logs/updater/'
        # Making sure the directory exists
        if not os.access(log_dirname, os.F_OK):
            os.makedirs(log_dirname)
        log_filename = os.path.join(log_dirname, 'updater')

        # Add file handler
        handler = TimedConcurrentRotatingFileHandler(
            log_filename, when='midnight', backupCount=14, suffix='log')
        handler.setFormatter(formatter_file)
        logger.addHandler(handler)

        # Add handler which prints to the screen
        handler = logging.StreamHandler()
        handler.setFormatter(formatter_screen)
        logger.addHandler(handler)

        # Logging level for the two loggers
        for i, target in enumerate(['File', 'Screen']):
            log_level = self.config.ifgetstr('Logging', '%sLevel' % target,
                                             'debug')
            if log_level in LEVELS:
                logger.handlers[i].setLevel(level=LEVELS[log_level])
                logger.info('%s logging level set to %s' % (target, log_level))
            else:
                logger.warning("Illegal %s logging level '%s' in config, "
                               "using debug" % (target, log_level))

    def checkIfUpdateToInstall(self):
        """Check if there is already an admin update to install

        Also check if you are currently in user or admin mode

        """
        is_admin = checkFiles.checkIfAdmin()
        currentAdmin = self.config.get("Version", "CurrentAdmin")
        currentUser = self.config.ifgetint("Version", "CurrentUser")

        logger.info("You are Administrator: " + is_admin)
        logger.info("Current Admin Version: %s" % currentAdmin)
        logger.info("Current User Version:  %s" % currentUser)

        if is_admin:
            location = "../../persistent/downloads"
            found, file_found = checkFiles.checkIfNewerFileExists(
                location, ADMINUPDATE_NAME, int(currentAdmin))
            if found:
                logger.info("Found: %s" % file_found)
                os.system(".\\runAdminUpdate.bat "
                          "../../persistent/downloads/%s" % file_found)

    def calculateInitialDelay(self):
        if self.checkerInitialDelay == 1:
            # Calculate the time now
            # ..and the time it is be today at four and at noon
            now = int(time.time())
            last_midnight = now - (now % 86400)
            today_at_starttime = last_midnight + self.timeStartCheckInterval
            today_at_stoptime = last_midnight + self.timeStopCheckInterval

            # Check if you are allowed to update already
            # (in the interval between starttime and stoptime)
            if today_at_starttime < now < today_at_stoptime:
                today_random_moment = random.randint(now, today_at_stoptime)
                return today_random_moment - now
            else:
                tomorrow_at_four = today_at_starttime + 86400
                tomorrow_at_noon = today_at_stoptime + 86400
                tomorrow_random_moment = random.randint(tomorrow_at_four,
                                                        tomorrow_at_noon)
                return tomorrow_random_moment - now
        else:
            return 0

    def performOneUpdateCheck(self):
        delay = self.calculateInitialDelay()
        self.scheduler.enter(delay, 1, self.checker.checkForUpdates, '')
        self.scheduler.run()

    def performContinuousCheck(self):
        while True:
            self.scheduler.enter(self.timeBetweenChecks, 1,
                                 self.checker.checkForUpdates, '')
            self.scheduler.run()


if __name__ == "__main__":
    try:
        updater = Updater()
        updater.checkIfUpdateToInstall()
        updater.performOneUpdateCheck()
        updater.performContinuousCheck()
    except KeyboardInterrupt:
        exit
    except:
        logger.exception("Updating failed, restart the checker!")
        exit
