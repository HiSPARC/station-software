from datetime import datetime

from Event import BaseWeatherEvent
import EventExportValues


class WeatherError(BaseWeatherEvent):
    """A Weather error class to makes all data handling easy."""

    def parseMessage(self):
        tmp = self.message.split("\t")
        tmp.reverse()

        date_fmt = "%Y-%m-%d %H:%M:%S"
        self.datetime = datetime.strptime(tmp.pop().strip(), date_fmt)
        self.nanoseconds = 0  # Weather is not accurate enough
        self.second = self.datetime.second
        self.minute = self.datetime.minute
        self.hour = self.datetime.hour
        self.day = self.datetime.day
        self.month = self.datetime.month
        self.year = self.datetime.year

        self.error_message = tmp.pop()

        self.check_unread_values(tmp)

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
