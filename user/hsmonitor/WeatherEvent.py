from datetime import datetime

from Event import BaseWeatherEvent
import EventExportValues


class WeatherEvent(BaseWeatherEvent):
    """A Weather event class to makes all data handling easy."""

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

        time_difference = float(tmp.pop())
        self.tempInside = float(tmp.pop())
        self.tempOutside = float(tmp.pop())
        self.humidityInside = int(float(tmp.pop()))
        self.humidityOutside = int(float(tmp.pop()))
        self.barometer = float(tmp.pop())
        self.windDir = int(float(tmp.pop()))
        self.windSpeed = float(tmp.pop())
        self.solarRad = int(float(tmp.pop()))
        self.UV = int(float(tmp.pop()))
        self.ET = float(tmp.pop())
        self.rainRate = float(tmp.pop())
        self.heatIndex = int(float(tmp.pop()))
        self.dewPoint = float(tmp.pop())
        self.windChill = float(tmp.pop())

        self.check_unread_values(tmp)

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
