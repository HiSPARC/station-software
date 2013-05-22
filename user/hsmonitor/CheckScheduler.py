import time
import threading
import logging

from Check import EventRate, StorageGrowth, StorageSize, TriggerRate
from NagiosPush import NagiosPush
from StorageManager import StorageManager
from UserExceptions import ThreadCrashError

logger = logging.getLogger('hsmonitor.checkscheduler')

class ScheduledJob:
    def __init__(self, job, jobfunc, interval, args):
        self.job = job
        self.jobfunc = jobfunc
        self.interval = interval
        self.args = args
        self.last_run = 0


class Scheduler:
    def __init__(self, status):
        self.jobs = {}
        self.jobcounter = 0
        self.current_tid = 0
        self.status = status

    def addJob(self, job, interval, args=None):
        self.jobcounter += 1

        # Perform the task, as the yield function call is a
        # generator made
        jobgen = job(self, args)

        # Add the task to the list
        schedjob = ScheduledJob(jobgen, job, interval, args)
        self.jobs[self.jobcounter] = schedjob

        return self.jobcounter

    def schedule(self, nagiosPush, config):
        toremove = []
        tostart = []
        timeCurrent = time.time()

        # Go through all tasks
        for tid, schedjob in self.jobs.iteritems():
            self.current_tid = tid
            timeDifference = timeCurrent - schedjob.last_run

            if timeDifference >= schedjob.interval:
                schedjob.last_run = timeCurrent

                try:
                    returnValues = schedjob.job.next()
                    nagiosPush.sendToNagios(returnValues)

                except StopIteration:
                    logger.error('JOB STOPPED!')
                    toremove.append(tid)

                except Exception, msg:
                    logger.error('Uncatched expection in job: %s. ' % msg)
                    logger.error('Restarting...')
                    toremove.append(tid)
                    tostart.append(tid)

        # restart new threads
        for tid in tostart:
            j = self.jobs[tid]
            self.addJob(j.jobfunc, j.interval, j.args)

        tostart = []

        # remove all threads that completed / stopped
        for tid in toremove:
            self.jobs.pop(tid, None)

        toremove = []


class CheckScheduler(threading.Thread):
    def __init__(self, config, interpreter):
        # invoke constructor of parent class (threading)
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

        self.status = None
        self.sched = Scheduler(self.status)
        self.dicConfig = config

        # create a nagios push object
        self.nagiosPush = NagiosPush(config)
        self.storageManager = StorageManager()
        self.interpreter = interpreter

        ### Event rate:
        self.eventRate = EventRate()

    def getEventRate(self):
        return self.eventRate

    def stop(self):
        self.stop_event.set()

    crashes = []

    def init_restart(self):
        """Support for restarting crashed threads"""

        if len(self.crashes) > 3 and time.time() - self.crashes[-3] < 60.:
            raise ThreadCrashError("Thread has crashed three times in "
                                   "less than a minute")
        else:
            super(CheckScheduler, self).__init__()
            self.crashes.append(time.time())

    # This is what the thread actually runs; the required name is run().
    # The threading.Thread.start() calls threading.Thread.run(),
    # which is always overridden.
    def run(self):
        logger.debug('Thread started!')
        self.storageManager.openConnection()

        ### Trigger rate:
        triggerRate = TriggerRate(self.interpreter)
        TR_interval = int(self.dicConfig['triggerrate_interval'])
        self.sched.addJob(triggerRate.check, interval=TR_interval,
                          args=self.dicConfig)
        ### Storage size:
        storageSize = StorageSize(self.storageManager)
        SS_interval = int(self.dicConfig['storagesize_interval'])
        self.sched.addJob(storageSize.check, interval=SS_interval,
                          args=self.dicConfig)
        ### Event rate:
        ER_interval = int(self.dicConfig['eventrate_interval'])
        self.sched.addJob(self.eventRate.check, interval=ER_interval,
                          args=self.dicConfig)
        ### Storage growth:
        storageGrowth = StorageGrowth(self.storageManager)
        SG_interval = int(self.dicConfig['storagegrowth_interval'])
        self.sched.addJob(storageGrowth.check, interval=SG_interval,
                          args=self.dicConfig)

        while not self.stop_event.isSet():
            # run all checks
            self.sched.schedule(self.nagiosPush, self.dicConfig)

            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except:
                pass
        logger.warning('Thread stopped!')
