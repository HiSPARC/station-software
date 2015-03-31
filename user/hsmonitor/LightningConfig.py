from datetime import datetime
import time

from Event import BaseLightningEvent
import EventExportValues


class LightningConfig(BaseLightningEvent):
    """A Lightning config class to makes all data handling easy."""

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
        self.com_port = int(tmp[1])
        self.baud_rate = int(tmp[2])
        self.station_id = int(tmp[3])
        self.database_name = tmp[4]
        self.help_url = tmp[5]
        self.daq_mode = self.fix_boolean(tmp[6])
        self.latitude = float(tmp[7])
        self.longitude = float(tmp[8])
        self.altitude = float(tmp[9])
        self.squelch_setting = int(tmp[10])
        self.close_alarm_distance = int(tmp[11])
        self.severe_alarm_distance = int(tmp[12])
        self.noise_beep = self.fix_boolean(tmp[13])
        self.minimum_gps_speed = int(tmp[14])
        self.angle_correction = float(tmp[15])

        # Get all event data necessary for an upload.
        self.export_values = EventExportValues.export_values[self.uploadCode]
        return self.getEventData()
