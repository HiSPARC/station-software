from datetime import datetime
import time

from Event import BaseWeatherEvent
import EventExportValues


class WeatherConfig(BaseWeatherEvent):
    """A Weather config class to makes all data handling easy."""

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
        self.daq_mode = self.fix_boolean(tmp[6])
        self.latitude = float(tmp[7])
        self.longitude = float(tmp[8])
        self.altitude = float(tmp[9])
        self.temperature_inside = self.fix_boolean(tmp[10])
        self.temperature_outside = self.fix_boolean(tmp[11])
        self.humidity_inside = self.fix_boolean(tmp[12])
        self.humidity_outside = self.fix_boolean(tmp[13])
        self.barometer = self.fix_boolean(tmp[14])
        self.wind_direction = self.fix_boolean(tmp[15])
        self.wind_speed = self.fix_boolean(tmp[16])
        self.solar_radiation = self.fix_boolean(tmp[17])
        self.uv_index = self.fix_boolean(tmp[18])
        self.evapotranspiration = self.fix_boolean(tmp[19])
        self.rain_rate = self.fix_boolean(tmp[20])
        self.heat_index = self.fix_boolean(tmp[21])
        self.dew_point = self.fix_boolean(tmp[22])
        self.wind_chill = self.fix_boolean(tmp[23])
        self.offset_inside_temperature = float(tmp[24])
        self.offset_outside_temperature = float(tmp[25])
        self.offset_inside_humidity = int(tmp[26])
        self.offset_outside_humidity = int(tmp[27])
        self.offset_wind_direction = int(tmp[28])
        self.offset_station_altitude = float(tmp[29])
        self.offset_bar_sea_level = float(tmp[30])

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
