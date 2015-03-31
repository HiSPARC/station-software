from datetime import datetime
import time

from Event import BaseWeatherEvent
import EventExportValues


class WeatherEvent(BaseWeatherEvent):
    """A Weather event class to makes all data handling easy."""

    def parseMessage(self):
        tmp = self.message.split("\t")
        t = time.strptime(tmp[0].strip(), "%Y-%m-%d %H:%M:%S")
        self.datetime = datetime(t[0], t[1], t[2], t[3], t[4], t[5])
        self.nanoseconds = 0  # Weather is not accurate enough
        self.second = self.datetime.second
        self.minute = self.datetime.minute
        self.hour = self.datetime.hour
        self.day = self.datetime.day
        self.month = self.datetime.month
        self.year = self.datetime.year
        self.tempInside = float(tmp[1])
        self.tempOutside = float(tmp[2])
        self.humidityInside = int(float(tmp[3]))
        self.humidityOutside = int(float(tmp[4]))
        self.barometer = float(tmp[5])
        self.windDir = int(float(tmp[6]))
        self.windSpeed = float(tmp[7])
        self.solarRad = int(float(tmp[8]))
        self.UV = int(float(tmp[9]))
        self.ET = float(tmp[10])
        self.rainRate = float(tmp[11])
        self.heatIndex = int(float(tmp[12]))
        self.dewPoint = float(tmp[13])
        self.windChill = float(tmp[14])

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
