from datetime import datetime

from Event import BaseWeatherEvent
import EventExportValues


class WeatherConfig(BaseWeatherEvent):
    """A Weather config class to makes all data handling easy."""

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

        self.com_port = int(float(tmp.pop()))
        self.baud_rate = int(float(tmp.pop()))
        self.station_id = int(float(tmp.pop()))
        self.database_name = tmp.pop()
        self.help_url = tmp.pop()

        # stand_alone_mode
        self.fix_boolean(tmp.pop())

        self.daq_mode = self.fix_boolean(tmp.pop())
        self.latitude = float(tmp.pop())
        self.longitude = float(tmp.pop())
        self.altitude = float(tmp.pop())

        self.temperature_inside = self.fix_boolean(tmp.pop())
        self.temperature_outside = self.fix_boolean(tmp.pop())
        self.humidity_inside = self.fix_boolean(tmp.pop())
        self.humidity_outside = self.fix_boolean(tmp.pop())
        self.barometer = self.fix_boolean(tmp.pop())
        self.wind_direction = self.fix_boolean(tmp.pop())
        self.wind_speed = self.fix_boolean(tmp.pop())
        self.solar_radiation = self.fix_boolean(tmp.pop())
        self.uv_index = self.fix_boolean(tmp.pop())
        self.evapotranspiration = self.fix_boolean(tmp.pop())
        self.rain_rate = self.fix_boolean(tmp.pop())
        self.heat_index = self.fix_boolean(tmp.pop())
        self.dew_point = self.fix_boolean(tmp.pop())
        self.wind_chill = self.fix_boolean(tmp.pop())

        self.offset_inside_temperature = float(tmp.pop())
        self.offset_outside_temperature = float(tmp.pop())
        self.offset_inside_humidity = int(float(tmp.pop()))
        self.offset_outside_humidity = int(float(tmp.pop()))
        self.offset_wind_direction = int(float(tmp.pop()))
        self.offset_station_altitude = float(tmp.pop())
        self.offset_bar_sea_level = float(tmp.pop())

        self.check_unread_values(tmp)

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
