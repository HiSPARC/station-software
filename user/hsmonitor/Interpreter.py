"""Process HiSPARC messages from a buffer.

This module processes binary messages from a HiSPARC station buffer and
creates Events from them. The Events are passed on to the StorageManager.

"""

import logging

logger = logging.getLogger('hsmonitor.interpreter')

from HiSPARCEvent import HiSPARCEvent
from HiSPARCError import HiSPARCError
from HiSPARCConfig import HiSPARCConfig
from HiSPARCComparator import HiSPARCComparator
# from HiSPARCSingles import HiSPARCSingles
from WeatherEvent import WeatherEvent
from WeatherError import WeatherError
from WeatherConfig import WeatherConfig
from LightningEvent import LightningEvent
from LightningError import LightningError
from LightningConfig import LightningConfig
from LightningStatus import LightningStatus
from LightningNoise import LightningNoise

# create a dictionary to store all type_codes of events
event_type_codes = {'1': 'CIC', '2': 'ERR', '3': 'CFG', '4': 'CMP', '5': 'SIN',
                    '16': 'WTR', '17': 'WER', '18': 'WCG',
                    '32': 'LIT', '33': 'LER', '34': 'LCG', '35': 'LST',
                    '36': 'LNS'}


class TriggerRateHolder(object):
    def __init__(self, triggerRate, date):
        self.triggerRate = triggerRate
        self.date = date


class Interpreter(object):

    def __init__(self, storageManager):
        # init variables here if needed
        self.storageManager = storageManager
        self.triggerRate = TriggerRateHolder(0, 0)

    def openStorage(self):
        self.storageManager.openConnection()

    def createEvent(self, eventcode, message):
        # create an event corresponding to the eventcode
        if eventcode == 'CIC':
            event = HiSPARCEvent(message)
        elif eventcode == 'ERR':
            event = HiSPARCError(message)
        elif eventcode == 'CFG':
            event = HiSPARCConfig(message)
        elif eventcode == 'CMP':
            event = HiSPARCComparator(message)
        # elif eventcode == 'SIN':
        #     event = HiSPARCSingles(message)
        elif eventcode == 'WTR':
            event = WeatherEvent(message)
        elif eventcode == 'WER':
            event = WeatherError(message)
        elif eventcode == 'WCG':
            event = WeatherConfig(message)
        elif eventcode == 'LIT':
            event = LightningEvent(message)
        elif eventcode == 'LER':
            event = LightningError(message)
        elif eventcode == 'LCG':
            event = LightningConfig(message)
        elif eventcode == 'LST':
            event = LightningStatus(message)
        elif eventcode == 'LNS':
            event = LightningNoise(message)
        else:
            logger.warning('Unknown message type %s (%d).' %
                           (eventcode, self.type_id))
            return None

        event.uploadCode = eventcode
        event.data = event.parseMessage()
        return event

    def setTriggerRate(self, triggerRate):
        self.triggerRate = triggerRate

    def getTriggerRate(self):
        return self.triggerRate

    def parseMessages(self, messages):
        """

        This function unpacks messages, creates events, retrieves relevant
        data from the events and returns it as an elaborate data object which
        can be serialized for transfer via an HTTP POST request.

        """
        self.eventlist = []
        self.event_ids = []
        self.discard_event_ids = []
        # this variable stores the trigger rate of the recent event
        trigger_rate = TriggerRateHolder(0, 0)
        logger.debug('Parsing %d messages.' % len(messages))

        firsttime = True
        for message in messages:
            try:
                # get the event message code
                eventcode = event_type_codes['%d' % message[0]]
                # create an event object
                event = self.createEvent(eventcode, message)
                # skip processing event if it is None
                if event is None:
                    continue
                # create the event header
                # new server uses datetime, old uses date and time
                # for compatibility, include both
                header = {'eventtype_uploadcode': event.uploadCode,
                          'datetime': event.datetime,
                          'date': event.datetime.date().isoformat(),
                          'time': event.datetime.time().isoformat(),
                          'nanoseconds': event.nanoseconds}

                # store the trigger rate variable, only for the newest event
                if eventcode == 'CIC' and firsttime:
                    firsttime = False
                    trigger_rate.triggerRate = event.eventrate
                    trigger_rate.date = event.datetime

            except Exception, (errormsg):
                # add parsed event_id into the list of event_ids
                self.discard_event_ids.append(message[2])
                logger.error('Event exception (discarding event): %s.' %
                             errormsg)
                logger.debug('Bad event: %s' % message)
            else:
                # add parsed event into the list of events
                self.eventlist.append({'header': header,
                                       'datalist': event.data})
                # add parsed event_id into the list of event_ids
                self.event_ids.append(message[2])

        # set the trigger rate in Storage Manager
        if trigger_rate.triggerRate != 0:
            self.setTriggerRate(trigger_rate)

        # add all parsed events into the Storage
        res = self.storageManager.addEvents(self.eventlist)
        # clear the event id list if events cannot be stored in Storage DB
        if not res:
            self.event_ids = []
            return self.discard_event_ids

        self.event_ids.extend(self.discard_event_ids)
        return self.event_ids
