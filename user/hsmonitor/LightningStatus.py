from datetime import datetime
import time

from Event import BaseLightningEvent
import EventExportValues


class LightningStatus(BaseLightningEvent):
    """A Lightning status class to makes all data handling easy."""

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
        self.closeStrikeRate = int(tmp[1])
        self.totalStrikeRate = int(tmp[2])
        self.closeAlarm = self.fix_boolean(tmp[3])
        self.severeAlarm = self.fix_boolean(tmp[4])
        self.currentHeading = float(tmp[4])

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
