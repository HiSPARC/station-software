#!/usr/bin/env python

from datetime import datetime
import time
#import base64

from Event import Event
import EventExportValues


class WeatherConfig(object, Event):
    """A Weather config class to makes all data handling easy."""

    def __init__(self, message):
        """Invoke constructor of parent class."""
        Event.__init__(self)
        self.message = message[1]
  	
    def fixBoolean(self, datastring):
        return eval(datastring.title())

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
        self.com_port = int(tmp[1])
        self.baud_rate = int(tmp[2])
        self.station_id = int(tmp[3])
        self.database_name = tmp[4]
        self.help_url = tmp[5]
        self.daq_mode = fixBoolean(tmp[6])
        self.latitude = float(tmp[7])
        self.longitude = float(tmp[8])
        self.temperature_inside = fixBoolean(tmp[9])
        self.temperature_outside = fixBoolean(tmp[10])
        self.humidity_inside = fixBoolean(tmp[11])
        self.humidity_outside = fixBoolean(tmp[12])
        self.barometer = fixBoolean(tmp[13])
        self.wind_direction = fixBoolean(tmp[14])
        self.wind_speed = fixBoolean(tmp[15])
        self.solar_radiation = fixBoolean(tmp[16])
        self.uv_index = fixBoolean(tmp[17])
        self.evapotranspiration = fixBoolean(tmp[18])
        self.rain_rate = fixBoolean(tmp[19])
        self.heat_index = fixBoolean(tmp[20])
        self.dew_point = fixBoolean(tmp[21])
        self.wind_chill = fixBoolean(tmp[22])
        self.offset_inside_temperature = float(tmp[23])
        self.offset_outside_temperature = float(tmp[24])
        self.offset_inside_humidity = int(tmp[25])
        self.offset_outside_humidity = int(tmp[26])
        self.offset_wind_direction = int(tmp[27])
        self.offset_station_altitude = float(tmp[28])
        self.offset_bar_sea_level = float(tmp[29])
        self.altitude = float(tmp[30])

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
