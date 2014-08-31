#!/usr/bin/env python

from datetime import datetime
import time
#import base64

from Event import Event
import EventExportValues


class LightningNoise(object, Event):
    """A Lighting noise class to makes all data handling easy."""

    def __init__(self, message):
        """Invoke constructor of parent class."""
        Event.__init__(self)
        self.message = message[1]

    def parseMessage(self):
        tmp = self.message.split("\t")
        t = time.strptime(tmp[0].strip(), "%Y-%m-%d %H:%M:%S")
        self.datetime = datetime(t[0], t[1], t[2], t[3], t[4], t[5])
        self.nanoseconds = 0  # Lightning is not accurate enough
        self.second = self.datetime.second
        self.minute = self.datetime.minute
        self.hour = self.datetime.hour
        self.day = self.datetime.day
        self.month = self.datetime.month
        self.year = self.datetime.year

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        if name == "date":
            return self.datetime.date().isoformat()
        elif name == "time":
            return self.datetime.time().isoformat()
        else:
            raise AttributeError, name

    def getEventData(self):
        """Get all event data necessary for an upload.

        This function parses the export_values variable declared in the
        EventExportValues and figures out what data to collect for an upload to
        the eventwarehouse. It returns a list of dictionaries, one for each
        data element.

        """

        eventdata = []
        for value in self.export_values:
            eventdata.append({"calculated": value[0],
                              "data_uploadcode": value[1],
                              "data": self.__getattribute__(value[2])})
                    #"data": base64.b64encode(self.__getattribute__(value[2]))

        return eventdata
